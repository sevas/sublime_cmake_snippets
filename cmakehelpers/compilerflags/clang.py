
import os
import glob
import json
import subprocess

from .core import CompilerFlag, convert_compilerflags_to_dicts, convert_dicts_to_compilerflags


def filter_options_lines(clang_help):
    # remove the header and the blank lines
    header_lines_count = 6
    return [x for x in clang_help[header_lines_count:] if x]


def extract_flag_template(flag_string):
    """
    >>> extract_flag_template('-E')
    ('-E', '-E')
    >>> extract_flag_template('-F <value>')
    ('-F', '-F ${1:value}')
    >>> extract_flag_template('-X <arg> <arg>')
    ('-X', '-X ${1:arg} ${2:arg}')

    >>> extract_flag_template('-code-completion-at <file>:<line>:<column>')
    ('-code-completion-at', '-code-completion-at ${1:file}:${2:line}:${3:column}')
    """

    split = flag_string.split('<')
    flag_trigger, flag_args = split[0].strip(), split[1:]

    sep = " "
    # detect if args look like : -foo <bar>:<baz>:<quux> to
    # know if we need to rejoin the placeholders with a colon
    if '>:<' in flag_string:
        sep = ':'

    placeholders = ["${{{0}:{1}}}".format(i+1, each.strip('>: ')) for i, each in enumerate(flag_args)]

    template_string = "{0} {1}".format(flag_trigger, sep.join(placeholders)).strip()

    return flag_trigger,  template_string


def parse_oneliner_flag(flag_line):
    """
    >>> parse_oneliner_flag('-Eonly                  Just run preprocessor, no output (for timings)')
    ('-Eonly', CompilerFlag(description='Just run preprocessor, no output (for timings)', replace_with='-Eonly'))
    >>> parse_oneliner_flag('-F <value>              Add directory to framework include search path')
    ('-F', CompilerFlag(description='Add directory to framework include search path', replace_with='-F ${1:value}'))
    """
    indentation_column_index = 24
    flag, description = flag_line[:indentation_column_index].strip(), flag_line[indentation_column_index:]
    flag, flag_template = extract_flag_template(flag)
    return flag, CompilerFlag(description=description, replace_with=flag_template)


def parse_compiler_flags(clang_help_output):
    """Parses the output of clang --help and extracts the compiler flags

    Parameters
    ----------
    clang_help_output: str
        The unmodified content dumped by the ``clang -cc1 --help`` command

    Returns
    -------
    dict
        Keys are full strings used to trigger a completion.
        Values of CompilerFlag instances

    """
    clang_flags = filter_options_lines(clang_help_output.split('\n'))
    compiler_flags = list()
    idx = 0
    line_count = len(clang_flags)

    while idx < line_count:
        current_flag_line = clang_flags[idx].strip()

        # fetch subsequent indented lines for long options
        j = 1
        multiline_description = list()
        multiline_indentation = ' '*6
        while idx+j < line_count and clang_flags[idx+j].startswith(multiline_indentation):
            multiline_description.append(clang_flags[idx+j].strip())
            j += 1

        if multiline_description:
            flag_trigger, flag_template = extract_flag_template(current_flag_line)
            description = ' '.join(multiline_description)
            compiler_flag = CompilerFlag(description=description, replace_with=flag_template)
        else:
            flag_trigger, compiler_flag = parse_oneliner_flag(current_flag_line)

        compiler_flags.append((flag_trigger, compiler_flag))
        idx += j

    return dict(compiler_flags)


def get_command_output(cmd, expected_returncode):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    if p.returncode != expected_returncode:
        print out
        print err
        raise ValueError('Something went wrong')

    return out



def make_compiler_options_database(cc_executable='clang'):

    clang_help_output = get_command_output([cc_executable, '-cc1', '--help'], expected_returncode=1)
    clang_flags = parse_compiler_flags(clang_help_output)

    clang_version_output = get_command_output([cc_executable, '-dumpversion'], expected_returncode=0)

    return clang_flags, clang_version_output.strip()


def save_compiler_options_database(data_dir, clang_flags, clang_version):
    database_fpath = os.path.join(data_dir, "clang_{}.json".format(clang_version))

    with open(database_fpath, 'w') as f:
        json.dump(convert_compilerflags_to_dicts(clang_flags), f, indent=2)


def load_compiler_options_database(clang_executable='clang'):
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "data")
    database_file_pattern = os.path.join(data_dir, "clang*.json")
    candidate_databases = glob.glob(database_file_pattern)

    if not candidate_databases:
        clang_flags, clang_version = make_compiler_options_database(clang_executable)
        save_compiler_options_database(data_dir, clang_flags, clang_version)

        return clang_flags
    else:
        database_fpath = candidate_databases[0]
        with open(database_fpath) as f:
            content = json.load(f)
            return convert_dicts_to_compilerflags(content)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

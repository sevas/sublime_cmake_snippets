
import subprocess
from core import CompilerFlag, get_candidate_flag_prefix


def filter_header(clang_help):
    return clang_help[6:]


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
    clang_flags = filter_header(clang_help_output.split('\n'))

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


def make_compiler_flags_database(clang_executable='clang'):
    p = subprocess.Popen([clang_executable, '-cc1', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()

    if p.returncode != 1:
        raise ValueError('hello')

    clang_flags = parse_compiler_flags(out)
    return clang_flags

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

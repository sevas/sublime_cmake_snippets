from collections import namedtuple

CompilerFlag = namedtuple('CompilerFlag', 'description replace_with')


def get_candidate_flag_prefix(line):
    """Retrieves a candidate flag prefix from a string. This candidate will be used  to search for completion candidates.

    >>> get_candidate_flag_prefix('-I')
    '-I'
    >>> get_candidate_flag_prefix('-I -J')
    '-J'
    >>> get_candidate_flag_prefix('-long-option')
    '-long-option'
    >>> get_candidate_flag_prefix('--long-option')
    '--long-option'
    >>> get_candidate_flag_prefix('-s -long-option')
    '-long-option'
    >>> get_candidate_flag_prefix('')
    ''
    >>> get_candidate_flag_prefix('hello')
    ''
    >>> get_candidate_flag_prefix('-v 0')
    ''
    >>> get_candidate_flag_prefix('set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -M')
    '-M'
    """
    if not line:
        return ''
    words = [x for x in line.split(' ') if x]
    candidate = words[-1]
    if candidate[0] == '-':
        return candidate
    else:
        return ''


def find_completions(compiler_name, compiler_flags, line, cursor_pos=None):
    """

    Parameters
    ----------
    compiler_name: str
        Name of the compiler that will be prefixed to the
        autocomplete proposals in the popup box
    compiler_flags: dict
        The completion database. Keys are
    line: str
        The text content
    cursor_pos: int, Optional
        The index of the user cursor inside the line.
        Used to crop the text content before detecting candidate.

    Returns
    -------
    list
        list of 3-uples: (<found_tag>, <>, <template string with args placeholders>)
    """
    if cursor_pos:
        line = line[:cursor_pos]

    candidate_flag_prefix = get_candidate_flag_prefix(line)
    if candidate_flag_prefix:
        completions = [(x, "[{0}] {1} {2}".format(compiler_name, x, compiler_flags[x].description), compiler_flags[x].replace_with) for x in compiler_flags.keys() if x.startswith(candidate_flag_prefix)]
        return sorted(completions)
    else:
        return []


def convert_compilerflags_to_dicts(flags_database):
    """
    >>> from pprint import pprint
    >>> d = dict(foo=CompilerFlag(description='foo', replace_with='foo'))
    >>> pprint(convert_compilerflags_to_dicts(d))
    {'foo': {'description': 'foo', 'replace_with': 'foo'}}
    """
    out = dict()

    for k, v in flags_database.items():
        out[k] = dict(v._asdict())
    return out


def convert_dicts_to_compilerflags(flags_database):
    """
    >>> from pprint import pprint
    >>> d = {'foo': {'description': 'foo', 'replace_with': 'foo'}}
    >>> pprint(convert_dicts_to_compilerflags(d))
    {'foo': CompilerFlag(description='foo', replace_with='foo')}

    """
    out = dict()
    for k, v in flags_database.items():
        out[k] = CompilerFlag(**v)
    return out

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
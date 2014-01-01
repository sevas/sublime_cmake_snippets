
from nose.tools import eq_, ok_
from cmakehelpers.compilerflags.core import find_completions, CompilerFlag


MOCK_CLANG_FLAGS_DB = {
    "-E": CompilerFlag(description="Only run the preprocessor", replace_with='-E'),
    "-F": CompilerFlag(description="Add directory to framework include search path", replace_with='-F ${1:value}'),
    "-H": CompilerFlag(description="Show header includes and nesting depth", replace_with='-H'),
    "-I": CompilerFlag(description="Add directory to include search path", replace_with='-I ${1:value}'),
    "-MG": CompilerFlag(description="Add missing headers to dependency list", replace_with='-MG'),
    "-MP": CompilerFlag(description="Create phony target for each dependency CompilerFlag(description=han main file)", replace_with='-MP'),
    "-MQ": CompilerFlag(description="Specify target to quote for dependency", replace_with='-MQ ${1:value}'),
    "-MT": CompilerFlag(description="Specify target for dependency", replace_with='-MT ${1:value}'),
}


def test_find_completions_bad_prefix():
    found_completions = find_completions('clang', MOCK_CLANG_FLAGS_DB, 'hello')
    ok_(not found_completions)


def test_find_completions_no_args():
    found_completions = find_completions('clang', MOCK_CLANG_FLAGS_DB, '-E')
    eq_(len(found_completions), 1)
    expected_candidate = ('-E', '[clang] -E Only run the preprocessor', '-E')
    eq_(expected_candidate, found_completions[0])


def test_find_completions_positional_args():
    found_completions = find_completions('clang', MOCK_CLANG_FLAGS_DB, '-F')
    eq_(len(found_completions), 1)
    expected_candidate = ('-F', '[clang] -F Add directory to framework include search path', '-F ${1:value}')
    eq_(expected_candidate, found_completions[0])
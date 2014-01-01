from nose.tools import eq_, nottest

from cmakehelpers.compilerflags.core import CompilerFlag
from cmakehelpers.compilerflags import clang

SAMPLE_CLANG_OUTPUT = """
OVERVIEW: LLVM 'Clang' Compiler: http://clang.llvm.org

USAGE: clang -cc1 [options] <inputs>

OPTIONS:
  -Eonly                  Just run preprocessor, no output (for timings)
  -E                      Only run the preprocessor
  -I <value>              Add directory to include search path
  -analyzer-viz-egraph-graphviz
                          Display exploded graph using GraphViz
  -analyzer-constraints <value>
                          Source Code Analysis - Symbolic Constraint Engines'

"""


EXPECTED_COMPILER_FLAGS = {
    '-Eonly':   CompilerFlag(description='Just run preprocessor, no output (for timings)', replace_with='-Eonly'),
    '-E':       CompilerFlag(description='Only run the preprocessor', replace_with='-E'),
    '-I':       CompilerFlag(description='Add directory to include search path', replace_with='-I ${1:value}'),

    '-analyzer-viz-egraph-graphviz':    CompilerFlag(description='Display exploded graph using GraphViz', replace_with='-analyzer-viz-egraph-graphviz'),
    '-analyzer-constraints':            CompilerFlag(description='Source Code Analysis - Symbolic Constraint Engines', replace_with='-analyzer-constraints ${1:value}')
}

@nottest
def test_parse_compiler_flags():
    compiler_flags = clang.parse_compiler_flags(SAMPLE_CLANG_OUTPUT)
    eq_(len(EXPECTED_COMPILER_FLAGS), len(compiler_flags))
    eq_(EXPECTED_COMPILER_FLAGS, compiler_flags)
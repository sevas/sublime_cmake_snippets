import sublime_plugin

from cmakehelpers.compilerflags.core import find_completions

CLANG_FLAGS = None
GCC_FLAGS = None


def plugin_loaded():
    CLANG_FLAGS = clang.make_compiler_flags_database()
    GCC_FLAGS = dict()


class CompilerFlagAutocomplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0],
                "source.cmake"):
            return []

        cursor = locations[0]
        # print '*** prefix: ', prefix
        # print '*** cursor pos:', cursor
        line_region = view.line(cursor)
        line_start, line_end = line_region.a, line_region.b
        cursor_offset = cursor - line_start
        current_line = view.substr(line_region)[:]
        # print '*** line before cursor: ', [current_line]
        clang_completions = find_completions('clang', CLANG_FLAGS, current_line, cursor_offset)
        gcc_completions = find_completions('gcc',  GCC_FLAGS, current_line, cursor_offset)
        return clang_completions + gcc_completions

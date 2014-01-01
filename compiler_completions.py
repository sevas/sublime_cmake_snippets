import sublime_plugin

from cmakehelpers.compilerflags import clang, gcc
from cmakehelpers.compilerflags import find_completions


COMPLETION_DATABASES = dict(
    clang=dict(loader=clang, database=None),
    gcc=dict(loader=gcc, database=None))


def log_message(s):
    print("CMakeSnippets: {0}".format(s))


def load_completion_databases():
    global COMPLETION_DATABASES
    for compiler_name, database_info in COMPLETION_DATABASES.iteritems():
        loader = database_info['loader']
        completion_database = loader.make_compiler_options_database()
        log_message("Loading {0} options database: {1} entries".format(compiler_name, len(completion_database)))
        database_info['database'] = completion_database


load_completion_databases()


class CompilerFlagAutocomplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "source.cmake"):
            return []

        cursor = locations[0]
        # print('*** prefix: ' + str(prefix))
        # print('*** cursor pos: ' + str(cursor))
        line_region = view.line(cursor)
        line_start, line_end = line_region.a, line_region.b
        cursor_offset = cursor - line_start
        current_line = view.substr(line_region)[:]
        # print '*** line befor cursor: ', [current_line]

        all_completions = list()
        for compiler_name, database_info in COMPLETION_DATABASES.iteritems():
            compiler_options_db = database_info['database']
            all_completions.extend(find_completions(compiler_name, compiler_options_db, current_line, cursor_offset))

        return all_completions

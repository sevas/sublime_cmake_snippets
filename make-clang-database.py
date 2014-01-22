
import os
import argparse

from cmakehelpers.compilerflags.clang import make_compiler_options_database, save_compiler_options_database


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--executable', action='store')
    parser.add_argument('--output-dir', action='store')

    args = parser.parse_args()

    clang_executable = 'clang'
    output_dir = os.getcwd()

    if args.executable:
        clang_executable = args.executable

    if args.output_dir:
        output_dir = args.output_dir

    clang_flags, clang_version = make_compiler_options_database(clang_executable)
    save_compiler_options_database(output_dir, clang_flags, clang_version)

if __name__ == "__main__":
    main()
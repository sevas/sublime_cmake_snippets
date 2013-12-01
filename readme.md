
# CMake snippets for Sublime Text 2/3 

## What is this?

An attempt to solve the pain induced writing CMakelists.

This package does not handle syntax highlighting. I rely on [this one](https://github.com/jcowgar/CMake-Sublime-Package) at the moment.

## Features

- Snippets for most of CMake's commands
- Completions for all CMake builtins variables 
- Quick access to commands and variables description in CMake's online documentation
- Compiler and linker flags completion for the following toolchains:
    - clang/clang++
    - gcc/g++
    - MSVC 2008 to 2012 (``cl.exe``)
    - Intel Composer XE 2013


## Choices

### Reasonable defaults

Some commands come with many options, but are very often used in a simpler fashion. When possible, I added these common usage patterns as snippets.

### Lowercase commands

These snippets 
The main reason is that I am not found of being yelled at by text files.

### Source list variables by default

For all the command that use a list of files as parameter (e.g. ``add_executable()``, ``add_library()``, ``source_group()``), the snippet assume that the files have been defined in a list. 

Even if CMake does not enforce this style, I find the following structure:

```CMake

    set(Hello_SOURCE_FILES 
        src/foo.cpp 
        src/bar.cpp 
        src/baz.cpp)

    add_executable(Hello ${Hello_SOURCE_FILES})
```

preferable to:

```CMake

    add_executable(Hello src/foo.cpp src/bar.cpp src/baz.cpp)
```

Source lists are reusable. CMakelists diffs and merges are easier to understand.

### Quoted paths

I find CMake files easier to scan when paths to files and directories are between quotes. All the snippets follow that rule.


### Unsupported commands

Some commands are not autocompleted. Mostly because they cover advanced CMake features, but also because they are pretty complicated to break down in tab-navigable snippets.



This is the current list of unsupported commands:

- ``add_compile_options()``
- ``cmake_host_system_information()``
- ``cmake_policy()``
- ``define_property()``




## License

The MIT license. See LICENSE.txt.


# CMakeSnippets for Sublime Text 2/3 

## Build status

[![Build Status (master)](https://travis-ci.org/sevas/sublime_cmake_snippets.png?branch=master)](https://travis-ci.org/sevas/sublime_cmake_snippets) (master)
[![Build Status (development)](https://travis-ci.org/sevas/sublime_cmake_snippets.png?branch=git/development)](https://travis-ci.org/sevas/sublime_cmake_snippets) (development)


## What is this?

An attempt to ruin the sheer joy of going back and forth hundred times a week between my text editor and the [online CMake documentation](http://www.cmake.org/cmake/help/v2.8.12/cmake.htm).

This is a collection of snippets for the CMake commands and variables.

## What is this not?

This package does not handle syntax highlighting. For this purpose, I rely on [this package](https://github.com/jcowgar/CMake-Sublime-Package) at the moment. You will need to install it as well to register the CMake file type in Sublime Text.

This is not a fully-featured completion engine for the CMake language. This means that you cannot move the cursor inside an already existing CMake command, hit <kbd>CTRL</kbd> <kbd>Tab</kbd> and get relevant suggestions. 

I can sense your disapointment. I feel the same.


## Features

- Snippets for CMake's commands
- Completions for all of CMake builtins variables 

### Planned features

- Quick access to commands and variables description in CMake's online documentation
- Compiler and linker flags completion for the following toolchains:
    - clang/clang++
    - gcc/g++
    - Microsoft Visual C++ 2008 to 2012
    - Intel Composer XE 2013


## Installation

The recommended way to install CMakeSnippets is to use [Package Control][wbond].
As mentionned before, you must first install the [CMake package](https://sublime.wbond.net/packages/CMake), also from Package Control.

### Manual installation

Download or clone this repository on your system in a directory called ``CMakeSnippets``, in the Sublime Text Packages directory for your platform:

- Mac: ``hg clone https://bitbucket.org/sevas/sublime_cmake_snippets ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/CMakeSnippets``
- Windows: ``hg clone https://bitbucket.org/sevas/sublime_cmake_snippets %APPDATA%\Sublime/ Text/ 2/\CMakeSnippets``
- Linux: ``hg clone https://bitbucket.org/sevas/sublime_cmake_snippets ~/.Sublime\ Text\ 2/Packages/CMakeSnippets``

This repository is mirrored on github, so you can also use git, if you are into that kind of things (here for Sublime Text 3):

- Mac: ``git clone https://github.com/sevas/sublime_cmake_snippets.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/User/CMakeSnippets``
- Windows: ``git clone https://github.com/sevas/sublime_cmake_snippets.git %APPDATA%\Sublime/ Text/ 3/\User\CMakeSnippets``
- Linux: ``git clone https://github.com/sevas/sublime_cmake_snippets.git ~/.Sublime\ Text\ 3/Packages/User/CMakeSnippets``


Restart Sublime Text and open a CMake build script.


## Usage

From whithin a CMake build script (e.g. a file named *CMakeLists.txt* or any file with a *.cmake* extension), when you start typing the snippet string, the suggestions popup list should appear. Hit <kbd>CTRL</kbd> <kbd>Tab</kbd> if it doesn't. Select the entry you want in the list and hit <kbd>Tab</kbd> to expand the shortcut into the associated snippet. 

All snippet short strings start the same way as the associated CMake command, and follow a loosely defined naming convention, which involves the first characters of the following words in the command. 

For instance:

- **add**\_**c**ustom\_**c**ommand() becomes _**addcc**_
- **string**(**APP**END) becomes _**stringapp**_
- **get**\_**f**ilename\_**c**omponent(**P**ATH) becomes _**getfcp**_

They are not all that intuitive, but I think they are pretty okay.
The main problem comes from the limited width of Sublime Text 2's suggestions box. Snippet strings have to stay quite small so there is space for the description string. Sublime Text 3, however, seems to adapt the size to the content.

A complete list of snippets is available from the Command Palette. Open the palette, type ``CMake`` to filter the CMake snippets, and type the beginning of a command to filter out only the snippets for that command. 


## Design choices

### Reasonable defaults

Some commands, such as [``find_library()``][cmake_find_library] or [``install()``][cmake_install] offer many different behaviours depending on the arguments you use. When possible, I added simpler, more common usage patterns as snippets. These shorthands are based both on the variants presented in the CMake documentation, and my personal experience writing CMake build scripts. Expectations may vary.



### Lowercase commands

I'm sure that there is a raging battle somewhere on the internet about whether one should use uppercase or lowercase characters for CMake commands. 

This package takes the strong stance of using lowercase. The main reason is that I am not fond of being yelled at by text files. 

Incidentally, the CMake documentation agrees with that.

### Source list variables by default

For all the commands that use a list of files as parameter (e.g. ``add_executable()``, ``add_library()``,or ``source_group()``), the associated snippet assumes that the files have been defined as a list variable. 

Even if CMake does not enforce this style, I find the following structure:

```
set(Hello_SOURCE_FILES 
    "src/foo.cpp" 
    "src/bar.cpp" 
    "src/baz.cpp")

source_group("hello" FILES ${Hello_SOURCE_FILES})

add_executable(Hello ${Hello_SOURCE_FILES})
```

preferable to:

```
add_executable(Hello src/foo.cpp src/bar.cpp src/baz.cpp)
```

Source lists are reusable. Layouting your source lists with one file per line makes diffing and merging CMake build scripts way easier. You should do it.


### Quoted paths

I find CMake files easier to scan when paths to files and directories are between quotes, because Sublime Text's CMake mode colors quoted strings in a different way.
You also never know when a path will contain spaces.

```
include_directories(
    "${Hello_INCLUDE_DIRS}"
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)
add_executable(Hello ${SOURCE_FILES})
```

Quoting paths removes the uncertainty about how the list of paths will be concatenated. All the snippets follow that rule.

### Variable arguments

When a snippet presents you two parameter placeholders prefilled with a name with index, like:

```
list(APPEND LIST_VARIABLE item1 item2)
```

it means this parameter accepts a variable number of arguments. The first two are laid out, add (or remove) whatever you need.

Choices between incompatible parameters are either indicated by 

- listing all the choices separated by a pipe (``|``) symbol (e.g. ``add_custom_command(TARGET targetname PRE_BUILD|PRE_LINK|POST_BUILD)``)
- having completely different snippets (e.g. ``string()`` and ``file()`` commands)

### Two spaces per indentation level

Don't email me.     

## License

CMakeSnippets is released under the [MIT license][opensource]. Do template files really count as code? I'm wondering.



## Acknowledgements

Many thanks to the author and contributors of the [InsertNums][insertnums] package. I couldn't have [done this][happynumbering] without you.


[wbond]: http://wbond.net/sublime_packages/package_control
[insertnums]: https://github.com/jbrooksuk/InsertNums
[opensource]: http://www.opensource.org/licenses/MIT
[happynumbering]: https://bitbucket.org/sevas/sublime_cmake_snippets/src/b827bbd909fc15d8fa956061fb517541d9a433b5/snippets/find_package_allopts.sublime-snippet?at=default
[cmake_find_library]: http://www.cmake.org/cmake/help/v2.8.12/cmake.html#command:find_library
[cmake_install]: http://www.cmake.org/cmake/help/v2.8.12/cmake.html#command:install


# CMake Snippets for Sublime Text 2/3 

## What is this?

An attempt to ruin the sheer joy of going back and forth hundred times a week between my text editor and the online CMake documentation.

This is a collection of snippets for the CMake commands and variables.

## What is this not?

This package does not handle syntax highlighting. For this purpose, I rely on [this package](https://github.com/jcowgar/CMake-Sublime-Package) at the moment. You will need to install it as well to register the CMake file type in Sublime Text.

This is not a fully-featured completion engine for the CMake language. This means that you cannot move the cursor inside an already existing CMake command, hit <kbd>CTRL</kbd> <kbd>TAB</kbd> and get relevant suggestions. 

I can sense your disapointment. I feel the same.


## Features

- Snippets for CMake's commands
- Completions for all of CMake builtins variables 

### Planned features

- Quick access to commands and variables description in CMake's online documentation
- Compiler and linker flags completion for the following toolchains:
    - clang/clang++
    - gcc/g++
    - MSVC 2008 to 2012 (``cl.exe``)
    - Intel Composer XE 2013


## Installation

1. Install Sublime Package Control
2. From inside Sublime Text 2, open Package Control's Command Pallet: CTRL SHIFT P (Windows, Linux) or CMD SHIFT P on Mac.
3. Type install package and hit Return. A list of available packages will be displayed.
4. Type CmakeSnippets and hit Return. The package will be downloaded to the appropriate directory.
5. Restart Sublime Text 2 to complete installation. Open a Markdown file and this custom theme. The features listed above should now be available.

Package control or copy to <STROOT>/Packages

But probably package control.


## Usage

From whithin a CMake script (e.g. a file named *CMakeLists.txt* or any file with a *.cmake* extension), when you start typing the snippet string, the completion popup list should appear. Hit <kbd>CTRL</kbd><kbd>TAB</kbd> if it doesn't. Select the entry you want in the list and hit <kbd>TAB</kbd>to expand it. 

Most snippet strings start the same way as the associated CMake command, and follow a loosely defined naming convention, which involves the first characters of the following words in the command. 

For instance:

- **add**\_**c**ustom\_**c**ommand() becomes _**addcc**_
- **string**(**APP**END) becomes _**stringapp**_
- **get**\_**f**ilename\_**c**omponent(**P**ATH) becomes _**getfcp**_

They are not all that intuitive, but I think they are pretty okay.
The main problem comes from the limited width of Sublime Text's suggestion box. Snippet strings have to stay quite small so there is space for the description string.

A complete list of snippets is available from the Command Palette. Open the palette, type ``CMake`` to filter the CMake snippets, and type the beginning of a command to filter out only the snippets for that command. 


## Choices

### Reasonable defaults

Some commands, such as [``find_library()``](http://www.cmake.org/cmake/help/v2.8.12/cmake.html#command:find_library) or [``install()``](http://www.cmake.org/cmake/help/v2.8.12/cmake.html#command:install) offer many different behaviours depending on the arguments you use. When possible, I added simpler, more common usage patterns as snippets. These shorthands are based both on CMake's documentation and my personal experience writing CMake build scripts. Expectations may vary.



### Lowercase commands

I'm sure that there is a raging battle somewhere on the internet about whether one should use uppercase or lowercase for CMake commands. 

This package takes the strong stance of using lowercase. The main reason is that I am not fond of being yelled at by text files. 

Incidentally, the CMake documentation agrees with that.

### Source list variables by default

For all the command that use a list of files as parameter (e.g. ``add_executable()``, ``add_library()``, ``source_group()``), the associated snippet assumes that the files have been defined as a list variable. 

Even if CMake does not enforce this style, I find the following structure:

```CMake
    set(Hello_SOURCE_FILES 
        "src/foo.cpp" 
        "src/bar.cpp" 
        "src/baz.cpp")

    source_group("hello" FILES ${Hello_SOURCE_FILES})

    add_executable(Hello ${Hello_SOURCE_FILES})
```

to be preferable to:

```CMake
    add_executable(Hello src/foo.cpp src/bar.cpp src/baz.cpp)
```

Source lists are reusable. Having source lists with one file per line makes
diffing and merging CMake scripts way easier. You should do it.


### Quoted paths

I find CMake files easier to scan when paths to files and directories are between quotes. You also never know when a path will contain spaces, so 
All the snippets follow that rule.

### Variable arguments

When a snippet presents you two parameter placeholders prefilled with a name like ``PARAM item1 item2``, it means this parameter accepts a variable number of arguments. The first two are laid out, add whatever you need

Choices between incompatible parameters are either indicated by 

- listing all the choices separated by a pipe (``|``) symbol (e.g. `` add_custom_command(TARGET targetname PRE_BUILD|PRE_LINK|POST_BUILD)``)
- having completely different snippets (e.g. ``string()`` and ``file()`` commands)

## License

The MIT license. See LICENSE.txt.


## Acknowledgements

Many thanks to the author and contributors of the [InsertNums](https://github.com/jbrooksuk/InsertNums) package. 
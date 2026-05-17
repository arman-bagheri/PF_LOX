## PF_LOX

PF_LOX is a tree walk interpreter for a functional variant
of the lox programming language written in python. The design and specifications of
the language are inspired by the book 'Crafting Interpreters' by Robert Nystrom.

This is an educational interpreter for a minimal functional language
with first-class functions, static scoping, and dynamic types. It is designed
to clearly illustrate lexing, parsing, ast generation and a basic tree walk
interpretation technique. 

## Features

- Lexing
- Recursive descent parsing
- First class functions
- Dynamic types
- Arrays
- Tree-walk interpretation
- Clear separation of evaluation and interpretation
- Closure and variable capturing
- Recursive functions
- Builtin functions
- Expressions
- Control flow
- syntax error and runtime error handling

## Installation and Use

### Requirements

Python 3.10+ (recommended)

### Usage

clone the repository:

>> git clone https://github.com/arman-bagheri/PF_LOX
>> cd pf_lox

Usage:

simply run the lox script in the main project directory by either giving the
address of a text file containing the a script:

>> ./lox examples/array.lox

or run it with no arguments for the shell version of the interpreter:

>> ./lox
>> 		println("Hello lox!");



## Documentation

Detailed documentation is available in the '/docs' directory.



## Project Status

This project is intended for educational purposes and experimentation.

It is not optimized for performance or production use.
## Architecture

This file contains the high level structure of the interpreter. 

Source Code
    |
    v
Lexer
    |
    v
Parser
    |
    v
Interpretation


### Lexer

The lexer reads the source code and by following the rules of the syntactic grammar, described
in the syntax.md file, produces a list of meaningful token objects.

### Parser

Taking the token list produced by the lexer, the parser produces an abstract syntax tree
representation of the written code, which in turn, could be used to produce another form of 
intermediate representation, to produce bytecode, or in this case directly interpreted.

### Interpreter

The interpreter here is a simple one. It defines a minimal runtime environment, including scoping, dictionaries as symbol tables, error handling, and other features, and directly walks the tree and interprets the program. 



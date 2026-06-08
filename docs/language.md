# Overview

PF_LOX is functional variant of the lox programming language from the book 
"crafting interpreters" written in python. it supports arrays, first class functions,
closures, and other features covered in this document.

## Values

Numbers     ->         Floating point representation
Boolean     ->         Boolean objects in python
String      ->         Immutable list of characters
NIL         ->         None in python
Functions   ->         represented as python objects containing a function definition and
                       a dictionary of captured variales
Arrays      ->         python list of other value types


## Variables and scoping

Variables are introduced and defined using the "let" keyword. The language is statically scoped.
we start with a global environment, which is just a dictionary of name-value pairs. Environments also have
one parent environment each. Each block statement creates a new environment whose parent is the environment of
the outer block statements. When referencing a variable, it is first checked in the current environment, then
the parent environment and then all the way down to the global environment. if not found an UndefinedVar error is
raised. This also creates a shadowing effect, if a variable is defined in a parent environment as well as a child
environment, the child environment's definition is used.

The parent environment of a function, is the environment in which it was defined, not where it is called. And in 
cases where the parent environment of a function might be destroyed after the function is defined, as in blocks
or inside other functions, we have closures which store their parent environment directly. This means that we also
have to define a call stack, to keep track of where our environment is and where it should go back to.

## Expressions and Statements

PF_LOX programs, are a sequence of statements, which in turn may or may not contain expressions that need evaluation.
Expressions in pf_lox are always evaluated to a primitive value, but statements are interpreted, and have effects like 
printing or defining execution flow or changing the state of the runtime environment.

## Functions

Functions are first class primitive values in lox. They can be assigned to variables, returned by other functions, 
and passed as argument. Closures are the way we store the lexical scope of where the function was defined.

var x = fun(x){return 2 * x;};
fun apply(f, x){
    return f(x);
}

During function calls, arguments are evaluated before the function is executed. 


## Truthiness

Lox has simple truthiness rules, only false and nil are falsy, other values are truthy.



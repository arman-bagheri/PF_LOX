## The syntax

In this file I will specify the syntactical structure of the grammar of the lox programming language implemented by this interpreter.

### Lexical Grammar
IDENTIFIER ::= LETTER ( LETTER | DIGIT )* ;
NUMBER ::= DIGIT+ ( "." DIGIT+ )? ;
STRING ::= "\"" ( ANY_CHAR - "\"" )* "\"" ;

DIGIT ::= "0"..."9" ;
LETTER ::= "a"..."z" | "A"..."Z" | "_";

### Syntactic Grammar

program ::= statement* ;

statement ::= 
              function_decl
            | var_decl
            | expr_stmt
            | while_stmt
            | for_stmt
            | if_stmt
            | return_stmt
            | block_stmt ;
            
function_decl ::= "fun" IDENTIFIER "(" parameters? ")" block_stmt ;
parameters ::= IDENTIFIER ( "," IDENTIFIER )* ;

var_decl ::= "var" IDENTIFIER ( "=" expression )? ";" ;
expr_stmt ::= expression ";" ;
while_stmt ::= "while" "(" expression ")" statement ;
for_stmt ::= "for" "(" ( var_decl | expr_stmt | ";")
                        expression? ";"
                        expression? ")" statement ;
if_stmt ::= "if" "(" expression ")" statement ("else" statement)? ;
return_stmt ::= "return" expression? ";" ;
block_stmt ::= "{" statement* "}" ;

### Expression grammar

expression ::= assignment ;
assignment ::= IDENTIFIER "=" assignment | logic_or ;
logic_or ::= logic_and ( "or" logic_and )* ;
logic_and ::= equality ( "and" equality)* ;
equality ::= comparison ( ("==" | "!=" ) comparison)* ;
comparison ::= term ( ("<" | ">" | "<=" | ">=") term )* ;
term ::= factor ( ( "+" | "-" ) factor)* ;
factor ::= unary ( ( "*" | "/" ) unary)* ;
unary ::= ( "!" | "-" ) unary | post ;
post ::= primary ( "[" expression "]" | "(" expresson ("," expression)* ")" )* ; 
primary ::= "true" | "false" | "nil" | NUMBER | STRING | IDENTIFIER | FUNCTION | ARRAY;

ARRAY ::= "[" ( expression ( "," expression )* )? "]" ;
FUNCTION ::= "fun" "(" parameters ")" "{" statement* "}";

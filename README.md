# Parser With GUI
This is a project in which we are to implemenet a Parser in Python along side a GUI for a basic programming language that represents a calculator.

## Context Free Grammar

line            → VAR = expression ;

line            → VAR ;

line            → exit_command

line            → UserIn VAR '=' expression ;

line            → Print expression ;

***

expression      → term

expression      → term '+' expression

expression      → term '-' expression

***

term            → factor

term            → factor '*' term

term            → factor '/' term


***

factor          → primary

factor          → primary '^' factor

***

primary         → NUMBER

primary         → VAR

primary         → '(' expression ')'

***

exit_command    → EXIT

***

## Explaination

Line:
- An expression followed by an exit command
- A line followed by an expression and an exit command
- An exit command
- A line followed by an exit command
- User input stored in a variable followed by an expression
- Print statements takes an expression and displays the result

Expression:
- A term
- A term followed by '+' and another expression
- A term followed by '-' and another expression
- A term followed by user input
- A variable

Term:
- A factor
- A factor multiplied by another term
- A factor divided by another term
- A factor followed by user input
- A variable

Factor:
- A primary expression
- A primary expression raised to the power of another factor
- A primary expression followed by user input
- A variable

Primary:
- A number
- An expression enclosed in parentheses

Exit Command:
- The exit command "EXIT"
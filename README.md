# Set Of Grammar Rules:

Line:
- An expression followed by an exit command
- A line followed by an expression and an exit command
- An exit command
- A line followed by an exit command
- User input stored in a variable followed by an expression

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

***

line            : expression exit_command     
                | line expression exit_command
                | exit_command		            
                | line exit_command
                | UserIn VAR '=' expression
                ;

expression      : term          
                | term '+' expression
                | term '-' expression
                | term UserIn
                | VAR                   
                ;

term            : factor    
                | factor '*' term
                | factor '/' term
                | factor UserIn       
                | VAR             
                ;

factor          : primary     
                | primary '^' factor   
                | primary UserIn
                | VAR                  
                ;

primary         : number            
                | '(' expression ')'
                ;

exit_command    : EXIT
                ;
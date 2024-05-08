import re

def tokenize(input_string):
    # Define regex patterns for each token type
    patterns = [
        (r'\+', 'Operator'),
        (r'-', 'Operator'),
        (r'\*', 'Operator'),
        (r'/', 'Operator'),
        (r'\^', 'Operator'),
        (r'=', 'Assignment'),
        (r';', 'Delimiter'),
        (r'User\s+In:', 'UserInput'),
        (r'Print:', 'Print'),
        (r'EXIT', 'ExitCommand'),
        (r'[a-zA-Z_][a-zA-Z0-9_]*', 'Var'),
        (r'\d+(\.\d*)?', 'Number'),
        (r'\(', 'LeftParen'),
        (r'\)', 'RightParen'),
        (r'\s+', 'Whitespace')
    ]

    
    tokens = []
    input_string = input_string.strip()
    line_number = 1
    
    while input_string:
        match = None
        for pattern, token_type in patterns:
            regex_match = re.match(pattern, input_string)
            if regex_match:
                match = (token_type, regex_match.group(0), line_number)
                input_string = input_string[regex_match.end():].strip()
                if token_type == 'UserInput' or token_type == 'Print':
                    line_number += 1
                break
        if not match:
            raise ValueError("Invalid token at line {}: '{}'".format(line_number, input_string))
        if match[1] != 'Whitespace':
            tokens.append(match)
    
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = 0

    def parse(self):
        self.advance()
        return self.line()

    def advance(self):
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
            self.index += 1
        else:
            self.current_token = None

    def match(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError("Unexpected token: {}".format(self.current_token))

    def line(self):
        if self.current_token[0] == 'UserInput':
            self.match('UserInput')
            var_name = self.current_token[1]
            self.match('Var')
            self.match('Assignment')
            expr_value = self.expression()
            self.match('Delimiter')
            return ('UserInput', var_name, expr_value)
        elif self.current_token[0] == 'Print':
            self.match('Print')
            expr_value = self.expression()
            self.match('Delimiter')
            return ('Print', expr_value)
        elif self.current_token[0] == 'ExitCommand':
            self.match('ExitCommand')
            return ('Exit',)
        elif self.current_token[0] == 'Var':
            var_name = self.current_token[1]
            self.match('Var')
            if self.current_token and self.current_token[0] == 'Assignment':
                self.match('Assignment')
                expr_value = self.expression()
                self.match('Delimiter')
                return ('Assignment', var_name, expr_value)
            elif self.current_token and self.current_token[0] == 'Delimiter':
                self.match('Delimiter')
                return ('Var', var_name)
            else:
                raise SyntaxError("Unexpected token: {}".format(self.current_token))

        else:
            raise SyntaxError("Unexpected token: {}".format(self.current_token))


    def expression(self):
        term_value = self.term()
        if self.current_token and self.current_token[0] == 'Operator':
            operator = self.current_token[1]
            if operator in ('+', '-'):
                self.match('Operator')
                return ('BinaryOp', operator, term_value, self.expression())
        return term_value

    def term(self):
        factor_value = self.factor()
        if self.current_token and self.current_token[0] == 'Operator':
            operator = self.current_token[1]
            if operator in ('*', '/'):
                self.match('Operator')
                return ('BinaryOp', operator, factor_value, self.term())
        return factor_value

    def factor(self):
        primary_value = self.primary()
        if self.current_token and self.current_token[0] == 'Operator':
            if self.current_token[1] == '^':
                self.match('Operator')
                return ('Exponentiation', primary_value, self.factor())
        return primary_value


    def primary(self):
        if self.current_token[0] == 'Var':
            var_name = self.current_token[1]
            self.match('Var')
            return ('Var', var_name)
        elif self.current_token[0] == 'Number':
            number_value = float(self.current_token[1])
            self.match('Number')
            return ('Number', number_value)
        elif self.current_token[0] == 'LeftParen':
            self.match('LeftParen')
            expr_value = self.expression()
            self.match('RightParen')
            return expr_value
        else:
            raise SyntaxError("Unexpected token: {}".format(self.current_token))
        
# Example usage:
# input_string = "c = a + b ;"

input_string = "Print: x / (a + b);"


try:
    tokens = tokenize(input_string)
    for token_type, token_value, line_number in tokens:
        print("Line:", line_number, "Token Type:", token_type, "Token Value:", token_value)

    parser = Parser(tokens)
    result = parser.parse()
    print("Parse Result:", result)

except ValueError as e:
    print("Error:", e)


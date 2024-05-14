import tkinter as tk
from tkinter import messagebox
import re


class Scanner:
    def __init__(self):
        # Define regex patterns for each token type
        self.patterns = [
            (r'\+', 'Operator'),
            (r'-', 'Operator'),
            (r'\*', 'Operator'),
            (r'/', 'Operator'),
            (r'\^', 'Operator'),
            (r'=', 'Assignment'),
            (r';', 'Delimiter'),
            (r'UserIn:', 'UserInput'),
            (r'Print:', 'Prisnt'),
            (r'EXIT', 'ExitCommand'),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'Var'),
            (r'\d+(\.\d*)?', 'Number'),
            (r'\(', 'LeftParen'),
            (r'\)', 'RightParen'),
            (r'\s+', 'Whitespace')
        ]

    def tokenize(self, input_string):
        tokens = []
        input_string = input_string.strip()
        line_number = 1

        while input_string:
            match = None
            for pattern, token_type in self.patterns:
                regex_match = re.match(pattern, input_string)
                if regex_match:
                    match = (token_type, regex_match.group(0), line_number)
                    input_string = input_string[regex_match.end():].strip()
                    if token_type == 'UserInput' or token_type == 'Print':
                        line_number += 1
                    break
            if not match:
                raise ValueError("Invalid token at line {}: '{}'".format(
                    line_number, input_string))
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
            raise SyntaxError("Unexpected token: {} at line {}".format(
                self.current_token, self.current_token[2]))

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
                raise SyntaxError("Unexpected token: {} at line {}".format(
                    self.current_token, self.current_token[2]))

        else:
            raise SyntaxError("Unexpected token: {} at line {}".format(
                self.current_token, self.current_token[2]))

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
            raise SyntaxError("Unexpected token: {} at line {}".format(
                self.current_token, self.current_token[2]))


def check_syntax():
    input_string = input_box.get("1.0", "end-1c")
    scanner_output.delete("1.0", "end")
    parser_output.delete("1.0", "end")
    error_box.delete("1.0", "end")
    try:
        # Call the scanner tokenize function
        scanner = Scanner()
        tokens = scanner.tokenize(input_string)
        for token in tokens:
            scanner_output.insert(
                "end", "Token Type: {}, Token Value: {}\n".format(token[0], token[1]))
        scanner_output.insert("end", "Tokenization complete.\n")
        error_box.insert("end", "Syntax check passed. No errors found.")
    except ValueError as e:
        error_box.insert("end", str(e))
    except Exception as e:
        error_box.insert("end", str(e))


def execute():
    input_string = input_box.get("1.0", "end-1c")
    scanner_output.delete("1.0", "end")
    parser_output.delete("1.0", "end")
    error_box.delete("1.0", "end")
    try:
        # Call the scanner and parser functions
        scanner = Scanner()
        tokens = scanner.tokenize(input_string)
        parser = Parser(tokens)
        result = parser.parse()
        parser_output.insert("end", "Parse Result: {}".format(result))
    except Exception as e:
        error_box.insert("end", str(e))


# GUI Setup
root = tk.Tk()
root.title("Parser and Scanner GUI")

# Input Box
input_label = tk.Label(root, text="Input String:")
input_label.grid(row=0, column=0, sticky="w")
input_box = tk.Text(root, height=4, width=50)
input_box.grid(row=0, column=1, columnspan=2)

# Output Boxes
scanner_output_label = tk.Label(root, text="Scanner Output:")
scanner_output_label.grid(row=1, column=0, sticky="w")
scanner_output = tk.Text(root, height=10, width=50)
scanner_output.grid(row=1, column=1, columnspan=2)

parser_output_label = tk.Label(root, text="Parser Output:")
parser_output_label.grid(row=2, column=0, sticky="w")
parser_output = tk.Text(root, height=4, width=50)
parser_output.grid(row=2, column=1, columnspan=2)

error_label = tk.Label(root, text="Errors:")
error_label.grid(row=3, column=0, sticky="w")
error_box = tk.Text(root, height=4, width=50)
error_box.grid(row=3, column=1, columnspan=2)

# Buttons
check_syntax_button = tk.Button(
    root, text="Check Syntax", command=check_syntax)
check_syntax_button.grid(row=4, column=1)

execute_button = tk.Button(root, text="Execute", command=execute)
execute_button.grid(row=4, column=2)

root.mainloop()

import re

def tokenize(input_string):
    # Define regex patterns for each token type
    patterns = [
        (r'\+', 'Operator: '),
        (r'-', 'Operator: '),
        (r'\*', 'Operator: '),
        (r'/', 'Operator: '),
        (r'\^', 'Operator: '),
        (r'=', 'Assignment: '),
        (r';', 'Delimiter: '),
        (r'User\s+In:', 'User In:'),
        (r'Print:', 'Print:'),
        (r'[a-zA-Z_][a-zA-Z0-9_]*', 'Var:'),
        (r'\d+(\.\d*)?', 'Number:'),
        (r'\(', 'Left Paren: '),
        (r'\)', 'Right Paren: ')
    ]
    
    tokens = []
    input_string = input_string.strip()
    
    while input_string:
        match = None
        for pattern, token_type in patterns:
            regex_match = re.match(pattern, input_string)
            if regex_match:
                match = (token_type, regex_match.group(0))
                input_string = input_string[regex_match.end():].strip()
                break
        if not match:
            raise ValueError("Invalid token at: '{}'".format(input_string))
        tokens.append(match)
    
    return tokens

# Example usage:
# Example usage:
# input_string = "Print: a + b * (c - 3) ^ 2"
input_string = "c = a % b"

try:
    tokens = tokenize(input_string)
    for token_type, token_value in tokens:
        print(token_type, token_value)
except ValueError as e:
    print("Error:", e)

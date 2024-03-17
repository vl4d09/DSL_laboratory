from enum import Enum
from typing import List

# Enum defining different types of tokens
class TokenType(Enum):
    NUMBER = 0        # Represents numeric values
    OPERATOR = 1      # Represents arithmetic operators (+, -, *, /)
    LEFT_PAREN = 2    # Represents left parenthesis '('
    RIGHT_PAREN = 3   # Represents right parenthesis ')'
    WHITESPACE = 4    # Represents whitespace characters
    ERROR = 5         # Represents an error token

# Class representing a token with its type, value, and position in the input string
class Token:
    def __init__(self, type: TokenType, value: str, position: int):
        self.type = type
        self.value = value
        self.position = position

    def __str__(self):
        return f"[{self.type}: {self.value}, position: {self.position}]"

# Class responsible for lexing arithmetic expressions, breaking them down into tokens
class ArithmeticLexer:
    def __init__(self, ignore_whitespace: bool = False):
        self.ignore_whitespace = ignore_whitespace

    def tokenize(self, input: str) -> List[Token]:
        tokens = []  # List to store tokens
        current_token = ''  # String to build the current token
        current_position = 0  # Current position in the input string
        left_paren_count = 0  # Count of left parentheses
        right_paren_count = 0  # Count of right parentheses
        last_digit_starting_position = 0  # Starting position of the last digit encountered

        # Iterate through each character in the input string
        for c in input:
            if c.isspace():
                # If whitespace should be ignored, skip to the next character
                if self.ignore_whitespace:
                    current_position += 1
                    continue
                # Add the current number token if any, and add the whitespace token
                self.add_number_if_needed(current_token, tokens, last_digit_starting_position)
                tokens.append(Token(TokenType.WHITESPACE, c, current_position))
            elif c in ['+', '-', '*', '/']:
                # Add the current number token if any, and add the operator token
                self.add_number_if_needed(current_token, tokens, last_digit_starting_position)
                tokens.append(Token(TokenType.OPERATOR, c, current_position))
            elif c.isdigit():
                # If the current token is empty, update the starting position of the last digit encountered
                if not current_token:
                    last_digit_starting_position = current_position
                # Append the digit to the current token
                current_token += c
            elif c == '(':
                # Add the current number token if any, and add the left parenthesis token
                self.add_number_if_needed(current_token, tokens, last_digit_starting_position)
                tokens.append(Token(TokenType.LEFT_PAREN, c, current_position))
                left_paren_count += 1
            elif c == ')':
                # Add the current number token if any, and add the right parenthesis token
                self.add_number_if_needed(current_token, tokens, last_digit_starting_position)
                right_paren_count += 1
                # Check if there are more right parentheses than left parentheses
                if right_paren_count > left_paren_count:
                    return self.invalid_token_error(c, current_position)
                tokens.append(Token(TokenType.RIGHT_PAREN, c, current_position))
            else:
                return self.invalid_token_error(c, current_position)
            current_position += 1  # Move to the next position in the input string

        # Check if the number of left parentheses matches the number of right parentheses
        if left_paren_count != right_paren_count:
            return self.invalid_token_error("Mismatched parentheses", len(input))

        # Add the current number token if any
        self.add_number_if_needed(current_token, tokens, last_digit_starting_position)

        return tokens  # Return the list of tokens

    # Method to add the current number token to the list if it's not empty
    def add_number_if_needed(self, current_token, tokens, last_digit_starting_position):
        if current_token:
            tokens.append(self.create_token(current_token, last_digit_starting_position))
            current_token = ''  # Clear the current token

    # Method to create a token from the provided string and position
    def create_token(self, token_string, position):
        if token_string.isdigit():
            return Token(TokenType.NUMBER, token_string, position)
        else:
            return Token(TokenType.ERROR, f"Invalid expression: {token_string} at position {position}.", position)

    # Method to create an error token with the provided message and position
    def invalid_token_error(self, token, position):
        return [Token(TokenType.ERROR, f"Invalid expression: {token} at position {position}.", position)]

# Example usage
lexer = ArithmeticLexer()
tokens = lexer.tokenize("3 + 4 * (2 - 1)")
for token in tokens:
    print(token)

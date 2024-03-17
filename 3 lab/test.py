from arithmetic_lexer import ArithmeticLexer

lexer = ArithmeticLexer()
expressions = [
    "3 + 4 * (2 - 1)",
    "10 / (5 - 3) + 2",
    "1 + 2 + 3 + 4 + 5",
    "10 / 0"  
]

for expression in expressions:
    tokens = lexer.tokenize(expression)
    print(f"Expression: {expression}")
    print("Tokens:")
    for token in tokens:
        print(token)
    print()

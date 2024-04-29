# Topic: Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Cretu Dumitru and cudos to the Vasile Drumea with Irina Cojuhari
### Author: Ungureanu Vlad
----

## Overview
&ensp;&ensp;&ensp; The process of gathering syntactical meaning or doing a syntactical analysis over some text can also be called parsing. It usually results in a parse tree which can also contain semantic information that could be used in subsequent stages of compilation, for example.

&ensp;&ensp;&ensp; Similarly to a parse tree, in order to represent the structure of an input text one could create an Abstract Syntax Tree (AST). This is a data structure that is organized hierarchically in abstraction layers that represent the constructs or entities that form up the initial text. These can come in handy also in the analysis of programs or some processes involved in compilation.


## Objectives:
1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens. 
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.

## Introduction:

In computer science, parsing is the process of analyzing a string of symbols according to the rules of a formal grammar. It is a fundamental step in many language processing tasks, such as compiling programming languages, interpreting commands, and analyzing data formats.

One common type of parsing is syntax analysis, which involves breaking down a sequence of tokens (symbols) into a hierarchical structure that represents the grammatical structure of the input. This hierarchical structure is typically represented by an abstract syntax tree (AST), which is used for further processing or evaluation.

In this context, we will explore how to tokenize an arithmetic expression, parse the tokens into an AST, and then print the tokens and the AST. We will use Python to implement a lexer to tokenize the input, a parser to build the AST, and functions to print the tokens and the AST in a human-readable format.

This process will demonstrate the fundamental concepts of lexical analysis, parsing, and abstract syntax trees, which are essential components in many language processing applications.



    
## Implementation


1. **Lexer (Tokenization):**
   - The lexer (`Lexer` class) takes an input string and breaks it down into tokens.
   - It uses regular expressions to match token patterns such as integers, operators, and parentheses.
   - Each token is represented by a `Token` object, which contains a type (from the `TokenType` enumeration) and a value (the actual token value).

   ```python
   class Lexer:
       def __init__(self, text):
           self.text = text
           self.pos = 0
           self.current_token = None
           self.tokens = []

       def tokenize(self):
           token_specification = [
               (TokenType.INTEGER, r'\d+'),
               (TokenType.PLUS, r'\+'),
               (TokenType.MINUS, r'\-'),
               (TokenType.TIMES, r'\*'),
               (TokenType.DIVIDE, r'\/'),
               (TokenType.LPAREN, r'\('),
               (TokenType.RPAREN, r'\)'),
               (TokenType.EOF, r'\Z')
           ]

           token_regex = '|'.join(f'(?P<{tok.name}>{pattern})' for tok, pattern in token_specification)
           for mo in re.finditer(token_regex, self.text):
               kind = mo.lastgroup
               value = mo.group()
               tok_type = TokenType[kind]
               if tok_type == TokenType.INTEGER:
                   value = int(value)  # Convert to integer
               self.tokens.append(Token(tok_type, value))

           self.tokens.append(Token(TokenType.EOF, None))
   ```

2. **Parser (Syntax Analysis):**
   - The parser (`Parser` class) takes the list of tokens produced by the lexer and parses them into an abstract syntax tree (AST).
   - It uses recursive descent parsing, where each method corresponds to a different level of the grammar.

   ```python
   class Parser:
       def __init__(self, lexer):
           self.lexer = lexer
           self.tokens = lexer.tokens
           self.current_token = None
           self.pos = -1
           self.advance()

       def advance(self):
           self.pos += 1
           if self.pos < len(self.tokens):
               self.current_token = self.tokens[self.pos]
           else:
               self.current_token = Token(TokenType.EOF, None)

       def parse(self):
           return self.expression()

       def expression(self):
           return self.addition()

       def addition(self):
           result = self.term()

           while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
               op = self.current_token
               self.advance()
               right = self.term()
               result = BinOp(left=result, op=op, right=right)

           return result

       # Other methods (term, factor) go here...
   ```

3. **Abstract Syntax Tree (AST):**
   - The AST represents the structure of the arithmetic expression in a tree-like format.
   - Each node in the tree corresponds to an operation or a value in the expression.

   ```python
   class AST:
       pass

   class BinOp(AST):
       def __init__(self, left, op, right):
           self.left = left
           self.op = op
           self.right = right

   class Num(AST):
       def __init__(self, token):
           self.token = token
           self.value = token.value
   ```

4. **AST Printing:**
   - The `print_ast` function recursively prints the AST in a human-readable format.

   ```python
   def print_ast(node, level=0):
       indent = '  ' * level
       if isinstance(node, BinOp):
           print(f'{indent}BinOp:')
           print(f'{indent}  Left:')
           print_ast(node.left, level+2)
           print(f'{indent}  Op: {node.op.value}')
           print(f'{indent}  Right:')
           print_ast(node.right, level+2)
       elif isinstance(node, Num):
           print(f'{indent}Num: {node.value}')
   ```

5. **Main Function:**
   - The `main` function combines the lexer, parser, and AST classes to process an arithmetic expression.

   ```python
   def main():
       text = "3 + 4 * (2 - 1)"
       lexer = Lexer(text)
       lexer.tokenize()
       parser = Parser(lexer)
       ast = parser.parse()

       print("Tokens:")
       for token in lexer.tokens:
           print(token)

       print("\nAST:")
       print_ast(ast)

   if __name__ == "__main__":
       main()
   ```

The code presented is a simplified implementation of a lexer, parser, and abstract syntax tree (AST) for arithmetic expressions. This implementation follows a traditional approach to language processing, where the input expression is tokenized, parsed, and transformed into a structured representation for further analysis or evaluation.

1. **Lexer (Tokenization):**
   - The lexer is the first stage of the language processing pipeline. Its primary responsibility is to break down the input expression into tokens, which are the smallest units of the language's syntax.
   - Regular expressions are commonly used in lexers to define token patterns and match them against the input text. This approach provides flexibility and ease of defining token types.
   - Each token has a type (e.g., INTEGER, PLUS) and a value (the actual token value). This separation allows for more straightforward handling and processing of tokens in subsequent stages.

2. **Parser (Syntax Analysis):**
   - The parser receives the sequence of tokens produced by the lexer and analyzes their arrangement to determine the syntactic structure of the input expression.
   - Recursive descent parsing is a widely used parsing technique that aligns well with the structure of the grammar. Each method in the parser corresponds to a production rule in the grammar, making the parsing process more intuitive and modular.
   - The parser constructs an abstract syntax tree (AST) as it parses the input expression. The AST represents the hierarchical structure of the expression, making it easier to perform further analysis or evaluation.

3. **Abstract Syntax Tree (AST):**
   - The AST is a structured representation of the syntactic elements of the input expression. It consists of nodes representing operations (e.g., addition, multiplication) and values (e.g., integers).
   - Building an AST allows for a clearer separation of concerns between syntax and semantics. It provides a foundation for subsequent stages of compilation or interpretation, such as type checking, optimization, and code generation.

4. **Design Rationale:**
   - The chosen approach follows a traditional methodology for language processing, leveraging well-established techniques and principles.
   - Modular design: The code is organized into separate classes for the lexer, parser, and AST, promoting code reuse, maintainability, and extensibility.
   - Clear separation of concerns: Each component (lexer, parser, AST) has a distinct responsibility, making the codebase easier to understand, test, and modify.
   - Pythonic idioms: The code makes use of Python's features, such as classes, enumerations, and list comprehensions, to express concepts in a concise and readable manner.

5. **Future Considerations:**
   - Error handling: The current implementation lacks robust error handling mechanisms, such as reporting syntax errors or handling invalid input gracefully. Enhancing error reporting capabilities would improve the usability and robustness of the code.
   - Support for more complex expressions: While the current implementation handles basic arithmetic expressions, extending it to support variables, functions, and control structures would make it more versatile and applicable to a wider range of scenarios.
   - Optimization: Depending on the intended use case, optimizing the lexer, parser, and AST construction process may be necessary to improve performance, especially for large input expressions or high-frequency use scenarios.

    Overall, this code serves as a foundational building block for language processing tasks, providing a starting point for implementing more sophisticated compilers, interpreters, or domain-specific languages. Its modular and extensible design allows for further refinement and customization to suit specific requirements and use cases.
    
    ---

    **Visual**
    
    ![outputyo](/6%20lab/output.png)

    ---

## Conclusion:

In conclusion, we have explored the process of tokenizing an arithmetic expression, parsing the tokens into an abstract syntax tree (AST), and printing the tokens and the AST. This process demonstrates the fundamental concepts of lexical analysis, parsing, and abstract syntax trees, which are crucial in many language processing applications.

The lexer breaks down the input expression into tokens, which are then parsed by the parser to create an AST that represents the structure of the expression. The AST provides a hierarchical representation that can be used for further analysis or evaluation of the expression.

By understanding these concepts and implementing them in Python, we have gained insight into how languages can be processed and understood by computers. This knowledge can be applied to more complex language processing tasks, such as compiling programming languages, interpreting commands, and analyzing data formats.

Overall, this exercise has provided a practical introduction to parsing and abstract syntax trees, highlighting their importance in language processing and laying the foundation for further exploration in this field.
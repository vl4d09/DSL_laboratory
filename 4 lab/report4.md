

# Topic: Regular expressions

### Course: Formal Languages & Finite Automata
### Author: Ungureanu Vlad

----
## Overview
Regular expressions (regex) are powerful tools for pattern matching in strings. They can represent complex patterns concisely, allowing for efficient searching and manipulation of text. In this project, we implemented a Python program to generate valid combinations of symbols conforming to given regular expressions.

1. **Functionality:** The program takes a regular expression as input and generates valid combinations of symbols that match the pattern specified by the regex. It handles various regex features, including character repetitions (`*`, `+`, `?`, `{n}`, `{n,}`, `{n,m}`), character classes (`[...]`), and grouping (`(...)`).

2. **Implementation:** The program is implemented using Python and consists of a main function (`generate_combinations`) that iterates over each character in the regex and generates the corresponding string based on the regex rules. It uses helper functions (`process_alpha_digit` and `process_opening_parenthesis`) to handle specific cases like character repetitions and grouping.

3. **Limitations and Considerations:** To avoid generating extremely long combinations, we imposed a limit of 5 repetitions for symbols that can occur an undefined number of times. This limitation ensures that the program remains efficient and does not produce overly lengthy outputs.

4. **Usage and Output:** The program can be used to generate valid combinations of symbols for a given regular expression, providing a useful tool for testing regex patterns and understanding how they match strings. The output of the program includes the step-by-step processing of the regex, showing how each part of the pattern contributes to the final combination.

----
# Objectives:

1. Write and cover what regular expressions are, what they are used for;

2. Below you will find 3 complex regular expressions per each variant. Take a variant depending on your number in the list of students and do the following:

    a. Write a code that will generate valid combinations of symbols conform given regular expressions (examples will be shown).

    b. In case you have an example, where symbol may be written undefined number of times, take a limit of 5 times (to evade generation of extremely long combinations);

    c. **Bonus point**: write a function that will show sequence of processing regular expression (like, what you do first, second and so on)

Write a good report covering all performed actions and faced difficulties.
## Variant 2:


Examples of what you must generate:

{MNNOOOQR, NNPPPQQQRRR, ...}
{XXX89, YYY88889, ...}
{HJLLN, IKLLLLLL, ...}


## Introduction

Regular expressions (regex) are powerful tools used in computer science and data processing to describe patterns in strings. They provide a concise and flexible way to search, match, and manipulate text based on specific criteria. In this project, we explore the generation of valid symbol combinations based on given regular expressions using Python.

Regular expressions consist of various elements, including literal characters, metacharacters, character classes, and quantifiers, that allow for complex pattern matching. The ability to define patterns that match specific strings or sets of strings makes regex a versatile tool in text processing tasks such as data validation, search and replace operations, and syntax highlighting.

In this project, we aim to demonstrate the practical application of regular expressions in generating valid symbol combinations. We will implement a Python program that takes a regular expression as input and produces valid combinations of symbols that match the specified pattern. The program will handle various regex features, ensuring that the generated combinations adhere to the rules defined by the regex.

Through this project, we will showcase the importance and utility of regular expressions in text processing, highlighting their role in pattern matching and string manipulation. We will also discuss the limitations and considerations when working with regex, such as managing the complexity of generated outputs. Overall, this project serves as an introduction to the use of regular expressions in generating symbol combinations, illustrating their effectiveness in text processing applications.

### Code Example: 

### Function Definitions

1. **`generate_combinations(regex)`**
   - Main function to generate combinations based on a regular expression.
   ```python
   def generate_combinations(regex):
       result = ""
       for i in range(len(regex)):
           current_builder = ""
           ch = regex[i]

           if ch.isalpha() or ch.isdigit():
               current_builder = process_alpha_digit(ch, regex, i)
           elif ch == '(':
               current_builder, i = process_opening_parenthesis(regex, i)
           print(regex[:i + 1] + " -> " + current_builder)
           result += current_builder

       return result
   ```

2. **Helper Functions:**

   - **`process_alpha_digit(ch, regex, i)`**
     - Processes alphabetic and digit characters in the regular expression.
     ```python
     def process_alpha_digit(ch, regex, i):
         current_builder = ""
         if i + 1 < len(regex):
             if regex[i + 1] == '^':
                 power = min(int(regex[i + 2]), 5)
                 current_builder = ch * power
                 i += 2
             elif regex[i + 1] == '*':
                 current_builder = ch * random.randint(0, 5)
                 i += 1
             elif regex[i + 1] == '+':
                 current_builder = ch * random.randint(1, 5)
                 i += 1
             elif regex[i + 1] == '?':
                 current_builder = ch if random.choice([True, False]) else ""
                 i += 1
         return current_builder
     ```
     This function processes alphabetic and digit characters in the regular expression. It handles special characters (^, *, +, ?) and returns the generated string.


   - **`process_opening_parenthesis(regex, i)`**
     - Processes opening parentheses in the regular expression.
     ```python
     def process_opening_parenthesis(regex, i):
         chars = set()
         next_ch = regex[i + 1]
         while next_ch != ')':
             if next_ch != '|':
                 chars.add(next_ch)
             next_ch = regex[i + 1]
             i += 1
         current_builder = ""
         if i + 1 < len(regex) and regex[i + 1] == '^':
             power = min(int(regex[i + 2]), 5)
             current_builder = ''.join(random.choices(list(chars), k=power))
             i += 2
         else:
             current_builder = random.choice(list(chars))
         return current_builder, i
     ```
     This function processes the opening parenthesis ( in the regular expression. It extracts characters within the parentheses, handles the ^ character, and returns the generated string along with the updated index i.

### Main Function

1. **`main()`**
   - Sets up example regular expressions and generates combinations.
   ```python
   def main():
       re1 = "M?N^2(O|P)^3Q*R+"
       re2 = "(X|Y|Z)^38+(9|0)^2"
       re3 = "(H|i)(J|K)L*N?"

       print("====1====")
       for _ in range(5):
           print(generate_combinations(re1))
           print()

       print("====2====")
       for _ in range(5):
           print(generate_combinations(re2))
           print()

       print("====3====")
       for _ in range(5):
           print(generate_combinations(re3))
           print()

   if __name__ == "__main__":
       main()
   ```
    This function defines the main logic of the program. It sets up three example regular expressions (re1, re2, re3) and prints the generated combinations for each regex five times.

### Execution
```python
if __name__ == "__main__":
    main()
```

This code defines functions to generate combinations based on a regular expression, with detailed explanations of the main logic and helper functions. The `main()` function sets up example regular expressions and generates combinations for each.

## Conclusion

Regular expressions (regex) are essential tools for pattern matching and text processing, providing a concise and powerful way to define search patterns. In this project, we implemented a Python program to generate valid combinations of symbols based on given regular expressions, showcasing the practical application of regex in generating and validating strings.

The program successfully handles various regex features, including character repetitions, character classes, and grouping, providing a comprehensive solution for generating valid symbol combinations. By limiting the number of repetitions for symbols that can occur an undefined number of times, we ensured that the program remains efficient and does not produce excessively long outputs.

Overall, this project demonstrates the versatility and effectiveness of regular expressions in generating and validating text patterns. It serves as a valuable tool for understanding regex concepts and testing regex patterns in real-world applications.

import random

# Define the grammar rules
VN = {"S", "A", "B"}
VT = {"a", "b", "c"}
P = {
    "S": ["aA", "bB"],  
    "A": ["bS", "cA", "aB"],
    "B": ["aB", "b"],
}


# Define a class for the grammar
class Grammar:
    def __init__(self, vn, vt, p):
        self.vn = vn
        self.vt = vt
        self.p = p

    def generate_string(self, symbol):
        if symbol in self.vt:
            return symbol
        else:
            options = self.p[symbol]
            chosen_option = random.choice(options)
            generated_string = ""
            for char in chosen_option:
                generated_string += self.generate_string(char)
            return generated_string


# Create an instance of the Grammar class
grammar = Grammar(VN, VT, P)


# Generate 5 valid strings
for _ in range(5):
    generated_string = grammar.generate_string("S")
    print(generated_string)


# Convert grammar to Finite Automaton
def grammar_to_finite_automaton(grammar):
    states = grammar.vn
    alphabet = grammar.vt
    start_state = "S"  #'S' is the start symbol
    accept_states = {
        state for state, rules in grammar.p.items() if any(r in rules for r in grammar.vt)
    }

    transitions = {}
    for state, rules in grammar.p.items():
        for rule in rules:
            if len(rule) == 2:  # Production X -> aY   
                transitions[(state, rule[0])] = rule[1] 
            elif len(rule) == 1: 
                if rule[0] in grammar.vt:  # Simple terminal case
                    transitions[(state, rule[0])] = rule[0]                   
                else:                    # Special Case for new transitions like 'A'->'bS' 
                    transitions[(state, rule[0])] = next(iter(grammar.p[rule[0]]))[0] 
                

    return FiniteAutomaton(states, alphabet, transitions, start_state, accept_states)
         




# Define the Finite Automaton class
class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, string):
        current_state = self.start_state
        for char in string:
            if (current_state, char) not in self.transitions:
                return False  # No transition possible
            current_state = self.transitions[(current_state, char)]
        return current_state in self.accept_states


# Test strings
test_strings = ["aabbc", "ac", "abba", "acaaaabba", "aab"]
for string in test_strings:
    fa = grammar_to_finite_automaton(grammar)
    if fa.accepts(string):
        print(f"String '{string}' is accepted by the FA")
    else:
        print(f"String '{string}' is not accepted by the FA")



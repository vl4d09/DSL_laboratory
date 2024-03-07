import random

class FiniteAutomaton:
    def __init__(self):
        # Initialize the finite automaton with empty sets
        self.Q = set()      # Set of states
        self.Sigma = set()  # Input alphabet
        self.delta = set()  # Transitions
        self.q0 = None      # Initial state
        self.F = set()      # Set of accepting states

    def string_belongs_to_language(self, input_string):
        # Check if the input string belongs to the language recognized by the automaton
        current_state = self.q0
        for symbol in input_string:
            next_states = {next_state for (state, input_symbol, next_state) in self.delta
                           if state == current_state and input_symbol == symbol}
            if not next_states:
                return False
            current_state = next_states.pop()
        return current_state in self.F

    def to_regular_grammar(self):
        # Convert the finite automaton to a regular grammar
        regular_grammar = Grammar()
        regular_grammar.VN = self.Q
        regular_grammar.VT = self.Sigma
        regular_grammar.P = {}

        for state in self.Q:
            regular_grammar.P[state] = []

        for transition in self.delta:
            if transition[2] != 'X':
                next_state_str = ''.join(transition[2])  # Convert tuple to string
                regular_grammar.P[transition[0]].append(transition[1] + next_state_str)  # Concatenate strings

        return regular_grammar

    def is_deterministic(self):
        # Check if the automaton is deterministic
        for state in self.Q:
            for symbol in self.Sigma:
                next_states = {next_state for (_, input_symbol, next_state) in self.delta
                               if _ == state and input_symbol == symbol}
                if len(next_states) > 1:
                    return False
        return True

    def to_deterministic_finite_automaton(self):
        # Convert the non-deterministic finite automaton (NFA) to a deterministic finite automaton (DFA)
        dfa = FiniteAutomaton()
        dfa.Sigma = self.Sigma
        dfa.q0 = frozenset([self.q0])  # Initial state is the epsilon closure of the original initial state
        dfa.F = set()
        dfa.Q = set()  # Initialize set of states
        dfa.delta = set()

        def epsilon_closure(state):
            # Compute epsilon closure of a state in the NFA
            closure = set(state)
            stack = list(state)
            while stack:
                currentState = stack.pop()
                for (_, input_symbol, nextState) in self.delta:
                    if currentState == nextState and input_symbol == 'ε' and nextState not in closure:
                        closure.add(nextState)
                        stack.append(nextState)
            return frozenset(closure)

        unprocessed_states = [dfa.q0]
        dfa.Q.add(dfa.q0)

        while unprocessed_states:
            current_state = unprocessed_states.pop(0)
            for symbol in dfa.Sigma:
                next_state = set()
                for state in current_state:
                    next_state |= {next_state for (_, input_symbol, next_state) in self.delta
                                   if state in current_state and input_symbol == symbol}
                next_state_closure = epsilon_closure(next_state)
                if next_state_closure:
                    dfa.delta.add((current_state, symbol, next_state_closure))
                    if next_state_closure not in dfa.Q:
                        dfa.Q.add(next_state_closure)
                        unprocessed_states.append(next_state_closure)
                    if any(state in self.F for state in next_state_closure):
                        dfa.F.add(next_state_closure)

        return dfa

class Grammar:
    def __init__(self):
        # Initialize the grammar with empty sets and dictionary
        self.VN = set()  # Set of non-terminals
        self.VT = set()  # Set of terminals
        self.P = {}      # Dictionary of productions

    def generate_string(self):
        # Generate strings from the grammar
        generated_strings = []
        for _ in range(5):
            generated_string = self._generate_string_helper('S', '')
            generated_strings.append(generated_string)
        return generated_strings

    def _generate_string_helper(self, symbol, current_string):
        # Helper function to recursively generate strings
        if symbol in self.VT:
            return current_string + symbol
        else:
            productions = self.P[symbol]
            chosen_production = random.choice(productions)
            for s in chosen_production:
                current_string = self._generate_string_helper(s, current_string)
            return current_string

    def to_finite_automaton(self):
        # Convert the grammar to a finite automaton
        finite_automaton = FiniteAutomaton()

        finite_automaton.Q = self.VN.union(self.VT)
        finite_automaton.Sigma = self.VT
        finite_automaton.delta = set()

        for non_terminal, productions in self.P.items():
            for production in productions:
                if len(production) > 1:
                    current_state = production[0]
                    next_state = production[1]
                    finite_automaton.delta.add((non_terminal, current_state, next_state))
                else:
                    if non_terminal in finite_automaton.F:
                        finite_automaton.delta.add((non_terminal, production, 'X'))
                    else:
                        if production == 'b':
                            finite_automaton.delta.add((non_terminal, production, 'X'))
                        elif production == 'd':
                            finite_automaton.delta.add((non_terminal, production, 'X'))
                        else:
                            finite_automaton.delta.add((non_terminal, production, production))

        finite_automaton.q0 = 'S'
        finite_automaton.F = {'X'}

        return finite_automaton

    def check_grammar_type(self):
        start_symbol = None
        has_epsilon = False
        for non_terminal, productions in self.P.items():
            if not start_symbol:
                start_symbol = non_terminal
            for production in productions:
                if 'ε' in production:
                    has_epsilon = True
                if len(production) > 2:
                    return "Type-0 (Unrestricted)"
                if len(production) == 2:
                    if production[0] in self.VN and production[1] in self.VT:
                        return "Type-1 (Context-Sensitive)"
                if len(production) == 1:
                    if production[0] in self.VT:
                        return "Type-3 (Regular)"
        if start_symbol and not has_epsilon:
            return "Type-2 (Context-Free)"
        return "Type-0 (Unrestricted)"  # Most general case

# Define the grammar variant
grammar = Grammar()
grammar.VN = {"S", "A", "B"}
grammar.VT = {"a", "b", "c"}
grammar.P = {
    "S": ["aA", "bB"],
    "A": ["bS", "cA", "aB"],
    "B": ["aB", "b"],
}

# Check the type of each grammar
print("Grammar Classification:", grammar.check_grammar_type())

# Define the finite automaton variant ( states )
finite_automaton = FiniteAutomaton()
finite_automaton.Q = {'q0', 'q1', 'q2', 'q3'}
finite_automaton.Sigma = {'a', 'b'}
finite_automaton.delta = {('q0', 'a', 'q1'), ('q1', 'b', 'q2'), ('q1', 'a', 'q3'),
                          ('q0', 'b', 'q2'), ('q2', 'b', 'q3'), ('q1', 'a', 'q1')}
finite_automaton.q0 = 'q0'
finite_automaton.F = {'q3'}

# Convert finite automaton to regular grammar
regular_grammar = finite_automaton.to_regular_grammar()

# Print the regular grammar productions
print("Conversion to grammar:")
for non_terminal, productions in regular_grammar.P.items():
    for production in productions:
        print(non_terminal, "->", production)

# Determine if the finite automaton is deterministic
is_deterministic = finite_automaton.is_deterministic()

if is_deterministic:
    print("The NDFA is deterministic.")
else:
    print("The NDFA is non-deterministic.")

# Convert finite automaton to deterministic finite automaton
dfa = finite_automaton.to_deterministic_finite_automaton()

# Check if the resulting DFA is deterministic
is_deterministic_dfa = dfa.is_deterministic()
if is_deterministic_dfa:
    print("The converted DFA is deterministic.")
else:
    print("The converted DFA is non-deterministic.")

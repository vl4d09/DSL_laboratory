from collections import defaultdict

class CNFConverter:
    def __init__(self, VN, VT, P, S):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S
        self.epsilon = 'ε'

    def remove_epsilon_productions(self):
        # Find nullable symbols (symbols that can produce epsilon)
        nullable = set()
        for prod in self.P:
            if self.epsilon in self.P[prod]:
                nullable.add(prod)
        
        # Calculate the closure of nullable symbols
        while True:
            new_nullable = set()
            for prod in self.P:
                if all(ch in nullable for ch in self.P[prod]):
                    new_nullable.add(prod)
            if new_nullable.issubset(nullable):
                break
            nullable |= new_nullable

        # Remove epsilon productions
        new_P = defaultdict(set)
        for prod in self.P:
            for null_set in self.powerset(self.P[prod]):
                if len(null_set) > 0 and len(null_set) < len(self.P[prod]):
                    new_P[prod].add(''.join(null_set))
            if len(new_P[prod]) == 0:
                new_P[prod].add(self.epsilon)
        
        self.P = new_P

    def remove_unit_productions(self):
        # Find unit productions (A -> B)
        unit_prods = defaultdict(set)
        for var in self.VN:
            for prod in self.P[var]:
                if len(prod) == 1 and prod in self.VN:
                    unit_prods[var].add(prod)
        
        # Calculate the closure of unit productions
        while True:
            new_unit_prods = defaultdict(set)
            for var in unit_prods.copy():
                for unit_prod in unit_prods[var].copy():
                    new_unit_prods[var] |= unit_prods[unit_prod]
            if all(new_unit_prods[var].issubset(unit_prods[var]) for var in unit_prods):
                break
            for var in new_unit_prods:
                unit_prods[var] |= new_unit_prods[var]

        # Remove unit productions
        new_P = defaultdict(set)
        for var in self.VN:
            for prod in self.P[var]:
                if len(prod) > 1 or prod not in self.VN:
                    new_P[var].add(prod)
            for unit_prod in unit_prods[var]:
                new_P[var] |= self.P[unit_prod]

        self.P = new_P

    def remove_inaccessible_symbols(self):
        # Find reachable symbols from the start symbol
        reachable = set()
        reachable.add(self.S)
        while True:
            new_reachable = set()
            for var in self.VN:
                if any(ch in reachable for prod in self.P[var] for ch in prod):
                    new_reachable.add(var)
            if new_reachable.issubset(reachable):
                break
            reachable |= new_reachable

        # Remove unreachable symbols
        new_P = defaultdict(set)
        for var in reachable:
            new_P[var] = self.P[var]

        self.VN = reachable
        self.P = new_P

    def remove_non_productive_symbols(self):
        # Find productive symbols
        productive = set()
        for var in self.VN:
            if any(all(ch in productive or ch in self.VT for ch in prod) for prod in self.P[var]):
                productive.add(var)

        # Remove non-productive symbols
        new_P = defaultdict(set)
        for var in productive:
            new_P[var] = self.P[var]

        self.VN = productive
        self.P = new_P

    def convert_to_cnf(self):
        # Apply all conversion steps
        self.remove_epsilon_productions()
        self.remove_unit_productions()
        self.remove_inaccessible_symbols()
        self.remove_non_productive_symbols()

        # Convert the grammar to Chomsky Normal Form (CNF)
        new_P = defaultdict(set)
        new_VN = set()
        new_VT = set()
        for var in self.VN:
            for prod in self.P[var]:
                if len(prod) == 1 and prod in self.VT:
                    # Terminal productions stay the same
                    new_P[var].add(prod)
                    new_VT.add(prod)
                else:
                    # Non-terminal productions are split into pairs of non-terminals or terminals
                    new_var = var
                    for ch in prod:
                        if ch in self.VT:
                            # If it's a terminal, add it directly to the new production
                            new_var += ch
                        else:
                            # If it's a non-terminal, create a new non-terminal and add it to the production
                            new_non_term = ch
                            new_VN.add(new_non_term)
                            new_P[new_non_term].add(ch)
                            new_var += new_non_term
                    new_P[var].add(new_var)

        self.VN = new_VN
        self.VT = new_VT
        self.P = new_P

    def powerset(self, s):
        # Helper function to generate the powerset of a set
        x = len(s)
        masks = [1 << i for i in range(x)]
        for i in range(1 << x):
            yield [ss for mask, ss in zip(masks, s) if i & mask]

# Define the grammar
VN = {'S', 'A', 'B', 'D'}
VT = {'a', 'b', 'd'}
P = {
    'S': {'aBA', 'AB'},
    'A': {'AbBA', 'd', 'dS'},
    'B': {'A', 'a'},
    'D': {'Aba'}
}
S = 'S'

# Convert the grammar to CNF
cnf_converter = CNFConverter(VN, VT, P, S)
cnf_converter.convert_to_cnf()

# Print the formatted output
print("VN:")
print(cnf_converter.VN)
print("\nVT:")
print(cnf_converter.VT)
print("\nP:")
for var in cnf_converter.P:
    print(f"{var}: {cnf_converter.P[var]}")
print("\nS:", cnf_converter.S)

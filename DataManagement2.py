import json
from finite_automata import FiniteAutomata

# Add to_dict method
def to_dict(self):
    return {
        'id': self.id,
        'all_states': list(self.all_states),
        'alphabet': list(self.alphabet),
        'transitions': {
            state: {symbol: list(next_states) for symbol, next_states in trans.items()}
            for state, trans in self.transitions.items()
        },
        'starting_state': self.starting_state,
        'accepting_states': list(self.accepting_states)
    }

# Add from_dict method
@staticmethod
def from_dict(data):
    return FiniteAutomata(
        id=data.get('id', ''),
        all_states=set(data['all_states']),
        alphabet=set(data['alphabet']),
        transitions={
            state: {symbol: set(next_states) for symbol, next_states in trans.items()}
            for state, trans in data['transitions'].items()
        },
        starting_state=data['starting_state'],
        accepting_states=set(data['accepting_states'])
    )

# Add epsilon_closure method
def epsilon_closure(self, state):
    """
    Compute ε-closure of a given state in the automaton.
    Assumes ε-transitions are represented by the empty string ''.
    """
    closure = {state}
    stack = [state]

    while stack:
        current = stack.pop()
        epsilon_transitions = self.transitions.get(current, {}).get('', set())
        for next_state in epsilon_transitions:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)

    return closure

# Attach methods to FiniteAutomata class
FiniteAutomata.to_dict = to_dict
FiniteAutomata.from_dict = from_dict
FiniteAutomata.epsilon_closure = epsilon_closure

# Save multiple FAs
def save_all_fas_to_file(fa_list, filename):
    data = [fa.to_dict() for fa in fa_list]
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"{len(fa_list)} FAs saved to '{filename}'.")

# Load multiple FAs
def load_all_fas_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    fa_list = [FiniteAutomata.from_dict(fa_data) for fa_data in data]
    print(f"{len(fa_list)} FAs loaded from '{filename}'.")
    return fa_list

import json
from finite_automata import FiniteAutomata

# Add these methods to your FiniteAutomata class
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

@staticmethod
def from_dict(data):
    return FiniteAutomata(
        id=data['id'],
        all_states=set(data['all_states']),
        alphabet=set(data['alphabet']),
        transitions={
            state: {symbol: set(next_states) for symbol, next_states in trans.items()}
            for state, trans in data['transitions'].items()
        },
        starting_state=data['starting_state'],
        accepting_states=set(data['accepting_states'])
    )

# Attach methods to class if not already inside
FiniteAutomata.to_dict = to_dict
FiniteAutomata.from_dict = from_dict

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

import json
from finite_automata import FiniteAutomata

# Helper to convert sets inside __dict__ to lists for JSON
def prepare_fa_dict(fa):
    fa_dict = fa.__dict__.copy()
    fa_dict['all_states'] = list(fa_dict['all_states'])
    fa_dict['alphabet'] = list(fa_dict['alphabet'])
    fa_dict['accepting_states'] = list(fa_dict['accepting_states'])
    # Convert transition sets to lists
    fa_dict['transitions'] = {
        state: {symbol: list(next_states) for symbol, next_states in trans.items()}
        for state, trans in fa_dict['transitions'].items()
    }
    return fa_dict

# Save multiple FAs
def save_all_fas_to_file(fa_list, filename):
    data = [prepare_fa_dict(fa) for fa in fa_list]
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"{len(fa_list)} FAs saved to '{filename}'.")

# Load multiple FAs
def load_all_fas_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    fa_list = [FiniteAutomata(
        id=fa_data['id'],
        all_states=set(fa_data['all_states']),
        alphabet=set(fa_data['alphabet']),
        transitions={
            state: {symbol: set(next_states) for symbol, next_states in trans.items()}
            for state, trans in fa_data['transitions'].items()
        },
        starting_state=fa_data['starting_state'],
        accepting_states=set(fa_data['accepting_states'])
    ) for fa_data in data]
    print(f"{len(fa_list)} FAs loaded from '{filename}'.")
    return fa_list

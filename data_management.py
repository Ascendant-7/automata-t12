import json
from finite_automata import FiniteAutomata

# Save multiple FAs
def save_fas(fa_list: list[FiniteAutomata], filename: str):
    data = [fa.get_normalized() for fa in fa_list]
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"{len(fa_list)} FAs saved to '{filename}'.")

# Load multiple FAs
def load_fas(filename: str) -> list[FiniteAutomata]:
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"File '{filename}' is not valid JSON.")
        return []
    fa_list = [FiniteAutomata(
        name=fa_data['name'],
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
import json
from finite_automata import FiniteAutomata

def save_fa_to_file(fa: FiniteAutomata, filename: str):
    """Save a FiniteAutomata instance to a JSON file."""
    data = {
        'all_states': list(fa.all_states),
        'alphabet': list(fa.alphabet),
        'transitions': {
            state: {symbol: list(next_states) for symbol, next_states in trans.items()}
            for state, trans in fa.transitions.items()
        },
        'starting_state': fa.starting_state,
        'accepting_states': list(fa.accepting_states)
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"FA saved to '{filename}'.")


def load_fa_from_file(filename: str) -> FiniteAutomata:
    """Load a FiniteAutomata instance from a JSON file."""
    with open(filename, 'r') as f:
        data = json.load(f)

    all_states = set(data['all_states'])
    alphabet = set(data['alphabet'])
    transitions = {
        state: {symbol: set(next_states) for symbol, next_states in trans.items()}
        for state, trans in data['transitions'].items()
    }
    starting_state = data['starting_state']
    accepting_states = set(data['accepting_states'])

    fa = FiniteAutomata(
        all_states=all_states,
        alphabet=alphabet,
        transitions=transitions,
        starting_state=starting_state,
        accepting_states=accepting_states
    )
    print(f"FA loaded from '{filename}'.")
    return fa

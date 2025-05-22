def nfa(states, alphabet, transitions, starting_state, accepting_states, input_str):
    current_states = {starting_state}
    for symbol in input_str:
        next_states = set()
        for state in current_states:
            next_states.update(transitions.get(state, symbol), [])
        current_states = next_states
    return any(state in accepting_states for state in current_states)
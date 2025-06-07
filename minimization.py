from finite_automata import FiniteAutomata
def minimize_dfa(dfa: FiniteAutomata) -> FiniteAutomata:
    if not dfa.is_dfa():
        raise ValueError("Only DFAs can be minimized.")

    # Step 1: Initialize partitions: accepting vs non-accepting states
    non_accepting = dfa.all_states - dfa.accepting_states
    partitions = [dfa.accepting_states, non_accepting]
    new_partitions = []

    def get_partition(state, partitions):
        for idx, group in enumerate(partitions):
            if state in group:
                return idx
        return -1

    # Step 2: Refine partitions
    while True:
        new_partitions = []
        for group in partitions:
            # Split group by transitions
            split_map = {}
            for state in group:
                key = tuple(
                    get_partition(
                        next(iter(dfa.transitions.get(state, {}).get(symbol, {None}))),
                        partitions
                    ) for symbol in dfa.alphabet
                )
                split_map.setdefault(key, set()).add(state)
            new_partitions.extend(split_map.values())
        if new_partitions == partitions:
            break
        partitions = new_partitions

    # Step 3: Create minimized DFA
    state_mapping = {frozenset(group): f'M{idx}' for idx, group in enumerate(partitions)}
    new_states = set(state_mapping.values())
    new_transitions = {}
    new_accepting_states = set()
    new_start_state = None

    for group in partitions:
        rep_state = next(iter(group))  # Representative state
        new_state_name = state_mapping[frozenset(group)]
        new_transitions[new_state_name] = {}

        if rep_state in dfa.accepting_states:
            new_accepting_states.add(new_state_name)
        if dfa.starting_state in group:
            new_start_state = new_state_name

        for symbol in dfa.alphabet:
            target_states = dfa.transitions.get(rep_state, {}).get(symbol)
            if target_states:
                target_state = next(iter(target_states))
                for part in partitions:
                    if target_state in part:
                        new_transitions[new_state_name][symbol] = {state_mapping[frozenset(part)]}
                        break

    return FiniteAutomata(
        id=dfa.id + "_minimized",
        all_states=new_states,
        alphabet=dfa.alphabet,
        transitions=new_transitions,
        starting_state=new_start_state,
        accepting_states=new_accepting_states
    )

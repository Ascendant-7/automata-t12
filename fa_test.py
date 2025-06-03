from finite_automata import FiniteAutomata
# ----------------------------
# Test: DFA and NFA Samples
# ----------------------------

dfa1 = FiniteAutomata(
    id="DFA-1",
    all_states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transitions={
        'q0': {'a': {'q1'}},
        'q1': {'b': {'q2'}},
        'q2': {}
    },
    starting_state='q0',
    accepting_states={'q2'}
)

dfa2 = FiniteAutomata(
    id="DFA-2",
    all_states={'q0', 'q1'},
    alphabet={'0', '1'},
    transitions={
        'q0': {'0': {'q0'}, '1': {'q1'}},
        'q1': {'0': {'q0'}, '1': {'q1'}}
    },
    starting_state='q0',
    accepting_states={'q0'}
)

nfa1 = FiniteAutomata(
    id="NFA-1",
    all_states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transitions={
        'q0': {'a': {'q0', 'q1'}},
        'q1': {'b': {'q2'}},
        'q2': {}
    },
    starting_state='q0',
    accepting_states={'q2'}
)

nfa2 = FiniteAutomata(
    id="NFA-2",
    all_states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transitions={
        'q0': {'a': {'q0', 'q1'}},
        'q1': {'b': {'q2'}}
    },
    starting_state='q0',
    accepting_states={'q0', 'q2'}
)

fa_list = [dfa1, dfa2, nfa1, nfa2]
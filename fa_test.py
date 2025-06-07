import re
from data_management import *
from finite_automata import FiniteAutomata
# ----------------------------
# Test: DFA and NFA Samples
# ----------------------------

dfa1 = FiniteAutomata(
    name="^ab$",
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
    name="0$",
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
    name="^a+b$",
    all_states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transitions={
        'q0': {'a': {'q0', 'q1'}},
        'q1': {'b': {'q2'}}
    },
    starting_state='q0',
    accepting_states={'q2'}
)

nfa2 = FiniteAutomata(
    name="^a*b?$",
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

test_str = "ab"
test_fa = nfa1

is_dfa = test_fa.is_dfa()
converted_nfa = None

print(f"'{test_fa.name}' is a dfa? {is_dfa}")

if not is_dfa:
    converted_nfa = test_fa.to_dfa()

fa_accepted = test_fa.test(test_str)
print(f"\nis '{test_str}' accepted by '{test_fa.name}'? {fa_accepted}")

converted_fa_accepted = True
if converted_nfa is not None:
    converted_fa_accepted = converted_nfa.test(test_str)
    print(f"is '{test_str}' accepted by '{converted_nfa.name}'? {converted_fa_accepted}")

_, pattern = test_fa.name.split(' >> ', 1)
regex_accepted = bool(re.match(pattern, test_str))
print(f"is '{test_str}' accepted by '{test_fa.name}'? {regex_accepted}")

print(f'\nThe tests return {all([fa_accepted, converted_fa_accepted, regex_accepted])}')

save_fas(fa_list, "data.json")
new_list = load_fas("data.json")

correct_save_load_count = 0
for i in range(len(fa_list)):
    if normalize_fas(fa_list[i]) == normalize_fas(new_list[i]):
        correct_save_load_count += 1

print(f"correct save/load count: {correct_save_load_count}")
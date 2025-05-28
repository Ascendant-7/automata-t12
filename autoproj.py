def validate_fa(all_states, alphabet, transitions, starting_state, accepting_states, input_str):
    '''
    Validates that all given components match the structure of a finite automaton (FA).
    Checks types and values of transition key-value pairs, starting state, and accepting states.
    All validation uses the provided sets of states (Q) and input symbols (X).
    '''
    # validate transition-table type
    if not isinstance(transitions, dict):
        print("type error: transitions must be of type 'dict'.")
        return False
    
    # validate transition-table key-value pairs
    for key, values in transitions.items():
        # validate the transition keys
        if not isinstance(key, tuple):
            print(f"type error: a transition key must be a tuple. key: {key} is of type {type(key)}")
            return False
        if len(key) != 2:
            print(f"type error: a transition key isn't of length 2. key: {key} is of length {len(key)}")
            return False
        if key[0] not in all_states:
            print(f"state error: the partial key: '{key[0]}' of key: '{key}' is not present in the given states (Q).")
            return False
        if key[1] not in alphabet:
            print(f"symbol error: the partial key: '{key[1]}' of key: '{key}' is not present in the given alphabet (X).")
            return False
        
        # validate the transition values
        if not isinstance(values, set):
            print(f"type error: a transition value must be a set. key: {key}, value: {values}")
            return False
        for value in values:
            if value not in all_states:
                print(f"state error: a state is not present in the given states (Q). key: {key}, value: {values}, state: {value}")
                return False
            
    # validate starting state and accepting states
    if starting_state not in all_states:
        print(f"state error: the starting state '{starting_state}' is not present in the given states (Q).")
        return False
    for state in accepting_states:
        if state not in all_states:
            print(f"state error: the state '{state}' in the set of accepting states is not present in the given states (Q).")
            return False
    
    # validate input string
    for symbol in input_str:
        if symbol not in alphabet:
            print(f"the symbol {symbol} in the input string is not present in the given alphabet (Q).")
    return True

def fa(all_states, alphabet, transitions, starting_state, accepting_states, input_str):
    '''for the given fa components, validate the given input string'''
    if not validate_fa(all_states, alphabet, transitions, starting_state, accepting_states, input_str):
        print(f"argument error: the given arguments do not match the standard fa components.")
        return False
    current_states = {starting_state}
    for symbol in input_str:
        next_states = set()
        for state in current_states:
            next_states.update(transitions.get((state, symbol), set()))
        current_states = next_states
    return bool(current_states & accepting_states)

input_str = "aab"
res = fa(
    all_states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transitions={
        ('q0', 'a'): {'q1'},
        ('q1', 'b'): {'q2'}
    },
    starting_state='q0',
    accepting_states={'q2'},
    input_str=input_str
)
print(res)
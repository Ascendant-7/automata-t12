class FiniteAutomata:
    '''
    A class for simulating a finite automata. It has components such as:
    _set of states Q
    _alphabet X
    _transitions d
    _starting state q0
    _accepting states f
    '''
    def __init__(self, all_states, alphabet, transitions, starting_state, accepting_states):
        self.all_states = all_states
        self.alphabet = alphabet
        self.transitions = transitions
        self.starting_state = starting_state
        self.accepting_states = accepting_states
        
    def test(self, input_str):
        '''for the given fa components, validate the given input string'''
        if not self.validate_FA(input_str):
            print(f"argument error: the given arguments do not match the standard fa components.")
            return False
        current_states = {self.starting_state}
        for symbol in input_str:
            next_states = set()
            for state in current_states:
                next_states.update(self.transitions.get(state, {}).get(symbol, set()))
            current_states = next_states
        return bool(current_states & self.accepting_states)


    def validate_FA(self, input_str):
        '''
        Validates that all given components match the structure of a finite automaton (FA).
        Checks types and values of transition key-value pairs, starting state, and accepting states.
        All validation uses the provided sets of states (Q) and input symbols (X).

        Note: Transitions that don't exist in the transition-dictionary will return no value,
        therefore the decision branch of that transition will meet a deadend.
        '''
        # validate transition-table type
        if not isinstance(self.transitions, dict):
            print("type error: 'transitions' must be of type 'dict'.")
            return False
        
        # validate transition-table key-value pairs
        for outer_key, outer_value in self.transitions.items():
            # validate the transition-table first-level key
            if outer_key not in self.all_states:
                print(f"value error: the state-key '{outer_key}' must exist in the 'all_states'.")
                return False
            
            # validate the transition-table first-level value
            if not isinstance(outer_value, dict):
                print("type error: 'transitions' first-level value must be of type 'dict'.")
                return False
            
            for  inner_key, inner_value in outer_value.items():
                # validate the transition-table second-level key
                if inner_key not in self.alphabet:
                    print(f"value error: the symbol-key '{inner_key}' must exist in the 'alphabet'.")
                    return False
                
                # validate the transition-table second-level value
                if not isinstance(inner_value, set):
                    print("type error: 'transitions' second-level value must be of type 'set'.")
                    return False
                
                # validate the end-states
                for val in inner_value:
                    if val not in self.all_states:
                        print(f"value error: the next-possible-state '{val}' from ({outer_key}, {inner_key}) must exist in the 'all_states'.")
                        return False
                
        # validate starting state and accepting states
        if self.starting_state not in self.all_states:
            print(f"state error: the starting state '{self.starting_state}' must exist in the 'all_states'.")
            return False
        for state in self.accepting_states:
            if state not in self.all_states:
                print(f"state error: the accepting state '{state}' must exist in the 'all_states'.")
                return False
        
        # validate input string
        for symbol in input_str:
            if symbol not in self.alphabet:
                print(f"the symbol {symbol} in the input string must exist in the 'alphabet'.")

        print(f"FA is valid.")
        return True

# first test

input_str = "ab"
fa = FiniteAutomata(
    all_states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transitions={
        'q0': {
            'a': {'q1'}
        },
        'q1': {
            'b': {'q2'}
        }
    },
    starting_state='q0',
    accepting_states={'q2'}
)
print(f"The FA accepts '{input_str}'? {fa.test(input_str)}")
class FiniteAutomata:
    '''
    A class for simulating a finite automaton. It has components such as:
    _set of states Q
    _alphabet X
    _transitions d
    _starting state q0
    _accepting states f
    '''

    def __init__(self, id:str, all_states:set[str], alphabet:set[str], transitions:dict[str, dict[str, set[str]]], starting_state:str, accepting_states:set[str]):
        self.id = id
        self.all_states = all_states
        self.alphabet = alphabet
        self.transitions = transitions
        self.starting_state = starting_state
        self.accepting_states = accepting_states
        
    def test(self, input_str: str) -> bool:
        '''for the given fa components, validate the given input string'''
        if not self.is_valid(input_str):
            print(f"argument error: the given arguments do not match the standard fa components.")
            return False
        current_states = {self.starting_state}
        if input_str == '':
            return bool(self.eclose(current_states) & self.accepting_states)
        for symbol in input_str:
            next_states = set()
            for state in current_states:
                trans = self.transitions.get(state, {})
                next_states.update(trans.get(symbol, set()))
            current_states = self.eclose(next_states)
        return bool(current_states & self.accepting_states)

    def is_valid(self, input_str: str) -> bool:
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
                if inner_key != '' and inner_key not in self.alphabet:
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

    def construct_subset(self):
        '''
        WARNING: use only during NFA conversion, no manual uses unless you understood.
        It simulate the two-step transitions of the NFA conversion, where you:
        1. get all state transitions from the subset, returns subset A
        2. get all e-transition from subset A, returns subset B
        Unlike, the starting state where we only get all e-transitions of q0,
        but we do make q0' go through the 2-step transitions.
        '''
        pass

    def eclose(self, subset: set[str]) -> set[str]:
        prev = set()
        curr = subset

        while prev != curr:
            prev = curr
            for state in prev:
                curr.update(self.transitions.get(state, {}).get('', set()))

        return curr

    def is_dfa(self) -> bool:
        '''
        Checks if the FA is deterministic (DFA).
        Returns True if it is, otherwise False.
        '''
        for state, transitions_for_state in self.transitions.items():

            for symbol, next_states in transitions_for_state.items():

                if len(next_states) != 1:
                    return False

        return True
    

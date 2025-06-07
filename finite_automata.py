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

 def to_dfa(self):
        """Convert ε-NFA to DFA using subset construction"""
        dfa_states = {}
        dfa_transitions = {}
        queue = deque()

        # Start state is ε-closure of the NFA start state
        start_closure = frozenset(self.epsilon_closure({self.start_state}))
        dfa_states[start_closure] = 'A'  # Assign names like A, B, C, ...
        queue.append(start_closure)
        state_names = ['A']
        name_index = 1

        while queue:
            current = queue.popleft()
            current_name = dfa_states[current]
            dfa_transitions[current_name] = {}

            for symbol in self.alphabet - {'ε'}:
                next_states = set()
                for nfa_state in current:
                    next_states |= self.transitions[nfa_state].get(symbol, set())
                closure = self.epsilon_closure(next_states)
                closure_frozen = frozenset(closure)

                if not closure:
                    continue

                if closure_frozen not in dfa_states:
                    name = chr(ord('A') + name_index)
                    name_index += 1
                    dfa_states[closure_frozen] = name
                    queue.append(closure_frozen)
                else:
                    name = dfa_states[closure_frozen]

                dfa_transitions[current_name][symbol] = name

        # Determine accept states
        dfa_accept_states = set()
        for state_set, name in dfa_states.items():
            if self.accept_states & state_set:
                dfa_accept_states.add(name)

        return DFA(set(dfa_states.values()), self.alphabet - {'ε'}, dfa_transitions, 'A', dfa_accept_states)

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def print_dfa(self):
        print("States:", self.states)
        print("Alphabet:", self.alphabet)
        print("Start State:", self.start_state)
        print("Accept States:", self.accept_states)
        print("Transitions:")
        for state in self.states:
            for symbol in self.alphabet:
                dest = self.transitions.get(state, {}).get(symbol, None)
                if dest:
                    print(f"  delta({state}, {symbol}) -> {dest}")

states = {'q0', 'q1', 'q2'}
alphabet = {'a', 'b', 'ε'}
transitions = [
    ('q0', 'ε', 'q1'),
    ('q0', 'ε', 'q2'),
    ('q1', 'a', 'q1'),
    ('q1', 'b', 'q1'),
    ('q2', 'a', 'q2'),
    ('q2', 'b', 'q2')
]
start_state = 'q0'
accept_states = {'q1'}

enfa = def __init__(self, states, alphabet, transitions, start_state, accept_states)
dfa = enfa.to_dfa()
dfa.print_dfa()

    

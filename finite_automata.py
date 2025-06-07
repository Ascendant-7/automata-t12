from queue import Queue
import re

class FiniteAutomata:
    '''
    A class for simulating a finite automaton. It has components such as:
    _set of states Q
    _alphabet X
    _transitions d
    _starting state q0
    _accepting states f
    '''

    def __init__(self, name:str, all_states:set[str], alphabet:set[str], transitions:dict[str, dict[str, set[str]]], starting_state:str, accepting_states:set[str]):
        self.all_states = all_states
        self.alphabet = alphabet
        self.transitions = transitions
        self.starting_state = starting_state
        self.accepting_states = accepting_states
        if re.match("^(dfa|nfa) >>", name):
            self.name = name
        else:
            self.name = f"dfa >> {name}" if self.is_dfa() else f"nfa >> {name}"
        
    def __eq__(self, other):
        if not isinstance(other, FiniteAutomata):
            return NotImplemented
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
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
    
    def desc(self):
        print(self.__dict__)

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
            prev = curr.copy()
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

    def to_dfa(self) -> "FiniteAutomata":
        """Convert ε-NFA to DFA using subset construction"""
        dfa_states = {} # holds all the new dfa states as keys and their nfa composite states as values
        dfa_transitions = {} # hold all the new dfa transitions using the new dfa states
        queue = Queue() # tracks non-constructed composite states (comp_state that doesn't have a dfa state to represent it)

        # Start state is ε-closure of the NFA start state
        start_comp_state = frozenset(self.eclose({self.starting_state})) # composite of NFA states = dfa state
        dfa_states[start_comp_state] = 'q0'  # Assign names like A, B, C, ...
        queue.put(start_comp_state)

        while not queue.empty():
            current_comp_state = queue.get()
            current_dfa_state = dfa_states[current_comp_state]
            dfa_transitions[current_dfa_state] = {}

            for symbol in self.alphabet:
                next_comp_states = set()
                for nfa_state in current_comp_state:
                    next_comp_states |= self.transitions.get(nfa_state, {}).get(symbol, set())
                next_comp_states = self.eclose(next_comp_states)
                next_comp_states = frozenset(next_comp_states)

                if not next_comp_states:
                    continue

                if next_comp_states not in dfa_states:
                    state = f"q{len(dfa_states)}"
                    dfa_states[next_comp_states] = state
                    queue.put(next_comp_states)
                else:
                    state = dfa_states[next_comp_states]

                dfa_transitions[current_dfa_state][symbol] = {state}
        
        # Determine accept states
        dfa_accepting_states = set()
        for comp_state, dfa_state in dfa_states.items():
            if self.accepting_states & comp_state:
                dfa_accepting_states.add(dfa_state)

        try:
            _, fa_regex = self.name.split(' >> ', 1)
        except ValueError as e:
            print(f"Error: {e}")
            fa_regex = self.name
        return FiniteAutomata(
            f"{fa_regex}",
            set(dfa_states.values()), 
            self.alphabet, 
            dfa_transitions, 
            'q0', 
            dfa_accepting_states
            )
    
    def get_minimized(self) -> "FiniteAutomata":
        if not self.is_dfa():
            raise ValueError("Only DFAs can be minimized.")

        # Step 1: Remove all non-reachable states
        reachable = {self.starting_state}
        queue = [self.starting_state]

        # queue for tracking traversal
        while queue:
            state = queue.pop()
            for next_states in self.transitions.get(state, {}).values():
                for ns in next_states:
                    if ns not in reachable:
                        reachable.add(ns)
                        queue.append(ns)

        # Filter states
        self.all_states = reachable
        self.accepting_states = self.accepting_states.intersection(reachable)

        # Remove unreachable states from transitions keys and next states
        self.transitions = {
            state: {
                symbol: next_states.intersection(reachable)
                for symbol, next_states in symbol_dict.items()
            }
            for state, symbol_dict in self.transitions.items() if state in reachable
        }

        # Step 2: Initialize partitions: accepting vs non-accepting states
        non_accepting_states = self.all_states - self.accepting_states
        partitions = [self.accepting_states, non_accepting_states]

        def get_partition_index(state: str|None, partitions: list[set[str]]):
            if state is None:
                return -1
            for idx, group in enumerate(partitions):
                if state in group:
                    return idx
            return -1

        # Step 3: Refine partitions
        while True:
            new_partitions = []
            for group in partitions:
                # Split group by transitions
                split_map = {}
                for state in group:
                    key = tuple(
                        get_partition_index(
                            next(iter(self.transitions.get(state, {}).get(symbol, set())), None),
                            partitions
                        ) for symbol in self.alphabet
                    )
                    split_map.setdefault(key, set()).add(state)
                new_partitions.extend(split_map.values())
            if new_partitions == partitions:
                break
            partitions = new_partitions

        # Step 4: Create minimized DFA
        state_mapping = {frozenset(group): f'q{idx}' for idx, group in enumerate(partitions)}
        new_states = set(state_mapping.values())
        new_transitions = {}
        new_accepting_states = set()
        new_start_state = '__INVALID__'

        for group in partitions:
            rep_state = next(iter(group))  # Representative state
            new_state_name = state_mapping[frozenset(group)]
            new_transitions[new_state_name] = {}

            if rep_state in self.accepting_states:
                new_accepting_states.add(new_state_name)
            if self.starting_state in group:
                new_start_state = new_state_name

            for symbol in self.alphabet:
                target_states = self.transitions.get(rep_state, {}).get(symbol)
                if target_states:
                    target_state = next(iter(target_states))
                    for part in partitions:
                        if target_state in part:
                            new_transitions[new_state_name][symbol] = {state_mapping[frozenset(part)]}
                            break

        try:
            _, regex = self.name.split(' >> ', 1)
        except ValueError as e:
            print(f'Error: {e}')
            regex = self.name
        
        if new_start_state == '__INVALID__':
            raise ValueError("Starting state was removed or not found in any partition.")
        
        return FiniteAutomata(
            name=f"dfa minimized >> {regex}",
            all_states=new_states,
            alphabet=self.alphabet,
            transitions=new_transitions,
            starting_state=new_start_state,
            accepting_states=new_accepting_states
        )

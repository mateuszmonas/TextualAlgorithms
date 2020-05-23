from queue import Queue
from typing import Dict, List


class Node:
    def __init__(self) -> None:
        super().__init__()
        self.state: int = 0
        self.fail: 'Node' = None
        self. transitions: Dict[str, 'Node'] = {}


class Automaton:
    def __init__(self, pattern: List[str], alphabet: str) -> None:
        super().__init__()
        self.final_states: List[int] = []
        self.final_states_automaton: Dict[int, List[int]] = {}
        self.trie: Node = Node()
        self.current_state: Node = self.trie

        state_id_counter = 0
        self.trie.state = state_id_counter
        state_id_counter += 1

        for column in pattern:
            temp = self.trie
            for letter in column:
                if letter not in temp.transitions:
                    temp.transitions[letter] = Node()
                    temp.transitions[letter].state = state_id_counter
                    state_id_counter += 1
                temp = temp.transitions[letter]

        q: Queue[Node] = Queue()

        for letter in alphabet:
            if letter in self.trie.transitions:
                self.trie.transitions[letter].fail = self.trie
                q.put(self.trie.transitions[letter])
            else:
                self.trie.transitions[letter] = self.trie

        while not q.empty():
            current_node = q.get()
            for letter in alphabet:
                if letter in current_node.transitions:
                    next_node = current_node.transitions[letter]
                    q.put(next_node)
                    temp = current_node.fail
                    while letter not in temp.transitions:
                        temp = temp.fail
                    next_node.fail = temp.transitions[letter]

        self.compute_final_states(pattern)
        self.compute_final_states_automaton()

    def read_char(self, letter: str):
        while letter not in self.current_state.transitions.keys():
            self.current_state = self.current_state.fail
            if self.current_state is None:
                self.current_state = self.trie
                return self.current_state.state
        self.current_state = self.current_state.transitions[letter]
        return self.current_state.state

    def rollback(self):
        self.current_state = self.trie

    def compute_final_states(self, patter: List[str]):
        for column in patter:
            self.final_states.append(0)
            for letter in column:
                self.final_states[-1] = self.read_char(letter)
            self.rollback()

    def compute_final_states_automaton(self):
        for state in self.final_states:
            if state not in self.final_states_automaton.keys():
                self.final_states_automaton[state] = [0] * (len(self.final_states) + 1)
        long_ps = 0
        self.final_states_automaton[self.final_states[0]][0] = 1
        for i in range(len(self.final_states_automaton)):
            for state in self.final_states_automaton.values():
                state[i] = state[long_ps]
            if i < len(self.final_states):
                self.final_states_automaton[self.final_states[i]][i] = i + 1
                long_ps = self.final_states_automaton[self.final_states[i]][long_ps]

    def parse_line(self, line: List[int]):
        result: List[int] = []
        state = 0
        for i in range(len(line)):
            if line[i] not in self.final_states_automaton:
                state = 0
                continue
            state = self.final_states_automaton[line[i]][state]
            if state == len(self.final_states):
                result.append(i)
        return result

    def find(self, text: List[str]):
        result: List[(int, List[int])] = []
        length = 0
        automaton_output: List[List[int]] = []
        for word in text:
            length = max(length, len(word))
            automaton_output.append([])

        for i in range(length):
            for j in range(len(text)):
                if i < len(text[j]):
                    automaton_output[j].append(self.read_char(text[j][i]))
            self.rollback()

        for i in range(len(automaton_output)):
            temp: List[int] = self.parse_line(automaton_output[i])
            if len(temp) != 0:
                result.append((i, temp))

        return result


# with open('haystack.txt', 'r') as file:
text = ['atha',
        ' th ']
pattern = ['tt',
           'hh']
automaton = Automaton(pattern, 'th a')
print(automaton.find(text))

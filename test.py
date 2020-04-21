from heapq import heappush, heappop
from queue import LifoQueue, Queue
from typing import Dict, List
from bitarray import bitarray


class Node:
    def __init__(self, weight: int, letter: str = None, index: int = -1,  parent: 'Node' = None, left: 'Node' = None, right: 'Node' = None) -> None:
        super().__init__()
        self.weight = weight
        self.letter = letter
        self.parent = parent
        self.left = left
        self.right = right
        self.index = index

    def create_dict(self, dictionary: Dict, code: bitarray = bitarray()):
        if self.letter:
            dictionary[self.letter] = code
        if self.left:
            code_copy = code.copy()
            code_copy.append(0)
            self.left.create_dict(dictionary, code_copy)
        if self.right:
            code_copy = code.copy()
            code_copy.append(1)
            self.right.create_dict(dictionary, code_copy)

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        else:
            return self.weight < other.weight

    def __le__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        else:
            return self.weight <= other.weight

    def __repr__(self):
        return f"{self.weight} : {self.letter if self.letter is not None else '_'}"

    @staticmethod
    def swap(node1: 'Node', node2: 'Node'):
        if node1 == node2 or node1.parent == node2 or node2.parent == node1:
            return
        if node1.parent==node2.parent:
            if node1.parent.left == node1:
                node1.parent.left = node2
                node1.parent.right = node1
            else:
                node1.parent.left = node1
                node1.parent.right = node2
            return
        node1_parent = node1.parent
        node2_parent = node2.parent
        if node1 == node1_parent.left:
            node1_parent.left = node2
        else:
            node1_parent.right = node2
        if node2 == node2_parent.left:
            node2_parent.left = node1
        else:
            node2_parent.right = node1
        node1.parent = node2_parent
        node2.parent = node1_parent

class HuffmanTree:
    def __init__(self, letters: Dict[str, int]) -> None:
        super().__init__()
        h = []
        for letter, weight in letters.items():
            heappush(h, Node(weight, letter))
        while 1 < len(h):
            node1 = heappop(h)
            node2 = heappop(h)
            heappush(h, Node(node1.weight+node2.weight, left=node1, right=node2))
        self.root = h[0]
        self.dictionary = {}
        self.root.create_dict(self.dictionary)


class AdaptiveHuffmanTree:
    def __init__(self) -> None:
        super().__init__()
        self.root = self.NYT = Node(0, letter='\0')
        self.code_dictionary: Dict[str, bytearray] = {}
        self.leafs: Dict[str, Node] = {}
        self.root.create_dict(self.code_dictionary)
        self.nodes: List[Node] = []

    def split_nyt(self, new_node):
        new_nyt = Node(0, letter='\0')
        self.NYT.left = new_nyt
        self.NYT.right = new_node
        self.NYT.letter = None
        new_node.parent = self.NYT
        new_nyt.parent = self.NYT
        self.NYT = new_nyt

    def find_leader(self, node: Node):
        index = node.index - 1
        while 0 <= index and self.nodes[index].weight < node.weight:
            index -= 1
        return self.nodes[index + 1]

    def update_indexes(self):
        self.nodes: List[Node] = []
        queue = Queue()
        queue.put(self.root)
        index = 0
        while not queue.empty():
            node = queue.get()
            self.nodes.append(node)
            node.index = index
            if node.right is not None:
                queue.put(node.right)
            if node.left is not None:
                queue.put(node.left)
            index += 1

    def increment(self, node: Node) -> bool:
        tree_updated = False
        while node is not None:
            node.weight += 1
            leader = self.find_leader(node)
            if not (leader == node or node.parent == leader or leader.parent == node):
                Node.swap(node, leader)
                self.update_indexes()
                tree_updated = True
            node = node.parent
        return tree_updated

    def update_tree(self, letter: str) -> bool:
        if letter not in self.leafs.keys():
            new_node = Node(1, letter)
            self.leafs[letter] = new_node
            self.split_nyt(new_node)
            new_parent = new_node.parent
            new_parent.index = len(self.nodes)
            self.nodes.append(new_parent)
            new_node.index = len(self.nodes)
            self.nodes.append(new_node)
            self.increment(new_parent)
            tree_updated = True
        else:
            tree_updated = self.increment(self.leafs[letter])
        if tree_updated:
            self.root.create_dict(self.code_dictionary)
        return tree_updated

    def search(self, code: bitarray):
        node = self.root
        if node.left is None and node.right is None:
            return node.letter
        for bit in code:
            if bit:
                node = node.right
            else:
                node = node.left
        if node.left is not None and node.right is not None:
            return None
        return node.letter

    @property
    def dictionary(self):
        if self.root.left is None and self.root.right is None:
            code = bitarray()
            code.append(0)
            return {self.root.letter: code}
        return self.code_dictionary


def encode(text: str):
    tree = AdaptiveHuffmanTree()
    bits = bitarray()
    current_dict = tree.dictionary.copy()
    for letter in text:
        if tree.update_tree(letter):
            bits += current_dict['\0']
            current_dict = tree.dictionary.copy()
            letter_code = bitarray()
            letter_code.fromstring(letter)
            bits += letter_code
        bits += current_dict[letter]
    return bits


def decode(bits: bitarray):
    tree = AdaptiveHuffmanTree()
    i = 1
    text = ""
    while bits:
        code = bits[:i]
        letter = tree.search(code)
        if letter is not None:
            bits = bits[i:]
            if letter == '\0':
                tree.update_tree(bits[:8].tobytes().decode())
                bits = bits[8:]
            else:
                text += letter
            i = 0
        i += 1
    return text


print(decode(encode("japierdole kurwa mac nie bdzuaal")))

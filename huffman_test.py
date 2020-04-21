from heapq import heappush, heappop
from typing import Dict
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
        self.root = self.NYT = Node(0, letter='##')
        self.dictionary: Dict[str, bytearray] = {}
        self.leafs: Dict[str, Node] = {}
        self.root.create_dict(self.dictionary)
        self.nodes: List[Node] = []

    def split_nyt(self, new_node):
        new_nyt = Node(0, letter='##')
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
            self.root.create_dict(self.dictionary)
        return tree_updated


def encoding_table(tree) -> bitarray:
    table = bitarray()
    for key, value in tree.dictionary.items():
        length = bitarray()
        length.frombytes(len(value).to_bytes(1, byteorder='big', signed=False))
        letter = bitarray()
        letter.fromstring(key)
        table += letter + length + value
    table_length = bitarray()
    table_length.frombytes(len(table).to_bytes(1, byteorder='big', signed=False))
    return table_length + table


# format
# encoding table length - {1 byte}
# encoding table - {1 byte} letter - {1byte} code - length - code
# encoded text
def encode(text: str) -> bitarray:
    letters = {}
    for letter in text:
        if letter not in letters.keys():
            letters[letter] = 0
        letters[letter] += 1
    tree = HuffmanTree(letters)
    bits = encoding_table(tree)
    for letter in text:
        bits += tree.dictionary[letter]
    return bits


def bitarray_to_int(bits: bitarray) -> int:
    number = 0
    for bit in bits:
        number = (number << 1) | bit
    return number


def decoding_table(bits: bitarray) -> (bitarray, Dict[int, str]):
    table_length = int.from_bytes(bits[:8], byteorder='big', signed=True)
    bits = bits[8:]
    i = 0
    table = {}
    while i < table_length:
        letter = bits[:8].tobytes().decode()
        i += 8
        bits = bits[8:]
        length = bitarray_to_int(bits[:8])
        i += 8
        bits = bits[8:]
        code = bits[:length]
        i += length
        bits = bits[length:]
        table[bitarray_to_int(code)] = letter
    return bits, table


def decode(bits: bitarray) -> str:
    bits, table = decoding_table(bits)
    i = 1
    text = ""
    while bits:
        key = bitarray_to_int(bits[:i])
        if key in table.keys():
            text += table[key]
            bits=bits[i:]
            i = 0
        i += 1
    return text


print(decode(encode("abracadabra")))

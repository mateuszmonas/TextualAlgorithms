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
    def __init__(self, weights: Dict[str, int]) -> None:
        super().__init__()
        h = []
        for letter, weight in weights.items():
            heappush(h, Node(weight, letter))
        while 1 < len(h):
            node1 = heappop(h)
            node2 = heappop(h)
            heappush(h, Node(node1.weight+node2.weight, left=node1, right=node2))
        self.root = h[0]
        self.code_dictionary = {}
        self.root.create_dict(self.code_dictionary)

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


def bitarray_to_int(bits: bitarray) -> int:
    number = 0
    for bit in bits:
        number = (number << 1) | bit
    return number


def encoding_table(letters: [str, int]) -> bitarray:
    table = bitarray()
    for key, value in letters.items():
        letter = bitarray()
        letter.fromstring(key)
        weight = bitarray()
        weight.frombytes(value.to_bytes(4, byteorder='big', signed=False))
        table += letter + weight
    table_length = bitarray()
    table_length.frombytes(len(table).to_bytes(4, byteorder='big', signed=False))
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
    bits = encoding_table(letters)
    for letter in text:
        bits += tree.dictionary[letter]
    return bits


def decoding_table(bits: bitarray) -> (bitarray, HuffmanTree):
    table_length = int.from_bytes(bits[:32], byteorder='big', signed=True)
    bits = bits[32:]
    i = 0
    letters = {}
    while i < table_length:
        letter = bits[:8].tobytes().decode()
        i += 8
        bits = bits[8:]
        weight = bitarray_to_int(bits[:32])
        i += 32
        bits = bits[32:]
        letters[letter] = weight
    return bits, HuffmanTree(letters)


def decode(bits: bitarray) -> str:
    bits, tree = decoding_table(bits)
    i = 1
    text = ""
    while bits:
        letter = tree.search(bits[:i])
        if letter is not None:
            text += letter
            bits = bits[i:]
            i = 0
        i += 1
    return text


print(decode(encode("aoisjdoi[wehfoiqw")))

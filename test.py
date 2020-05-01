import os
from heapq import heappush, heappop
from queue import LifoQueue, Queue
from time import perf_counter
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

class StaticHuffmanTree:
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

    @property
    def dictionary(self):
        if self.root.left is None and self.root.right is None:
            code = bitarray()
            code.append(0)
            return {self.root.letter: code}
        return self.code_dictionary

    @staticmethod
    def encode(text: str) -> bitarray:
        letters = {}
        for letter in text:
            if letter not in letters.keys():
                letters[letter] = 0
            letters[letter] += 1
        tree = StaticHuffmanTree(letters)
        table = bitarray()
        for key, value in letters.items():
            letter = bitarray()
            letter.fromstring(key)
            weight = bitarray()
            weight.frombytes(value.to_bytes(4, byteorder='big', signed=False))
            table += letter + weight
        table_length = bitarray()
        table_length.frombytes(len(table).to_bytes(4, byteorder='big', signed=False))
        bits = table_length + table
        for letter in text:
            bits += tree.dictionary[letter]
        return bits

    @staticmethod
    def decode(bits: bitarray) -> str:
        table_length = int.from_bytes(bits[:32], byteorder='big', signed=True)
        bits = bits[32:]
        i = 0
        letters = {}
        while i < table_length:
            letter = bits[:8].tobytes().decode()
            i += 8
            bits = bits[8:]
            weight = 0
            for bit in bits[:32]:
                weight = (weight << 1) | bit
            i += 32
            bits = bits[32:]
            letters[letter] = weight
        tree = StaticHuffmanTree(letters)
        i = 0
        text = ""
        while i < len(bits):
            node = tree.root
            while node.left is not None and node.right is not None:
                if bits[i]:
                    node = node.right
                else:
                    node = node.left
                i += 1
            text += node.letter
        return text

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

    @property
    def dictionary(self):
        if self.root.left is None and self.root.right is None:
            code = bitarray()
            code.append(0)
            return {self.root.letter: code}
        return self.code_dictionary

    @staticmethod
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

    @staticmethod
    def decode(bits: bitarray):
        tree = AdaptiveHuffmanTree()
        i = 1
        text = ""
        updated = False
        while i < len(bits):
            node = tree.root
            while node.left is not None and node.right is not None:
                if bits[i]:
                    node = node.right
                else:
                    node = node.left
                i += 1
            if node.letter == '\0':
                tree.update_tree(bits[i:i+8].tobytes().decode())
                updated = True
                i += 8
            else:
                if not updated:
                    tree.update_tree(node.letter)
                updated = False
                text += node.letter
        return text



def test(input_file_name: str):
    output_file_name = "result.txt"
    uncompressed_size = os.path.getsize(input_file_name)
    with open(input_file_name, "r") as file:
        text = file.read()
    print('Static huffman tree ')
    with open(output_file_name, "wb") as file:
        file.truncate()
        start = perf_counter()
        bits = StaticHuffmanTree.encode(text)
        end = perf_counter()
        print(f'encode: {end-start}')
        start = perf_counter()
        StaticHuffmanTree.decode(bits)
        end = perf_counter()
        print(f'decode: {end-start}')
        bits.tofile(file)
    compressed_size = os.path.getsize(output_file_name)
    print(f'compression: {compressed_size * 100 / uncompressed_size}%')
    print('Adaptive huffman tree ')
    with open(output_file_name, "wb") as file:
        file.truncate()
        start = perf_counter()
        bits = AdaptiveHuffmanTree.encode(text)
        end = perf_counter()
        print(f'encode: {end-start}')
        start = perf_counter()
        AdaptiveHuffmanTree.decode(bits)
        end = perf_counter()
        print(f'decode: {end-start}')
        bits.tofile(file)
    compressed_size = os.path.getsize(output_file_name)
    print(f'compression: {compressed_size * 100 / uncompressed_size}%')


# test("test.txt")

with open("1kb.txt", "r") as file:
    text = file.read()
print(AdaptiveHuffmanTree.decode(AdaptiveHuffmanTree.encode(text)))
# asd = StaticHuffmanTree("asd")[2]

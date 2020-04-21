from collections import defaultdict
from bitarray import bitarray
import random

blocks = defaultdict(list)

def inorder(tree, depth=0):
    if 0 in tree.children:
        inorder(tree.children[0], depth= depth+1)

    print(depth,': ',tree.letter, ' ', tree.weight)
    
    if 1 in tree.children:
        inorder(tree.children[1], depth=depth+1)


def bitarray_to_char(ba):
    return chr(int(ba.to01(),2))

def get_key(val, d): 
    for key, value in d.items(): 
         if val == value: 
             return key 
  
    return "key doesn't exist"

def swap_nodes(nodeA, nodeB):
    parentA = nodeA.parent
    parentB = nodeB.parent
    bitA = get_key(nodeA, parentA.children)
    bitB = get_key(nodeB, parentB.children)
    parentB.children[bitB] = nodeA
    parentA.children[bitA] = nodeB
    nodeA.parent = parentB
    nodeB.parent = parentA

def find_fahrest(node, W):
    # if len(blocks[W])>0:
        # gitreturn blocks[W][0]
    q = []
    if 1 in node.children:
            q.append(node.children[1])
    if 0 in node.children:
            q.append(node.children[0])
    while len(q) > 0 and q[0].weight > W:
        v = q.pop(0)
        if 1 in v.children:
            q.append(v.children[1])
        if 0 in v.children:
            q.append(v.children[0])
    
    if len(q) > 0 and q[0].weight == W:
        return q[0]

    return None

def parent_chain(node):
    c = node.parent
    if c:
        parents = {c}
    else:
        return set()
    while c.parent:
        parents.add(c)
        c = c.parent
    return parents

def find_root(node):
    c = node
    while c.parent != None:
        c = c.parent
    return c

class Node:
    def __init__(self, letter, parent=None, weight=0):
        self.letter = letter
        self.parent = parent
        self.weight = weight
        self.children = dict()

    def code(self):
        if self.parent == None:
            return bitarray()
        else:
            return self.parent.code() + self.parent.child_bit(self)

    def add_child(self, bit, node):
        self.children[bit] = node

    def get_child(self, bit):
        return self.children[bit]

    def child_bit(self, child):
        if(child == self.children[0]):
            return bitarray('0')
        if(child == self.children[1]):
            return bitarray('1')
        return None

    def validate(self, to_validate):
        if len(self.children) > 0:
            child = None
            if len(self.get_child(0).children) == 0 and self.get_child(0).weight > 0:
                child = self.get_child(0)
            if len(self.get_child(1).children) == 0 and self.get_child(1).weight > 0:
                child = self.get_child(1)
            
            if child and child.weight < to_validate.weight:
                swap_nodes(child, to_validate)
                self.validate(to_validate)

        if self.parent != None:
            self.parent.validate(to_validate)



    def update(self):
        if 0 in self.children and 1 in self.children:
            if self in blocks[self.weight]:
                blocks[self.weight].remove(self)
            self.weight = self.children[0].weight + self.children[1].weight
            blocks[self.weight].append(self)
            if self.children[0].weight > self.children[1].weight:
                temp = self.children[0]
                self.children[0] = self.children[1]
                self.children[1] = temp
        if self.parent != None:
            self.parent.update()

    def increment(self):
        self.weight += 1
        if self in blocks[self.weight-1]:
            blocks[self.weight-1].remove(self)

        blocks[self.weight].append(self)
        if self.weight > 1:    
            root = find_root(self)
            f = find_fahrest(root, self.weight-1)
            parents = parent_chain(self)
            if f and f not in parents and self != root:
                fparents = parent_chain(f)
                if self not in fparents:
                    swap_nodes(f, self)
                    f.update()

        if self.parent != None:
            self.parent.increment()

def adaptive_huffman(text):
    count = defaultdict(int)
    nodes = {"#": Node("#", weight=0)}
    root = nodes["#"]
    result = bitarray()
    for letter in list(text):
        # inorder(root)
        # print("----")
        if letter not in count:
            count[letter] = 1
        else:
            count[letter] += 1

        if letter in nodes:
            node = nodes[letter]
            result+=node.code()
            parent = node.parent
            node.increment()
            # parent.update()
        else:
            updated_node = nodes["#"]
            result+=updated_node.code()
            result.frombytes(letter.encode("ascii"))
            node = Node(letter, parent=updated_node, weight=0)
            nodes[letter] = node
            del nodes["#"]
            zero_node = Node("#", parent=updated_node, weight=0)
            updated_node.add_child(0, zero_node)
            updated_node.add_child(1, node)
            nodes["#"] = zero_node
            node.increment()
    
    return result


def adaptive_huffman_decode(binary):
    nodes = {"#": Node("#", weight=0)}
    root = nodes["#"]
    result = ""
    while binary:
        current = root
        while len(current.children) != 0:
            current = current.get_child(int(binary[0]))
            binary = binary[1:]
        if current.letter == '#':
            letter = bitarray_to_char(binary[:8])
            binary = binary[8:]
            updated_node = nodes["#"]
            result+=letter
            node = Node(letter, parent=updated_node,weight=0)
            nodes[letter] = node
            del nodes["#"]
            zero_node = Node("#", parent=updated_node, weight=0)
            updated_node.add_child(0, zero_node)
            updated_node.add_child(1, node)
            nodes["#"] = zero_node
            node.increment()
        else:
            result+=current.letter
            parent = nodes[current.letter].parent
            nodes[current.letter].increment()
            # parent.validate(nodes[current.letter])
            # parent.update()

    return result

# text = ''.join([random.choice('abcefg') for i in range(0,2000)])
# text = "The approach used here is to find two separate lists of keys and values. Then fetch the key using the position of the value in the val_list. As key at any position N in key_list will have corresponding value at position N in val_list."
# text1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eget eros rutrum, imperdiet eros id, tincidunt libero. Proin a vehicula ante. Sed quis bibendum arcu. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aenean bibendum magna in nunc scelerisque congue. Curabitur laoreet purus nec dolor pellentesque egestas. Vestibulum sollicitudin nisl non magna pulvinar, nec accumsan metus ullamcorper. Sed euismod imperdiet risus sit amet dignissim."
text1 = "abcddddddddddddddddddddddddddddd"
text = ""
for i in range(1, 2):
    text +=text1 #"The approach used here is to find two separate lists of keys and values. Then fetch the key using the position of the value in the val_list. As key at any position N in key_list will have corresponding value at position N in val_list."

chunk = ""
result = ""
print(8*len(text))
textcpy = text
result_len = 0
while len(text) > 0:
    chunk = text[:200]
    text = text[200:]
    ba = adaptive_huffman(chunk)
    result_len+=len(ba)
    decoded= adaptive_huffman_decode(ba)
    result +=decoded


print(result_len)
if(result == textcpy):
    print("Succes")
else:
    print("Failed")
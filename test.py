from typing import Dict

slow_find_count = 0
fast_find_count = 0

class SuffixTreeNode:

    def __init__(self, text: str, start: int = 0, end: int = 0, depth: int = 0, parent: 'SuffixTreeNode' = None) -> None:
        super().__init__()
        self.depth = depth
        self.start = start
        self.end = end
        self.full_text = text
        self.children: Dict[str, SuffixTreeNode] = dict()
        self.parent: SuffixTreeNode = parent
        self.link: SuffixTreeNode = None

    def graft(self, start) -> 'SuffixTreeNode':
        start = start + self.depth
        text = self.full_text[start:]
        child = SuffixTreeNode(self.full_text, start, len(self.full_text), self.depth + len(text), self)
        self.children[text[0]] = child
        return child

    def break_path(self, text: str) -> 'SuffixTreeNode':
        length = len(text)
        child = self.children[text[0]]
        new_node = SuffixTreeNode(self.full_text, child.start, child.start + length, self.depth + length, self)
        child.start = child.start + length
        child.parent = new_node
        new_node.children[child.label[0]] = child
        self.children[text[0]] = new_node
        return new_node

    def fast_find(self, text: str) -> 'SuffixTreeNode':
        if len(text) == 0:
            return self
        child = self.children[text[0]]
        if len(child.label) < len(text):
            return child.fast_find(text[len(child.label):])
        elif len(child.label) == len(text):
            return child
        else:
            return self.break_path(text)

    def slow_find(self, text: str) -> 'SuffixTreeNode':
        if len(text) == 0 or text[0] not in self.children.keys():
            return self
        child = self.children[text[0]]
        for i in range(1, len(child.label)):
            if child.label[i] != text[i]:
                return self.break_path(text[:i])
        return child.slow_find(text[len(child.label):])

    @property
    def label(self):
        return self.full_text[self.start:self.end]

    def __contains__(self, item):
        if len(item) == 0:
            return True
        if not isinstance(item, str) or item[0] not in self.children:
            return False
        child = self.children[item[0]]
        for i in range(1, min(len(child.label), len(item))):
            if child.label[i] != item[i]:
                return False
        return len(item) < len(child.label) or item[len(child.label):] in child

    def __repr__(self) -> str:
        return f"[{self.start}:{self.end}] {self.full_text[self.start:self.end]}"


class SuffixTree:

    def __init__(self, text: str) -> None:
        self.root = old_head = SuffixTreeNode(text)
        leaf = self.root.graft(0)
        for i in range(1, len(text)):
            if old_head == self.root:
                old_head = self.root.slow_find(leaf.label[1:])
                leaf = old_head.graft(i)
                continue
            parent = old_head.parent
            if parent == self.root:
                head_slink = parent.fast_find(old_head.label[1:])
            else:
                head_slink = parent.link.fast_find(old_head.label)
            if len(head_slink.children) == 1:
                new_head = head_slink
            else:
                new_head = head_slink.slow_find(leaf.label)
            leaf = new_head.graft(i)
            old_head.link = head_slink
            old_head = new_head

    def __contains__(self, item):
        return isinstance(item, str) and item in self.root


from time import perf_counter


def time_eval(func, args, w_print=False, name=None, count=10):
    start = perf_counter()
    for i in range(count):
        func(*args)
    end = perf_counter()
    avg = (end-start)/count
    if w_print:
        print(f"{name} average time: {avg}")
    else:
        return avg


with open('1997_714.txt', 'r') as file:
    text = file.read()
    text = text[:2000]
    text += '\0'
    tree = SuffixTree(text)
    time_eval(tree.root.fast_find, [text], True, "fast", count=10)
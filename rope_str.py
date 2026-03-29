#!/usr/bin/env python3
"""rope_str - Rope data structure for efficient string operations."""
import sys

class RopeNode:
    __slots__ = ['left', 'right', 'text', 'weight', 'height']
    def __init__(self, text=None):
        self.left = None
        self.right = None
        self.text = text
        self.weight = len(text) if text else 0
        self.height = 0

class Rope:
    LEAF_SIZE = 64
    
    def __init__(self, text=""):
        self.root = self._build(text) if text else None
    
    def _build(self, text):
        if len(text) <= self.LEAF_SIZE:
            return RopeNode(text)
        mid = len(text) // 2
        node = RopeNode()
        node.left = self._build(text[:mid])
        node.right = self._build(text[mid:])
        node.weight = self._total_length(node.left)
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        return node
    
    def _height(self, node):
        return node.height if node else -1
    
    def _total_length(self, node):
        if not node:
            return 0
        if node.text is not None:
            return len(node.text)
        return node.weight + self._total_length(node.right)
    
    def __len__(self):
        return self._total_length(self.root)
    
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            start, stop, _ = idx.indices(len(self))
            return self.substring(start, stop)
        if idx < 0:
            idx += len(self)
        return self._index(self.root, idx)
    
    def _index(self, node, idx):
        if not node:
            raise IndexError
        if node.text is not None:
            return node.text[idx]
        if idx < node.weight:
            return self._index(node.left, idx)
        return self._index(node.right, idx - node.weight)
    
    def concat(self, other):
        result = Rope()
        node = RopeNode()
        node.left = self.root
        node.right = other.root if isinstance(other, Rope) else Rope(other).root
        node.weight = len(self)
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        result.root = node
        return result
    
    def _split(self, node, idx):
        if not node:
            return None, None
        if node.text is not None:
            left = RopeNode(node.text[:idx]) if idx > 0 else None
            right = RopeNode(node.text[idx:]) if idx < len(node.text) else None
            return left, right
        if idx <= node.weight:
            ll, lr = self._split(node.left, idx)
            right = RopeNode()
            right.left = lr
            right.right = node.right
            right.weight = self._total_length(lr)
            return ll, right
        else:
            rl, rr = self._split(node.right, idx - node.weight)
            left = RopeNode()
            left.left = node.left
            left.right = rl
            left.weight = node.weight
            return left, rr
    
    def insert(self, idx, text):
        left, right = self._split(self.root, idx)
        mid = Rope(text)
        result = Rope()
        n1 = RopeNode()
        n1.left = left
        n1.right = mid.root
        n1.weight = self._total_length(left)
        n2 = RopeNode()
        n2.left = n1
        n2.right = right
        n2.weight = self._total_length(n1)
        result.root = n2
        return result
    
    def delete(self, start, end):
        left, mid_right = self._split(self.root, start)
        mid, right = self._split(mid_right, end - start)
        result = Rope()
        if left and right:
            n = RopeNode()
            n.left = left
            n.right = right
            n.weight = self._total_length(left)
            result.root = n
        else:
            result.root = left or right
        return result
    
    def substring(self, start, end):
        chars = []
        self._collect(self.root, start, end, 0, chars)
        return "".join(chars)
    
    def _collect(self, node, start, end, offset, chars):
        if not node or offset >= end:
            return
        if node.text is not None:
            node_end = offset + len(node.text)
            if node_end > start:
                lo = max(0, start - offset)
                hi = min(len(node.text), end - offset)
                chars.append(node.text[lo:hi])
            return
        self._collect(node.left, start, end, offset, chars)
        left_len = self._total_length(node.left)
        self._collect(node.right, start, end, offset + left_len if node.left else offset, chars)
    
    def __str__(self):
        return self.substring(0, len(self))

def test():
    r = Rope("Hello, World!")
    assert len(r) == 13
    assert r[0] == "H"
    assert r[7] == "W"
    assert str(r) == "Hello, World!"
    
    # Concat
    r2 = r.concat(Rope(" Goodbye!"))
    assert str(r2) == "Hello, World! Goodbye!"
    
    # Insert
    r3 = r.insert(7, "Beautiful ")
    assert str(r3) == "Hello, Beautiful World!"
    
    # Delete
    r4 = r.delete(5, 7)
    assert str(r4) == "HelloWorld!"
    
    # Substring
    assert r[0:5] == "Hello"
    
    # Large string
    big = Rope("a" * 10000)
    assert len(big) == 10000
    assert big[5000] == "a"
    
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: rope_str.py test")

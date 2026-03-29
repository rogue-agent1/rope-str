#!/usr/bin/env python3
"""Rope String - Efficient string concatenation, split, and editing."""
import sys

class Rope:
    def __init__(self, text="", left=None, right=None):
        self.left = left; self.right = right
        self.text = text if not left else None
        self.weight = len(text) if not left else left.length()
    def length(self):
        if self.text is not None: return len(self.text)
        return (self.left.length() if self.left else 0) + (self.right.length() if self.right else 0)
    def index(self, i):
        if self.text is not None: return self.text[i]
        if i < self.weight: return self.left.index(i)
        return self.right.index(i - self.weight)
    def to_string(self):
        if self.text is not None: return self.text
        return (self.left.to_string() if self.left else "") + (self.right.to_string() if self.right else "")
    def split(self, i):
        if self.text is not None: return Rope(self.text[:i]), Rope(self.text[i:])
        if i <= self.weight:
            ll, lr = self.left.split(i) if self.left else (Rope(""), Rope(""))
            return ll, concat(lr, self.right)
        rl, rr = self.right.split(i - self.weight) if self.right else (Rope(""), Rope(""))
        return concat(self.left, rl), rr
    def insert(self, i, text):
        l, r = self.split(i)
        return concat(concat(l, Rope(text)), r)
    def delete(self, start, end):
        l, _ = self.split(start); _, r = self.split(end)
        return concat(l, r)
    def depth(self):
        if self.text is not None: return 0
        return 1 + max(self.left.depth() if self.left else 0, self.right.depth() if self.right else 0)

def concat(a, b):
    if a.length() == 0: return b
    if b.length() == 0: return a
    r = Rope(left=a, right=b); r.weight = a.length(); return r

def main():
    r = Rope("Hello, World!")
    print(f"=== Rope String ===\n")
    print(f"Original: '{r.to_string()}' (len={r.length()}, depth={r.depth()})")
    r2 = r.insert(7, "Beautiful ")
    print(f"Insert:   '{r2.to_string()}' (len={r2.length()}, depth={r2.depth()})")
    r3 = r2.delete(7, 17)
    print(f"Delete:   '{r3.to_string()}' (len={r3.length()})")
    big = Rope("")
    for i in range(100):
        big = big.insert(big.length(), f"chunk{i} ")
    print(f"\n100 appends: len={big.length()}, depth={big.depth()}")
    print(f"Index [50]: '{big.index(50)}'")

if __name__ == "__main__":
    main()

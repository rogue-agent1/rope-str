#!/usr/bin/env python3
"""rope_str - Rope data structure for efficient string ops."""
import sys
class Rope:
    def __init__(s,left=None,right=None,val=""):
        s.left=left;s.right=right;s.val=val;s.weight=len(val) if val else(left.length() if left else 0)
    def length(s):
        if s.val:return len(s.val)
        return(s.left.length() if s.left else 0)+(s.right.length() if s.right else 0)
    def index(s,i):
        if s.val:return s.val[i]
        if s.left and i<s.weight:return s.left.index(i)
        return s.right.index(i-s.weight)
    def __str__(s):
        if s.val:return s.val
        return str(s.left or"")+str(s.right or"")
    @staticmethod
    def concat(a,b):return Rope(a,b)
    def split(s,i):
        if s.val:return Rope(val=s.val[:i]),Rope(val=s.val[i:])
        if i<=s.weight:
            l,r=s.left.split(i) if s.left else(Rope(val=""),Rope(val=""))
            return l,Rope(r,s.right)
        else:
            l,r=s.right.split(i-s.weight) if s.right else(Rope(val=""),Rope(val=""))
            return Rope(s.left,l),r
    def insert(s,i,text):
        l,r=s.split(i);return Rope.concat(Rope.concat(l,Rope(val=text)),r)
    def delete(s,i,j):
        l,_=s.split(i);_,r=s.split(j);return Rope.concat(l,r)
if __name__=="__main__":
    r=Rope(val="Hello, ");r=Rope.concat(r,Rope(val="World!"))
    print(f"String: {r}");print(f"Length: {r.length()}")
    r=r.insert(7,"Beautiful ");print(f"After insert: {r}")
    r=r.delete(7,17);print(f"After delete: {r}")
    print(f"Char at 4: {r.index(4)}")

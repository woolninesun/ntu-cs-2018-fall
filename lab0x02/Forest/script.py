#!/usr/bin/env python2
from pwn import *

file1 = './forest'
file2 = './string.txt'

# ========================================================================
class Tree:
    class Node:
        def __init__(self, data):
            self.L = None
            self.R = None
            self.data = data
    
    def __init__(self, tree_string):
        root = None
        for char in tree_string:
            root = self.insert( root, char )
        self.root = root

    def insert(self, node , data):
        #if tree is empty , return a root node
        if node is None:
            return self.Node(data)

        # if data is smaller than parent,
        # insert it into left side or insert it into right side.
        if data < node.data:
            node.L = self.insert(node.L, data)
        elif data > node.data:
            node.R = self.insert(node.R, data)

        return node

    def search(self, string):
        if self.root is None or string == '':
            return self.root.data

        node = self.root
        for LorR in string:
            node = node.L if LorR == 'L' else node.R
        return node.data

tree  = Tree( 'yuoteavpxqgrlsdhwfjkzi_cmbn' )

string_in_file = open(file2, "r").readline().rstrip()
strings = string_in_file.split('D')[:-1]

# We can get string: 'you_could_see_the_forest_for_the_trees_ckyljfxyfmsw'
FLAG = ''
for string in strings:
    FLAG += tree.search(string)

output = process(argv=[file1, FLAG, string_in_file]).recvuntil('\n').rstrip()
if output == 'You did it! Put the input in the flag{}.':
    print ('flag{'+ FLAG +'}')

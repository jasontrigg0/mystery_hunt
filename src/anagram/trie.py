from sortedcontainers import SortedDict

#adapted from wiki: https://en.wikipedia.org/wiki/Trie
class Node():
    def __init__(self):
        self.children = SortedDict() # mapping from val ==> Node
        self.value = []

def counter_to_list(cntr):
    return [i for x in sorted(cntr.items()) for i in [x[0]] * x[1]]

class Trie():
    def __init__(self, datatype):
        self.root = Node()
        self.datatype = datatype

    def preprocess_input(self, val):
        if not isinstance(val, self.datatype): raise
        if (isinstance(val,list)):
            l = sorted(val)
        elif (isinstance(val,set)):
            l = sorted(list(val))
        elif (isinstance(val,Counter)):
            l = counter_to_list(val)
            print(l)
        return l

    def find(self, val, wildcards=0):
        l = self.preprocess_input(val)
        node = self.root
        def _find_helper(node, sorted_list, wildcards):
            out = []
            if len(sorted_list) == 0 and wildcards == 0:
                out += node.value
            else:
                for x in node.children:
                    if len(sorted_list) > 0 and sorted_list[0] < x and wildcards == 0: break
                    if len(sorted_list) > 0 and sorted_list[0] == x:
                        out += _find_helper(node.children[x],sorted_list[1:],wildcards)
                    elif wildcards > 0:
                        out += _find_helper(node.children[x],sorted_list,wildcards-1)
            return out
        return _find_helper(self.root, l, wildcards)

    def insert(self, val, value):
        l = self.preprocess_input(val)
        node = self.root
        index_last = None
        for index, x in enumerate(l):
            if x in node.children:
                node = node.children[x]
            else:
                index_last = index
                break

        # append new nodes for the remaining values, if any
        if index_last is not None:
            for x in l[index_last:]:
                node.children[x] = Node()
                node = node.children[x]

        # store value in the terminal node
        node.value.append(value)

    def find_supersets(self, val):
        def _find_superset_helper(node,sorted_list):
            out = []
            if len(sorted_list) == 0 and node.value:
                out += node.value
            for k in node.children:
                if len(sorted_list) > 0 and k > sorted_list[0]:
                    break #no nodes in this subtree contain multi[0]
                if len(sorted_list) > 0 and sorted_list[0] == k: #a match!
                    out += _find_superset_helper(node.children[k],sorted_list[1:])
                else:
                    out += _find_superset_helper(node.children[k],sorted_list)
            return out
        return _find_superset_helper(self.root, self.preprocess_input(val))

    def find_subsets(self, val, wildcards=0):
        #find subsets of the val input
        #wildcards are 'mulligans'
        #ie allow sets that include no more wildcards values not in the input
        def _find_subset_helper(node, sorted_list, wildcards):
            out = []
            if node.value:
                out += node.value
            for k in node.children:
                while (sorted_list and k > sorted_list[0]):
                    sorted_list = sorted_list[1:]
                if wildcards == 0 and len(sorted_list) == 0: break
                if len(sorted_list) > 0 and sorted_list[0] == k:
                    out += _find_subset_helper(node.children[k], sorted_list[1:], wildcards)
                elif wildcards > 0:
                    out += _find_subset_helper(node.children[k], sorted_list, wildcards - 1)
            return out
        return _find_subset_helper(self.root, self.preprocess_input(val), wildcards)


def test_trie():
    sets = [{1,3}, {1,3,5}, {1,4}, {1,2,4}, {2,4}, {2,3,5}]
    t = Trie(set)
    for s in sets:
        t.insert(s,s)

    # print(t.find_supersets({4}))
    # print(t.find_supersets({1,4}))
    # print(t.find_supersets(set()))
    # print(t.find_subsets({1,3,4,5,7}))
    # print(t.find({3,4},1))

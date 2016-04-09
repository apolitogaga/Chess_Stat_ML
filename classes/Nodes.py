__author__ = "codingMonkey"
__project__ = "ChessML"
from collections import defaultdict

class Node(object):
    back_nodes=None
    forward_nodes=None
    name=None

    results =None
    ALLNODES={}
    def __init__(self, name,result):
        self.name = name
        self.results = list(result)

        Node.ALLNODES[name] = self

    def __init__(self, name,result, back_node):
        self.__init__(name,result)
        self.add_node(self.back_nodes,back_node)


    def add_node(self, nodes, node):
        if node.name in nodes:
            nodes[node.name][0] += 1
        else:
            nodes[node.name] = [1,node]
        pass

    def get_number_games(self):
        return len(self.results)


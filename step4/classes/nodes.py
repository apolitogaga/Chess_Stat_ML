__author__ = "codingMonkey"
__project__ = "ChessML"

from collections import defaultdict

WHITE = 1
BLACK = -1
DRAW = 0


class NodeException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,"ERROR: node exception",*args,**kwargs)


class Node(object):
    back_nodes = None
    forward_nodes = None
    name = None
    all_nodes = None
    results = None
    id = None
    frequency = None
    score = None
    movements = None
    ALLNODES = {}
    ID_STATIC = 0
    id_all = None

    def __init__(self, name, result, score):
        self.name = name
        self.results = [result]
        self.back_nodes = {}
        self.forward_nodes = {}
        self.movements = {}
        self.id = Node.ID_STATIC
        self.score = score

        Node.ALLNODES[name] = self
        Node.ID_STATIC += 1


    @classmethod
    def init_back_node(self, name, result, back_node, score):
        node = Node(name, result, score)
        node.add_node(node.back_nodes,back_node.name)
        return node

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __add__(self, other):
        self.add_nodes(self.back_nodes,other.back_nodes)
        self.add_nodes(self.forward_nodes,other.forward_nodes)
        pass

    def __str__(self):
        text = "%d <> %d, %d, %d"%(self.get_weight(),self.get_movement_total(),self.get_nodes_weight(self.forward_nodes),self.get_nodes_weight(self.back_nodes))
        # for key, value in self.forward_nodes.iteritems():
        #     # print type(i[1])
        #     text += "%s"%(key)
        return text

    def __repr__(self):
        return "<Node %d: %s>"%(self.get_weight(),self.name)

    def addition(self, other_node, other_all_nodes):
        other = other_all_nodes[other_node]
        self.add_nodes(self.back_nodes,other.back_nodes, other_all_nodes)
        self.add_nodes(self.forward_nodes,other.forward_nodes, other_all_nodes)
        self.add_movements(other)
        self.results.extend(other.results)
        pass

    def set_score(self,score):
        self.score = score

    def append_node(self, appendable_node):
        appendable_node.id = self.id_all
        self.id_all += 1
        self.all_nodes[appendable_node.name] = appendable_node

    def get_nodes_weight(self,nodes):
        num = 0
        if nodes != None:
            for n in nodes.values():
                num += n
            return num

    def calculate_frequency(self):
        self.frequency = self.get_nodes_weight(self.forward_nodes)

    def add_forward_nodes(self, other_node):
        self.add_nodes(self.forward_nodes, other_node.forward_nodes)

    def add_backward_nodes(self, other_node):
        self.add_nodes(self.back_nodes, other_node.back_nodes)

    def add_movements(self, other_node):
        for key, val in other_node.movements.iteritems():
            self.add_movement(key, val)
        pass

    def add_nodes(self,nodes,other_nodes, other_all_nodes):
        '''
        Adds the forward or backward nodes to the current node
        :param nodes:
        :param other_nodes:
        :param all_nodes:
        :return:
        '''
        for key, value in other_nodes.iteritems():
            node = other_all_nodes[key]
            occurences = value
            self.add_node(nodes,node.name,occurences)


    def add_node(self, nodes, name_next, val=1):
        if name_next in nodes:
            nodes[name_next] += val
        else:
            nodes[name_next] = val

    def save_all_nodes(self):
        self.all_nodes = Node.ALLNODES
        self.id_all = Node.ID_STATIC

    def print_all_nodes(self):
        for key in self.all_nodes.keys():
            print key

    def add_result(self,result):
        self.results.append(result)

    def get_number_games(self):
        return len(self.results)

    def get_results_proportions(self):
        num = len(self.results)
        white = self.results.count(WHITE)
        draw = self.results.count(DRAW)
        black = self.results.count(BLACK)
        print "%d %d %d, %d "%(white,draw,black,num)

    def sort_vertices(self,nodes):
        sorted(nodes.items(), key=lambda e: e[0])

    def check_nodes(self, nodes, message=''):
        if len(nodes)>0:
            for node in nodes.values():
                print "%s: %d-> %s "%(message,node[0], node[1])
        else:
            if not self.__class__.__name__ == "EndNode":
                raise NodeException


    def add_movement(self,movement, number=1):
        '''
        :param movement: Movement number to add to this node
        '''
        if movement in self.movements:
            self.movements[movement] += number
        else:
            self.movements[movement] = number

    def get_movements(self):
        for mov in self.movements:
            print str(mov)+","

    def test_added_nodes(self):
        print "testing: %s "%self
        try:
            self.check_nodes(self.back_nodes)
            self.check_nodes(self.forward_nodes)
        except NodeException as e:
            print self.__class__.__name__ + " " + self.name
            # print self.end_node
            print e
        pass

    def get_weight(self):
        return len(self.results)

    def get_ordered_forward_nodes(self):
        return sorted(self.forward_nodes.items(), key=lambda x:x[1])[::-1]

    def get_ordered_backward_nodes(self):
        return sorted(self.back_nodes.items(), key=lambda x:x[1])[::-1]

    def order_out_nodes(self):
        self.forward_nodes = self.get_ordered_forward_nodes()
        self.back_nodes = self.get_ordered_backward_nodes()

    def print_branched_nodes(self):
        print "name %d"%self.get_weight()+"--->>> \t\t\t" + self.name + " %d <> %d"%(len(self.forward_nodes),len(self.back_nodes))
        # if self.name == "rnbqkbnr/pppppppp/......../......../......../..N...../PPPPPPPP/R.BQKBNR":
        #     for nodes in self.forward_nodes.values():
        #         print "%d <> %s"%(nodes[0], nodes[1])
        #
        #     for nodes in self.back_nodes.values():
        #         print "%d <> %s"%(nodes[0], nodes[1])
        pass

    def get_result_string(self):
        """
        Returns a string with the probability of white, draw and black result, so far seen here.
        :return:
        """
        n = len(self.results)+.0
        return str(self.results.count(1)/n+.0) +"," + str(self.results.count(0)/n) + "," + str(self.results.count(-1)/n)

    def get_stats(self):
        '''
        Gets important stats in the following format
        #of times visited, number of incoming nodes, % most frequent node, number of posterior nodes, % most frequent back node, movements found in, victory %,
        :return: text with the preceding text
        '''
        n = self.get_weight() + 0.0
        text =  str(n) + ","
        text += str(len(self.back_nodes)) + ","
        if len(self.back_nodes) > 0:
            text += str(self.get_ordered_backward_nodes()[0][1]/n) + ","
        else:
            text += "0,"
        text += str(len(self.forward_nodes)) + ","
        if len(self.forward_nodes) > 0:
            text += str(self.get_ordered_forward_nodes()[0][1]/n) + ","
        else:
            text += "0,"
        text += str(len(self.movements)) + ","
        text += self.get_result_string()
        return text

    def get_movement_total(self):
        total = 0
        for num in self.movements.values():
            total += num
        return total

def get_node(name, res, score, b_node):
    new_node = None
    if name not in Node.ALLNODES:
        new_node = Node.init_back_node(name, res, b_node, score)
        b_node.add_node(b_node.forward_nodes, new_node)
    else:
        new_node = Node.ALLNODES[name]
        new_node.add_result(res)
        new_node.add_node(new_node.back_nodes, b_node)
        b_node.add_node(b_node.forward_nodes, new_node)
    return new_node

def merge_nodes(node,other_node):
    keys_a = set(node.all_nodes.keys())
    keys_b = set(other_node.all_nodes.keys())
    intersection = keys_a & keys_b


    # print intersection

    # Node.ALLNODES = node.all_nodes
    # node_list = get_nodes_from_name(intersection,other_node.all_nodes)


    # print "Other_node: \n\n\n"
    # for i in intersection:
    #     other_node.all_nodes[i].print_branched_nodes()
    # print "Node: \n\n\n"
    # for i in intersection:
    #     node.all_nodes[i].print_branched_nodes()


    print "Intersection \n\n" + str(len(intersection))
    for key in intersection:
        node.all_nodes[key].addition(key,other_node.all_nodes)

    # for i in intersection:
    #     node.all_nodes[i].print_branched_nodes()

    unique_b =  keys_b - keys_a
    # print "Unique " + str(len(unique_b))
    # print unique_b

    for key in unique_b:
        '''
        Adds the intersection nodes, those that are already in our pivoting tree
        '''
        node.append_node(other_node.all_nodes[key])
        # other_node.back_nodes = node.replace_nodes(node.back_nodes, other_node.back_nodes, other_node.all_nodes)
        # other_node.forward_nodes = node.replace_nodes(node.forward_nodes, other_node.forward_nodes, other_node.all_nodes)
    return len(unique_b)


def get_nodes_from_name(keys, all_nodes):
    node_list = []
    for key in keys:
        node_list.append(all_nodes[key])
    return node_list




class EndNode(Node):
    end_node = True

    def __init__(self, name, score):
        super(EndNode, self).__init__(name, -2, score)
        self.results = []

    def init(self, name, res, score):
        node = super(EndNode, self).__init__(name, res, score)
        return node




Node


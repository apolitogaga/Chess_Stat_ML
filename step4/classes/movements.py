__author__ = "codingMonkey"
__project__ = "ChessML"

from os import linesep
MAX_MOVEMENTS = 457 # obtained from the dataset itself

class Movement(object):

    last_movement = None
    next_movement = None
    nodes = None
    number_str = None
    all_movements = None

    ALL_MOVEMENTS = {}

    def __init__(self, number):
        Movement.ALL_MOVEMENTS[number] = (self)
        self.number_str = str(number)
        self.nodes = {}
        self.n_white = 0
        self.n_black = 0
        self.n_draw = 0
        self.total_movements = 0

    def __str__(self):
        return "%s %s"%(self.number_str, self.get_number_nodes())

    def __repr__(self):
        return "<Movement %s: %d>"%(self.number_str, self.get_number_nodes())

    def __add__(self, other):
        for node in other.nodes.values():
            self.add_node(node[1],node[0])
        return self

    @classmethod
    def initi_all_possible_movements(cls):
        for i in range(1,457):
            Movement(i)

    @classmethod
    def init_node(cls, number, name_node):
        mov = Movement(number)
        mov.add_node(name_node)
        return mov

    @classmethod
    def init_last(cls, number, node, mov_l):
        '''
        Initializes the last node
        :param number:
        :param node:
        :param mov_l:
        :return:
        '''
        mov = Movement.init_node(number, node)
        mov.set_last_movement(mov_l)
        mov_l.set_next_movement(mov)
        return mov

    def set_total_movements(self):
        self.total_movements = self.n_white + self.n_black + self.n_draw
        n  = self.get_number_nodes()
        if self.total_movements != n:
            print "ERROR: not same number of movements(%d) and nodes(%d)"%(self.total_movements, n)

    def add_result(self, result):
        if result == 1:
            self.n_white +=1
        elif result == -1:
            self.n_black +=1
        elif result == 0:
            self.n_draw +=1

    def add_results(self, n_white, n_black, n_draw):
        self.n_white += n_white
        self.n_black += n_black
        self.n_draw += n_draw

    def get_results_string(self):
        self.set_total_movements()
        return "%d, %d, %d, %d"%(self.n_white, self.n_black, self.n_draw, self.get_number_nodes())


    def add_node(self,name, val=1):
        if name in self.nodes:
            self.nodes[name][0] += val
        else:
            self.nodes[name] = [val, name]

    def set_last_movement(self, mov):
        self.last_movement = mov

    def set_next_movement(self, mov):
        self.next_movement = mov

    def save_all_movements(self):
        self.all_movements = Movement.ALL_MOVEMENTS

    def get_number_nodes(self):
        num =0
        for node in self.nodes.values():
            num += node[0]
        return num

    def freq_freq(self):
        text =''
        for key, mov in self.all_movements.iteritems():
            n_nodes = mov.get_number_nodes()
            if n_nodes > 0:
                text += str(key) + ","+ str(len(self.nodes)) +"," + str(n_nodes) + linesep
        return text

    def get_ordered_backward_nodes(self):
        return sorted(self.back_nodes.items(), key=lambda x:x[1])[::-1]


def merge_movements(movement, other_movement):
    for i in range(len(movement.all_movements)):
        try:
            # mov = movement.all_movements[i]
            # print "%d %d"%(i,mov.get_number_nodes())
            movement.all_movements[i] += other_movement.all_movements[i]
            # print "%d %d"%(i,mov.get_number_nodes())
        except:
            print"ERRRRRR"
    print
    return movement



def define_probabilities_movements(root_movements, NODE_ALL_MOVEMENTS):
    for i, movement in root_movements.ALL_MOVEMENTS.iteritems():
        # if i >40:
        #     break
        # for node in movement.nodes:
        #     node_object = NODE_ALL_MOVEMENTS[node]
        #     black =  node_object.get_black_victories()
        #     white =  node_object.get_white_victories()
        #     draw = node_object.get_draw_results()
        #     movement.add_results(white, black, draw)

        print movement.get_results_string()








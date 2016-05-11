__author__ = "codingMonkey"
__project__ = "ChessML"

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

    def add_nodes(self,other_nodes):

        pass

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




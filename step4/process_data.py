__author__ = "codingMonkey"
__project__ = "ChessML"

from dev2.step2.classes.competitors import Competitor, process_name, calculate_average
from dev2.step2.classes.events import Event
from dev2.step2.classes.games import Game, format_Result

from dev2.step4.classes.nodes import Node, EndNode
from dev2.step4.classes.movements import Movement
from dev2.step4.classes import nodes, movements, stats
from dev2.tools import read_pieces, read_json, tools


from dev2.step4 import TEST_INPUT_FOLDER, TRAIN_INPUT_FOLDER, OUTPUT_JSON_FOLDER, INPUT_FOLDER, CURRENT_DIR, TEST_OUTPUT_FOLDER, TRAIN_OUTPUT_FOLDER

from dev2.step4 import  ALT_TEST_INPUT_FOLDER, ALT_TRAIN_INPUT_FOLDER

import multiprocessing
import time

COMPETITORS = {}
GAMES = {}
EVENTS = {}
ROOT_NODE = None
FIRST_MOVEMENT = None
NAMES = "_final"


# OUT_FOLDER = TEST_OUTPUT_FOLDER
# IN_FOLDER = TEST_INPUT_FOLDER

# OUT_FOLDER = TRAIN_OUTPUT_FOLDER
# IN_FOLDER = TRAIN_INPUT_FOLDER

# OUT_FOLDER = TEST_OUTPUT_FOLDER
# IN_FOLDER = ALT_TEST_INPUT_FOLDER

OUT_FOLDER = TEST_OUTPUT_FOLDER
IN_FOLDER = ALT_TRAIN_INPUT_FOLDER


#for testing purposes

LIMIT_GRID = 1
LIMIT_GAMES = 10
#
LIMIT_GAMES = None
# LIMIT_GRID = None

def load_games(data):
    white = data["white"]
    black = data["black"]
    white_elo = data["white_elo"]
    black_elo = data["black_elo"]
    name = data["name"]
    fen = data['fen']
    fen_eval = data['fen_eval']
    round = data['round']
    event = data['event']
    result = data['result']

    if name not in GAMES:
        GAMES[name] = Game.re_init(name, fen, EVENTS[event], COMPETITORS[white], COMPETITORS[black], result, white_elo, black_elo, round, fen_eval)


def load_events(data):
    date = data['date']
    event = data['event']
    if event not in EVENTS:
        EVENTS[event] = Event(event, date)


def load_competitors(data):
    white = data["white"]
    black = data["black"]
    white_elo = data["white_elo"]
    black_elo = data["black_elo"]
    white_elo_avg = data["white_avg_elo"]
    black_elo_avg = data["black_avg_elo"]

    add_json_competitor(white, white_elo, white_elo_avg)
    add_json_competitor(black, black_elo, black_elo_avg)

def add_json_competitor(name, elo, avg):
    """
    loads a competitor into our directory.
    :param name:
    :param elo:
    :param avg:
    :return:
    """
    if name in COMPETITORS:
        COMPETITORS[name].avg_elo = avg
        COMPETITORS[name].newElo(elo)
    else:
        COMPETITORS[name] = Competitor(name, elo, avg)

def load_nodes(data):
    fen = data['fen']
    fen_eval = data['fen_eval']
    result = data['result']

    for i in range(0,len(fen)):
        if fen[i] not in Node.ALLNODES:
            n = Node(fen[i], result, fen_eval[i])
            n.results=[]
    ROOT_NODE.save_all_nodes()

def load_list_files_json(output_files, pattern, extension):
    """

    :return:
    """
    return read_pieces.getFilesToProcess(output_files, pattern, extension)

def getJsonFile(i, path=IN_FOLDER, pattern=NAMES, extension=".json"):
    """

    :rtype: object
    """
    return path + pattern + "_" + str(i) + extension

def process_final_json(new_file, process_nodes=False):
    global COMPETITORS, GAMES, EVENTS
    del (GAMES)
    del (COMPETITORS)
    del (EVENTS)
    COMPETITORS = {}
    GAMES = {}
    EVENTS = {}

    data = read_json.get_data(new_file)
    print "len: > " + str(len(data[:LIMIT_GAMES]))
    for d in data[:LIMIT_GAMES]:
        load_competitors(d)
        load_events(d)
        load_games(d)
        if process_nodes:
            load_nodes(d)


def multiprocess_white_percentage(new_file):
    process_final_json(OUTPUT_JSON_FOLDER + new_file)
    list = stats.get_white_percentage(GAMES)
    return list


def multiprocess_game_statistics(new_file):
    process_final_json(OUTPUT_JSON_FOLDER + new_file)
    file_write = CURRENT_DIR + "games_stats/" + new_file.split(".")[0] + ".csv"
    f = open(file_write, "w+")
    text = stats.game_statistics(GAMES)
    f.write(text.encode("utf8"))
    f.close()


def multiprocess_graph_stats(file_name):
    global ROOT_NODE, FIRST_MOVEMENT
    ROOT_NODE = nodes.EndNode(u'rnbqkbnr/pppppppp/......../......../......../......../PPPPPPPP/RNBQKBNR', 0)
    FIRST_MOVEMENT = movements.Movement(0)
    process_final_json(IN_FOLDER + file_name, True)
    # FIRST_MOVEMENT.add_node(ROOT_NODE.name, len(games))
    Movement.initi_all_possible_movements()

    VICT_NODE = nodes.EndNode("END", 0)
    # ROOT_NODE.all_nodes.pop("test", None)

    # print ROOT_NODE.__class__.__name__ + ROOT_NODE.name
    # print "%s >>  %d"%(new_file,len(games))

    start = time.clock()
    lista = stats.build_position_graph(GAMES, VICT_NODE, ROOT_NODE.all_nodes)

    end = time.clock()
    print "TIME TO LOAD "
    print end - start

    # list.save_all_nodes()
    # list.print_all_nodes()
    print "LEN all nodes: " + str(len(lista[0].all_nodes))

    # pickle = NODE_OUTPUT + new_file.split(".")[0] + ".pickle"
    pickle = OUT_FOLDER + file_name.split(".")[0] + ".pickle"
    # tools.save_pickle(pickle, [lista[0], VICT_NODE, lista[1]])

    #--------------------------------------------------------
    # to erase in memory all the data
    #--------------------------------------------------------
    # ROOT_NODE.all_nodes = {}
    # FIRST_MOVEMENT.all_movements = {}
    # Node.ALLNODES = {}
    # Movement.ALL_MOVEMENTS = {}
    return [lista[0], VICT_NODE, lista[1]]



def lambda_multiprocess_stat(opt=1):
    '''
    Multiprocess different tasks, to obtain statistics of the data.
    Option 1: Writes a statistic of ?????
    Option 2: Generates a pickle with the three of games, and the game numbers.
    Option 3: ?????
    :param opt:
    :return:
    '''
    pool = multiprocessing.Pool()
    infiles = []
    results = []
    if opt == 1:
        infiles = read_pieces.getFilesFromFolder(INPUT_FOLDER)
        results = pool.map(multiprocess_white_percentage, infiles)

    elif opt == 2:
        # to process only unprocesssed files
        file_numbers = load_list_files_json(OUT_FOLDER+"", NAMES, ".pickle")
        for i in file_numbers:
            infiles.append(getJsonFile(i, "", NAMES, ".json"))
        infiles = infiles[:LIMIT_GRID]
        results = []
        # results = pool.map(multiprocess_graph_stats, infiles)
        for file in infiles:
            results.append(multiprocess_graph_stats(file))

    elif opt == 3:
        files = load_list_files_json(INPUT_FOLDER + "games_stats/", NAMES, ".csv")

        for i in files:
            infiles.append(getJsonFile(i, "", NAMES, ".json"))

    return results

def get_stat_graph():
    final_output = CURRENT_DIR + "final/"

    results = lambda_multiprocess_stat(2)


    # pick = load_pickle(final_output+"final.pickle")
    # file_result = DATA_PATH + "/stats/results_graph_results.txt"

    # print results

    # movs = pick[2]
    # text = ""
    # for m in movs.all_movements.values():
    #     text += "%d, %d"%(len(m.nodes), m.get_number_nodes()) + linesep
    #
    # print text

    # save_pickle(final_output+"final.pickle", [_root_node_, _end_node_, _first_movement_])
    pass


def test_something():
    """
    To test something erase later.
    :return:
    """
    file = "_final_0.json"
    var = multiprocess_graph_stats(file)
    root_node = var[0]
    end_node =  var[1]
    movements = var[2]
    print "breakpoint"
    print "lalala"

    nod = end_node.get_ordered_backward_nodes()
    for i in nod[:10]:
        print i


def main():
    get_stat_graph()
    pass

if __name__ == '__main__':
    # main()
    test_something()
    # file = "/Volumes/DOCS/thesData/_test_all_from_zero/4/train_pickles/_final_0.pickle"
    # start = time.clock()
    # tools.load_pickle(file)
    #
    # end = time.clock()
    # print "Load pickle time:"
    # print (end - start)
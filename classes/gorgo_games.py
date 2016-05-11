__author__ = "codingMonkey"
__project__ = "ChessML"

from os.path import expanduser
from dev.misc.read_json import getFilesFromFolder
from dev.misc import read_json, read_pieces
from competitors import Competitor, process_name, calculate_average
from events import Event
from nodes import Node
import nodes
import movements
from movements import *
from games import Game, format_Result
from os import linesep, remove
import multiprocessing, sys
import json, operator
import cPickle as pickle

from stats import *

games = {}
events = {}
COMPETITORS = {}
ROOT_NODE = None
FIRST_MOVEMENT = None

'''
We will use each name of these events or games to create a key for each of them.
'''
'/Users/hectorapolorosalespulido/Documents/thesisDataFast/json/DATASET_0.json'
PATH_INPUT = expanduser("~/Documents/thesisDataFast/out/")
PATH_OUTPUT_CSV = expanduser("~/Documents/thesisDataFast/csv/")
PATH_OUTPUT_JSON = expanduser("~/Documents/thesisDataFast/json/")
NODE_OUTPUT = expanduser("~/Documents/thesisDataFast/stats/nodes/")
STATS_OUTPUT = expanduser("~/Documents/thesisDataFast/stats/")

COMPETITORS_PICKLE = "../../data/competitors_tst.pickle"
GAMES_PICKLE = "../../data/games.pickle"
EVENTS_PICKLE = "../../data/events.pickle"
COMPETITORS_TXT = "../../data/competitors.txt"
DATA_PATH = "../../data/"
STATS_PATH = '../../data/stats/'
PAT_IN = "OUT"
PAT_OUT = "DATASET"

TAG_BLACK_ELO = "blackElo"
TAG_WHITE_ELO = "WhiteElo"
TAG_WHITE = "white"
TAG_BLACK = "black"

FILES_TO_PROCESS = 3
DATA_TO_PROCESS = 5


def get_tag(data, field, error=None, fen=""):
    name = ""
    if field in data:
        return fen.join(data[field]).encode("utf8")
    else:
        if error is None:
            strErr = "ERROR: field '" + field + "' missing"
            raise NameError(strErr)
        else:
            return error


def add_competitor(data, comp_str="Black", elo_str="BlackElo"):
    name = process_name(get_tag(data, comp_str))
    elo = get_tag(data, elo_str, error="")
    if name in COMPETITORS:
        COMPETITORS[name].newElo(elo)
        pass
    else:
        COMPETITORS[name] = Competitor(name, elo)


def add_event(data):
    event = get_tag(data, "Event")
    date = get_tag(data, "Date", error="")
    if event not in events:
        events[event] = Event(event, date)
    else:
        events[event].add_Date(date)
        # todo: parse dates somehow
        pass


def add_game(data):
    welo = get_tag(data, "WhiteElo", "")
    belo = get_tag(data, "BlackElo", "")
    white = process_name(get_tag(data, "White"))
    black = process_name(get_tag(data, "Black"))
    event = get_tag(data, "Event")
    result = format_Result(get_tag(data, "Result"))
    round = get_tag(data, "Round", "")
    # fen = get_tag(data, "fen", fen="***")
    try:
        fen = data['fen']
    except KeyError as e:
        raise NameError("ERROR: fen non existant")

    c_w = COMPETITORS[white]
    c_b = COMPETITORS[black]
    name = event + "--" + white + "--" + black + "--" + str(round)
    name = name.replace(" ", "_")

    games[name] = Game(name, fen, events[event], c_w, c_b, result, welo, belo, round)


def getJsonFile(i, path=PATH_INPUT, pattern=PAT_IN, extension=".json"):
    """

    :rtype: object
    """
    return path + pattern + "_" + str(i) + extension


def get_out_file(i, path=PATH_OUTPUT_CSV, extension=".csv", pattern=PAT_OUT):
    return path + pattern + "_" + str(i) + extension


def save_pickle(file, dic):
    with open(file, "wb") as f:
        pickle.dump(dic, f)


def load_pickle(file):
    with open(file, "rb") as f:
        return pickle.load(f)


def load_competitors_pickle():
    global COMPETITORS
    COMPETITORS = load_pickle(COMPETITORS_PICKLE)
    print "Competitors Loaded"


def addict(dict, str):
    if str in dict:
        dict[str] += 1
    else:
        dict[str] = 1


def read_all_results():
    results = {}
    files = read_pieces.getFilesFromFolder(PATH_INPUT)
    for json in files[:3]:
        data = read_json.get_data(PATH_INPUT + json)
        print json
        for d in data[:]:
            try:
                result = get_tag(d, 'WhiteElo')
                addict(results, result)
            except NameError as e:
                print "skipping " + str(e)
    print results


def read_all_competitors():
    pool = multiprocessing.Pool()
    files = read_pieces.getFilesFromFolder(PATH_INPUT)
    for json in files[:]:
        data = read_json.get_data(PATH_INPUT + json)
        print json
        for d in data[:]:
            try:
                add_competitor(d)
                add_competitor(d, "White", "WhiteElo")
            except NameError as e:
                print "skipping " + str(e)

    res = pool.map(calculate_average, COMPETITORS.values())
    # # print res
    #
    li = COMPETITORS.values()
    for i in range(len(COMPETITORS)):
        li[i].avg_elo = res[i]

    print "writing ELO"
    save_pickle(COMPETITORS_PICKLE, COMPETITORS)


def save_files():
    data = []
    file_num = read_pieces.getNewFileToProcess(PATH_OUTPUT_CSV, PAT_OUT, '.csv')
    load_competitors()
    file_write = read_pieces.getFilesFromFolder(file_num)
    f = open(file_write, "w")
    file = getJsonFile(file_num)
    print "Processing " + file
    data = read_json.get_data(file)
    for d in data[:1]:
        try:
            # add_competitor(d)
            # add_competitor(d,"White","WhiteElo")
            add_event(d)
            add_game(d)

        except NameError as e:
            print "skipping " + str(e)
        except KeyError as e:
            f.close()
            remove(file_write)
            print e
            return -1

    # print type(games)
    temp = ""
    for value in games.itervalues():
        temp += value.toStrFormat().encode("utf8") + linesep

    print "writing " + file_write
    f.write(temp)
    f.close()


def elos_to_csv():
    file_num = read_pieces.getNewFileToProcess(STATS_PATH + "elo/", "ELO", '.csv')

    file_write = get_out_file(file_num, STATS_PATH + "elo/", '.csv', "ELO")
    f = open(file_write, "w")
    file_read = getJsonFile(file_num, PATH_OUTPUT_JSON, PAT_OUT)

    print "Processing " + file_read
    data = read_json.get_data(file_read)
    text = ""
    for d in data[:]:
        try:
            # add_competitor(d)
            # add_competitor(d,"White","WhiteElo")
            white = d["white"]
            black = d["black"]
            white_elo = d["white_elo"]
            black_elo = d["black_elo"]
            white_avg_elo = d["white_avg_elo"]
            black_avg_elo = d["black_avg_elo"]
            white_elo = int(white_elo)
            black_elo = int(black_elo)
            res = d["result"]
            len_match = len(d["fen"])
            # l= [white,black,white_elo,black_elo,white_avg_elo,black_avg_elo]
            text += white + "," + black + "," + str(white_elo) + "," + str(black_elo) + "," + str(
                white_avg_elo) + "," + str(black_avg_elo) + "," + str(res) + "," + str(len_match) + linesep
            # print text
        except Exception as e:
            # print e
            pass
            # print "skipping " + str(e)
            # except KeyError as e:
            #     f.close()
            #     remove(file_write)
            #     print e
            #     return -1

            # for val in games.itervalues():
            # json.dump(val.as_dict(), f, encoding='utf-8')
    f.write(text.encode("utf8"))
    f.close()


def save_json():
    data = []
    file_num = read_pieces.getNewFileToProcess(PATH_OUTPUT_JSON, PAT_OUT, '.json')
    file_write = get_out_file(file_num, PATH_OUTPUT_JSON, '.json')

    f = open(file_write, "w")
    file = getJsonFile(file_num)
    print "Processing " + file
    data = read_json.get_data(file)

    for d in data[:]:
        try:
            # add_competitor(d)
            # add_competitor(d,"White","WhiteElo")
            add_event(d)
            add_game(d)
        except NameError as e:
            print "skipping " + str(e)
            # except KeyError as e:
            #     f.close()
            #     remove(file_write)
            #     print e
            #     return -1

    for val in games.itervalues():
        json.dump(val.as_dict(), f, encoding='utf-8')
        f.write('\n')
    f.close()


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

    if name not in games:
        games[name] = Game(name, fen, events[event], COMPETITORS[white], COMPETITORS[black], result, white_elo,
                           black_elo, round, fen_eval)


def load_nodes(data):
    fen = data['fen']
    fen_eval = data['fen_eval']
    result = data['result']

    for i in range(0,len(fen)):
        if fen[i] not in Node.ALLNODES:
            n = Node(fen[i], result, fen_eval[i])
            n.results=[]
    ROOT_NODE.save_all_nodes()


def load_events(data):
    date = data['date']
    event = data['event']

    if event not in events:
        events[event] = Event(event, date)


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
    if name in COMPETITORS:
        COMPETITORS[name].avg_elo = avg
        COMPETITORS[name].newElo(elo)
    else:
        COMPETITORS[name] = Competitor(name, elo, avg)


def process_final_json(new_file, process_nodes=False):
    global COMPETITORS, games, events
    del (games)
    del (COMPETITORS)
    del (events)
    COMPETITORS = {}
    games = {}
    events = {}

    data = read_json.get_data(new_file)
    print "len: > " + str(len(data[:]))
    for d in data[:100]:
        load_competitors(d)
        load_events(d)
        load_games(d)
        if process_nodes:
            load_nodes(d)


def multiprocess_white_percentage(new_file):
    process_final_json(PATH_OUTPUT_JSON + new_file)
    list = get_white_percentage(games)
    return list


def multiprocess_game_statistics(new_file):
    process_final_json(PATH_OUTPUT_JSON + new_file)
    file_write = STATS_OUTPUT + "games_stats/" + new_file.split(".")[0] + ".csv"
    f = open(file_write, "w+")
    text = game_statistics(games)
    f.write(text.encode("utf8"))
    f.close()


def competitor_stats():
    load_competitors_pickle()
    file = STATS_PATH + "competitors_stats2.csv"
    text = ""
    for c in COMPETITORS.values():
        elos = ""
        # for e in c.elo:
        #     elos += ","+str(e)
        text += c.name + "," + str(c.avg_elo) + "," + str(len(c.elo)) + elos + linesep

    with open(file, "w+") as f:
        f.write(text)
        f.close()


def multiprocess_graph_stats(new_file):
    global ROOT_NODE, FIRST_MOVEMENT
    ROOT_NODE = nodes.EndNode(u'rnbqkbnr/pppppppp/......../......../......../......../PPPPPPPP/RNBQKBNR', 0)
    FIRST_MOVEMENT = movements.Movement(0)
    process_final_json(PATH_OUTPUT_JSON + new_file, True)
    # FIRST_MOVEMENT.add_node(ROOT_NODE.name, len(games))
    Movement.initi_all_possible_movements()

    VICT_NODE = nodes.EndNode("END", 0)
    # ROOT_NODE.all_nodes.pop("test", None)

    # print ROOT_NODE.__class__.__name__ + ROOT_NODE.name
    # print "%s >>  %d"%(new_file,len(games))
    lista = build_position_graph(games, VICT_NODE, ROOT_NODE.all_nodes)
    # list.save_all_nodes()
    # list.print_all_nodes()
    print "LEN all nodes:" + str(len(lista[0].all_nodes))

    # pickle = NODE_OUTPUT + new_file.split(".")[0] + ".pickle"
    pickle = STATS_OUTPUT+"test/" + new_file.split(".")[0] + ".pickle"
    print pickle
    save_pickle(pickle, [lista, VICT_NODE])

    ROOT_NODE.all_nodes = {}
    FIRST_MOVEMENT.all_movements = {}
    Node.ALLNODES = {}
    Movement.ALL_MOVEMENTS = {}
    return [lista[0], VICT_NODE, lista[1]]


def lambda_multiprocess_stat(opt=1):
    '''

    :param opt:
    :return:
    '''
    pool = multiprocessing.Pool()
    infiles = []
    results = []
    if opt == 1:
        infiles = read_pieces.getFilesFromFolder(PATH_OUTPUT_JSON)
        results = pool.map(multiprocess_white_percentage, infiles)

    elif opt == 2:
        file_numbers = load_list_files_json(STATS_OUTPUT+"test/", PAT_OUT, ".pickle")

        for i in file_numbers:
            infiles.append(getJsonFile(i, "", PAT_OUT, ".json"))
        infiles = infiles[:]
        results = []

        # results = pool.map(multiprocess_graph_stats, infiles)
        for file in infiles:
            infiles = infiles[:]
            results.append(multiprocess_graph_stats(file))

    elif opt == 3:

        files = load_list_files_json(STATS_OUTPUT + "games_stats/", PAT_OUT, ".csv")

        for i in files:
            infiles.append(getJsonFile(i, "", PAT_OUT, ".json"))

        # for file in infiles:
        #     infiles = infiles[:]
        #     results.append(multiprocess_game_statistics(file))
        #
        results = pool.map(multiprocess_game_statistics, infiles)

    return results


def get_stat_white_percentage():
    white = 0
    draw = 0
    black = 0
    games = 0
    file_result = DATA_PATH + "/stats/results_txt"
    results = lambda_multiprocess_stat(1)
    for r in results:
        # print r
        white += r[0]
        draw += r[1]
        games += r[2]
    black = games - white - draw

    text = "white,draw,black,games" + linesep
    text += "%d,%d,%d,%d" % (white, draw, black, games)

    print "writing: %s" % text
    with open(file_result, "w+") as f:
        f.write(text)


def test_root_node(nodes):
    for node in nodes.values():
        print " \t\t %d %s" % (node[0], node[1])


def get_stat_graph():
    final_output = STATS_OUTPUT + "final/"

    pick = load_pickle(final_output+"final.pickle")
    movs = pick[2]
    text = ""
    for m in movs.all_movements.values():
        text += "%d, %d"%(len(m.nodes), m.get_number_nodes()) + linesep

    print text

    # file_result = DATA_PATH + "/stats/results_graph_results.txt"
    # results = lambda_multiprocess_stat(2)
    # print results

    # input_list = getFilesFromFolder(STATS_OUTPUT+"test/")
    input_list = getFilesFromFolder(NODE_OUTPUT)
    file_to_open = NODE_OUTPUT + input_list[0]
    # file_to_open = STATS_OUTPUT + "test/" + input_list[0]
    print file_to_open
    # p = load_pickle(file_to_open)
    # _root_node_ = p[0][0]
    # _first_movement_ = p[0][1]
    # _end_node_ = p[1]

    # print file_to_open


    #
    # _end_node_.print_branched_nodes()
    #
    # print str(len(_root_node_.all_nodes))
    # num = len(_root_node_.all_nodes)
    # # file_to_open = ""
    # for l in input_list[1:10]:
    #     file_to_open = NODE_OUTPUT + l
    #     # file_to_open = STATS_OUTPUT + "test/" + l
    #     p = load_pickle(file_to_open)
    #     root_nod = p[0][0]
    #     first_mov = p[0][1]
    #     end_nod = p[1]
    #
    #     #     # nodes.merge_nodes(end_nod,end_nod)
    #     num += nodes.merge_nodes(_root_node_, root_nod)
    #     _end_node_.add_nodes(_end_node_.back_nodes,end_nod.back_nodes,root_nod.all_nodes)
    #     _first_movement_ = merge_movements(_first_movement_, first_mov)
    #
    #     print file_to_open + " " + str(len(first_mov.nodes))
    #     test_root_node(first_mov.nodes)

    # save_pickle(final_output+"final.pickle", [_root_node_, _end_node_, _first_movement_])



def write_game_stats():
    results = lambda_multiprocess_stat(3)

    # text = linesep.join(results)
    # with open(STATS_OUTPUT+"games_stats/games_stats.txt") as f:


def load_list_files_json(output_files, pattern, extension):
    """

    :return:
    """

    return read_pieces.getFilesToProcess(output_files, pattern, extension)


def main():
    get_stat_graph()
    # write_game_stats()


if __name__ == '__main__':
    # load_competitors_pickle()
    for i in range(0, 1):
        main()
        del (games)
        del (COMPETITORS)
        del (events)
        games = {}
        COMPETITORS = {}
        events = {}

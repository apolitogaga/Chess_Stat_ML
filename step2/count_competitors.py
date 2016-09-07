__author__ = "codingMonkey"
__project__ = "ChessML"


from dev2.step2 import INPUT_FOLDER, OUTPUT_REFINED_JSON_FOLDER, PICKLE_COMPETITORS
from dev2.step2.classes.competitors import Competitor, process_name, calculate_average
from dev2.step2.classes.events import Event
from dev2.step2.classes.games import Game, format_Result

import multiprocessing
from dev2.tools import read_pieces, read_json, tools

# first we must save the competitors average, so we must process them all.
# from stats import *

GAMES = {}
EVENTS = {}
COMPETITORS = {}
ROOT_NODE = None
FIRST_MOVEMENT = None

NAME = "OUT"



#########################################################
#############  JSON MANIPULATION  #######################
#########################################################

def do_step_1():
    """
    Reads all the competitors, and generates an average elo for each one of them.
    :return: saves a pickle file.
    """
    read_all_competitors()

def do_step_2():
    """
    dsfsadf
    :return:
    """
    global COMPETITORS, EVENTS, GAMES
    load_competitors_pickle()
    for i in range(0, 1000):
        read_all_matches()
        del (GAMES)
        # del (COMPETITORS)
        del (EVENTS)
        GAMES = {}
        # COMPETITORS = {}
        EVENTS = {}


def get_tag(data, field, error=None, fen=""):
    """
    Obtains the desired field from the data, and returns it's value if found.
    :param data: dictionary of games
    :param field: desired field
    :param error: error string
    :param fen: ??
    :return:
    """
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
    '''
    Obtain the competitors from the data, used when we want the black or white properties.
    Name and elo.
    :param data:
    :param comp_str:
    :param elo_str: s
    :return:
    '''
    name = process_name(get_tag(data, comp_str))
    elo = get_tag(data, elo_str, error="")
    if name in COMPETITORS:
        COMPETITORS[name].newElo(elo)
        pass
    else:
        COMPETITORS[name] = Competitor.short_init(name, elo)


def add_event(data):
    '''

    :param data:
    :return:
    '''
    event = get_tag(data, "Event")
    date = get_tag(data, "Date", error="")
    if event not in EVENTS:
        EVENTS[event] = Event(event, date)
    else:
        EVENTS[event].add_Date(date)
        # todo: parse dates somehow
        pass


def add_game(data):
    '''

    :param data:
    :return:
    '''
    welo = get_tag(data, "WhiteElo", "")
    welo = tools.try_float(welo)
    belo = get_tag(data, "BlackElo", "")
    belo = tools.try_float(belo)

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

    GAMES[name] = Game.init_fenless(name, fen, EVENTS[event], c_w, c_b, result, welo, belo, round)

def load_competitors_pickle():
    """
    Loads into memory all the competitors that were previously processed
    :return:
    """
    global COMPETITORS
    COMPETITORS = tools.load_pickle(PICKLE_COMPETITORS)
    print "Competitors Loaded"

def read_all_competitors():
    """
    GO over all the competitors to average the ELO's of found competitors, and fill in when there's no known ELO.
    :return:
    """
    pool = multiprocessing.Pool()
    files = read_pieces.getFilesFromFolder(INPUT_FOLDER)
    for json in files[:]:
        data = read_json.get_data(INPUT_FOLDER + json)
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
    tools.save_pickle(PICKLE_COMPETITORS, COMPETITORS)


def read_all_matches():
    """
    go over all the data and reconstruct a better version of json.
    :return:
    """
    data = []
    file_num = read_pieces.getNewFileToProcess(OUTPUT_REFINED_JSON_FOLDER, NAME, '.json')
    file_write = tools.get_out_file(file_num, OUTPUT_REFINED_JSON_FOLDER, '.json',NAME)
    file = tools.getJsonFile(file_num)
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
        tools.save_new_json(GAMES, file_write)


if __name__ == '__main__':
    # do_step_1()
    do_step_2()



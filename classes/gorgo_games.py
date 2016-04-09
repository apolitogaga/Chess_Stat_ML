from os.path import expanduser

from dev.misc.read_json import getFilesFromFolder

__author__ = "codingMonkey"
__project__ = "ChessML"
from dev.misc import read_json, read_pieces
from competitors import Competitor, process_name, calculate_average
from events import Event
from games import Game, format_Result
from os import linesep, remove
from multiprocessing import pool
import multiprocessing
import pickle, json

from stats import *

games = {}
events = {}
COMPETITORS = {}

'''
We will use each name of these events or games to create a key for each of them.
'''

PATH_INPUT = expanduser("~/Documents/thesisDataFast/out/")
PATH_OUTPUT_CSV = expanduser("~/Documents/thesisDataFast/csv/")
PATH_OUTPUT_JSON = expanduser("~/Documents/thesisDataFast/json/")
COMPETITORS_PICKLE = "../../data/competitors.pickle"
GAMES_PICKLE = "../../data/games.pickle"
EVENTS_PICKLE = "../../data/events.pickle"
COMPETITORS_TXT = "../../data/competitors.txt"
DATA_PATH = "../../data/"

PAT_IN = "OUT"
PAT_OUT = "DATASET"


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


def getJsonFile(i):
    """

    :rtype: object
    """
    return PATH_INPUT + PAT_IN + "_" + str(i) + ".json"


def get_out_file(i, path=PATH_OUTPUT_CSV, pattern=".csv"):
    return path + PAT_OUT + "_" + str(i) + pattern


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

    add_competitor(white, white_elo, white_elo_avg)
    add_competitor(black, black_elo, black_elo_avg)


def add_competitor(name, elo, avg):
    if name in COMPETITORS:
        COMPETITORS[name].avg_elo = avg
        COMPETITORS[name].newElo(elo)
    else:
        COMPETITORS[name] = Competitor(name, elo, avg)


def process_final_json(new_file):
    global COMPETITORS, games, events
    COMPETITORS = {}
    games = {}
    events = {}
    file = PATH_OUTPUT_JSON + new_file

    data = read_json.get_data(file)
    for d in data[:20]:
        load_competitors(d)
        load_events(d)
        load_games(d)


def multiprocess_white_percentage(new_file):
    process_final_json(new_file)
    list = get_white_percentage(games)
    return list


def multiprocess_graph_stats(new_file):
    process_final_json(new_file)
    list = get_fen_graph(games)
    return list


def pool_white_percentage(pool,infiles):
    return pool.map(multiprocess_white_percentage, infiles)

def lambda_multiprocess_stat(opt=1):
    pool = multiprocessing.Pool()
    infiles = load_list_files_json()
    infiles = infiles[:2]
    results = None
    if opt==1:
        print 1
        results = pool.map(multiprocess_white_percentage, infiles)
    elif opt==2:
        print 2
        results = pool.map(multiprocess_graph_stats, infiles)
        # results = multiprocess_graph_stats(infiles[0])

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


def get_stat_graph():
    file_result = DATA_PATH + "/stats/results_graph_results.txt"
    print "afsdfas"
    results = lambda_multiprocess_stat(2)
    print results
    # for r in results:
    #     print r



    # text = "white,draw,black,games" + linesep
    # text += "%d,%d,%d,%d" % (white, draw, black, games)

    # print "writing: %s" % text
    # with open(file_result, "w+") as f:
    #     f.write(text)



def load_list_files_json():
    """

    :return:
    """
    return getFilesFromFolder(PATH_OUTPUT_JSON)


def main():
    # save_json()
    get_stat_graph()
    # calc = Calc_Stats(COMPETITORS, games, events)
    # calc.get_white_percentage()


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

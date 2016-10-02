__author__ = "codingMonkey"
__project__ = "ChessML"

from dev2.generate_statistics import ALT_TRAIN_INPUT_FOLDER, ALT_TEST_INPUT_FOLDER, STAT_DATA_FOLDER
from dev2.step4 import process_data
from dev2.step4.classes import movements
from dev2.tools import tools, read_json, read_pieces


import multiprocessing


ALT_TRAIN = ALT_TRAIN_INPUT_FOLDER
ALT_TEST = ALT_TEST_INPUT_FOLDER

IN_FOLDER = ALT_TRAIN
OUT_FOLDER = STAT_DATA_FOLDER

BASIC_STATS_NAME = "BASIC_STATS_"
NEW_PREFIX ="_new_"
FILE_EXTENSION = ".csv"

# fields that are in the JSON:
BLACK = "black"
WHITE = "white"
BLACK_ELO = "black_elo"
WHITE_ELO = "white_elo"
BLACK_AVG_ELO = "black_avg_elo"
WHITE_AVG_ELO = "white_avg_elo"
RESULT = "result"
FEN = "fen"
LEN_FEN = "LEN_FEN"

#####

def get_number_from_filename(fileStr):
    """

    :param fileStr:
    :return:
    """
    num = int(fileStr.split(".")[0].split("_")[-1])
    return num

def multiprocess_file(function):
    pool = multiprocessing.Pool()
    list = read_pieces.getFilesFromFolder(IN_FOLDER)
    res = pool.map(function, list)


def get_file(file, function, new_name=NEW_PREFIX, new_file_path = OUT_FOLDER, *arg_list):
    data =  read_json.get_data(IN_FOLDER+file)
    file_num = get_number_from_filename(file)

    path = new_file_path + str(file_num)+ "/"
    newName =  new_name + str(file_num) + FILE_EXTENSION
    list_tuples = function(data)
    print path + newName
    tools.write_csv_from_list(path + newName, list_tuples, arg_list[0])

def get_elos_result_longGame_etc(data):
    """
    Returns the desired data in a list of tuples, to be written in csv.
    :param data:
    :return: transformed tuple
    """
    list_tuple=[]
    for game in data[:]:
        black = game[BLACK].encode("utf8")
        white = game[WHITE].encode("utf8")
        welo = tools.to_int(game[WHITE_ELO])
        belo =  tools.to_int(game[BLACK_ELO])
        avg_belo = game[BLACK_AVG_ELO]
        avg_welo = game[WHITE_AVG_ELO]
        res = game[RESULT]
        flen = len(game[FEN])

        tup = (white, black, welo, belo, avg_welo, avg_belo, res, flen)
        list_tuple.append(tup)
    return list_tuple

def write_basic_stats(file):
    header = [WHITE, BLACK, WHITE_ELO, BLACK_ELO, WHITE_AVG_ELO, BLACK_AVG_ELO, RESULT, LEN_FEN]
    get_file(file, get_elos_result_longGame_etc, BASIC_STATS_NAME, OUT_FOLDER, header)


if __name__ == '__main__':
    # get_fie("REF_final_0.json")
    # print get_number_from_filename("REF_final_0.json")
    write_basic_stats("REFREF_final_0.json")
    # multiprocess_file(write_basic_stats)
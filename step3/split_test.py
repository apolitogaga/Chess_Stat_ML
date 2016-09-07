__author__ = "codingMonkey"
__project__ = "ChessML"


from dev2.step4 import TEST_INPUT_FOLDER, TRAIN_INPUT_FOLDER, BASE_INPUT_FOLDER
from dev2.step3 import  TEST_REFINED_DATA_OUTPUT
from dev2.tools import tools, read_json, read_pieces

import multiprocessing
NEW_PREFIX = "REF"
ALT_NAME = ""
MAX_NUMBER_MOVEMENTS = 20

ALT_TRAIN_OUTPUT_FOLDER = BASE_INPUT_FOLDER + "alt_train/"
ALT_TEST_OUTPUT_FOLDER = BASE_INPUT_FOLDER + "alt_test/"

ALT_TRAIN_INPUT_FOLDER = BASE_INPUT_FOLDER + "alt_train_2/"
ALT_TEST_INPUT_FOLDER = BASE_INPUT_FOLDER + "alt_test_2/"

# IN_FOLDER = TEST_INPUT_FOLDER
# OUT_FOLDER = ALT_TEST_OUTPUT_FOLDER
#
# IN_FOLDER = TRAIN_INPUT_FOLDER

OUT_FOLDER = ALT_TEST_OUTPUT_FOLDER
IN_FOLDER = ALT_TEST_INPUT_FOLDER

STANDARD_STARTING_BOARD = u'rnbqkbnr/pppppppp/......../......../......../......../PPPPPPPP/RNBQKBNR'

# IN_FOLDER = TEST_INPUT_FOLDER
# OUT_FOLDER = ALT_TEST_OUTPUT_FOLDER
#
# IN_FOLDER = TRAIN_INPUT_FOLDER

OUT_FOLDER = ALT_TEST_OUTPUT_FOLDER
IN_FOLDER = ALT_TEST_INPUT_FOLDER

def refine_json(file, new_file_path = OUT_FOLDER):
    """
    Reduces the number of data to provide a more test-like file.
    :param file: file to process
    :param new_file_path: file output
    :return: nothing, saves a new file
    """
    data =  read_json.get_data(IN_FOLDER+file)
    newName = NEW_PREFIX + file
    for i, d in enumerate(data[:]):
        d['fen'] = d['fen'][:MAX_NUMBER_MOVEMENTS]
        d['fen_eval'] = d['fen_eval'][:MAX_NUMBER_MOVEMENTS]
        data[i] = d
    read_json.save_json(data, new_file_path + newName)


def multiprocess_test_files():
    pool = multiprocessing.Pool()
    list = read_pieces.getFilesFromFolder(IN_FOLDER)
    res = pool.map(refine_json, list)
    pass


def divide_fen(file, new_file_path = OUT_FOLDER):
    """
    Deletes half moves to reduce file size.
    :param file: file to process
    :param new_file_path: file output
    :return: nothing, saves a new file
    """
    data =  read_json.get_data(IN_FOLDER+file)
    newName = NEW_PREFIX + file
    for i, d in enumerate(data[:]):
        last =  len(d['fen'])-1
        del d['fen'][1:last:2]
        del d['fen_eval'][1:last:2]
        data[i] = d
    print new_file_path + newName
    read_json.save_json(data, new_file_path + newName)
def refine_json(file, new_file_path = OUT_FOLDER):
    """
    Reduces the number of data to provide a more test-like file.
    :param file: file to process
    :param new_file_path: file output
    :return: nothing, saves a new file
    """
    data =  read_json.get_data(IN_FOLDER+file)
    newName = NEW_PREFIX + file
    for i, d in enumerate(data[:]):
        d['fen'] = d['fen'][:MAX_NUMBER_MOVEMENTS]
        d['fen_eval'] = d['fen_eval'][:MAX_NUMBER_MOVEMENTS]
        data[i] = d
    read_json.save_json(data, new_file_path + newName)


def multiprocess_test_files():
    pool = multiprocessing.Pool()
    list = read_pieces.getFilesFromFolder(IN_FOLDER)
    res = pool.map(refine_json, list)
    pass


def divide_fen(file, new_file_path = OUT_FOLDER):
    """
    Deletes half moves to reduce file size.
    :param file: file to process
    :param new_file_path: file output
    :return: nothing, saves a new file
    """
    data =  read_json.get_data(IN_FOLDER+file)
    newName = NEW_PREFIX + file
    for i, d in enumerate(data[:]):
        last =  len(d['fen'])-1
        del d['fen'][1:last:2]
        del d['fen_eval'][1:last:2]
        data[i] = d
    print new_file_path + newName
    read_json.save_json(data, new_file_path + newName)

def multiprocess_divide_fen():
    pool = multiprocessing.Pool()
    list = read_pieces.getFilesFromFolder(IN_FOLDER)
    res = pool.map(divide_fen, list)
    pass

def delete_started_games(file, new_file_path = OUT_FOLDER):
    """
    Deletes half moves to reduce file size.
    :param file: file to process
    :param new_file_path: file output
    :return: nothing, saves a new file
    """
    data =  read_json.get_data(IN_FOLDER+file)
    newName = NEW_PREFIX + file
    temp_data = []
    print len(data)
    for i, d in enumerate(data[:]):
        # last =  len(d['fen'])-1
        # del d['fen'][1:last:2]
        # del d['fen_eval'][1:last:2]
        # data[i] = d
        if STANDARD_STARTING_BOARD.__eq__(d['fen'][0]):
            temp_data.append(d)
        else:
            # print d['fen'][0]
            pass

    print "print deleted %d games" % (len(data) - len(temp_data))
    # print new_file_path + newName
    read_json.save_json(temp_data, new_file_path + newName)

if __name__ == '__main__':
    # multiprocess_test_files()
    # multiprocess_divide_fen()
    # delete_started_games("REF_final_0.json")


    pool = multiprocessing.Pool()
    list = read_pieces.getFilesFromFolder(IN_FOLDER)
    res = pool.map(delete_started_games, list)
    print "fafasfa"


'''
'
'       Add code here that contributes to the whole project.
'
'
'''
__author__ = "codingMonkey"
__project__ = "ChessML"

from dev2.step2 import INPUT_FOLDER
import cPickle as pickle
import json, csv



def save_new_json(dic, file):
    with open(file,"w") as f:
        for val in dic.itervalues():
            json.dump(val.as_dict(), f, encoding='utf-8')
            f.write('\n')
        f.close()

def save_pickle(file, dic):
    with open(file, "wb") as f:
        pickle.dump(dic, f)

def load_pickle(file):
    with open(file, "rb") as f:
        return pickle.load(f)

def get_out_file(i, path = INPUT_FOLDER , extension=".csv", pattern = "DATASET"):
    return path + pattern + "_" + str(i) + extension


def write_csv_from_list(file, data, *arg_list):
    """
    Writes a csv file from the data.
    :param file: Path to file
    :param data: A list of tuples
    :param arg_list: list of headers to add
    :return:
    """
    with open(file, "wb") as f:
        str = ""
        wr = csv.writer(f, dialect='excel')
        # header = ",".join(args)
        try:
            wr.writerow(tuple(arg_list[0]))
        except IndexError:
            # no header has been added
            pass
        for row in data[:]:
            wr.writerow(row)

def getJsonFile(i, path=INPUT_FOLDER, pattern="OUT", extension=".json"):
    """

    :rtype: object
    """
    return path + pattern + "_" + str(i) + extension


def try_float(str):
    """
    tries to convert str to int
    :return:
    """
    try:
        return float(str)
    except ValueError:
        return str
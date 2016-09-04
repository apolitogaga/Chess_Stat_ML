__author__ = "codingMonkey"
__project__ = "ChessML"


from dev2.step4 import TEST_INPUT_FOLDER, TRAIN_INPUT_FOLDER, BASE_INPUT_FOLDER
from dev2.step3 import TEST_REFINED_DATA_OUTPUT, CURRENT_DIR
from dev2.tools import tools, read_json, read_pieces

import multiprocessing, json, csv

from collections import Counter
from operator import add


ALT_TRAIN_OUTPUT_FOLDER = BASE_INPUT_FOLDER +"alt_train/"
ALT_TEST_OUTPUT_FOLDER = BASE_INPUT_FOLDER +"alt_test/"

TRAIN_OUT = BASE_INPUT_FOLDER + "_test_all_from_zero/ref_alt_train/"
TEST_OUT = BASE_INPUT_FOLDER + "_test_all_from_zero/ref_alt_test/"

FILE_OUTPUT = CURRENT_DIR + "all.json"
FILE_OUTPUT = CURRENT_DIR + "all_train.csv"
IN_FOLDER = ALT_TRAIN_OUTPUT_FOLDER
# FILE_OUTPUT = CURRENT_DIR + "all_test.csv"
# IN_FOLDER = ALT_TEST_OUTPUT_FOLDER
OUT_FOLDER = TRAIN_OUT
NAME = "ref_"


def extract_data(file):
    print file
    temp = {}
    newName = NAME + file
    data =  read_json.get_data(IN_FOLDER+file)
    for i, d in enumerate(data[:]):
        for move in d['fen'][:]:
            read_pieces.addict(temp, move)



    # print "finish sorting."

    # temp = {}
    # del(temp)
    return temp


def updateInPlace(a,b):
    a.update(b)
    return a


def multiprocess_extraction():
    pool = multiprocessing.Pool()
    list = read_pieces.getFilesFromFolder(IN_FOLDER)
    res = pool.map(extract_data, list[:])
    dic = reduce(updateInPlace, (Counter(dict(x)) for x in res))

    print "finish merging."
    sort = sorted(dic.items(), key=lambda x:x[1])[::-1]
    print "finished sorting"
    with open(FILE_OUTPUT, "wb") as f:
        str = ""


        wr = csv.writer(f, dialect='excel')
        wr.writerow(['name','num'])
        num = len(sort)
        n =  int(num/20)
        print num
        for row in sort[:n]:
            wr.writerow(row)
        # f.write(str+"\n")
        print "finishing writning"
        f.close()

if __name__ == '__main__':
    # multiprocess_extraction()

    pass


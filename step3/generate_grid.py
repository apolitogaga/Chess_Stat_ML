"""
split data into train-test parts.
"""
__author__ = "codingMonkey"
__project__ = "ChessML"

from os.path import expanduser
from dev.classes import gorgo_games
from read_json import getFilesFromFolder, get_data, save_json
from collections import defaultdict
import random, json, os
import csv, sys
import multiprocessing, collections

FILE_PATH = expanduser("/Volumes/DOCS/thesData/")
TEST_PATH = FILE_PATH + "test/"
TEST_GRID_PATH = FILE_PATH +"test_grid/"
TEST_FINAL_PATH = FILE_PATH +"test_data/"

TRAIN_PATH = FILE_PATH + "train/"
TRAIN_GRID_PATH = FILE_PATH +"train_grid/"
TRAIN_FINAL_PATH = FILE_PATH +"train_data/"

INPUT_FOLDER = gorgo_games.PATH_OUTPUT_JSON
INPUT_RANGES = gorgo_games.STATS_PATH + "ranges.csv"


def split_document(file,percentage=.7):
    # def file_len(fname):
    name = file.split(".")[0]
    file = INPUT_FOLDER + file
    test_output =  TEST_PATH+"test_"+name +".json"
    train_output =  TRAIN_PATH+"train_"+name +".json"
    with open(file) as data:
        with open(test_output, 'w') as test:
            with open(train_output, 'w') as train:
                header = next(data)
                test.write(header)
                train.write(header)
                for line in data:
                    if random.random() < percentage:
                        train.write(line)
                    else:
                        test.write(line)
                len_file = file_len(file)+0.0
                len_test = file_len(test_output)
                # len_train = file_len(train_output)
                # print "%f <>  %f"%(len_train/len_file,len_test/len_file)
                return len_test/len_file

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def split_documents():
    pool = multiprocessing.Pool()
    input_list = getFilesFromFolder(INPUT_FOLDER)
    res = pool.map(split_document,input_list)

    var = sum(res)/len(input_list)
    # 0.300114029074
    print var


def split_doc_by_ranges(file,dic,test=False):
    if test:
        file = TEST_PATH + file
    else:
        file = TRAIN_PATH + file
    json_data = get_data(file)
    grid_number = -1
    final = defaultdict(list)
    for game in json_data[:]:
        black_elo = game["black_avg_elo"]
        white_elo = game["white_avg_elo"]
        if black_elo is not  None and white_elo is not None:
            # print '%s %s'%(black_elo,white_elo)
            white_grid = get_white_grid_number(white_elo)
            black_dick = dic[white_grid]
            try:
                grid_number = black_dick[black_elo]
            except KeyError:
                print "ERROR:  %d, <%s, %s>"%(white_grid,white_elo,black_elo)
                raise Exception
            try:
                final[grid_number].append(game)
            except Exception as e:
                print e

    return final


def write_docs_from_grid(final_docs, folder,file_number,pattern = "DATASET"):
    num_items = 0
    for key, value in final_docs.iteritems():
        num_items += len(value)
        fi = "%s%d/%s_%s.json"%(folder,key,pattern,file_number)

        with open(fi,"w") as f:
            json.dump(value,f)
    return "%d %d %s"%(len(final_docs),num_items,fi.split(".")[0])
    pass


def process_files_to_grid(file_to_process, references, output_foder, test=False):
    number = file_to_process.split(".")[0].split("_")[2]
    final_doc = split_doc_by_ranges(file_to_process, dic=references, test=test)
    text = write_docs_from_grid(final_doc,output_foder,number)
    final_doc = {}
    return text

def split_by_grid_ranges(test=False):
    if test:
        input_folder = TEST_PATH
        output_foder = TEST_GRID_PATH
    else:
        input_folder = TRAIN_PATH
        output_foder = TRAIN_GRID_PATH
    input_list = getFilesFromFolder(input_folder)
    log = ""
    with open(INPUT_RANGES) as csvfile:
        reader = csv.DictReader(csvfile)
        references = create_table_of_references(reader)

        for i in input_list[:]:
            print i
            log+= process_files_to_grid(i,references,output_foder, test) + os.linesep

    with open(TEST_GRID_PATH+"log.txt","w") as f:
        f.write(log)




# [1] "100 2043"
# [1] "2044 2160"
# [1] "2161 2235"
# [1] "2236 2293"
# [1] "2294 2347"
# [1] "2348 2397"
# [1] "2398 2448"
# [1] "2449 2498"
# [1] "2499 2558"
# [1] "2559 2875"

def get_white_grid_number(white_elo):
    if  white_elo <  2043: return 0
    elif white_elo < 2160: return 1
    elif white_elo < 2235: return 2
    elif white_elo < 2293: return 3
    elif white_elo < 2347: return 4
    elif white_elo < 2397: return 5
    elif white_elo < 2448: return 6
    elif white_elo < 2498: return 7
    elif white_elo < 2558: return 8
    #elif white_elo <= 2875: return 9
    else: return 9


def create_table_of_references(reader):
    results = defaultdict(lambda: collections.defaultdict(list))
    j = 0
    dict = {}
    black_min = 'bmin'
    black_max = 'bmax'
    white_min = 'wmin'
    white_max = 'wmax'
    max_elo = 3000
    for i, grid in enumerate(reader):
        min_b = int(grid[black_min])
        max_b = int(grid[black_max])
        # print "%d %d"%(min_b,max_b)
        if (i) % 10 == 0:
            create_dictionary_references(0,max_b, i,dict)
        elif (i-9)%10==0:
            create_dictionary_references(min_b,max_elo, i,dict)
        else:
            create_dictionary_references(min_b,max_b, i,dict)
        if (i+1) % 10 == 0:
            results[j] = dict.copy()
            j = j+1
            dic = {}
    # test_grid(results)
    return results


def test_grid(result):
    temp = 0
    for grid in result.values():
        for key, value in grid.iteritems():
            if temp != value:
                print "%d %d"%(key, value)
                temp = value


def create_dictionary_references(bmin, bmax, number, dict):
    # print '\n %d -- %d'%(bmin,bmax)
    for i in range(bmin,bmax+1):
        # sys.stdout.write("%d "%i)
        dict[i] = number
    #return dict




def merge_grid_files(folder, number, final_folder):
    folder = folder + "%d/"%number

    files = getFilesFromFolder(folder)
    final_file = final_folder + "_final_%d.json"%number
    all_data = []
    ### got files:

    for file in files:
        # print "writing file %s"%file
        f = folder + file
        temp = []
        d = get_data(f)

        for e in d:
            for el in e:
                all_data.append(el)


    save_json(all_data,final_file)
    print "should be around: %d lines"%len(all_data)
    all_data = None
    del(all_data)

def go_over_files(folder, final_folder):
    list = []
    for i in range(0,1):
        print i
        merge_grid_files(folder,i,final_folder)
    return



def clear_final_from_folder(folder=TRAIN_GRID_PATH):
    for i in  range(100):
        file = folder+"%d/_final_%d.json"%(i,i)
        try:
            os.remove(file)
        except Exception:
            print file

        #files = getFilesFromFolder(folder)


if __name__ == "__main__":
    go_over_files(TRAIN_GRID_PATH,TRAIN_FINAL_PATH)
    # clear_final_from_folder(TEST_GRID_PATH)
    # split_by_grid_ranges(True)

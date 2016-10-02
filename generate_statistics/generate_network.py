__author__ = "codingMonkey"
__project__ = "ChessML"



from dev2.tools import tools, read_json, read_pieces
from dev2.generate_statistics import DATA_FOLDER, ALT_TEST_INPUT_FOLDER, ALT_TRAIN_INPUT_FOLDER
from dev2.step2.classes.competitors import add_competitor_result
import multiprocessing

INPUT_FILE = ALT_TRAIN_INPUT_FOLDER + "_final_0.json"
I2_FILE = ALT_TRAIN_INPUT_FOLDER + "REFREF_final_0.json"

IN_FOLDER = ALT_TRAIN_INPUT_FOLDER
OUT_FOLDER = DATA_FOLDER
OUT_FILE = DATA_FOLDER + "network_0.csv"

NAME = "network_"
BLACK_PLAYER = "black"
WHITE_PLAYER = "white"
RESULT = "result"

COMPETITOR_DATABASE = OUT_FOLDER + "competitors.json"

def write_network(file):
    """
    GETS DATA and saves it from csv.
    white, black, and some weight
    :param file: file to read
    """
    print file
    # header = ["white","black","result"]
    data = read_json.get_data(IN_FOLDER+ file)
    numb = tools.get_number_from_filename(file)
    file = OUT_FOLDER + NAME + str(numb)+ ".csv"
    #todo:
    temp = []
    for game in data[:]:
        white = game[WHITE_PLAYER].replace(" ","_").encode("utf8")
        black = game[BLACK_PLAYER].replace(" ","_").encode("utf8")
        result = game[RESULT]
        temp.append((white,black, result))
    tools.write_csv_from_list(file, temp)


def player_win_percentage():
    competitors = {}
    file_list = read_pieces.getFilesFromFolder(IN_FOLDER)
    for file in file_list[:]:
        print file
        data =  read_json.get_data(IN_FOLDER+file)
        for d in data[:]:
            add_competitor_result(d,competitors)
    # print competitors

    all = []
    for competitor in competitors.itervalues():
        competitor.set_stats()
        all.append(competitor.get_dict_stats())
    read_json.save_json(all, COMPETITOR_DATABASE)
    # tools.write_csv_from_list(COMPETITOR_DATABASE, all)

def process_files():
    pool = multiprocessing.Pool()
    list = read_pieces.getFilesFromFolder(IN_FOLDER)
    res = pool.map(write_network, list)

def test_args(*list_args):
    print ",".join(list_args[0])

if __name__ == '__main__':
    # header = ["white","black","result"]
    # # print test_args(header)
    # # write_network(INPUT_FILE)
    # print "\n\n\n\n\n\n"
    # data = get_data(I2_FILE)
    # print type(data[0])
    # tools.write_csv_from_list(OUT_FILE, data, header)

    # process_files()
    # write_network("REFREF_final_38.json")


    player_win_percentage()

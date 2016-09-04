__author__ = "codingMonkey"
__project__ = "ChessML"


from dev2.step4 import TEST_INPUT_FOLDER, TRAIN_INPUT_FOLDER, BASE_INPUT_FOLDER
from dev2.step3 import  TEST_REFINED_DATA_OUTPUT, CURRENT_DIR
from dev2.tools import tools, read_json, read_pieces

INPUT_FILE = TRAIN_INPUT_FOLDER + "_final_0.json"
I2_FILE = TEST_REFINED_DATA_OUTPUT + "REF_final_0.json"

CSV_OUTPUT = CURRENT_DIR +"csv/"
OUT_FILE = CSV_OUTPUT + "network_0.csv"

BLACK_PLAYER = "black"
WHITE_PLAYER = "white"
RESULT = "result"

def get_data(file):

    data = read_json.get_data(file)
    # GETS DATA and saves it from csv.
    # white, black, and some weight

    #todo:
    temp = []
    for game in data[:]:
        white = game[WHITE_PLAYER]
        black = game[BLACK_PLAYER]
        result = game[RESULT]
        temp.append((white,black, result))
    return temp

def generate_network():

    pass


def test_args(*list_args):
    print ",".join(list_args[0])

if __name__ == '__main__':
    header = ["white","black","result"]
    # print test_args(header)
    # get_data(INPUT_FILE)
    print "\n\n\n\n\n\n"
    data = get_data(I2_FILE)
    print type(data[0])
    tools.write_csv_from_list(OUT_FILE, data, header)

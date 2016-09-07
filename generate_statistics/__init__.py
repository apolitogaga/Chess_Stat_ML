__author__ = "codingMonkey"
__project__ = "ChessML"


from dev2.tools import tools, read_json, read_pieces
import multiprocessing

from dev2 import BASE_DIR
from dev2.step4 import ALT_TRAIN_INPUT_FOLDER, ALT_TEST_INPUT_FOLDER



STAT_DATA_FOLDER = BASE_DIR + "/R_code/data/"
ALT_TRAIN = ALT_TRAIN_INPUT_FOLDER
ALT_TEST = ALT_TEST_INPUT_FOLDER

OUT_FOLDER = STAT_DATA_FOLDER +"0/"


def get_fie(file, new_file_path = OUT_FOLDER):



if __name__ == '__main__':
    get_fie("REF_final_0.json")
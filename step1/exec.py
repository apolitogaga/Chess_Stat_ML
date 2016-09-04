'''
This file executes the pgn_to_json file.
It inputs the pgn file, and the corresponding out file.
This process takes a lot of time due to interpreting the pgn steps into board positions for each game.
'''
import subprocess
import os

from dev2.step1 import OUTPUT_FOLDER
from dev2.step1 import OUTPUT_JSON_FOLDER
from dev2.step1.split_pgn import NAMES

for i in range(0,1000):
    # print i
    ifile = OUTPUT_FOLDER + NAMES + "_"+str(i)+".pgn"
    ofile =  OUTPUT_JSON_FOLDER + NAMES + "_"+str(i)+".json"
    arg1=" -i " + ifile
    arg2=" -o" + ofile
    cmd = "python pgn_to_json.py"
    status = subprocess.call( cmd+arg1+arg2, shell=True)
    # print cmd+arg1+arg2
    # status = os.system( cmd+arg1+arg2)
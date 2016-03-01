import subprocess
import os

OUTPUT=  "/Users/hectorapolorosalespulido/Documents/thesisDataFast/out/OUT"
DUMP=  "/Users/hectorapolorosalespulido/Documents/thesisDataFast/pgn/OUT"

for i in range(360,400):
    # print i
    ifile = DUMP +"_"+str(i)+".pgn"
    ofile =  OUTPUT+"_"+str(i)+".json"
    arg1=" -i " + ifile
    arg2=" -o" + ofile
    cmd = "python pgn_to_json.py"
    status = subprocess.call( cmd+arg1+arg2, shell=True)
    # print cmd+arg1+arg2
    # status = os.system( cmd+arg1+arg2)
from genericpath import isfile
from os.path import expanduser, join

from os import listdir

__author__ = "codingMonkey"
__project__ = "ChessML"


INPUT =  expanduser("~/Documents/thesisDataFast/out/")
PATH_OUTPUT= expanduser("~/Documents/thesisDataFast/csv/")

PAT_IN = "OUT"
PAT_OUT = "DATASET"

def getFilesFromFolder(infiles):
    onlyfiles = [f for f in listdir(infiles) if isfile(join(infiles, f))]
    if '.DS_Store' in onlyfiles:
        onlyfiles.__delitem__(onlyfiles.index('.DS_Store'))
    return onlyfiles

def getPatList(pat, ext, limit = 1000):
    return [pat +"_"+str(i)+ext for i in range(0,limit)]

def getNewFileToProcess(input_path, pattern, ext):
    infiles =  getFilesFromFolder(input_path)
    # l = getPatList(pattern,ext)
    for i in range(0,1000):
        f = pattern+"_"+str(i)+ext
        if f not in infiles:
            return i








def main():
    # var = getNewFileToProcess(INPUT, PAT_IN,".json")
    var2 = getNewFileToProcess(PATH_OUTPUT,PAT_OUT,'.csv')


if __name__ == '__main__':
    main()
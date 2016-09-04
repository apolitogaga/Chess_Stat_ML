from genericpath import isfile
from os.path import expanduser, join
from os import listdir

__author__ = "codingMonkey"
__project__ = "ChessML"

INPUT = expanduser("~/Documents/thesisDataFast/out/")
PATH_OUTPUT = expanduser("~/Documents/thesisDataFast/csv/")

PAT_IN = "OUT"
PAT_OUT = "DATASET"


def getFilesFromFolder(infiles):
    """

    :param infiles:
    :return:
    """
    only_files = [f for f in listdir(infiles) if isfile(join(infiles, f))]
    if '.DS_Store' in only_files:
        only_files.__delitem__(only_files.index('.DS_Store'))
    return only_files


def getPatList(pat, ext, limit=1000):
    """

    :param pat:
    :param ext:
    :param limit:
    :return:
    """
    return [pat + "_" + str(i) + ext for i in range(0, limit)]


def getFilesToProcess(out_path, pattern, extension):
    infiles = getFilesFromFolder(out_path)
    # l = getPatList(pattern,ext)
    l = []
    for i in range(0, 1000):
        f = pattern + "_" + str(i) + extension
        if f not in infiles:
            l.append(i)
    return l
    pass

def getNewFileToProcess(input_path, pattern, ext):
    """

    :rtype: int
    :param input_path: path of the input
    :param pattern: pattern of the file (before the number)
    :param ext:
    :return: int
    """
    infiles = getFilesFromFolder(input_path)
    # l = getPatList(pattern,ext)
    for i in range(0, 1000):
        f = pattern + "_" + str(i) + ext
        if f not in infiles:
            return i

def addict(dict, str):
    """
    Adds string to dictionary.
    :param dict:
    :param str:
    :return:
    """
    if str in dict:
        dict[str] += 1
    else:
        dict[str] = 1

def main():
    # var = getNewFileToProcess(INPUT, PAT_IN,".json")
    var2 = getNewFileToProcess(PATH_OUTPUT, PAT_OUT, '.csv')


if __name__ == '__main__':
    main()

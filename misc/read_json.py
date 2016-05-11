__author__ = "codingMonkey"
__project__ = "ChessML"


import json
from StringIO import StringIO
from pprint import pprint
from collections import defaultdict
# from nltk.metrics.distance import edit_distance

from os.path import isfile, join, expanduser
from os import listdir, linesep

TFILE = "../../data/test.json"
OUTPUT=  "/Users/hectorapolorosalespulido/Documents/thesisDataFast/out/OUT_20.json"
i=1
ofile =  OUTPUT+"_"+str(i)+".json"
infiles = "/Users/hectorapolorosalespulido/Documents/thesisDataFast/out/"
PATH_OUTPUT= expanduser("~/Documents/thesisDataFast/data/")


def getFilesFromFolder(infiles=infiles):
    onlyfiles = [f for f in listdir(infiles) if isfile(join(infiles, f))]
    if '.DS_Store' in onlyfiles:
        onlyfiles.__delitem__(onlyfiles.index('.DS_Store'))
    return onlyfiles


def addList(dict, list):
    for l in list:
        addit(dict, l)


def addit(dict, element):
    if element in dict:
        dict[element] +=1
    else:
        dict[element]=1

def addCompetitor(defDict, string):
    string = process_text(string)
    nameList = string.split()
    lastname = nameList[0]
    name = " ".join(nameList[1:])
    if lastname in defDict:
        addit(defDict[lastname],name)
    else:
        defDict[lastname] = {name:1}

def process_text(string):
    temp = string.replace(",","")
    temp = temp.replace(".","")
    return temp


def dict2Text(dic):
    """
    We sort and return the data in a text file.
    :rtype: str text
    """
    text=""
    sor = sorted(dic.items(), key=lambda x:x[len(x)-1],reverse=True)
    for key, value in sor:
        text += key.encode("utf8") + " " + str(value) + linesep
    return text




def saveFile(data, filename):
    '''
    Save the file
    :rtype: object
    
    '''
    f = open(PATH_OUTPUT+filename,"w")
    f.write(data)
    f.close()


'''
Interpret the json
'''
def get_data(file):
    network = []
    with open(file) as f:
        jsn = f.read().splitlines()
        for line in jsn:
            network.append(json.loads(line))
    return network

if __name__ == '__main__':
    print "RUNNING THE PARSER FILE"
    data= get_data(OUTPUT)[1]
    print data['fen']

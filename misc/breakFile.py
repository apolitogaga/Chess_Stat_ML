from threading import Thread
import time

import cProfile

import json
import chess.pgn
from StringIO import StringIO


class Tclass (Thread):
    def __init__(self, threadID, name, counter, data):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.data = data

    def write_json(self):
        fout = open(self.name, 'w') # Or where you want it
        count = 1
        pgn = StringIO(self.data)# pgn file wont read string only stringIO
        node = chess.pgn.read_game(pgn)
        while node != None:
            info = node.headers
            info["fen"] = []
            while node.variations:
                next_node = node.variation(0)
                info["fen"].append(node.board().fen())
                node = next_node
            info["fen"].append(node.board().fen())
            node = chess.pgn.read_game(pgn)
            json.dump(info, fout, encoding='utf-8')
            fout.write('\n')
            count += 1
            if(count % 10000 == 0):
                print(count)
                # json.dump(dump, fout, encoding='utf-8')

        # json.dump(dump, fout, encoding='utf-8')
        fout.close()

    def run(self):
        # print "Starting " + self.name
        # print_time(self.name, self.counter, 5)
        self.write_json()
        print "Exiting " + self.name



exitFlag = 0

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

GORGO_BASE = "/Users/hectorapolorosalespulido/Documents/thesisDataFast/gorgoBase.pgn"
GORGO_OUT = "/Users/hectorapolorosalespulido/Documents/thesisDataFast/gorgoBase3.json"
IFILE =  "../../data/test.pgn"
OFILE =  "../../data/test_pgn2.json"
BFILE =  "../../data/bigTest.pgn"

OUTPUT=  "/Users/hectorapolorosalespulido/Documents/thesisDataFast/out/OUT"
DUMP=  "/Users/hectorapolorosalespulido/Documents/thesisDataFast/pgn/OUT"

from collections import defaultdict


FOLDS=1000
INPUT = GORGO_BASE

def main():
    dump = defaultdict(lambda : list)

    with open(INPUT) as f:
        data = f.read().splitlines()
        # print data
    pivot =  len(data)/FOLDS
    pivList  = []
    textList = []
    threadList = []
    prev=0
    for i in range(1,FOLDS):
        p = i*pivot
        p=goToPGN_Start(data,p)+1
        pivList.append(p)
        textList.append('\n'.join(data[prev:p]))
        prev=p
    textList.append('\n'.join(data[p:]))

    # print len(textList)


    for i in range(0,len(textList)):
        name = DUMP +"_"+str(i)+".pgn"
        # th =  Tclass(i+1,name,i+1, textList[i])
        # th.start()
        # th.join()
        writePGN(textList[i],name)
        # threadList.append(th)

    test = textList[len(textList)-1]

def writePGN(data, name):
     fout = open(name, 'w')
     fout.write(data)
     fout.close()

def goToPGN_Start(data, i):
    # print data[i]
    if(len(data[i])<1):
        if not (data[i-1].startswith("[")):
            return i
    return goToPGN_Start(data, i-1)

def write_json(self):
        fout = open(self.name, 'w') # Or where you want it
        count = 1
        pgn = StringIO(self.data)# pgn file wont read string only stringIO
        node = chess.pgn.read_game(pgn)
        while node != None:
            info = node.headers
            info["fen"] = []
            while node.variations:
                next_node = node.variation(0)
                info["fen"].append(node.board().fen())
                node = next_node
            info["fen"].append(node.board().fen())
            node = chess.pgn.read_game(pgn)
            json.dump(info, fout, encoding='utf-8')
            fout.write('\n')
            count += 1
            if(count % 10000 == 0):
                print(count)
                # json.dump(dump, fout, encoding='utf-8')

        # json.dump(dump, fout, encoding='utf-8')
        fout.close()

if __name__ == '__main__':
    start = time.time()

    main()
    # cProfile.run('main()')

    end = time.time()
    print "\n\n\t\tTIME: " +str(end - start)

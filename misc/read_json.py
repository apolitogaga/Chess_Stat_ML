'''
Author: Hector Apolo Rosales Pulido
'''
import json
from StringIO import StringIO
from pprint import pprint
from collections import defaultdict

from os.path import isfile, join
from os import listdir




TFILE = "../../data/test.json"
OUTPUT=  "/Users/hectorapolorosalespulido/Documents/thesisDataFast/out/OUT"
i=1
ofile =  OUTPUT+"_"+str(i)+".json"
infiles = "/Users/hectorapolorosalespulido/Documents/thesisDataFast/out/"

def getFilesFromFolder():
    onlyfiles = [f for f in listdir(infiles) if isfile(join(infiles, f))]
    if '.DS_Store' in onlyfiles:
        onlyfiles.__delitem__(onlyfiles.index('.DS_Store'))
    if 'OUT_173.json' in onlyfiles:
        onlyfiles.__delitem__(onlyfiles.index('OUT_173.json'))
    return onlyfiles

properties = {}

competitors = set()

network = defaultdict(lambda: defaultdict(set()))
netwrk = defaultdict(lambda: set())


def addList(dict, list):
    for l in list:
        addit(dict, l)

def addit(dict, element):
    if element in dict:
        dict[element] +=1
    else:
        dict[element]=1

def addFrozet(dict, element):
    pass


def main():
    properties = {}
    count =1
    files =  getFilesFromFolder()
    for f in files[0:1]:
        print f
        path= infiles+f
        # print path
        with open(path) as f:
            jsn = f.read().splitlines()
            for line in jsn:
                count +=1
                data={}
                data = json.loads(line)
                addList(properties,data.keys())
                if "Black" in data:
                    competitors.add(data["Black"])
                if "White" in data:
                    competitors.add(data["White"])
    print properties
    print count

    print len(competitors)
    comp = list(competitors)
    for i in range(0,len(competitors),5):
        # print i
        # print comp[i],comp[i+1],comp[i+2],comp[i+3],comp[i+4]
        print "%s \t %s \t $s \t %s \t %s"%(str(comp[i]),str(comp[i+1]),str(comp[i+2]),str(comp[i+3]),str(comp[i+4]))
        # i+=5


'''
example:

{"Event": "1st HM Corus", "Site": "?", "Date": "2008.??.??", "Round": "?", "White": "Vlasenko, V.", "Black": "[=0503.10a6g1", "Result": "1/2-1/2", "EventDate": "2008.??.??", "SetUp": "1", "PlyCount": "13", "FEN": "1r6/1PR5/K7/6r1/8/5n2/8/6k1 w - - 0 1", "fen": ["1r6/1PR5/K7/6r1/8/5n2/8/6k1 w - - 0 1", "1r6/1P6/K7/6r1/8/5n2/8/2R3k1 b - - 1 1", "1r6/1P6/K7/6r1/8/5n2/6k1/2R5 w - - 2 2", "1r6/1P6/K7/6r1/8/5n2/2R3k1/8 b - - 3 2", "1r6/1P6/K7/6r1/8/5nk1/2R5/8 w - - 4 3", "1rR5/1P6/K7/6r1/8/5nk1/8/8 b - - 5 3", "1rR5/1P6/K7/4n1r1/8/6k1/8/8 w - - 6 4", "1R6/1P6/K7/4n1r1/8/6k1/8/8 b - - 0 4", "1R6/1P6/K7/6r1/2n5/6k1/8/8 w - - 1 5", "6R1/1P6/K7/6r1/2n5/6k1/8/8 b - - 2 5", "6r1/1P6/K7/8/2n5/6k1/8/8 w - - 0 6", "6r1/KP6/8/8/2n5/6k1/8/8 b - - 1 6", "6r1/KP6/8/n7/8/6k1/8/8 w - - 2 7", "1Q4r1/K7/8/n7/8/6k1/8/8 b - - 0 7"]}
{"Event": "12th HIT Open A", "Site": "Nova Gorica SLO", "Date": "2007.01.28", "Round": "4", "White": "Miezis, N", "Black": "Borisek, J", "Result": "1/2-1/2", "WhiteElo": "2517", "BlackElo": "2518", "ECO": "A20", "fen": ["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1", "rnbqkbnr/pppp1ppp/8/4p3/2P5/8/PP1PPPPP/RNBQKBNR w KQkq - 0 2", "rnbqkbnr/pppp1ppp/8/4p3/2P5/6P1/PP1PPP1P/RNBQKBNR b KQkq - 0 2", "rnbqkbnr/pp1p1ppp/2p5/4p3/2P5/6P1/PP1PPP1P/RNBQKBNR w KQkq - 0 3", "rnbqkbnr/pp1p1ppp/2p5/4p3/2PP4/6P1/PP2PP1P/RNBQKBNR b KQkq - 0 3", "rnbqk1nr/pp1p1ppp/2p5/4p3/1bPP4/6P1/PP2PP1P/RNBQKBNR w KQkq - 1 4", "rnbqk1nr/pp1p1ppp/2p5/4p3/1bPP4/6P1/PP1BPP1P/RN1QKBNR b KQkq - 2 4", "rnbqk1nr/pp1p1ppp/2p5/4p3/2PP4/6P1/PP1bPP1P/RN1QKBNR w KQkq - 0 5", "rnbqk1nr/pp1p1ppp/2p5/4p3/2PP4/6P1/PP1QPP1P/RN2KBNR b KQkq - 0 5", "rnbqk1nr/pp3ppp/2pp4/4p3/2PP4/6P1/PP1QPP1P/RN2KBNR w KQkq - 0 6", "rnbqk1nr/pp3ppp/2pp4/4p3/2PP4/2N3P1/PP1QPP1P/R3KBNR b KQkq - 1 6", "rnbqk2r/pp3ppp/2pp1n2/4p3/2PP4/2N3P1/PP1QPP1P/R3KBNR w KQkq - 2 7", "rnbqk2r/pp3ppp/2pp1n2/4p3/2PP4/2N3P1/PP1QPP1P/3RKBNR b Kkq - 3 7", "rnb1k2r/pp2qppp/2pp1n2/4p3/2PP4/2N3P1/PP1QPP1P/3RKBNR w Kkq - 4 8", "rnb1k2r/pp2qppp/2pp1n2/4p3/2PP4/2N3P1/PP1QPPBP/3RK1NR b Kkq - 5 8", "rnb2rk1/pp2qppp/2pp1n2/4p3/2PP4/2N3P1/PP1QPPBP/3RK1NR w K - 6 9", "rnb2rk1/pp2qppp/2pp1n2/4p3/2PP4/2N2NP1/PP1QPPBP/3RK2R b K - 7 9", "rnb2rk1/pp2qppp/2pp1n2/8/2PPp3/2N2NP1/PP1QPPBP/3RK2R w K - 0 10", "rnb2rk1/pp2qppp/2pp1n2/8/2PPp3/2N1QNP1/PP2PPBP/3RK2R b K - 1 10", "rnb1r1k1/pp2qppp/2pp1n2/8/2PPp3/2N1QNP1/PP2PPBP/3RK2R w K - 2 11", "rnb1r1k1/pp2qppp/2pp1n2/8/2PPp3/2N1Q1P1/PP1NPPBP/3RK2R b K - 3 11", "rnb1r1k1/pp2qppp/2p2n2/3p4/2PPp3/2N1Q1P1/PP1NPPBP/3RK2R w K - 0 12", "rnb1r1k1/pp2qppp/2p2n2/3p4/2PPp3/2N1Q1PP/PP1NPPB1/3RK2R b K - 0 12", "rn2r1k1/pp2qppp/2p1bn2/3p4/2PPp3/2N1Q1PP/PP1NPPB1/3RK2R w K - 1 13", "rn2r1k1/pp2qppp/2p1bn2/3p4/2PPp1P1/2N1Q2P/PP1NPPB1/3RK2R b K - 0 13", "r3r1k1/pp1nqppp/2p1bn2/3p4/2PPp1P1/2N1Q2P/PP1NPPB1/3RK2R w K - 1 14", "r3r1k1/pp1nqppp/2p1bn2/3P4/3Pp1P1/2N1Q2P/PP1NPPB1/3RK2R b K - 0 14", "r3r1k1/pp1nqppp/4bn2/3p4/3Pp1P1/2N1Q2P/PP1NPPB1/3RK2R w K - 0 15", "r3r1k1/pp1nqppp/4bn2/3p4/3Pp1P1/2N1Q2P/PP2PPB1/3RKN1R b K - 1 15", "r3r1k1/pp2qppp/1n2bn2/3p4/3Pp1P1/2N1Q2P/PP2PPB1/3RKN1R w K - 2 16", "r3r1k1/pp2qppp/1n2bn2/3p4/3Pp1P1/1PN1Q2P/P3PPB1/3RKN1R b K - 0 16", "2r1r1k1/pp2qppp/1n2bn2/3p4/3Pp1P1/1PN1Q2P/P3PPB1/3RKN1R w K - 1 17", "2r1r1k1/pp2qppp/1n2bn2/3p4/3Pp1P1/1PN4P/P2QPPB1/3RKN1R b K - 2 17", "2r1r1k1/pp2qpp1/1n2bn2/3p3p/3Pp1P1/1PN4P/P2QPPB1/3RKN1R w K - 0 18", "2r1r1k1/pp2qpp1/1n2bn2/3p3p/3Pp1P1/1PN4P/P2QPPB1/2R1KN1R b K - 1 18", "2r1r1k1/pp2qpp1/1n2bn2/3p4/3Pp1p1/1PN4P/P2QPPB1/2R1KN1R w K - 0 19", "2r1r1k1/pp2qpp1/1n2bn2/3p4/3Pp1p1/1PN1N2P/P2QPPB1/2R1K2R b K - 1 19", "2r1r1k1/pp2qpp1/1n2bn2/3p4/3Pp3/1PN1N2p/P2QPPB1/2R1K2R w K - 0 20", "2r1r1k1/pp2qpp1/1n2bn2/3p4/3Pp3/1PN1N2B/P2QPP2/2R1K2R b K - 0 20", "4r1k1/pp2qpp1/1nr1bn2/3p4/3Pp3/1PN1N2B/P2QPP2/2R1K2R w K - 1 21", "4r1k1/pp2qpp1/1nr1bn2/3p4/3Pp3/1P2N2B/P2QPP2/2RNK2R b K - 2 21", "4r1k1/pp2qpp1/1n2bn2/3p4/3Pp3/1P2N2B/P2QPP2/2rNK2R w K - 0 22", "4r1k1/pp2qpp1/1n2bn2/3p4/3Pp3/1P2N2B/P3PP2/2QNK2R b K - 0 22", "4r1k1/pp3pp1/1n2bn2/3p4/1q1Pp3/1P2N2B/P3PP2/2QNK2R w K - 1 23", "4r1k1/pp3pp1/1n2bn2/3p4/1q1Pp3/1PQ1N2B/P3PP2/3NK2R b K - 2 23", "4r1k1/pp3pp1/1n2bn2/3p4/3Pp3/1Pq1N2B/P3PP2/3NK2R w K - 0 24", "4r1k1/pp3pp1/1n2bn2/3p4/3Pp3/1PN1N2B/P3PP2/4K2R b K - 0 24", "4r1k1/1p3pp1/pn2bn2/3p4/3Pp3/1PN1N2B/P3PP2/4K2R w K - 0 25", "4r1k1/1p3pp1/pn2bn2/3p4/3Pp3/1PN1N2B/P2KPP2/7R b - - 1 25", "4rk2/1p3pp1/pn2bn2/3p4/3Pp3/1PN1N2B/P2KPP2/7R w - - 2 26", "4rk2/1p3pp1/pn2Bn2/3p4/3Pp3/1PN1N3/P2KPP2/7R b - - 0 26", "4rk2/1p4p1/pn2pn2/3p4/3Pp3/1PN1N3/P2KPP2/7R w - - 0 27", "4rk1R/1p4p1/pn2pn2/3p4/3Pp3/1PN1N3/P2KPP2/8 b - - 1 27", "4r2R/1p3kp1/pn2pn2/3p4/3Pp3/1PN1N3/P2KPP2/8 w - - 2 28", "4r3/1p3kp1/pn2pn2/3p4/3Pp3/1PN1N3/P2KPP2/7R b - - 3 28", "4r3/1p1n1kp1/p3pn2/3p4/3Pp3/1PN1N3/P2KPP2/7R w - - 4 29", "4r3/1p1n1kp1/p3pn2/3p4/3Pp3/1PN5/P1NKPP2/7R b - - 5 29", "2r5/1p1n1kp1/p3pn2/3p4/3Pp3/1PN5/P1NKPP2/7R w - - 6 30", "2r5/1p1n1kp1/p3pn2/3p4/3Pp3/1PN2P2/P1NKP3/7R b - - 0 30", "2r5/1p1n1kp1/p3pn2/3p4/3P4/1PN2p2/P1NKP3/7R w - - 0 31", "2r5/1p1n1kp1/p3pn2/3p4/3P4/1PN2P2/P1NK4/7R b - - 0 31", "1nr5/1p3kp1/p3pn2/3p4/3P4/1PN2P2/P1NK4/7R w - - 1 32", "1nr5/1p3kp1/p3pn2/3p4/3P4/1P3P2/P1NKN3/7R b - - 2 32", "2r5/1p3kp1/p1n1pn2/3p4/3P4/1P3P2/P1NKN3/7R w - - 3 33", "2r5/1p3kp1/p1n1pn2/3p4/3P1N2/1P3P2/P1NK4/7R b - - 4 33", "2r5/1p3kp1/p1n2n2/3pp3/3P1N2/1P3P2/P1NK4/7R w - - 0 34", "2r5/1p3kp1/p1n2n2/3pP3/5N2/1P3P2/P1NK4/7R b - - 0 34", "2r5/1p3kp1/p4n2/3pn3/5N2/1P3P2/P1NK4/7R w - - 0 35", "2r5/1p3kp1/p4n2/3pn3/3N1N2/1P3P2/P2K4/7R b - - 1 35", "2r5/1p3k2/p4n2/3pn1p1/3N1N2/1P3P2/P2K4/7R w - - 0 36", "2r5/1p3k2/p4n2/3pn1p1/3N4/1P1N1P2/P2K4/7R b - - 1 36", "2r5/1p3k2/p4n2/3p2p1/3N4/1P1n1P2/P2K4/7R w - - 0 37", "2r5/1p3k2/p4n2/3p2p1/3N4/1P1K1P2/P7/7R b - - 0 37", "2r5/1p6/p4nk1/3p2p1/3N4/1P1K1P2/P7/7R w - - 1 38", "2r5/1p6/p4nk1/3p2p1/3N4/1P1K1P2/P7/6R1 b - - 2 38", "4r3/1p6/p4nk1/3p2p1/3N4/1P1K1P2/P7/6R1 w - - 3 39", "4r3/1p6/p4nk1/3p2p1/8/1P1K1P2/P3N3/6R1 b - - 4 39", "7r/1p6/p4nk1/3p2p1/8/1P1K1P2/P3N3/6R1 w - - 5 40", "7r/1p6/p4nk1/3p2p1/8/1P2KP2/P3N3/6R1 b - - 6 40", "8/1p6/p4nk1/3p2p1/8/1P2KP2/P3N2r/6R1 w - - 7 41", "8/1p6/p4nk1/3p2p1/P7/1P2KP2/4N2r/6R1 b - - 0 41", "8/1p6/p4nk1/3p2p1/P6r/1P2KP2/4N3/6R1 w - - 1 42", "8/1p6/p4nk1/3p2p1/P2N3r/1P2KP2/8/6R1 b - - 2 42", "8/1p6/p4nk1/3p2p1/P2N4/1P2KP2/7r/6R1 w - - 3 43", "8/1p6/p4nk1/3p2p1/P7/1P2KP2/4N2r/6R1 b - - 4 43", "8/1p6/p4n1k/3p2p1/P7/1P2KP2/4N2r/6R1 w - - 5 44", "8/1p6/p4n1k/P2p2p1/8/1P2KP2/4N2r/6R1 b - - 0 44", "8/1p6/p4n1k/P2p2p1/8/1P2KP1r/4N3/6R1 w - - 1 45", "8/1p6/p4n1k/P2p2p1/8/1P2KPRr/4N3/8 b - - 2 45", "8/1p6/p4n1k/P2p2p1/8/1P2KPR1/4N3/7r w - - 3 46", "8/1p6/p4n1k/P2p2p1/8/1P2KP2/4N3/6Rr b - - 4 46", "8/1p6/p4n1k/P2p2p1/8/1P2KP2/4N3/6r1 w - - 0 47", "8/1p6/p4n1k/P2p2p1/8/1P2KP2/8/6N1 b - - 0 47", "8/1p6/p4nk1/P2p2p1/8/1P2KP2/8/6N1 w - - 1 48", "8/1p6/p4nk1/P2p2p1/3K4/1P3P2/8/6N1 b - - 2 48", "8/1p3k2/p4n2/P2p2p1/3K4/1P3P2/8/6N1 w - - 3 49", "8/1p3k2/p4n2/P2p2p1/3K4/1P3P2/4N3/8 b - - 4 49", "8/1p6/p3kn2/P2p2p1/3K4/1P3P2/4N3/8 w - - 5 50", "8/1p6/p3kn2/P2p2p1/3K4/1P3P2/8/6N1 b - - 6 50", "8/1p6/p2k1n2/P2p2p1/3K4/1P3P2/8/6N1 w - - 7 51", "8/1p6/p2k1n2/P2p2p1/3K4/1P3P1N/8/8 b - - 8 51", "8/1p5n/p2k4/P2p2p1/3K4/1P3P1N/8/8 w - - 9 52", "8/1p5n/p2k4/P2p2p1/1P1K4/5P1N/8/8 b - - 0 52", "8/1p5n/p1k5/P2p2p1/1P1K4/5P1N/8/8 w - - 1 53", "8/1p5n/p1k5/P2p2p1/1P1K4/5P2/5N2/8 b - - 2 53", "5n2/1p6/p1k5/P2p2p1/1P1K4/5P2/5N2/8 w - - 3 54", "5n2/1p6/p1k5/P2p2p1/1P1K4/5P1N/8/8 b - - 4 54", "5n2/1p6/p7/Pk1p2p1/1P1K4/5P1N/8/8 w - - 5 55", "5n2/1p6/p7/Pk1p2N1/1P1K4/5P2/8/8 b - - 0 55", "5n2/1p6/p7/P2p2N1/1k1K4/5P2/8/8 w - - 0 56", "5n2/1p6/p7/P2K2N1/1k6/5P2/8/8 b - - 0 56", "5n2/1p6/p7/k2K2N1/8/5P2/8/8 w - - 0 57", "5n2/1p6/p7/k2K2N1/5P2/8/8/8 b - - 0 57", "5n2/1p6/p7/3K2N1/1k3P2/8/8/8 w - - 1 58", "5n2/1p6/p7/3K1PN1/1k6/8/8/8 b - - 0 58", "5n2/1p6/8/p2K1PN1/1k6/8/8/8 w - - 0 59", "5n2/1p6/5P2/p2K2N1/1k6/8/8/8 b - - 0 59", "5n2/1p6/5P2/3K2N1/pk6/8/8/8 w - - 0 60", "5n2/1p6/4NP2/3K4/pk6/8/8/8 b - - 1 60", "8/1p5n/4NP2/3K4/pk6/8/8/8 w - - 2 61", "8/1p3P1n/4N3/3K4/pk6/8/8/8 b - - 0 61", "8/1p3P1n/4N3/3K4/1k6/p7/8/8 w - - 0 62", "8/1p3P1n/8/3K2N1/1k6/p7/8/8 b - - 1 62", "5n2/1p3P2/8/3K2N1/1k6/p7/8/8 w - - 2 63", "5n2/1p3P2/4N3/3K4/1k6/p7/8/8 b - - 3 63", "8/1p3P2/4N1n1/3K4/1k6/p7/8/8 w - - 4 64", "8/1p3P2/4N1n1/8/1k2K3/p7/8/8 b - - 5 64", "8/1p3P2/4N1n1/8/1k2K3/8/p7/8 w - - 0 65", "8/1p3P2/4N1n1/5K2/1k6/8/p7/8 b - - 1 65", "8/1p3P2/4N1n1/5K2/1k6/8/8/q7 w - - 0 66", "8/1p3P2/4N1K1/8/1k6/8/8/q7 b - - 0 66", "8/1p3P2/4N1K1/8/1k6/8/8/6q1 w - - 1 67", "8/1p3P2/4NK2/8/1k6/8/8/6q1 b - - 2 67", "8/1p3P2/4NK2/8/1k6/8/8/5q2 w - - 3 68", "8/1p2KP2/4N3/8/1k6/8/8/5q2 b - - 4 68", "8/1p2KP2/4N3/8/2k5/8/8/5q2 w - - 5 69", "5Q2/1p2K3/4N3/8/2k5/8/8/5q2 b - - 0 69", "5q2/1p2K3/4N3/8/2k5/8/8/8 w - - 0 70", "5N2/1p2K3/8/8/2k5/8/8/8 b - - 0 70", "5N2/4K3/8/1p6/2k5/8/8/8 w - - 0 71", "8/3NK3/8/1p6/2k5/8/8/8 b - - 1 71", "8/3NK3/8/8/1pk5/8/8/8 w - - 0 72", "8/4K3/1N6/8/1pk5/8/8/8 b - - 1 72", "8/4K3/1N6/1k6/1p6/8/8/8 w - - 2 73", "8/4K3/8/1k1N4/1p6/8/8/8 b - - 3 73", "8/4K3/8/1k1N4/8/1p6/8/8 w - - 0 74", "8/4K3/8/1k6/8/1pN5/8/8 b - - 1 74", "8/4K3/8/8/2k5/1pN5/8/8 w - - 2 75", "8/4K3/8/8/N1k5/1p6/8/8 b - - 3 75"]}
{"Event": "20th North Sea Cup", "Site": "Esbjerg DEN", "Date": "2005.07.08", "Round": "8", "White": "Pedersen, Peter Brondt", "Black": "Pedersen, JaR", "Result": "1/2-1/2", "BlackElo": "2239", "ECO": "A22", "fen": ["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1", "rnbqkbnr/pppp1ppp/8/4p3/2P5/8/PP1PPPPP/RNBQKBNR w KQkq - 0 2", "rnbqkbnr/pppp1ppp/8/4p3/2P5/6P1/PP1PPP1P/RNBQKBNR b KQkq - 0 2", "rnbqkb1r/pppp1ppp/5n2/4p3/2P5/6P1/PP1PPP1P/RNBQKBNR w KQkq - 1 3", "rnbqkb1r/pppp1ppp/5n2/4p3/2P5/6P1/PP1PPPBP/RNBQK1NR b KQkq - 2 3", "rnbqkb1r/ppp2ppp/5n2/3pp3/2P5/6P1/PP1PPPBP/RNBQK1NR w KQkq - 0 4", "rnbqkb1r/ppp2ppp/5n2/3Pp3/8/6P1/PP1PPPBP/RNBQK1NR b KQkq - 0 4", "rnbqkb1r/ppp2ppp/8/3np3/8/6P1/PP1PPPBP/RNBQK1NR w KQkq - 0 5", "rnbqkb1r/ppp2ppp/8/3np3/8/2N3P1/PP1PPPBP/R1BQK1NR b KQkq - 1 5", "rnbqkb1r/ppp2ppp/8/4p3/8/2n3P1/PP1PPPBP/R1BQK1NR w KQkq - 0 6", "rnbqkb1r/ppp2ppp/8/4p3/8/2P3P1/P2PPPBP/R1BQK1NR b KQkq - 0 6", "r1bqkb1r/ppp2ppp/2n5/4p3/8/2P3P1/P2PPPBP/R1BQK1NR w KQkq - 1 7", "r1bqkb1r/ppp2ppp/2n5/4p3/8/2PP2P1/P3PPBP/R1BQK1NR b KQkq - 0 7", "r1b1kb1r/ppp2ppp/2n2q2/4p3/8/2PP2P1/P3PPBP/R1BQK1NR w KQkq - 1 8", "r1b1kb1r/ppp2ppp/2n2q2/4p3/8/2PP2P1/PB2PPBP/R2QK1NR b KQkq - 2 8", "r1b1k2r/ppp2ppp/2n2q2/2b1p3/8/2PP2P1/PB2PPBP/R2QK1NR w KQkq - 3 9", "r1b1k2r/ppp2ppp/2n2q2/2b1p3/8/2PP1NP1/PB2PPBP/R2QK2R b KQkq - 4 9", "r1b2rk1/ppp2ppp/2n2q2/2b1p3/8/2PP1NP1/PB2PPBP/R2QK2R w KQ - 5 10", "r1b2rk1/ppp2ppp/2n2q2/2b1p3/8/2PP1NP1/PB2PPBP/R2Q1RK1 b - - 6 10", "r4rk1/ppp2ppp/2n2q2/2b1p3/6b1/2PP1NP1/PB2PPBP/R2Q1RK1 w - - 7 11", "r4rk1/ppp2ppp/2n2q2/2b1p3/Q5b1/2PP1NP1/PB2PPBP/R4RK1 b - - 8 11", "r4rk1/pppb1ppp/2n2q2/2b1p3/Q7/2PP1NP1/PB2PPBP/R4RK1 w - - 9 12", "r4rk1/pppb1ppp/2n2q2/2b1p3/Q7/2PP2P1/PB1NPPBP/R4RK1 b - - 10 12", "r4rk1/pppb1ppp/2n4q/2b1p3/Q7/2PP2P1/PB1NPPBP/R4RK1 w - - 11 13", "r4rk1/pppb1ppp/2n4q/2b1p3/Q3N3/2PP2P1/PB2PPBP/R4RK1 b - - 12 13", "r4rk1/pppb1ppp/1bn4q/4p3/Q3N3/2PP2P1/PB2PPBP/R4RK1 w - - 13 14", "r4rk1/pppb1ppp/1bn4q/4p3/Q3N3/B1PP2P1/P3PPBP/R4RK1 b - - 14 14", "r3r1k1/pppb1ppp/1bn4q/4p3/Q3N3/B1PP2P1/P3PPBP/R4RK1 w - - 15 15", "r3r1k1/pppb1ppp/1bn4q/4p3/4N3/B1PP2P1/P1Q1PPBP/R4RK1 b - - 16 15", "r3r1k1/ppp2ppp/1bn4q/4p3/4N3/B1PP2Pb/P1Q1PPBP/R4RK1 w - - 17 16", "r3r1k1/ppp2ppp/1bn4q/4p3/4N3/B1PP2Pb/P3PPBP/R1Q2RK1 b - - 18 16", "r3r1k1/ppp2ppp/1bn5/4p2q/4N3/B1PP2Pb/P3PPBP/R1Q2RK1 w - - 19 17", "r3r1k1/ppp2ppp/1bn5/4p1Qq/4N3/B1PP2Pb/P3PPBP/R4RK1 b - - 20 17", "r3r1k1/ppp2ppp/1bn5/4p1q1/4N3/B1PP2Pb/P3PPBP/R4RK1 w - - 0 18", "r3r1k1/ppp2ppp/1bn5/4p1N1/8/B1PP2Pb/P3PPBP/R4RK1 b - - 0 18", "r3r1k1/ppp2ppp/1bn5/4p1N1/8/B1PP2P1/P3PPbP/R4RK1 w - - 0 19", "r3r1k1/ppp2ppp/1bn5/4p1N1/8/B1PP2P1/P3PPKP/R4R2 b - - 0 19", "r3r1k1/ppp3pp/1bn5/4ppN1/8/B1PP2P1/P3PPKP/R4R2 w - - 0 20", "r3r1k1/ppp3pp/1bn5/4ppN1/8/B1PP2P1/P3PPKP/1R3R2 b - - 1 20", "r3r1k1/ppp3p1/1bn4p/4ppN1/8/B1PP2P1/P3PPKP/1R3R2 w - - 0 21", "r3r1k1/ppp3p1/1bn4p/4pp2/8/B1PP1NP1/P3PPKP/1R3R2 b - - 1 21", "r3r1k1/ppp3p1/1bn4p/5p2/4p3/B1PP1NP1/P3PPKP/1R3R2 w - - 0 22", "r3r1k1/ppp3p1/1bn4p/5p2/4p2N/B1PP2P1/P3PPKP/1R3R2 b - - 1 22", "r5k1/ppp3p1/1bn4p/4rp2/4p2N/B1PP2P1/P3PPKP/1R3R2 w - - 2 23", "r5k1/ppp3p1/1bn3Np/4rp2/4p3/B1PP2P1/P3PPKP/1R3R2 b - - 3 23", "r5k1/ppp3p1/1bn3Np/r4p2/4p3/B1PP2P1/P3PPKP/1R3R2 w - - 4 24", "r5k1/ppp3p1/1bn3Np/r4p2/4p3/BRPP2P1/P3PPKP/5R2 b - - 5 24", "r7/ppp2kp1/1bn3Np/r4p2/4p3/BRPP2P1/P3PPKP/5R2 w - - 6 25", "r7/ppp2kp1/1bn4p/r4p2/4pN2/BRPP2P1/P3PPKP/5R2 b - - 7 25", "r7/ppp2k2/1bn4p/r4pp1/4pN2/BRPP2P1/P3PPKP/5R2 w - - 0 26", "r7/ppp2k2/1bn4p/r4pp1/4p3/BRPP2PN/P3PPKP/5R2 b - - 1 26", "r7/ppp2k2/1bn4p/r4pp1/8/BRPp2PN/P3PPKP/5R2 w - - 0 27", "r7/ppp2k2/1bn4p/r4pp1/8/BRPP2PN/P4PKP/5R2 b - - 0 27", "4r3/ppp2k2/1bn4p/r4pp1/8/BRPP2PN/P4PKP/5R2 w - - 1 28", "4r3/ppp2k2/1bn4p/r4pp1/8/BRPP2P1/P4PKP/5RN1 b - - 2 28", "4r3/ppp2k2/1b5p/r3npp1/8/BRPP2P1/P4PKP/5RN1 w - - 3 29", "4r3/ppp2k2/1b5p/r3npp1/2P5/BR1P2P1/P4PKP/5RN1 b - - 0 29", "4r3/pppn1k2/1b5p/r4pp1/2P5/BR1P2P1/P4PKP/5RN1 w - - 1 30", "4r3/pppn1k2/1b5p/r4pp1/2P5/BR1P2P1/P4PKP/3R2N1 b - - 2 30", "3r4/pppn1k2/1b5p/r4pp1/2P5/BR1P2P1/P4PKP/3R2N1 w - - 3 31", "3r4/pppn1k2/1b5p/r4pp1/2PP4/BR4P1/P4PKP/3R2N1 b - - 0 31", "3r4/pppn1k2/1b5p/5pp1/r1PP4/BR4P1/P4PKP/3R2N1 w - - 1 32", "3r4/pppn1k2/1b5p/2P2pp1/r2P4/BR4P1/P4PKP/3R2N1 b - - 0 32", "3r4/ppp2k2/1b5p/2n2pp1/r2P4/BR4P1/P4PKP/3R2N1 w - - 0 33", "3r4/ppp2k2/1b5p/2B2pp1/r2P4/1R4P1/P4PKP/3R2N1 b - - 0 33", "3r4/ppp2k2/7p/2b2pp1/r2P4/1R4P1/P4PKP/3R2N1 w - - 0 34", "3r4/pRp2k2/7p/2b2pp1/r2P4/6P1/P4PKP/3R2N1 b - - 0 34", "3r4/pRp2k2/1b5p/5pp1/r2P4/6P1/P4PKP/3R2N1 w - - 1 35", "3r4/pRp2k2/1b5p/5pp1/r2P4/5NP1/P4PKP/3R4 b - - 2 35", "3r4/pRp2k2/1b5p/5pp1/3P4/5NP1/r4PKP/3R4 w - - 0 36", "3r4/pRp2k2/1b5p/4Npp1/3P4/6P1/r4PKP/3R4 b - - 1 36", "3r4/pRp5/1b3k1p/4Npp1/3P4/6P1/r4PKP/3R4 w - - 2 37", "3r4/pRp5/1bN2k1p/5pp1/3P4/6P1/r4PKP/3R4 b - - 3 37", "8/pRp5/1bNr1k1p/5pp1/3P4/6P1/r4PKP/3R4 w - - 4 38", "8/pRp5/1bNr1k1p/5pp1/3P4/6P1/r4PKP/2R5 b - - 5 38", "8/pRp5/1bN1rk1p/5pp1/3P4/6P1/r4PKP/2R5 w - - 6 39", "1R6/p1p5/1bN1rk1p/5pp1/3P4/6P1/r4PKP/2R5 b - - 7 39", "1R6/p1p5/1bN2k1p/5pp1/3P4/6P1/r3rPKP/2R5 w - - 8 40", "1R6/p1p5/1bN2k1p/5pp1/3P4/6P1/r3rPKP/5R2 b - - 9 40", "1R6/p1p5/1bN2k1p/5pp1/3P4/6P1/2r1rPKP/5R2 w - - 10 41", "1R6/p1p5/1b3k1p/5pp1/1N1P4/6P1/2r1rPKP/5R2 b - - 11 41", "1R6/p1p5/1b3k1p/5pp1/1NrP4/6P1/4rPKP/5R2 w - - 12 42", "1R6/p1p5/1b3k1p/3N1pp1/2rP4/6P1/4rPKP/5R2 b - - 13 42", "1R6/p1p3k1/1b5p/3N1pp1/2rP4/6P1/4rPKP/5R2 w - - 14 43", "1R6/p1p3k1/1N5p/5pp1/2rP4/6P1/4rPKP/5R2 b - - 0 43", "1R6/2p3k1/1p5p/5pp1/2rP4/6P1/4rPKP/5R2 w - - 0 44", "3R4/2p3k1/1p5p/5pp1/2rP4/6P1/4rPKP/5R2 b - - 1 44", "3R4/2p3k1/1p5p/5pp1/3P4/6P1/2r1rPKP/5R2 w - - 2 45", "3R4/2p3k1/1p5p/5pp1/3P4/6PP/2r1rPK1/5R2 b - - 0 45", "3R4/2p3k1/1p5p/5pp1/3P4/6PP/2rr1PK1/5R2 w - - 1 46", "3R4/2p3k1/1p5p/5pp1/3P2P1/7P/2rr1PK1/5R2 b - - 0 46", "3R4/2p3k1/1p5p/6p1/3P2p1/7P/2rr1PK1/5R2 w - - 0 47", "3R4/2p3k1/1p5p/6p1/3P2P1/8/2rr1PK1/5R2 b - - 0 47", "3R4/2p3k1/1p5p/6p1/2rP2P1/8/3r1PK1/5R2 w - - 1 48", "8/2pR2k1/1p5p/6p1/2rP2P1/8/3r1PK1/5R2 b - - 2 48", "8/2pR4/1p3k1p/6p1/2rP2P1/8/3r1PK1/5R2 w - - 3 49", "8/2pR4/1p3k1p/6p1/2rP2P1/8/3r1PK1/7R b - - 4 49", "8/2pR4/1p3k1p/6p1/3r2P1/8/3r1PK1/7R w - - 0 50", "8/2pR4/1p3k1R/6p1/3r2P1/8/3r1PK1/8 b - - 0 50", "8/2pR4/1p5R/4k1p1/3r2P1/8/3r1PK1/8 w - - 1 51", "8/2p1R3/1p5R/4k1p1/3r2P1/8/3r1PK1/8 b - - 2 51", "8/2p1R3/1p5R/6p1/3r1kP1/8/3r1PK1/8 w - - 3 52", "8/2R5/1p5R/6p1/3r1kP1/8/3r1PK1/8 b - - 0 52", "8/2R5/1p5R/6p1/3r2k1/8/3r1PK1/8 w - - 0 53", "8/2R5/1p3R2/6p1/3r2k1/8/3r1PK1/8 b - - 1 53", "8/2R5/1p3R2/6p1/5rk1/8/3r1PK1/8 w - - 2 54", "8/2R5/1p6/6p1/5Rk1/8/3r1PK1/8 b - - 0 54", "8/2R5/1p6/6p1/5k2/8/3r1PK1/8 w - - 0 55", "8/5R2/1p6/6p1/5k2/8/3r1PK1/8 b - - 1 55", "8/5R2/1p6/4k1p1/8/8/3r1PK1/8 w - - 2 56", "8/6R1/1p6/4k1p1/8/8/3r1PK1/8 b - - 3 56", "8/6R1/1p3k2/6p1/8/8/3r1PK1/8 w - - 4 57", "8/1R6/1p3k2/6p1/8/8/3r1PK1/8 b - - 5 57", "8/1R6/1p1r1k2/6p1/8/8/5PK1/8 w - - 6 58", "8/1R6/1p1r1k2/6p1/8/6K1/5P2/8 b - - 7 58", "8/1R6/1p1r4/5kp1/8/6K1/5P2/8 w - - 8 59", "8/5R2/1p1r4/5kp1/8/6K1/5P2/8 b - - 9 59", "8/5R2/1p3r2/5kp1/8/6K1/5P2/8 w - - 10 60", "8/1R6/1p3r2/5kp1/8/6K1/5P2/8 b - - 11 60", "8/1R6/1pr5/5kp1/8/6K1/5P2/8 w - - 12 61", "8/5R2/1pr5/5kp1/8/6K1/5P2/8 b - - 13 61", "8/5R2/1pr3k1/6p1/8/6K1/5P2/8 w - - 14 62", "8/1R6/1pr3k1/6p1/8/6K1/5P2/8 b - - 15 62", "8/1R6/1p4k1/6p1/8/2r3K1/5P2/8 w - - 16 63", "8/1R6/1p4k1/6p1/6K1/2r5/5P2/8 b - - 17 63", "8/1R6/1p4k1/6p1/2r3K1/8/5P2/8 w - - 18 64", "8/1R6/1p4k1/6p1/2r5/6K1/5P2/8 b - - 19 64", "8/1R6/1p4k1/6p1/1r6/6K1/5P2/8 w - - 20 65", "1R6/8/1p4k1/6p1/1r6/6K1/5P2/8 b - - 21 65", "1R6/8/1p6/5kp1/1r6/6K1/5P2/8 w - - 22 66", "5R2/8/1p6/5kp1/1r6/6K1/5P2/8 b - - 23 66", "5R2/8/1p2k3/6p1/1r6/6K1/5P2/8 w - - 24 67", "6R1/8/1p2k3/6p1/1r6/6K1/5P2/8 b - - 25 67", "6R1/8/1p3k2/6p1/1r6/6K1/5P2/8 w - - 26 68", "5R2/8/1p3k2/6p1/1r6/6K1/5P2/8 b - - 27 68", "5R2/6k1/1p6/6p1/1r6/6K1/5P2/8 w - - 28 69", "1R6/6k1/1p6/6p1/1r6/6K1/5P2/8 b - - 29 69", "1R6/6k1/8/1p4p1/1r6/6K1/5P2/8 w - - 0 70", "8/6k1/1R6/1p4p1/1r6/6K1/5P2/8 b - - 1 70", "8/5k2/1R6/1p4p1/1r6/6K1/5P2/8 w - - 2 71", "8/5k2/1R6/1p4p1/1r6/5PK1/8/8 b - - 0 71", "8/6k1/1R6/1p4p1/1r6/5PK1/8/8 w - - 1 72", "1R6/6k1/8/1p4p1/1r6/5PK1/8/8 b - - 2 72", "1R6/8/7k/1p4p1/1r6/5PK1/8/8 w - - 3 73", "7R/8/7k/1p4p1/1r6/5PK1/8/8 b - - 4 73", "7R/6k1/8/1p4p1/1r6/5PK1/8/8 w - - 5 74", "1R6/6k1/8/1p4p1/1r6/5PK1/8/8 b - - 6 74", "1R6/8/6k1/1p4p1/1r6/5PK1/8/8 w - - 7 75", "6R1/8/6k1/1p4p1/1r6/5PK1/8/8 b - - 8 75"]}

'''
'''
 results:
{u'BlackTitle': 17, u'BlackElo': 187, u'Black': 224, u'Board': 2, u'BlackTeam': 10, u'White': 224,
 u'Opening': 32, u'fen': 224, u'EventType': 6, u'Variation': 16, u'WhiteFideId': 31, u'Date': 224,
  u'WhiteTeam': 10, u'WhiteElo': 188, u'WhiteTitle': 17, u'PlyCount': 6, u'Round': 224, u'BlackFideId': 32,
  u'Site': 224, u'Event': 224, u'ECO': 222, u'Result': 224, u'EventDate': 64}




{u'BlackTitle': 37479, u'BlackElo': 496871, u'EventCategory': 1, u'Black': 628015, u'Board': 591, u'BlackTeam': 16904,
u'White': 628015, u'WhiteTeamCountry': 12, u'Opening': 77361, u'fen': 628015, u'EventType': 9460, u'Variant': 5, u'Annotator': 12,
u'Variation': 35906, u'Date': 628015, u'WhiteTeam': 16902, u'BlackTeamCountry': 12, u'FEN': 61, u'EventCountry': 17, u'WhiteElo': 502488,
u'WhiteTitle': 39417, u'ECO': 624144, u'EventRounds': 3, u'PlyCount': 27019, u'Round': 628015, u'SetUp': 64, u'BlackFideId': 75805,
u'Site': 628015, u'EventDate': 178511, u'WhiteFideId': 76012, u'Result': 628015, u'Event': 628015}

'''



if __name__ == '__main__':
    print "RUNNING THE PARSER FILE"
    main()

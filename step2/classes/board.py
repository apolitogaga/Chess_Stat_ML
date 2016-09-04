from os.path import expanduser
from multiprocessing import Process, Pool
import re, time
import chess.pgn
import chess as ch

__author__ = "codingMonkey"
__project__ = "ChessML"



CHAR= "."
str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1rnbqkbnr/pp1ppppp/8/2p5/2P5/8/PP1PPPPP/RNBQKBNR w KQkq - 0 2rnbqkbnr/pp1ppppp/8/2p5/2P5/5N2/PP1PPPPP/RNBQKB1R b KQkq - 1 2rnbqkbnr/pp1ppp1p/6p1/2p5/2P5/5N2/PP1PPPPP/RNBQKB1R w KQkq - 0 3rnbqkbnr/pp1ppp1p/6p1/2p5/2PP4/5N2/PP2PPPP/RNBQKB1R b KQkq - 0 3rnbqk1nr/pp1pppbp/6p1/2p5/2PP4/5N2/PP2PPPP/RNBQKB1R w KQkq - 1 4rnbqk1nr/pp1pppbp/6p1/2pP4/2P5/5N2/PP2PPPP/RNBQKB1R b KQkq - 0 4rnbqk1nr/pp2ppbp/3p2p1/2pP4/2P5/5N2/PP2PPPP/RNBQKB1R w KQkq - 0 5rnbqk1nr/pp2ppbp/3p2p1/2pP4/2P1P3/5N2/PP3PPP/RNBQKB1R b KQkq - 0 5rn1qk1nr/pp2ppbp/3p2p1/2pP4/2P1P1b1/5N2/PP3PPP/RNBQKB1R w KQkq - 1 6rn1qk1nr/pp2ppbp/3p2p1/2pP4/2P1P1b1/5N1P/PP3PP1/RNBQKB1R b KQkq - 0 6rn1qk1nr/pp2ppbp/3p2p1/2pP4/2P1P3/5b1P/PP3PP1/RNBQKB1R w KQkq - 0 7rn1qk1nr/pp2ppbp/3p2p1/2pP4/2P1P3/5Q1P/PP3PP1/RNB1KB1R b KQkq - 0 7r2qk1nr/pp1nppbp/3p2p1/2pP4/2P1P3/5Q1P/PP3PP1/RNB1KB1R w KQkq - 1 8r2qk1nr/pp1nppbp/3p2p1/2pP4/2P1P3/2N2Q1P/PP3PP1/R1B1KB1R b KQkq - 2 8r2qk2r/pp1nppbp/3p1np1/2pP4/2P1P3/2N2Q1P/PP3PP1/R1B1KB1R w KQkq - 3 9r2qk2r/pp1nppbp/3p1np1/2pP4/2P1P3/2N2Q1P/PP2BPP1/R1B1K2R b KQkq - 4 9r2q1rk1/pp1nppbp/3p1np1/2pP4/2P1P3/2N2Q1P/PP2BPP1/R1B1K2R w KQ - 5 10r2q1rk1/pp1nppbp/3p1np1/2pP4/2P1P3/2N2Q1P/PP2BPP1/R1B2RK1 b - - 6 10r2q1rk1/1p1nppbp/p2p1np1/2pP4/2P1P3/2N2Q1P/PP2BPP1/R1B2RK1 w - - 0 11r2q1rk1/1p1nppbp/p2p1np1/2pP4/2P1P3/2N2Q1P/PP1BBPP1/R4RK1 b - - 1 111r1q1rk1/1p1nppbp/p2p1np1/2pP4/2P1P3/2N2Q1P/PP1BBPP1/R4RK1 w - - 2 121r1q1rk1/1p1nppbp/p2p1np1/2pP4/P1P1P3/2N2Q1P/1P1BBPP1/R4RK1 b - - 0 121r1qnrk1/1p1nppbp/p2p2p1/2pP4/P1P1P3/2N2Q1P/1P1BBPP1/R4RK1 w - - 1 131r1qnrk1/1p1nppbp/p2p2p1/2pP4/P1P1P3/2N2Q1P/1P1BBPP1/R4R1K b - - 2 131r1q1rk1/1pnnppbp/p2p2p1/2pP4/P1P1P3/2N2Q1P/1P1BBPP1/R4R1K w - - 3 141r1q1rk1/1pnnppbp/p2p2p1/2pP4/P1P1P3/2N3QP/1P1BBPP1/R4R1K b - - 4 141r1q1rk1/1pnn1pbp/p2pp1p1/2pP4/P1P1P3/2N3QP/1P1BBPP1/R4R1K w - - 0 151r1q1rk1/1pnn1pbp/p2pp1p1/2pP4/P1P1P3/2N3QP/1P1BBPP1/1R3R1K b - - 1 151r1q1rk1/1pnn1pbp/p2p2p1/2pp4/P1P1P3/2N3QP/1P1BBPP1/1R3R1K w - - 0 161r1q1rk1/1pnn1pbp/p2p2p1/2pP4/P1P5/2N3QP/1P1BBPP1/1R3R1K b - - 0 161r1qr1k1/1pnn1pbp/p2p2p1/2pP4/P1P5/2N3QP/1P1BBPP1/1R3R1K w - - 1 171r1qr1k1/1pnn1pbp/p2p2p1/2pP4/P1P5/2N3QP/1P1BBPP1/1R2R2K b - - 2 171r1qr1k1/1pnn2bp/p2p2p1/2pP1p2/P1P5/2N3QP/1P1BBPP1/1R2R2K w - - 0 181r1qr1k1/1pnn2bp/p2p2p1/2pP1p2/P1P5/2NB2QP/1P1B1PP1/1R2R2K b - - 1 181r1qr1k1/1pn3bp/p2p2p1/2pPnp2/P1P5/2NB2QP/1P1B1PP1/1R2R2K w - - 2 191r1qr1k1/1pn3bp/p2p2p1/2pPnp2/P1P5/2N3QP/1P1B1PP1/1R2RB1K b - - 3 191r1qr1k1/1pn4p/p2p1bp1/2pPnp2/P1P5/2N3QP/1P1B1PP1/1R2RB1K w - - 4 201r1qr1k1/1pn4p/p2p1bp1/2pPnp2/P1P5/2N4P/1P1B1PPQ/1R2RB1K b - - 5 20"
file  = expanduser("~/Documents/thesisDataFast/csv/test.txt")
scores = {'k':200,'q':9,'b':3,'n':3,'p':1,'r':5,'K':200,'Q':9,'B':3,'N':3,'P':1,'R':5}


class Board(object):
    def readFen(self):
        pass
    def __str__(self):
        pass

    def __init__(self):
        pass

def replaceNumbers(slist):
    tempString = ''
    for i in slist:
        try:
            num = int(i)
            tempString+= num*CHAR
        except:
            tempString += i

    # time.sleep(10)
    return tempString


def getScore(list):
    valor = 0
    for i in list:
        valor += scores[i]
    return valor

# todo: replace numbers with symbol
# todo: clean the code of board
# todo: create a scoring system.
# todo: interpret results.

def interpret_fen(fen_list):
    board = []
    score = []
    res = {}
    for fen in fen_list:
        d = read_line(fen)
        board.append(d['board'])
        score.append(d['score'])

    res["board"] = board
    res["score"] = score
    return res

def read_line(fen):
    split_fen = re.compile(r"[\s/]")
    board = fen.split(" ")[0]
    black = re.findall(r"[a-z]",board)
    white = re.findall(r'[A-Z]',board)
    # b = ch.Board(fen)
    # print len(b.legal_moves)
    res = {}


    fen=fen.strip()
    p= []
    lFen = split_fen.split(fen)

    # print black
    black_score = getScore(black)
    # print white
    white_score = getScore(white)

    t1 = re.compile(r"([0-9])")
    lFen = filter(None, lFen)
    for i in range(0,8):
        temp_list= t1.split(lFen[i])
        p.append(replaceNumbers(temp_list))

    res['board'] = "/".join(p)
    res['score'] =white_score - black_score
    return res

'''

'''
def main():
    f = open(file).readlines()
    b= Board()

    for i in f[:]:
        i = i.strip()
        print i
        print read_line(i)

    #

'''
Useful when using a multiprocessor.
'''
if __name__ == '__main__':
    main()

Board


# todo: update plan
# todo: a well done eval, not just numbers, taking into a count  k-k' q-q' etc. just one number.
# todo: return a processed ??
# todo: identify black and white pieces
# todo: create a distance metric based on a string

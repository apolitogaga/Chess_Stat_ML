# Converts the millionbase chess PGN database (http://www.top-5000.nl/pgn.htm) to json
# with one json dictionary per row. (That is, the resulting file is contain multiple json objects,
# not just one large).
import json
import chess.pgn # From python-chess https://github.com/niklasf/python-chess
# https://python-chess.readthedocs.org/en/latest/
from os import linesep
from collections import defaultdict
import sys, getopt

# GORGO_BASE = "/Users/hectorapolorosalespulido/Documents/thesisDataFast/gorgoBase.pgn"
# GORGO_OUT = "/Users/hectorapolorosalespulido/Documents/thesisDataFast/gorgoBase3.json"
# IFILE =  "../../data/test.pgn"
# OFILE =  "../../data/test.json"

# dump = defaultdict(lambda : list)
def to_json(ifile, ofile):
  count = 1
  pgn = open(ifile) # Or where you have put it
  fout = open(ofile, 'w') # Or where you want it
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

  fout.close()


def main(argv):
  inputfile = ''
  outputfile = ''
  try:
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
  except getopt.GetoptError:
    print 'test.py -i <inputfile> -o <outputfile>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
       print 'test.py -i <inputfile> -o <outputfile>'
       sys.exit()
    elif opt in ("-i", "--ifile"):
       inputfile = arg
    elif opt in ("-o", "--ofile"):
       outputfile = arg
  # print 'Input file is  '+inputfile
  # print 'Output file is '+outputfile
  to_json(inputfile,outputfile)


if __name__ == "__main__":
   main(sys.argv[1:])
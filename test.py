import pgn

GORGO_BASE = "/Users/hectorapolorosalespulido/Documents/thesisDataFast/gorgoBase.pgn"
pgn_text = open('../data/test.pgn').read()


gorgoText = open(GORGO_BASE).read()

# print gorgoText
# pgn_game = pgn.PGNGame()

print pgn.loads(gorgoText) # Returns a list of PGNGame




# print pgn.dumps(pgn_game) # Returns a string with a pgn game
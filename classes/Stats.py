__author__ = "codingMonkey"
__project__ = "ChessML"

from competitors import Competitor
from events import Event
from games import Game
from collections import defaultdict
from nodes import Node
# import mysql.connector

PATH = "../../data/stats/"

def get_white_percentage(GAMES):
    file = PATH + "white_percentage.txt"
    white = 0
    draw = 0
    n_games = len(GAMES)
    for g in GAMES.values():
        if g.result == 1:
            white += 1
        elif g.result == 0:
            draw += 1

    return [white, draw, n_games]


def get_fen_graph(GAMES):
    d = defaultdict(list)
    for g in GAMES.values():
        for fen in g.fen:
            # print fen
            if fen in d:
                d[fen][0]+=1
                d[fen][1].append(g.result)
            else:
                l = [1,[g.result]]
                d[fen]= l
        pass
    return d

def build_graph(games):
    for g in GAMES.values():
        root =
        for fen in g.fen:
            pass


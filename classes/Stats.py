__author__ = "codingMonkey"
__project__ = "ChessML"

from competitors import Competitor
from events import Event
from games import Game
from collections import defaultdict
from nodes import Node as Nod
from nodes import EndNode
from movements import  Movement
import nodes
from os import linesep

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

# def get

def get_fen_graph(GAMES):
    d = defaultdict(list)
    for g in GAMES.values():
        for fen in g.fen:
            # print fen
            if fen in d:
                d[fen][0] += 1
                d[fen][1].append(g.result)
            else:
                l = [1, [g.result]]
                d[fen] = l
        pass
    return d

def build_movement_graph(games, first_movement):
    '''
    :param games: Games of the
    :param first_movement: Root node of our movements network.
     We assume that the node has already been added to the object.
    :return: first_movement object
    '''
    first_move = games[0]
    first_movement.add_result(games[0])
    for g in games.values():
        game_name = games.name
        for i in range(1,len(g.fen)):
            str_mov = g.fen


def build_position_graph(games, victory_node, all_nodes=None):
    '''
    Creates a graph of nodes and movements.
    :param games:
    :param victory_node:
    :param all_nodes:
    :return:
    '''

    first_movement = Movement.ALL_MOVEMENTS[0]
    Nod.ALLNODES = all_nodes
    new_node = None
    g = games.itervalues().next()
    fen = g.fen[0]
    score = g.fen_eval[0]
    res = g.result
    if fen in Nod.ALLNODES:
        root = Nod.ALLNODES[fen]
        root.add_result(res)
    else:
        root = victory_node.init(g.fen[0], res, g.fen_eval[0])


    game_length = len(g.fen)
    if len(Movement.ALL_MOVEMENTS) > game_length:
        Movement.init_last(game_length,g.fen[game_length-2], Movement.ALL_MOVEMENTS[game_length-1])

    # print "%d games"%len(games)

    for g in games.values():
        # print "G>>>> %s: %d :: %s"%(g.name, len(g.fen),"")
        res = g.result
        fen = g.fen[0]
        if fen != "rnbqkbnr/pppppppp/......../......../......../......../PPPPPPPP/RNBQKBNR":
            print "error: %s <> %d <> %s"%(g.name, len(g.fen), fen)
        else:
            root.add_movement(0)

            first_movement.add_node(fen)
            for i in range(1, len(g.fen)):
                fen = g.fen[i]
                b_node = Nod.ALLNODES[g.fen[i - 1]]
                if fen not in Nod.ALLNODES:
                    score = g.fen_eval[i]
                    new_node = Nod.init_back_node(fen, res, b_node.name, score)
                else:
                    new_node = Nod.ALLNODES[fen]
                    new_node.add_result(res)

                b_node.add_node(b_node.forward_nodes, new_node.name)
                new_node.add_node(new_node.back_nodes,b_node.name)
                new_node.add_movement(i)

                movement = Movement.ALL_MOVEMENTS[i]
                movement.add_node(new_node.name)


            new_node.add_node(new_node.forward_nodes, victory_node.name)
            victory_node.add_node(victory_node.back_nodes, new_node.name)
            victory_node.add_result(res)
            # root.test_added_nodes()

    root.save_all_nodes()
    first_movement.save_all_movements()
    return [root,first_movement]


def game_statistics(games):
    text = ""
    for g in games.values():
        text += g.name + ", "
        text += g.fen[0] + ", "
        text += g.fen[1] + ", "
        text += str(len(g.fen))
        text += linesep
    return text

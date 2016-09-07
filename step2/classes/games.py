__author__ = "codingMonkey"
__project__ = "ChessML"

from base import BaseClass
from events import Event
from competitors import Competitor
from board import Board, interpret_fen
ID = 0

class Game(BaseClass):
    # white = None
    # black = None
    # event = None
    # welo = None
    # belo = None
    # round = None
    # result = None
    # id = None
    # fen = None
    # fen_eval = None
    ID = 1


    def __init__(self, name, fen, event, wplay, bplay, result, welo, belo, round):
        """
        :param str name:
        :param str fen:
        :param Event event:
        :param Competitor wplay:
        :param Competitor bplay:
        :param int result:
        :param int welo:
        :param int belo:
        :param int round:
        :return:
        """
        super(Game, self).__init__(name)
        self.result = result
        self.round = round
        self.white = wplay
        self.black = bplay
        self.event = event
        self.welo = welo
        self.belo = belo
        self.id = Game.ID
        self.fen = fen
        self.fen_eval = None

    @classmethod
    def init_fenless(self, name, fen, event, wplay, bplay, result, welo, belo, round=None):
        '''
        the first time we read a game, we have not evaluated the FEN(board), thus we must evaluate it.
        :param str name:
        :param str fen:
        :param Event event:
        :param Competitor wplay:
        :param Competitor bplay:
        :param int result:
        :param int welo:
        :param int belo:
        :param int round:
        :return:
        '''
        game = Game(name,fen, event, wplay, bplay, result, welo, belo, round)
        Game.ID += 1
        fen_eval = interpret_fen(fen)
        game.fen = fen_eval['board']
        game.fen_eval = fen_eval['score']
        return game

    @classmethod
    def re_init(self, name, fen, event, wplay, bplay, result, welo, belo, round, fen_eval):
        game = Game(name,fen, event, wplay, bplay, result, welo, belo, round)
        game.fen_eval = fen_eval
        return game

    def __str__(self):
        return super(Game, self).__str__()

    def as_dict(self):
        d = super(Game,self).as_dict()
        d["fen"] = self.fen
        d["fen_eval"] = self.fen_eval
        d["result"] = self.result
        d["round"] = self.round
        d["date"] = self.event.get_date()

        d["black"] = self.black.name
        d["black_avg_elo"] = self.black.avg_elo
        d["white_elo"] = self.welo

        d["white"] = self.white.name
        d["white_avg_elo"] = self.white.avg_elo
        d["black_elo"] = self.belo

        d["event"] = self.event.name
        return d


    def toStrFormat(self, sep=","):
        """

        :rtype: object
        """
        return self.event.name +","+ str(self.event.minDate)+","+ str(self.event.maxDate)+","+\
            str(self.date) +","+ self.white.name +","+ self.black.name+","+ str(self.welo)+","+ str(self.belo)+","+\
            str(self.white.avg_elo)+","+ str(self.black.avg_elo) +","+ str(self.result)+","+ self.fen

    pass


def format_Result(res):
    '''
    :param res: Result string from pgn file
    :var d: 1 white won, 0 draw, -1 black won
    :return: int
    '''
    try:
        d = {'1-0': 1, '1/2-1/2': 0, '0-1': -1}
        return d[res]
    except KeyError:
        raise NameError("ERROR: result '%s' invalid"%res)


Game

__author__ = "codingMonkey"
__project__ = "ChessML"
from base import BaseClass
import math


class Competitor(BaseClass):
    elo = None
    avg_elo = None

    def __init__(self, name, elo):
        super(Competitor, self).__init__(name)
        self.elo = []
        self.newElo(elo)

    def __init__(self, name, elo,avg):
        super(Competitor, self).__init__(name)
        self.elo = []
        self.newElo(elo)
        self.avg_elo = avg

    def get_elo(self):
        return self.elo

    def newElo(self, elo):
        """
        check new elo and add it to the list of elos.
        :rtype: NONE
        """
        try:
            elo = float(elo)
            self.elo.append(elo)
        except ValueError:
            self.avg_elo = None
            pass

    def __str__(self, sep=" "):
        return super(Competitor, self).__str__() + sep + str(self.avg_elo)

    def __repr__(self):
        return "<Competitor: "+  super(Competitor, self).__str__()  + " " + str(self.avg_elo) +">"


    def calc_avgElo(self):
        """
        Updates the average elo after adding a new one.
        """
        try:
            self.avg_elo = math.floor(sum(self.elo)/ len(self.elo))
        except ZeroDivisionError:
            self.avg_elo = None


def calculate_average(competitor):
    list_elo = competitor.elo
    try:
        return math.floor(sum(list_elo)/len(list_elo))
    except ZeroDivisionError:
        return None

def process_name(string):
    temp = string.replace(",", "")
    temp = temp.replace(".", "")
    return temp


Competitor

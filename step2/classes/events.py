__author__ = "codingMonkey"
__project__ = "ChessML"
from base import BaseClass
import dateparser

class Event(BaseClass):
    """

    """
    # minDate = None
    # maxDate = None

    def __init__(self, name, date):
        """

        :rtype: object
        """
        super(Event, self).__init__(name)
        try:
            date = dateparser.parse(date)
            self.minDate = date
            self.maxDate = date
        except TypeError:
            pass
        except AttributeError:
            pass

    def get_date(self):
        """

        :rtype: object
        """
        if self.minDate is None:
            return None
        else:
            return str(self.minDate.date())

    def __str__(self):
        """

        :return:
        """
        return super(Event,self).__str__()


    def add_Date(self,date):
        """

        :rtype: object
        """
        try:
            date = dateparser.parse(date)
            if(date< self.minDate):
                self.minDate = date
            elif(date>self.maxDate):
                self.maxDate = date
        except TypeError:
            pass






Event
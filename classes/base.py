__author__ = "codingMonkey"
__project__ = "ChessML"


class BaseClass(object):
    name = ""

    def __init__(self, name):
        self.name =  name

    def __str__(self):
         return self.name

    def __repr__(self):
        return "name:%s" % (self.name)

    def as_dict(self):
        return {"name":self.name}

    def toStrFormat(self, sep, *param2):
        temp = ""
        for a in param2:
            try:
                temp += str(a).encode("utf8")+sep
            except UnicodeDecodeError:
                temp += a.decode("utf8") +sep
            except:
                print "ERRR: " + a
        return temp

    pass



BaseClass
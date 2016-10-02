__author__ = "codingMonkey"
__project__ = "ChessML"


from dev2.generate_statistics import ALT_TRAIN_INPUT_FOLDER, ALT_TEST_INPUT_FOLDER, STAT_DATA_FOLDER

from dev2.tools import tools, read_json, read_pieces

# from dev2.generate_statistics.write_statistics_from_grid import multiprocess_file

import multiprocessing
import numpy as np
from tabulate import tabulate

# names of the files written by the other code:
from dev2.generate_statistics.write_statistics_from_grid import BASIC_STATS_NAME, RESULT, BLACK_AVG_ELO, BLACK_ELO, BLACK, LEN_FEN, WHITE_AVG_ELO, WHITE_ELO, WHITE
from  dev2.generate_statistics import RESULTS_FOLDER, FIGURES_FOLDER
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
# from
from dev2.step4 import FINAL_TEST_INPUT_FOLDER, FINAL_TRAIN_INPUT_FOLDER
from dev2.step4.process_data import multiprocess_graph_stats

# import matplotlib.pyplot as plt



DEF_EXTENSION = ".csv"
IN_FOLDER = STAT_DATA_FOLDER
OUT_FOLDER = RESULTS_FOLDER
FIGURES_FOLDER = FIGURES_FOLDER


#
# GENERAL METHODS
#


def get_list_files(input_file_pattern, in_folder= IN_FOLDER, extension= DEF_EXTENSION):
    file_list = []
    for i in range(100):
        file_list.append("%s%d/%s%d%s"%(in_folder, i, input_file_pattern, i, extension))
    return file_list


def get_file(file, function):
    print "Processing %s"%file
    file_number = tools.get_number_from_filename(file)
    data = np.genfromtxt(file, names= True, delimiter=',', dtype=None)
    res = function(data)
    res.insert(0, file_number)
    return res


def multiprocess_file(function, file_pattern, input_folder = IN_FOLDER):
    pool = multiprocessing.Pool()
    l = get_list_files(file_pattern)
    res = pool.map(function, l)
    # print res
    return res


#
# BASIC STATS
#

def write_basic_stats(data):
    """
    Writes the most basic data:
    :param data:
    :return: List of calc data.
    """
    # print count(data[RESULT])
    res = list(data[RESULT])
    n =  len(data[RESULT]) + 0.0
    r_white = res.count(1)
    r_black = res.count(-1)
    r_draw = res.count(0)
    mean_len = np.mean(data[LEN_FEN])
    med_len = np.median(data[LEN_FEN])
    std_len = np.var(data[LEN_FEN])
    return [r_white/n,r_black/n, r_draw/n, mean_len, med_len, std_len]


def interface_get_basic_statistics(file):
    res = get_file(file,write_basic_stats)
    return res

#
# ELO WINNING PERCENTAGE
#

def elo_winning_percentage(data):
    """
    Using average elo, we test who won the game
    0 = Draw.
    1 = Bigger ELO won.
    2 = Lower ELO won.
    :param data:
    :return:
    """
    avg_welo = data[WHITE_AVG_ELO]
    avg_belo = data[BLACK_AVG_ELO]
    result = data[RESULT]
    n_res =  []
    n = len(avg_welo) + 0.0
    for i in range(int(n)):
        if avg_welo[i] > avg_belo[i]:
            if result[i] == 1:
                n_res.append(1)
            elif result[i] == 0:
                n_res.append(0)
            else:
                n_res.append(2)
        else:
            if result[i] == -1:
                n_res.append(1)
            elif result[i] == 1:
                n_res.append(2)
            else:
                n_res.append(0)

    bigger = n_res.count(1)
    lower = n_res.count(2)
    draw = n_res.count(0)
    return [bigger/n,lower/n, draw/n]

def interface_elo_winning_percentage(file):
    res = get_file(file,elo_winning_percentage)
    return res


# Only executable methods


def multiprocess_elo_winning_percentage():
    headers = ["Grid Number", "Bigger ELO","Smaller ELO", "DRAW"]
    file = OUT_FOLDER +"elo_winning_percentage.txt"
    res = multiprocess_file(interface_elo_winning_percentage, BASIC_STATS_NAME)
    # for l in res:
    #     print l
    str = tabulate(res, headers, tablefmt="latex")
    tools.write_to_file(file, str)



def multiprocess_get_basic_statistics():
    """
    Multiprocess a file
    :return: Writes a file in the file described by file.

    """
    headers = ["Grid Number","% White", "% Black", "% Draw", "mean len","median len", "Variance"]
    file = OUT_FOLDER +"basic_stats.txt"
    res = multiprocess_file(interface_get_basic_statistics, BASIC_STATS_NAME)
    # str = tabulate(res, headers, tablefmt="latex")
    # tools.write_to_file(file, str)
    np_res =  np.array(res)



def test_scipy():
    #Sample data creation
    #number of points
    n=50
    t=linspace(-5,5,n)
    #parameters
    a=0.8; b=-4
    x=polyval([a,b],t)
    #add some noise
    xn=x+randn(n)

    #Linear regressison -polyfit - polyfit can be used other orders polys
    (ar,br)=polyfit(t,xn,1)
    xr=polyval([ar,br],t)
    #compute the mean square error
    err=sqrt(sum((xr-xn)**2)/n)

    print('Linear regression using polyfit')
    print('parameters: a=%.2f b=%.2f \nregression: a=%.2f b=%.2f, ms error= %.3f' % (a,b,ar,br,err))

    #matplotlib ploting
    title('Linear Regression Example')
    plot(t,x,'g.--')
    plot(t,xn,'k.')
    plot(t,xr,'r.-')
    legend(['original','plus noise', 'regression'])

    show()

    #Linear regression using stats.linregress
    (a_s,b_s,r,tt,stderr)=stats.linregress(t,xn)
    print('Linear regression using stats.linregress')
    print('parameters: a=%.2f b=%.2f \nregression: a=%.2f b=%.2f, std error= %.3f' % (a,b,a_s,b_s,stderr))

def test_plot():
    plt.figure(1, figsize=(6, 6))
    ax = axes([0.1, 0.1, 0.8, 0.8])

    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    fracs = [15, 30, 45, 10]

    explode = (0, 0.05, 0, 0)
    pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
    plt.title('Raining Hogs and Dogs', bbox={'facecolor': '0.8', 'pad': 5})

    # show()
    plt.savefig(FIGURES_FOLDER+'foo.png')
    plt.close()


def compare_grids(file_number =".json", folder = FINAL_TEST_INPUT_FOLDER):

    file = "FINAL_TEST_%d.json"%file_number

    var = multiprocess_graph_stats(file)
    root_node = var[0]

    print len(root_node.all_nodes)
    file2 = "FINAL_TEST_99.json"
    var = multiprocess_graph_stats(file2)
    root_node2 = var[0]
    print len(root_node2.all_nodes)
    keys_a = set(root_node.all_nodes.keys())
    keys_b = set(root_node2.all_nodes.keys())
    intersection = keys_a & keys_b

    print len(intersection)
    for i in intersection:
        print i


    pass

if __name__ == "__main__":
    # test_file = IN_FOLDER + "0/"+BASIC_STATS_NAME + "0.csv"
    # print get_file(test_file, elo_winning_percentage)


    # multiprocess_get_basic_statistics()
    # multiprocess_elo_winning_percentage()

    # test_plot()
    compare_grids()
    pass
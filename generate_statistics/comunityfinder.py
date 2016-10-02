from igraph import *
#import cairo
from random import randint

from dev2.tools import tools, read_pieces
from dev2.generate_statistics.generate_network import OUT_FILE, OUT_FOLDER, NAME
import multiprocessing
from tabulate import tabulate
INPUT_FILE = OUT_FILE
INPUT_FOLDER = OUT_FOLDER
IMG_NAME = "COMMUNITY_"

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

######## only works with weighted graphs
def _plot(g, membership=None,file=None):
    if membership is not None:
        gcopy = g.copy()
        edges = []
        edges_colors = []
        for edge in g.es():
            if membership[edge.tuple[0]] != membership[edge.tuple[1]]:
                edges.append(edge)
                edges_colors.append("gray")
            else:
                edges_colors.append("black")
        gcopy.delete_edges(edges)
        layout = gcopy.layout("kk")
        g.es["color"] = edges_colors
    else:
        layout = g.layout("kk")
        g.es["color"] = "gray"
    visual_style = {}
    visual_style["vertex_label_dist"] = 0
    visual_style["vertex_shape"] = "circle"
    visual_style["edge_color"] = g.es["color"]
    # visual_style["bbox"] = (4000, 2500)
    visual_style["vertex_size"] = 30
    visual_style["layout"] = layout
    visual_style["bbox"] = (1024, 768)
    visual_style["margin"] = 40
    visual_style["edge_label"] = truncate(g.es["weight"],4) ####### comment if not weighted graph idk if it works
    for vertex in g.vs():
        vertex["label"] = vertex['name']
    if membership is not None:
        colors = []
        for i in range(0, max(membership)+1):
            colors.append('%06X' % randint(0, 0xFFFFFF))
        for vertex in g.vs():
            vertex["color"] = str('#') + colors[membership[vertex.index]]
        visual_style["vertex_color"] = g.vs["color"]
    plot(g,file, **visual_style)



def plotMe(g,community,file):
    membership = community.as_clustering().membership
    file = "img/"+file+".png"
    _plot(g,membership,file)
    pass

def multiprocess_graphs():
    """

    :return:
    """
    head = ['#', 'N','E','k','d']
    pool = multiprocessing.Pool()
    # list = read_pieces.getFilesFromFolder(INPUT_FOLDER)
    file_list = tools.get_sorted_list(NAME, ".csv")
    # print file_list
    res = pool.map(load_network, file_list)
    print tabulate(res,head,tablefmt="latex")

def load_network(file):
    """
    Loads a network and returns its network summary.
    :param file: file to load
    :return: [E, N, K, d]
    """
    print file
    g = Graph.Read_Ncol(INPUT_FOLDER+file,names=True,directed=False)
    file_number = tools.get_number_from_filename(file)
    return get_summary_network(g, file_number)

def get_summary_network(g, name):
    table=[]
    E = len(g.es) + 0.0
    N = len(g.vs) + 0.0
    k = float(E/N)+0.0
    delta = float(2*E/(N*(N + 1)))+0.0
    table.append(name)
    table.append(N) # vertices
    table.append(E) # edges
    table.append(k) # mean degree
    table.append(delta) # network density changes
    return table




def print_table1(g,languages):
    # print tabulate(table, headers, tablefmt="latex")
    head = ['Language', 'N','E','k','d']
    # table=[]
    # for i in range(0,len(g)):
    #     table.append(get_t1_data(g[i],languages[i]))
    # print tabulate(table,head,tablefmt="latex")
    pass

def find_community(file = INPUT_FILE):
    '''
    # The input file must not have commas, I deleted them with the text editor.
    # but first we replaced the "," with "_" so that the names were clear, then we deleted the commas.
    '''
    fNum = tools.get_number_from_filename(file)

    g = Graph.Read_Ncol(file,names=True,directed=False)
    summary(g)
    # excl = g["Aronian_L"]

    # ed = g.vs.select(lambda x:x["name"]=="Aronian_L")
    # summary(g)
    # print(g)
    # print repr(ed)

    print "\n\n\n\n***************************" \
          "***************************" \
          "***************************" \
          "***************************" \
          "***************************"
    # summary(ed)
    # print(ed)
    # g2 = Graph.Read_Ncol(f_pat_idf,names=True,weights="True",directed=False)
    # cb = g.community_edge_betweenness()
    # ci = g.community_infomap()
    # cp = g.community_label_propagation()
    # cs = g.community_spinglass()

    ######
    # cw = g.community_walktrap()
    # print "Plotting"
    # img_name = IMG_NAME + str(fNum)
    # plotMe(g,cw,img_name)
    ######

        # print get_summary_network(g, "test")
    # cb2 = g.community_edge_betweenness()
    # cw2 = g.community_walktrap()
    # plotMe(g,ci,"infomap")  # doesn't work didn't have time to check it ;(,
    # 'VertexClustering' object has no attribute 'as_clustering', this is the error.
    # plotMe(g,cp,"propagation") # doesn't work didn't have time to check it ;(
    # plotMe(g,cs,"spinglass") # doesn't work didn't have time to check it ;(
    # plotMe(g,cw,"walktrap_idf_final")
    #
    #
    # plotMe(g2,cb2,"betweeness_sidf_final")
    # plotMe(g2,cw2,"walktrap_sidf_final")


######### we need cairo interface to plot http://stackoverflow.com/questions/12072093/python-igraph-plotting-not-available
if __name__ == '__main__':
    # multiprocess_graphs()
    find_community("data/network_99.csv")
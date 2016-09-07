__author__ = "codingMonkey"
__project__ = "ChessML"

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets

from dev2.step4 import process_data
from dev2.step4.classes import movements

def test():
    """
    To test something erase later.
    :return:
    """
    # file = "_final_0.json" # normal file
    file = "REF_final_0.json" # alt file
    var = process_data.multiprocess_graph_stats(file)
    root_node = var[0]
    end_node =  var[1]
    movs = var[2]
    print "breakpoint"
    print "lalala"

    movements.define_probabilities_movements(movs, root_node.ALLNODES)
    # nod = end_node.get_ordered_backward_nodes()
    # for i in nod[:10]:
    #     print i



def my_kernel(X, Y):
    """
    We create a custom kernel:

                 (2  0)
    k(X, Y) = X  (    ) Y.T
                 (0  1)
    """
    M = np.array([[2, 0], [0, 1.0]])
    return np.dot(np.dot(X, M), Y.T)

def test_2():
    # import some data to play with
    iris = datasets.load_iris()
    print iris
    X = iris.data[:, :2]  # we only take the first two features. We could
                          # avoid this ugly slicing by using a two-dim dataset
    print X

    Y = iris.target


    h = .02  # step size in the mesh

    # we create an instance of SVM and fit out data.
    clf = svm.SVC(kernel=my_kernel)
    clf.fit(X, Y)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, m_max]x[y_min, y_max].
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired)
    plt.title('3-Class classification using Support Vector Machine with custom'
              ' kernel')

    plt.axis('tight')
    plt.show()

def scikit_test():
    X = [[0, 0], [1, 1]]
    y = [0, 1]
    clf = svm.SVC()
    print clf.fit(X, y)
    pass


if __name__ == '__main__':
    test()
    # scikit_test()
    # test_2()
"""
Clément Dauvilliers - Applied Data Tourists - EPFL ADA Project
11/12/2021

Used to visualize the relationships graph.
"""
import networkx as ntx
import pyvis
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
from graph_processing import *


def read_json_graph(path):
    """
    Read a graph in a json file.
    """
    with open(path, "r") as file:
        data = json.load(file)
        graph = json_graph.adjacency_graph(data)
    return graph

def gender_condition(node):
    """
    :param node: node label, under the form "occupation_gender"
    :return: True if the node is associated
        with a gender other than 'male' or 'female'.
    """
    gender = node.split('_')[1]
    return gender not in ['male', 'female']

_USE_GENDER_ = False
_SAVE_DIR_ = "html_graphs"

if __name__ == "__main__":
    for year in ['2015', '2016', '2017', '2018', '2019', '2020']:
        if _USE_GENDER_:
            networkx_json = f"graph_occupation_gender{year}.json"
        else:
            networkx_json = f"graph_occupation{year}.json"
        ntx_graph = read_json_graph(os.path.join("data", networkx_json))

        filter_nodes(ntx_graph, 60, condition=None)

        network = pyvis.network.Network(height='750px', width='100%', directed=True)
        build_graph(ntx_graph, network, edges_proportion=0.05, use_genders=_USE_GENDER_)

        network.barnes_hut(central_gravity=0.3, spring_strength=0.01, spring_length=50)
        network.show_buttons(filter_=['physics'])

        if _USE_GENDER_:
            filename = f"nt_occupation_gender_{year}.html"
        else:
            filename = f'nt_occupation_{year}.html'
        network.show(os.path.join(_SAVE_DIR_, filename))

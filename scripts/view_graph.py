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


if __name__ == "__main__":
    ntx_graph = read_json_graph(os.path.join("data/graph_occupation2015.json"))
    filter_nodes(ntx_graph, 10000)

    network = pyvis.network.Network(height='750px', width='100%', directed=True)
    build_graph(ntx_graph, network, edges_proportion=0.05, color_incoming_weights=True)

    network.barnes_hut(central_gravity=0.3, spring_strength=0.01, spring_length=50)
    network.show_buttons(filter_=['physics'])

    network.show('nt.html')

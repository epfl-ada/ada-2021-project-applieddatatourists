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
    for year in ['2015', '2016', '2017', '2018', '2019', '2020']:
        ntx_graph = read_json_graph(os.path.join(f"data/graph_occupation_gender{year}.json"))
        filter_nodes(ntx_graph, 60)

        network = pyvis.network.Network(height='750px', width='100%', directed=True)
        build_graph(ntx_graph, network, edges_proportion=0.05, use_genders=True)

        network.barnes_hut(central_gravity=0.3, spring_strength=0.01, spring_length=50)
        network.show_buttons(filter_=['physics'])

        network.show(f'nt_{year}.html')

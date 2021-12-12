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


def read_json_graph(path):
    """
    Read a graph in a json file.
    """
    with open(path, "r") as file:
        data = json.load(file)
        graph = json_graph.adjacency_graph(data)
    return graph


def filter_nodes(ntx_graph, min_weight=1000):
    """
    Reduces the amount of nodes in the networkx graph in
    the following manner:
    - if weight(n) < min_weight, remove n
    The graph is modified inplace.
    :param ntx_graph: networkx graph to filter
    :param min_weight: filtering parameter
    """
    for i, node_name in enumerate(list(ntx_graph.nodes)):
        node = ntx_graph.nodes.data()[node_name]
        if node['weight'] < min_weight:
            ntx_graph.remove_node(node_name)


def build_graph(ntx_graph, network, edges_proportion=0.05):
    """
    Builds the pyvis graph from the NetworkX graph.
    :param ntx_graph: networkx graph to translate
    :param network: PyVis graph to fill with the data from
        ntx_graph
    :param edges_proportion: float between 0 and 1. Proportion
        of the edges coming out of each node to be included in
        the PyVis graph. For example, 0.2 means only the 20%
        of edges with the largest weight will be displayed.
    :return: the PyVis version of the graph.
    """
    # Step 1: add the nodes
    for i, node_name in enumerate(list(ntx_graph.nodes)):
        node = ntx_graph.nodes.data()[node_name]
        # Adds a node in the pyvis network whose label is the occupation
        # name, and value is the number of speakers contained in the node
        network.add_node(node_name, label=node_name, value=node['weight'])
    # Step 2: add the edges
    nodes_data = ntx_graph.nodes.data()
    for node in ntx_graph.nodes:
        # Retrieves the data for each edge coming out of node
        out_weights = [ntx_graph.get_edge_data(node, s)['weight'] / nodes_data[s]['weight']
                       for s in ntx_graph.successors(node)
                       ]
        # Sets a minimum weight. All edges coming out of node
        # whose weight is inferior to that value will NOT be added
        # to the PyVis graph.
        min_accepted_weight = np.quantile(out_weights, 1 - edges_proportion)
        for k, succ in enumerate(ntx_graph.successors(node)):
            if out_weights[k] >= min_accepted_weight:
                network.add_edge(node, succ, value=out_weights[k])


if __name__ == "__main__":
    ntx_graph = read_json_graph(os.path.join("data/graph_occupation.json"))
    filter_nodes(ntx_graph, 10000)

    network = pyvis.network.Network(height='750px', width='100%', directed=True)
    build_graph(ntx_graph, network)

    network.barnes_hut(central_gravity=0.3, spring_strength=0.01, spring_length=50)
    network.show_buttons(filter_=['physics'])

    network.show('nt.html')

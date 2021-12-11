"""
Clément Dauvilliers - Applied Data Tourists - EPFL ADA Project
11/12/2021

Used to visualize the relationships graph.
"""
import networkx as ntx
import pyvis
import os
import json
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


def build_graph(ntx_graph, network):
    """
    Builds the pyvis graph from the NetworkX graph.
    :param ntx_graph: networkx graph to translate
    :param network: PyVis graph to fill with the data from
        ntx_graph
    :return: the PyVis version of the graph.
    """
    # Step 1: add the nodes
    for i, node_name in enumerate(list(ntx_graph.nodes)):
        node = ntx_graph.nodes.data()[node_name]
        # Adds a node in the pyvis network whose label is the occupation
        # name, and value is the number of speakers contained in the node
        network.add_node(node_name, label=node_name, value=node['weight'])
    # Step 2: add the edges
    for edge_data in ntx_graph.edges.data():
        node_a, node_b, props = edge_data
        weight = props['weight']
        network.add_edge(node_a, node_b)


if __name__ == "__main__":
    ntx_graph = read_json_graph(os.path.join("data/graph_occupation.json"))
    filter_nodes(ntx_graph, 10000)

    network = pyvis.network.Network(height='750px', width='100%', directed=True)
    build_graph(ntx_graph, network)
    network.show_buttons(filter_=['physics'])
    network.show('nt.html')

"""
Define functions to build and process the graph
using PyVis and networkx.
"""
import numpy as np


def filter_nodes(ntx_graph, min_weight=500):
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


def build_graph(ntx_graph, network, edges_proportion=0.05, color_incoming_weights=True):
    """
    Builds the pyvis graph from the NetworkX graph.
    :param ntx_graph: networkx graph to translate
    :param network: PyVis graph to fill with the data from
        ntx_graph
    :param edges_proportion: float between 0 and 1. Proportion
        of the edges coming out of each node to be included in
        the PyVis graph. For example, 0.2 means only the 20%
        of edges with the largest weight will be displayed.
    :param color_incoming_weights: boolean. If True, the nodes' opacities
        will depend on their incoming weight (total weight of incoming edges).
        This better represents the importance of each node for their predecessors:
        the darker a node N, the more its predecessor mention it proportionally.
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
        node_w = nodes_data[node]['weight']
        out_weights = [ntx_graph.get_edge_data(node, s)['weight'] / (nodes_data[s]['weight'] * node_w)
                       for s in ntx_graph.successors(node)
                       ]
        if len(out_weights) == 0:
            continue
        # Sets a minimum weight. All edges coming out of node
        # whose weight is inferior to that value will NOT be added
        # to the PyVis graph.
        min_accepted_weight = np.quantile(out_weights, 1 - edges_proportion)
        for k, succ in enumerate(ntx_graph.successors(node)):
            if out_weights[k] >= min_accepted_weight:
                network.add_edge(node, succ, value=out_weights[k])

    # Colors the nodes based on their incoming weight
    if color_incoming_weights:
        color_nodes_incoming_weight(network, ntx_graph)


def color_nodes_incoming_weight(network, ntx_graph):
    """
    Colors the nodes based on the total weight
    of their incoming edges.
    :param network: PyVis network to color.
    :param ntx_graph: NetworkX graph
    """
    nodes_data = ntx_graph.nodes.data()
    # First pass: compute the total incoming weight
    # of all nodes
    incoming_weights = []
    for id_node in range(len(network.nodes)):
        # Retrieve the label of the node in the NetworkX graph
        node_dict = network.nodes[id_node]
        node = node_dict['id']
        # Compute the total weight over all incoming edges
        # We again divide by the number of people in both nodes
        # to obtain a relative importance, which is more relevant
        incoming_weights.append(sum([ntx_graph.get_edge_data(p, node)['weight']
                                     / (nodes_data[node]['weight'] * nodes_data[p]['weight'])
                                     for p in ntx_graph.predecessors(node)]))
    # Normalize the weights between 0 and 1
    incoming_weights = np.array(incoming_weights)
    incoming_weights = incoming_weights / incoming_weights.max()
    # Second pass: color the nodes
    color = np.array([0, 0, 0])
    for id_node in range(len(network.nodes)):
        opacity = incoming_weights[id_node]
        network.nodes[id_node]['color'] = f'rgba({color[0]},{color[1]},{color[2]},{opacity})'
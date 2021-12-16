"""
Define functions to build and process the graph
using PyVis and networkx.
"""
import numpy as np

# Color palette for the gender-based nodes coloration
# Inspired from the Wong colorblind-friendly palette
_GENDERS_COLORS_ = {'male': '200, 50, 50',
                    'female': '50, 50, 200',
                    'non-binary': '0, 0, 0',
                    'transgender male': '255, 255, 0',
                    'transgender female': '255, 255, 0',
                    'transgender person': '255, 255, 0',
                    'genderfluid': '50, 255, 50',
                    'shemale': '76, 47, 39',
                    'bigender': '230, 159, 0',
                    'intersex': '0, 114, 178',
                    'eunuch': '0, 158, 115'}


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


def build_graph(ntx_graph, network, edges_proportion=0.05,
                use_genders=False):
    """
    Builds the pyvis graph from the NetworkX graph.
    :param ntx_graph: networkx graph to translate
    :param network: PyVis graph to fill with the data from
        ntx_graph
    :param edges_proportion: float between 0 and 1. Proportion
        of the edges coming out of each node to be included in
        the PyVis graph. For example, 0.2 means only the 20%
        of edges with the largest weight will be displayed.
    :param use_genders: boolean. If True, will color the nodes according to the gender.
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
        out_weights = [ntx_graph.get_edge_data(node, s)['weight']
                       for s in ntx_graph.successors(node)
                       ]
        out_weights = np.array(out_weights)
        out_weights = out_weights / np.sum(out_weights)
        if len(out_weights) == 0:
            continue
        # Sets a minimum weight. All edges coming out of node
        # whose weight is inferior to that value will NOT be added
        # to the PyVis graph.
        min_accepted_weight = np.quantile(out_weights, 1 - edges_proportion)
        for k, succ in enumerate(ntx_graph.successors(node)):
            if out_weights[k] >= min_accepted_weight:
                network.add_edge(node, succ, weight=out_weights[k])

    color_nodes(network, ntx_graph, use_genders)


def color_nodes(network, ntx_graph, use_gender=False):
    """
    Colors the nodes based on the total weight
    of their incoming edges, and potentially the gender.
    :param network: PyVis network to color
    :param ntx_graph: NetworkX graph
    :param use_gender: boolean. If True, the nodes' color will
        indicate the gender.
    """
    # Second pass: color the nodes
    base_color = '0, 0, 0'
    for id_node in range(len(network.nodes)):
        opacity = 0.5
        if use_gender:
            # The labels are "occupation_gender"
            gender = network.get_nodes()[id_node].split('_')[1]
            color = _GENDERS_COLORS_[gender]
        else:
            color = base_color
        network.nodes[id_node]['color'] = f'rgba({color},{opacity})'

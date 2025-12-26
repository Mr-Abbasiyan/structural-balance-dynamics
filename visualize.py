# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt

def unstable_edges(n, graph):
    """
    Return edges that belong to at least one unbalanced triangle
    """
    unstable = set()

    nodes = list(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if (i, j) in graph and (i, k) in graph and (j, k) in graph:
                    if graph[(i, j)] * graph[(i, k)] * graph[(j, k)] == -1:
                        unstable.update([(i, j), (i, k), (j, k)])

    return unstable


def draw_signed_network(n, graph, filename):
    G = nx.Graph()
    G.add_nodes_from(range(n))

    for (i, j), s in graph.items():
        G.add_edge(i, j, sign=s)

    pos = nx.kamada_kawai_layout(G)

    unstable = unstable_edges(n, graph)

    pos_edges = [(u, v) for u, v in G.edges() if G[u][v]["sign"] == 1]
    neg_edges = [(u, v) for u, v in G.edges() if G[u][v]["sign"] == -1]

    unstable_pos = [e for e in pos_edges if e in unstable]
    unstable_neg = [e for e in neg_edges if e in unstable]

    stable_pos = [e for e in pos_edges if e not in unstable]
    stable_neg = [e for e in neg_edges if e not in unstable]

    plt.figure(figsize=(8, 8))

    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="lightgray")

    nx.draw_networkx_edges(
        G, pos, edgelist=stable_pos, edge_color="black", width=1
    )

    nx.draw_networkx_edges(
        G, pos, edgelist=stable_neg, edge_color="black",
        style="dashed", width=1
    )

    nx.draw_networkx_edges(
        G, pos, edgelist=unstable_pos, edge_color="black", width=3
    )

    nx.draw_networkx_edges(
        G, pos, edgelist=unstable_neg, edge_color="black",
        style="dashed", width=3
    )

    nx.draw_networkx_labels(G, pos, font_size=9)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

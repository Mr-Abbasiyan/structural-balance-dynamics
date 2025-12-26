# -*- coding: utf-8 -*-

import random
import itertools

def create_signed_graph(n, p_pos, p_neg):
    """
    Create a signed undirected graph.
    +1 : positive edge
    -1 : negative edge
    """
    graph = {}
    for i in range(n):
        for j in range(i + 1, n):
            r = random.random()
            if r < p_pos:
                graph[(i, j)] = 1
            elif r < p_pos + p_neg:
                graph[(i, j)] = -1
    return graph


def get_triangles(n, graph):
    """Return all triangles existing in the graph"""
    return [
        (i, j, k)
        for i, j, k in itertools.combinations(range(n), 3)
        if (i, j) in graph and (i, k) in graph and (j, k) in graph
    ]


def triangle_sign(triangle, graph):
    """Product of the signs of the three edges of a triangle"""
    i, j, k = triangle
    return graph[(i, j)] * graph[(i, k)] * graph[(j, k)]


def count_unbalanced(triangles, graph):
    """Number of unbalanced triangles"""
    return sum(1 for t in triangles if triangle_sign(t, graph) == -1)


def systematic_relaxation(n, graph, max_iter=50):
    """
    Systematic relaxation:
    in each round, all unbalanced triangles are checked
    and edges are flipped to reduce imbalance.
    """
    triangles = get_triangles(n, graph)
    history = []

    for _ in range(max_iter):

        unbalanced = [t for t in triangles if triangle_sign(t, graph) == -1]
        history.append(len(unbalanced))

        if not unbalanced:
            break

        for (i, j, k) in unbalanced:
            edges = [(i, j), (i, k), (j, k)]

            best_edge = None
            best_improvement = 0
            current = count_unbalanced(triangles, graph)

            for e in edges:
                graph[e] *= -1
                new_value = count_unbalanced(triangles, graph)
                improvement = current - new_value
                graph[e] *= -1

                if improvement > best_improvement:
                    best_improvement = improvement
                    best_edge = e

            if best_edge is not None:
                graph[best_edge] *= -1

    return history, graph

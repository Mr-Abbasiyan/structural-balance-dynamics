# -*- coding: utf-8 -*-

import pandas as pd

from core import create_signed_graph, systematic_relaxation
from visualize import draw_signed_network


def main():
    # Parameters
    n = 50
    p_pos = 0.2
    p_neg = 0.2
    max_iter = 30

    # Initial graph
    graph = create_signed_graph(n, p_pos, p_neg)
    draw_signed_network(n, graph, "initial_network.png")

    # Dynamics
    history, final_graph = systematic_relaxation(n, graph, max_iter=max_iter)

    # Final graph
    draw_signed_network(n, final_graph, "final_network.png")

    # Save history to Excel
    df = pd.DataFrame({
        "iteration": list(range(len(history))),
        "unbalanced_triangles": history
    })
    df.to_excel("triangle_balance_history.xlsx", index=False)


if __name__ == "__main__":
    main()

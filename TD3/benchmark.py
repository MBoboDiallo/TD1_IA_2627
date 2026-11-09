
"""Benchmark Minimax, Alpha-Beta and MCTS."""

import matplotlib.pyplot as plt

from game import create_board
from algorithms import minimax, alphabeta, mcts


def benchmark(board, algorithm, **kwargs):
    """Execute an algorithm and collect its performance metrics."""

    result = algorithm(board, **kwargs)

    if algorithm.__name__ == "mcts":
        configuration = f"{kwargs['num_simulations']} simulations"
    else:
        configuration = f"Depth {kwargs['depth']}"

    return {
        "algorithm": algorithm.__name__,
        "configuration": configuration,
        "move": result["move"],
        "score": result["score"],
        "nodes": result["nodes_explored"],
        "time": result["time"]
    }


def main():

    board = create_board()
    results = []

    # 1. Minimax and Alpha-Beta comparison
    depths = [1, 2, 3, 4, 5]

    for depth in depths:

        results.append(
            benchmark(board, minimax, depth=depth)
        )

        results.append(
            benchmark(board, alphabeta, depth=depth)
        )

    # 2. MCTS comparison
    simulations = [100, 500, 1000, 2000]

    for n in simulations:

        results.append(
            benchmark(
                board,
                mcts,
                num_simulations=n,
                seed=42
            )
        )

    # 3. Display results
    print("\n========== BENCHMARK RESULTS ==========\n")

    print(
        f"{'Algorithm':<15}"
        f"{'Configuration':<20}"
        f"{'Move':<8}"
        f"{'Score':<12}"
        f"{'Nodes':<12}"
        f"{'Time (s)':<12}"
    )

    print("-" * 79)

    for r in results:

        print(
            f"{r['algorithm']:<15}"
            f"{r['configuration']:<20}"
            f"{str(r['move']):<8}"
            f"{str(r['score']):<12}"
            f"{r['nodes']:<12}"
            f"{r['time']:<12.6f}"
        )

    # 4. Verify Minimax and Alpha-Beta
    print("\n========== VERIFICATION ==========\n")

    for depth in depths:

        mini = next(
            r for r in results
            if r["algorithm"] == "minimax"
            and r["configuration"] == f"Depth {depth}"
        )

        alpha = next(
            r for r in results
            if r["algorithm"] == "alphabeta"
            and r["configuration"] == f"Depth {depth}"
        )

        print(
            f"Depth {depth}: "
            f"Same score = {mini['score'] == alpha['score']} | "
            f"Same move = {mini['move'] == alpha['move']} | "
            f"Alpha-Beta nodes <= Minimax = "
            f"{alpha['nodes'] <= mini['nodes']}"
        )

    # 5. Graph: explored nodes vs search depth
    minimax_nodes = [
        next(r["nodes"] for r in results
             if r["algorithm"] == "minimax"
             and r["configuration"] == f"Depth {d}")
        for d in depths
    ]

    alphabeta_nodes = [
        next(r["nodes"] for r in results
             if r["algorithm"] == "alphabeta"
             and r["configuration"] == f"Depth {d}")
        for d in depths
    ]

    plt.figure(figsize=(9, 5))

    plt.plot(depths, minimax_nodes, marker="o", label="Minimax")
    plt.plot(depths, alphabeta_nodes, marker="o", label="Alpha-Beta")

    plt.xlabel("Search depth")
    plt.ylabel("Number of explored nodes")
    plt.title("Minimax vs Alpha-Beta")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("comparison_nodes.png")
    plt.close()

    # 6. Graph: MCTS execution time vs simulations
    mcts_times = [
        next(r["time"] for r in results
             if r["algorithm"] == "mcts"
             and r["configuration"] == f"{n} simulations")
        for n in simulations
    ]

    plt.figure(figsize=(9, 5))

    plt.plot(simulations, mcts_times, marker="o")

    plt.xlabel("Number of simulations")
    plt.ylabel("Execution time (seconds)")
    plt.title("MCTS execution time")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("mcts_execution_time.png")
    plt.close()

    print("\n========== GRAPHS GENERATED ==========")
    print("comparison_nodes.png")
    print("mcts_execution_time.png")


if __name__ == "__main__":
    main()

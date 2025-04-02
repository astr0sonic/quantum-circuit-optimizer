import logging
import numpy as np
from src.quantum_circuit.ucr_circuit_optimizer.graph import bfs_single

logger = logging.getLogger(__name__)


def calculate_cnots_counts(
        num_qubits: int, dist_matrix: list[list[int]]
) -> tuple[list[int], list[int]]:
    """
    Count the number of CNOT gates for each target qubit index based on the minimal distances matrix.

    Args:
        num_qubits (int): Number of qubits.
        dist_matrix (list[list[int]]): Matrix of minimal distances between all qubit pairs.

    Returns:
        tuple[list[int], list[int]]: List of optimal target qubit indices and list of CNOT gate counts.
    """
    cnots_counts = []
    for target in range(num_qubits):
        cnots_count = calculate_cnots_count(target, num_qubits, dist_matrix)
        cnots_counts.append(cnots_count)
    optimal_indices = [index for index, val in enumerate(cnots_counts) if val == min(cnots_counts)]
    return (optimal_indices, cnots_counts)


def calculate_cnots_count(target: int, num_qubits: int, distance_matrix: list[list[int]]) -> int:
    """
    Calculate the number of CNOT gates for a fixed target qubit.

    Args:
        target (int): Index of the target qubit.
        num_qubits (int): Number of qubits.
        distance_matrix (list[list[int]]): Matrix of minimal distances.

    Returns:
        int: Number of CNOT gates.
    """
    cnots_count = 0
    current = 2
    for i in range(0, num_qubits - 1):
        control = i if target != i else num_qubits - 1
        d = distance_matrix[control][target]
        cnots_count += current * (2 * d - 1)
        if i != 0:
            current *= 2
    return cnots_count


# --- Implementation of the GraphTargetFinder class ---

class GraphTargetFinder:
    def __init__(self, graph: dict[int, list[int]]):
        """
        Initialize the GraphTargetFinder with a graph.

        Args:
            graph (dict[int, list[int]]): Graph represented as an adjacency list.
        """
        self.graph = graph
        self.vertices = sorted(graph.keys())
        self.n = len(graph)
        # Vector A: for i = 1..n-2, A[i] = 2^(n-1-i); for i = n-1, A = 2.
        self.A = np.array([2 ** (self.n - 1 - i) for i in range(1, self.n - 1)] + [2], dtype=int)
        logger.info(f"Vector A for computing F(v): {self.A}")

    def compute_F(self, v: int) -> int:
        """
        Compute the function F(v) for a given vertex v based on BFS distances.

        Args:
            v (int): Vertex.

        Returns:
            int: Computed F(v) value.
        """
        distances, _ = bfs_single(self.graph, v)
        dist_vals = [d for d in distances.values() if d > 0]
        if not dist_vals:
            return 0
        counts = np.bincount(dist_vals, minlength=self.n)
        F_val, cumulative = 0, 0
        for d in range(1, self.n):
            count = counts[d] if d < len(counts) else 0
            if count:
                F_val += (2 * d - 1) * self.A[cumulative:cumulative + count].sum()
                cumulative += count
        logger.info(f"Computed F({v}) = {F_val}")
        return F_val

    def find_target(self) -> int:
        """
        Find the optimal target qubit (with minimal F(v)).

        Returns:
            int: Index of the optimal target qubit.
        """
        F_values = {v: self.compute_F(v) for v in self.vertices}
        for v, F_v in F_values.items():
            logger.info(f"F({v}) = {F_v}")
        min_F = min(F_values.values())
        target = next(v for v, f in F_values.items() if f == min_F)
        logger.info(f"Optimal target: {target} with F(v) = {min_F}")
        return target

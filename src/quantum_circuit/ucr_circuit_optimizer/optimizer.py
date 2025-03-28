def calculate_cnots_counts(
    num_qubits: int, dist_matrix: list[list[int]]
) -> tuple[list[int], list[int]]:
    """Count the number of CNOT-gates depending on the target qubit's index
    for topology represented by the matrix of the minimal distances between all pairs of qubits

    Args:
        num_qubits (int): number of qubits
        dist_matrix (list[list[int]]): matrix of the minimal distances between all pairs of qubits

    Returns:
        tuple[list[int], list[int]]: list of optimal target qubit's indices and list of CNOT-gates number
    """
    cnots_counts = []
    for target in range(num_qubits):
        cnots_count = calculate_cnots_count(target, num_qubits, dist_matrix)
        cnots_counts.append(cnots_count)
    optimal_indices = [index for index, val in enumerate(cnots_counts) if val == min(cnots_counts)]
    return (optimal_indices, cnots_counts)


def calculate_cnots_count(target: int, num_qubits: int, distance_matrix: list[list[int]]) -> int:
    """Get the number of CNOT-gates for a fixed target qubit

    Args:
        target (int): index of the target qubit
        num_qubits (int): number of qubits
        distance_matrix (list[list[int]]): matrix of the minimal distances between all pairs of qubits

    Returns:
        int: number of CNOT-gates
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


###

# TODO

# class GraphTargetFinder:
#     def __init__(self, graph: dict[int, list[int]]):
#         self.graph = graph
#         self.vertices = sorted(graph.keys())
#         self.n = len(graph)
#         # Вектор A: для i = 1..n-2: A[i]=2^(n-1-i), для i = n-1: 2
#         self.A = np.array([2 ** (self.n - 1 - i) for i in range(1, self.n - 1)] + [2], dtype=int)
#         logger.info(f"Вектор A для расчёта F(v): {self.A}")

#     def compute_F(self, v: int) -> int:
#         distances, _ = bfs_single(self.graph, v)
#         dist_vals = [d for d in distances.values() if d > 0]
#         if not dist_vals:
#             return 0
#         counts = np.bincount(dist_vals, minlength=self.n)
#         F_val, cumulative = 0, 0
#         for d in range(1, self.n):
#             count = counts[d] if d < len(counts) else 0
#             if count:
#                 F_val += (2 * d - 1) * self.A[cumulative:cumulative + count].sum()
#                 cumulative += count
#         logger.info(f"Вычислено F({v}) = {F_val}")
#         return F_val

#     def find_target(self) -> int:
#         F_values = {v: self.compute_F(v) for v in self.vertices}
#         for v, F_v in F_values.items():
#             logger.info(f"F({v}) = {F_v}")
#         min_F = min(F_values.values())
#         target = next(v for v, f in F_values.items() if f == min_F)
#         logger.info(f"Оптимальный target: {target} с F(v) = {min_F}")
#         return target

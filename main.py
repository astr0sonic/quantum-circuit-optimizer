from circuit import get_quantum_circuit
from graph import floyd_warshall, get_matrix_from_edges, get_shortest_paths
from optimizer import optimize_cnots

if __name__ == "__main__":
    # num_qubits = 5
    # edges = [(0, 1), (1, 2), (1, 3), (3, 4)]

    # num_qubits = 5
    # edges = [(0, 1), (1, 2), (2, 3), (3, 4)]

    # num_qubits = 7
    # edges = [(0, 1), (1, 2), (1, 3), (3, 5), (4, 5), (5, 6)]

    num_qubits = 16
    edges = [
        (0, 1),
        (1, 4),
        (4, 7),
        (7, 10),
        (10, 12),
        (12, 15),
        (7, 6),
        (1, 2),
        (2, 3),
        (12, 13),
        (13, 14),
        (3, 5),
        (5, 8),
        (8, 11),
        (11, 14),
        (8, 9),
    ]

    # num_qubits = 27
    # edges = [
    #     (0, 1),
    #     (1, 4),
    #     (4, 7),
    #     (7, 10),
    #     (10, 12),
    #     (12, 15),
    #     (15, 18),
    #     (18, 21),
    #     (21, 23),
    #     (6, 7),
    #     (17, 18),
    #     (1, 2),
    #     (2, 3),
    #     (12, 13),
    #     (13, 14),
    #     (23, 24),
    #     (24, 25),
    #     (3, 5),
    #     (5, 8),
    #     (8, 11),
    #     (11, 14),
    #     (14, 16),
    #     (16, 19),
    #     (19, 22),
    #     (22, 25),
    #     (25, 26),
    #     (8, 9),
    #     (19, 20),
    # ]

    adj_matrix = get_matrix_from_edges(num_qubits, edges)
    dist_matrix, aux_path_matrix = floyd_warshall(adj_matrix)
    optimal_indices, cnots_counts = optimize_cnots(num_qubits, dist_matrix)
    print(f"Optimal indices: {optimal_indices}")
    print(f"CNOTs counts: {cnots_counts}")

    target = optimal_indices[0]
    params = [1.0] * (2**num_qubits)
    path_matrix = get_shortest_paths(aux_path_matrix)
    qc = get_quantum_circuit(target, num_qubits, params, path_matrix)

from graph import floyd_warshall, get_matrix_from_edges
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

    adj_matrix = get_matrix_from_edges(num_qubits, edges)
    dist_matrix, path_matrix = floyd_warshall(adj_matrix)
    optimal_indices, cnots_count = optimize_cnots(num_qubits, dist_matrix)
    print(optimal_indices)
    print(cnots_count)

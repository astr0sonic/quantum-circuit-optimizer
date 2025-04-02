from src.quantum_circuit.quantum_hashing_circuit.circuit import (
    get_quantum_hashing_circuit,
)
from src.quantum_circuit.ucr_circuit_optimizer.graph import (
    floyd_warshall,
    get_matrix_from_edges,
    get_shortest_paths,
    matrix_to_adj_list,
    bfs_single,
    reconstruct_path,
)

import logging

# Configure logging immediately
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler("quantum_circuit.log", mode="w")
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

import matplotlib

from src.quantum_circuit.ucr_circuit_optimizer.optimizer import (
    GraphTargetFinder,
)
from src.quantum_circuit.quantum_hashing_circuit.circuit import get_quantum_circuit2
from src.quantum_computer.architectures import *
from src.quantum_circuit.ucr_circuit_optimizer.optimizer import calculate_cnots_counts
from src.utils import show_quantum_circuit

# Configure matplotlib
matplotlib.use('TkAgg')
matplotlib.rcParams.update({'font.size': 8})


def optimize_1() -> None:
    num_qubits = FALCON_R511H_NUM_QUBITS
    edges = FALCON_R511H_EDGES

    adj_matrix = get_matrix_from_edges(num_qubits, edges)
    dist_matrix, aux_path_matrix = floyd_warshall(adj_matrix)
    optimal_indices, cnots_counts = calculate_cnots_counts(num_qubits, dist_matrix)
    print(f"Optimal indices: {optimal_indices}")
    print(f"CNOTs counts: {cnots_counts}")

    target = optimal_indices[0]
    params = [i for i in range(2 ** (num_qubits - 1))]
    path_matrix = get_shortest_paths(aux_path_matrix)
    is_amplitude_form = True
    qc = get_quantum_hashing_circuit(target, num_qubits, params, is_amplitude_form, path_matrix)


# TODO
def optimize_2() -> None:
    """
    Optimization method 2:
    - Builds the adjacency matrix for the qubit network.
    - Determines the optimal target qubit based on the minimal F(v) computed via BFS.
    - Constructs the quantum circuit and displays it.
    """
    matrix = [
        [0, 1, 0, 0, 0],
        [1, 0, 1, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 1],
        [0, 0, 0, 1, 0],
    ]
    logger.info("Original adjacency matrix:")
    for row in matrix:
        logger.info(",".join(map(str, row)))

    graph = matrix_to_adj_list(matrix)
    finder = GraphTargetFinder(graph)
    target = finder.find_target()
    logger.info(f"Optimal target qubit (optimized by F(v)): {target}")

    dist_m, parents_m = bfs_single(graph, target)
    paths_from_target = {
        v: ([v] if v == target else reconstruct_path(target, v, parents_m))
        for v in graph
    }

    num_qubits = len(matrix)
    params = [float(i + 1) for i in range(2 ** (num_qubits - 1))]

    qc = get_quantum_circuit2(target, num_qubits, params, paths_from_target)
    cnot_count = qc.count_ops().get('cx', 0)
    logger.info(f"Total number of CNOT gates: {cnot_count}")

    diagram = qc.draw(
        output='mpl', fold=60, vertical_compression='high',
        idle_wires=False, scale=1
    )
    diagram.tight_layout(pad=0.1)
    diagram.subplots_adjust(top=1.0, bottom=0.0, left=0.0, right=1.0)
    show_quantum_circuit(diagram.figure)


if __name__ == "__main__":
    optimize_2()

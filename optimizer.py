from sympy.combinatorics import GrayCode

from utils import get_diff_index


def optimize_cnots(num_qubits: int, dist_matrix: list[list[int]]) -> tuple[list[int], list[int]]:
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
        cnots_count = get_cnots_count(target, num_qubits, dist_matrix)
        cnots_counts.append(cnots_count)
    optimal_indices = [index for index, val in enumerate(cnots_counts) if val == min(cnots_counts)]
    return (optimal_indices, cnots_counts)


def get_cnots_count(target: int, num_qubits: int, distance_matrix: list[list[int]]) -> int:
    """Get the number of CNOT-gates for a fixed target qubit

    Args:
        target (int): index of the target qubit
        num_qubits (int): number of qubits
        distance_matrix (list[list[int]]): matrix of the minimal distances between all pairs of qubits

    Returns:
        int: number of CNOT-gates
    """
    cnots_count = 0
    current_code = GrayCode(num_qubits - 1)
    for _ in range(0, 2 ** (num_qubits - 2)):
        control = get_diff_index(current_code, target, num_qubits)
        current_cnots_count = 2 * distance_matrix[control][target] - 1
        cnots_count += current_cnots_count
        current_code = current_code.next()
    return cnots_count * 2

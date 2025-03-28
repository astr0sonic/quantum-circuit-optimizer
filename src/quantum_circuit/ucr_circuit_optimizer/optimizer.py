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

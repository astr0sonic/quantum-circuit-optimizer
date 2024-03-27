from sympy.combinatorics import GrayCode


def get_diff_index(current_code: GrayCode, target: int, num_qubits: int) -> int:
    """Get the index of the differing bit between 2 adjacent Gray code words

    Args:
        current (GrayCode): first Gray code word
        target (int): index of the target qubit
        num_qubits (int): number of qubits

    Returns:
        int: differing index in [0, num_qubits - 1]
    """
    current = current_code.current
    next = current_code.next().current
    for i in range(len(current)):
        if current[i] != next[i]:
            diff_index = i
    if diff_index == target:
        diff_index = num_qubits - 1
    return diff_index

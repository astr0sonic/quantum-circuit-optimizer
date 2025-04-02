import logging
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import RYGate, RZGate

from src.quantum_circuit.ucr_circuit_optimizer.circuit import get_ucr_circuit

logger = logging.getLogger(__name__)


def get_quantum_hashing_circuit(
        target: int,
        num_qubits: int,
        params: list[float],
        is_amplitude_form: bool,
        path_matrix: list[list[list[int]]],
) -> QuantumCircuit:
    """
    Construct a quantum circuit for quantum hashing adapted to the specific architecture.

    Args:
        target (int): Index of the target qubit.
        num_qubits (int): Number of qubits.
        params (list[float]): List of parameters (rotation angles).
        is_amplitude_form (bool): Indicates whether the amplitude form (True) or phase form (False) is used.
        path_matrix (list[list[list[int]]]): Matrix of the shortest paths between all pairs of qubits.

    Returns:
        QuantumCircuit: Quantum circuit for quantum hashing adapted to the specific architecture.
    """
    hadamard_layer_circuit = QuantumCircuit(num_qubits)
    apply_hadamard(hadamard_layer_circuit, target)

    rotation_gate = RYGate if is_amplitude_form else RZGate
    ucr_circuit = get_ucr_circuit(target, num_qubits, params, rotation_gate, path_matrix)
    result_qc = hadamard_layer_circuit.compose(ucr_circuit)
    return result_qc


def apply_hadamard(qc: QuantumCircuit, target: int) -> None:
    """
    Apply the Hadamard gate to each qubit in the circuit, except for the target qubit.

    Args:
        qc (QuantumCircuit): Quantum circuit.
        target (int): Index of the target qubit (in [0, qc.num_qubits - 1]).
    """
    for i in range(qc.num_qubits):
        if i == target:
            continue
        qc.h(i)
    qc.barrier()


def compute_M(k: int) -> np.ndarray:
    """
    Compute the matrix M based on binary and Gray codes.

    Args:
        k (int): Number of bits.

    Returns:
        np.ndarray: Computed matrix M.
    """
    N = 2 ** k
    arr = np.arange(N)
    b = ((arr[:, None] >> np.arange(k)) & 1).astype(np.int8)
    gray_ints = arr ^ (arr >> 1)
    g = ((gray_ints[:, None] >> np.arange(k)) & 1).astype(np.int8)
    dot = (b @ g.T) & 1
    M = np.where(dot == 0, 1, -1)
    logger.debug(f"Matrix M for k={k}:\n{M}")
    return M


def compute_a(a: list[float], k: int) -> np.ndarray:
    """
    Compute the transformed vector a' using matrix M.

    Args:
        a (list[float]): Input vector.
        k (int): Number of bits (should satisfy len(a) == 2^k).

    Returns:
        np.ndarray: Computed vector a'.
    """
    if len(a) != 2 ** k:
        raise ValueError(f"Length of params must be 2^k={2 ** k}, got {len(a)}")
    M = compute_M(k)
    a_arr = np.array(a, dtype=float)
    a_prime = (1 / (2 ** k)) * (M.T @ a_arr)
    logger.info(f"Input vector a: {a}")
    logger.info(f"Computed vector a':\n{a_prime}")
    return a_prime


def get_quantum_circuit2(
        target: int, num_qubits: int, params: list[float], paths_from_target: dict[int, list[int]]
) -> QuantumCircuit:
    """
    Assemble a quantum circuit using the unrolled ladder algorithm for implementing CNOT gates.

    Args:
        target (int): Index of the target qubit.
        num_qubits (int): Number of qubits.
        params (list[float]): List of parameters (rotation angles).
        paths_from_target (dict[int, list[int]]): Dictionary of paths from the target qubit.

    Returns:
        QuantumCircuit: Assembled quantum circuit.
    """
    qc = QuantumCircuit(num_qubits)
    apply_hadamard(qc, target)
    k = num_qubits - 1
    a_prime = compute_a(params, k)
    controls = sorted([q for q in range(num_qubits) if q != target],
                      key=lambda c: len(paths_from_target[c]) - 1)
    logger.info(f"Control qubits (sorted by path length): {controls}")
    N = 2 ** k
    gray_codes = compute_gray_codes(k)
    for i in range(N):
        logger.info(f"Iteration {i}: applying Ry({a_prime[i]}) to target {target}")
        qc.ry(a_prime[i], target)
        qc.barrier()
        next_idx = (i + 1) % N
        diff_idx = get_diff_index(gray_codes[i], gray_codes[next_idx])
        if diff_idx >= 0:
            controlling = controls[diff_idx]
            path_ct = list(reversed(paths_from_target[controlling]))
            logger.info(f"Gray code diff at iteration {i}: control qubit {controlling}, path {path_ct}")
            if len(path_ct) == 2:
                qc.cx(path_ct[0], path_ct[1])
            else:
                unrolled_ladder(qc, path_ct)
            qc.barrier()
    return qc


def unrolled_ladder(qc: QuantumCircuit, path: list[int]) -> None:
    """
    Implement the 'ladder' structure for sequential CNOT gates along the specified path.

    Args:
        qc (QuantumCircuit): Quantum circuit.
        path (list[int]): List of qubits representing the path.
    """
    d = len(path) - 1
    if d <= 0:
        return
    if d == 1:
        logger.info(f"Single CNOT: {path[0]} -> {path[1]}")
        qc.cx(path[0], path[1])
        return
    logger.info(f"Ladder: path={path}, d={d}, number of CNOT gates={2 * d - 1}")
    for i in range(d):
        qc.cx(path[i], path[i + 1])
    for i in range(d - 1)[::-1]:
        qc.cx(path[i], path[i + 1])


def get_diff_index(code1: np.ndarray, code2: np.ndarray) -> int:
    """
    Find the index of the first differing bit between two Gray codes.

    Args:
        code1 (np.ndarray): First Gray code.
        code2 (np.ndarray): Second Gray code.

    Returns:
        int: Index of the first differing bit, or -1 if the codes are identical.
    """
    diff = np.flatnonzero(code1 != code2)
    return int(diff[0]) if diff.size else -1


def compute_gray_codes(k: int) -> np.ndarray:
    """
    Generate Gray codes for a given number of bits k.

    Args:
        k (int): Number of bits.

    Returns:
        np.ndarray: Array of Gray codes.
    """
    N = 2 ** k
    gray_ints = np.arange(N) ^ (np.arange(N) >> 1)
    codes = ((gray_ints[:, None] >> np.arange(k)) & 1).astype(np.int8)
    logger.info(f"Gray codes for k={k}: generated {N} codes")
    return codes

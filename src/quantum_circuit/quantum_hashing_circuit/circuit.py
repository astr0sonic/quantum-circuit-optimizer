from qiskit import QuantumCircuit
from sympy.combinatorics import GrayCode

from src.quantum_circuit.ucr_circuit_optimizer.utils import get_diff_index


def get_quantum_circuit(
    target: int,
    num_qubits: int,
    params: list[float],
    path_matrix: list[list[list[int]]],
) -> QuantumCircuit:
    """Construct a for quantum hashing/fingerprinting adopted for the topology represented by the matrix
    of the shortest paths between all pairs of qubits

    Args:
        target (int): index of the target qubit
        num_qubits (int): _number of qubits
        params (list[float]): list of parameters of the scheme
        path_matrix (list[list[list[int]]]): matrix of the shortest paths between all pairs of qubits

    Returns:
        QuantumCircuit: adopted quantum circuit
    """
    qc = QuantumCircuit(num_qubits)
    apply_hadamard(qc)

    current_code = GrayCode(num_qubits - 1)
    for i in range(0, 2 ** (num_qubits - 1)):
        qc.ry(params[i], target)
        qc.barrier()

        control = get_diff_index(current_code, target, num_qubits)
        path = path_matrix[control][target]
        rev_path = list(reversed(path))

        for i in range(len(path) - 1):
            qc.cx(path[i], path[i + 1])
        for i in range(1, len(rev_path) - 1):
            qc.cx(rev_path[i + 1], rev_path[i])
        qc.barrier()

        current_code = current_code.next()

    return qc


def apply_hadamard(qc: QuantumCircuit) -> None:
    """Apply Hadamard gate for each qubit in the circuit

    Args:
        qc (QuantumCircuit): quantum circuit
    """
    for i in range(qc.num_qubits):
        qc.h(i)

from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from sympy.combinatorics import GrayCode

from src.quantum_circuit.ucr_circuit_optimizer.utils import get_diff_index


def get_ucr_circuit(
    target: int,
    num_qubits: int,
    params: list[float],
    rotation_gate: Gate,
    path_matrix: list[list[list[int]]],
) -> QuantumCircuit:
    """Construct a quantum circuit for uniformly controlled rotation that is adapted to the specific architecture
    (that represented by the matrix of the shortest paths between all pairs of qubits).

    Args:
        target (int): index of the target qubit
        num_qubits (int): number of the qubits
        params (list[float]): list of the parameters (rotation angles)
        rotation_gate (Gate): rotation gate (Ry or Rz)
        path_matrix (list[list[list[int]]]): matrix of the shortest paths between all pairs of qubits

    Returns:
        QuantumCircuit: quantum circuit for iniformly controlled rotation adapted to the specific architecture
    """
    qc = QuantumCircuit(num_qubits)

    current_code = GrayCode(num_qubits - 1)
    for i in range(0, 2 ** (num_qubits - 1)):
        qc.append(rotation_gate(params[i]), [target])
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

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
    (represented by the matrix of the shortest paths between all pairs of qubits).

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
        apply_rotation(qc, target, rotation_gate, params[i])
        control = get_control_index(target, num_qubits, current_code)
        apply_cnots(qc, target, control, path_matrix)
        current_code = current_code.next()
    return qc


def get_control_index(target: int, num_qubits: int, current_code: GrayCode) -> int:
    control = get_diff_index(current_code, target, num_qubits)
    return control


def apply_rotation(qc: QuantumCircuit, target: int, rotation_gate: Gate, angle: float) -> None:
    qc.append(rotation_gate(angle), [target])
    qc.barrier()


def apply_cnots(
    qc: QuantumCircuit, target: int, control: int, path_matrix: list[list[list[int]]]
) -> None:
    """Apply the CNOT gate according to the architecture restrictions.

    Args:
        qc (QuantumCircuit): quantum circuit
        target (int): index of the target qubit
        control (int): index of the control qubit
        path_matrix (list[list[list[int]]]): matrix of the shortest paths between all pairs of qubits
    """
    path = path_matrix[control][target]
    rev_path = list(reversed(path))

    for i in range(len(path) - 1):
        qc.cx(path[i], path[i + 1])
    for i in range(1, len(rev_path) - 1):
        qc.cx(rev_path[i + 1], rev_path[i])
    qc.barrier()

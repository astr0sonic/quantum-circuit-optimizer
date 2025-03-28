from qiskit import QuantumCircuit
from qiskit.circuit.library import RYGate, RZGate

from src.quantum_circuit.ucr_circuit_optimizer.circuit import get_ucr_circuit


def get_quantum_hashing_circuit(
    target: int,
    num_qubits: int,
    params: list[float],
    is_amplitude_form: bool,
    path_matrix: list[list[list[int]]],
) -> QuantumCircuit:
    """Construct a quantum circuit for quantum hashing that is adapted to the specific architecture
    (that represented by the matrix of the shortest paths between all pairs of qubits).

    Args:
        target (int): index of the target qubit
        num_qubits (int): number of the qubits
        params (list[float]): list of the parameters (rotation angles)
        is_amplitude_form (bool): indicates whether the amplitude form (True) or the phase form (False) is used
        path_matrix (list[list[list[int]]]): matrix of the shortest paths between all pairs of qubits

    Returns:
        QuantumCircuit: quantum circuit for quantum hashing adapted to the specific architecture
    """
    hadamard_layer_circuit = QuantumCircuit(num_qubits)
    apply_hadamard(hadamard_layer_circuit, target)

    rotation_gate = RYGate if is_amplitude_form else RZGate
    ucr_circuit = get_ucr_circuit(target, num_qubits, params, rotation_gate, path_matrix)
    result_qc = hadamard_layer_circuit.compose(ucr_circuit)
    return result_qc


def apply_hadamard(qc: QuantumCircuit, target: int) -> None:
    """Apply the Hadamard gate to each qubit in the circuit, except for the target qubit

    Args:
        qc (QuantumCircuit): quantum circuit
        target (int): index of the target qubit (in [0, qc.num_qubits - 1])
    """
    for i in range(qc.num_qubits):
        if i == target:
            continue
        qc.h(i)
    qc.barrier()

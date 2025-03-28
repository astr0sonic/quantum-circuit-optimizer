import numpy as np


def compute_M_matrix(k: int) -> np.ndarray:
    """
    Computes the matrix M of size (2^k x 2^k), where
    M[i, j] = (-1)^{b[i - 1] * g[j - 1]} for i, j in [1, 2^k],
    b[i] is the standard binary representation of the number i (with leading zeros up to the length k),
    g[j] is the Gray code for the number j,
    and the dot product is computed modulo 2.
    """
    N = 2**k
    indices = np.arange(N)

    # Standard binary representation of numbers from 0 to N-1
    B = ((indices[:, None] >> np.arange(k - 1, -1, -1)) & 1).astype(np.int64)

    # Compute the Gray codes for numbers from 0 to N-1: gray = n ^ (n >> 1)
    gray_indices = indices ^ (indices >> 1)
    G = ((gray_indices[:, None] >> np.arange(k - 1, -1, -1)) & 1).astype(np.int64)

    # Compute the matrix dot product modulo 2
    dot_mod2 = (B @ G.T) % 2

    # Compute M: (-1)^(dot_mod2)
    M = (-1) ** dot_mod2
    return M


def compute_modified_params(params: list[float], num_control_qubits: int) -> list[float]:
    """
    Computes the transformed vector a' using the formula:
      a' = 2^{-k} * (M^T) * a,
    where M is the matrix computed by compute_M_matrix, and a is the given vector.

    Parameters:
      num_control_qubits - a natural number (k) determining the size of the matrix (2^k x 2^k).
      params - the input vector.

    Returns:
      The transformed vector a' as a Python list of floats.
    """
    k = num_control_qubits

    a = np.array(params, dtype=np.float64)
    M = compute_M_matrix(k)
    modified_a = (2 ** (-k)) * (M.T @ a)
    return modified_a.tolist()

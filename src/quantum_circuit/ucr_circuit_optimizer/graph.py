import logging
from collections import deque

logger = logging.getLogger(__name__)

INFINITY = 1_000_000_000_000


def floyd_warshall(matrix: list[list[bool]]) -> tuple[list[list[int]], list[list[int]]]:
    """
    Floyd-Warshall algorithm for an unweighted, undirected graph.

    Args:
        matrix (list[list[bool]]): Adjacency matrix of the unweighted, undirected graph.

    Returns:
        tuple[list[list[int]], list[list[int]]]: Matrix of the shortest path lengths between all vertex pairs
        and an auxiliary matrix (of next vertices) for path reconstruction.
    """
    n = len(matrix)
    dist = [[1 if matrix[i][j] else 0 if i == j else INFINITY for j in range(n)] for i in range(n)]
    nxt = [[j if matrix[i][j] else i if i == j else -1 for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    continue
                if dist[i][k] == INFINITY or dist[k][j] == INFINITY:
                    continue
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    dist[j][i] = dist[i][j]
                    nxt[i][j] = nxt[i][k]
                    nxt[j][i] = nxt[j][k]
    return (dist, nxt)


def get_matrix_from_edges(num_vertices: int, edges: list[tuple[int, int]]) -> list[list[bool]]:
    """
    Generate an adjacency matrix for an unweighted, undirected graph from its list of edges.

    Args:
        num_vertices (int): Number of vertices.
        edges (list[tuple[int, int]]): List of edges.

    Returns:
        list[list[bool]]: Adjacency matrix.
    """
    matrix = [[False for _ in range(num_vertices)] for _ in range(num_vertices)]
    for edge in edges:
        i, j = edge
        matrix[i][j] = matrix[j][i] = True
    return matrix


def get_shortest_paths(next: list[list[int]]) -> list[list[list[int]]]:
    """
    Get the matrix of shortest paths between all pairs of vertices using the auxiliary matrix
    from the Floyd-Warshall algorithm.

    Args:
        next (list[list[int]]): Auxiliary matrix for path reconstruction.

    Returns:
        list[list[list[int]]]: Matrix of shortest paths between all vertex pairs.
    """
    n = len(next)
    min_paths: list[list[list[int]]] = [[[] for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            min_paths[i][j] = get_shortest_path(i, j, next)
            min_paths[j][i] = list(reversed(min_paths[i][j]))
    return min_paths


def get_shortest_path(i: int, j: int, next: list[list[int]]) -> list[int]:
    """
    Reconstruct the shortest path between vertices i (start) and j (end) using the auxiliary matrix.

    Args:
        i (int): Start vertex.
        j (int): End vertex.
        next (list[list[int]]): Auxiliary matrix for path reconstruction.

    Returns:
        list[int]: List of vertices representing the shortest path.
    """
    path = [i]
    next_vertex = next[i][j]
    while next_vertex != j:
        path.append(next_vertex)
        next_vertex = next[next_vertex][j]
    if i != j:
        path.append(j)
    return path


# --- Implementation of functions to be inserted ---

def matrix_to_adj_list(matrix: list[list[int]]) -> dict[int, list[int]]:
    """
    Convert an adjacency matrix into an adjacency list (dictionary).

    Args:
        matrix (list[list[int]]): Adjacency matrix.

    Returns:
        dict[int, list[int]]: Adjacency list.
    """
    adj_list = {i: [j for j, val in enumerate(row) if val] for i, row in enumerate(matrix)}
    logger.info(f"Converted matrix to adjacency list: {adj_list}")
    return adj_list


def bfs_single(graph: dict[int, list[int]], start: int):
    """
    Perform a breadth-first search (BFS) on a graph starting from the given vertex.

    Args:
        graph (dict[int, list[int]]): Graph represented as an adjacency list.
        start (int): Starting vertex.

    Returns:
        tuple[dict[int, int], dict[int, int]]: Distances and parent pointers.
    """
    distances = {start: 0}
    parents = {start: None}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        for nxt in graph[cur]:
            if nxt not in distances:
                distances[nxt] = distances[cur] + 1
                parents[nxt] = cur
                queue.append(nxt)
    logger.debug(f"BFS from vertex {start}: {distances}")
    return distances, parents


def reconstruct_path(start: int, end: int, parents: dict[int, int]) -> list[int]:
    """
    Reconstruct the path from start to end using parent pointers from BFS.

    Args:
        start (int): Starting vertex.
        end (int): Ending vertex.
        parents (dict[int, int]): Parent pointers from BFS.

    Returns:
        list[int]: The reconstructed path, or an empty list if unreachable.
    """
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = parents.get(cur)
    path.reverse()
    logger.debug(f"Path reconstructed from {start} to {end}: {path}")
    return path if path and path[0] == start else []

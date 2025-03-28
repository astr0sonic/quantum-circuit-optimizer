INFINITY = 1_000_000_000_000


def floyd_warshall(matrix: list[list[bool]]) -> tuple[list[list[int]], list[list[int]]]:
    """Floyd-Warshall algorithm for an unweighted, undirected graph

    Args:
        matrix (list[list[bool]]): adjacency matrix of the unweighted, undirected graph

    Returns:
        tuple[list[list[int]], list[list[int]]]: matrix of the lengths of the shortest paths
        between all pairs of vertices and auxiliary matrix (of next vertices) for shortest path reconstruction
    """
    n = len(matrix)
    dist = [[1 if matrix[i][j] else 0 if i == j else INFINITY for j in range(n)] for i in range(n)]
    next = [[j if matrix[i][j] else i if i == j else -1 for j in range(n)] for i in range(n)]
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
                    next[i][j] = next[i][k]
                    next[j][i] = next[j][k]
    return (dist, next)


def get_matrix_from_edges(num_vertices: int, edges: list[tuple[int, int]]) -> list[list[bool]]:
    """Get an adjacency matrix of the unweighted, undirected graph from its list of edges

    Args:
        num_vertices (int): number of the vertices
        edges (list[tuple[int, int]]): list of the edges

    Returns:
        list[list[bool]]: adjacency matrix
    """
    matrix = [[False for _ in range(num_vertices)] for _ in range(num_vertices)]
    for edge in edges:
        i = edge[0]
        j = edge[1]
        matrix[i][j] = matrix[j][i] = True
    return matrix


def get_shortest_paths(next: list[list[int]]) -> list[list[list[int]]]:
    """Get the matrix of the shortest paths between all pairs of vertices
    using the auxiliary matrix of the Floyd-Warshall algorithm output

    Args:
        next (list[list[int]]): auxiliary matrix for shortest path reconstruction

    Returns:
        list[list[list[int]]]: matrix of the shortest paths between all pairs of vertices
    """
    n = len(next)
    min_paths: list[list[list[int]]] = [[[] for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            min_paths[i][j] = get_shortest_path(i, j, next)
            min_paths[j][i] = list(reversed(min_paths[i][j]))
    return min_paths


def get_shortest_path(i: int, j: int, next: list[list[int]]) -> list[int]:
    """Get the shortest path between the vertices i (start) and j (finish)
    using the auxiliary matrix of the Floyd-Warshall algorithm output

    Args:
        i (int): start vertex
        j (int): finish vertex
        next (list[list[int]]): auxiliary matrix for shortest path reconstruction

    Returns:
        list[int]: list of the vertices that is the shortest path
    """
    path = [i]
    next_vertex = next[i][j]
    while next_vertex != j:
        path.append(next_vertex)
        next_vertex = next[next_vertex][j]
    if i != j:
        path.append(j)
    return path


###


# TODO
def matrix_to_adj_list(matrix: list[list[int]]) -> dict[int, list[int]]:
    pass


# TODO
def bfs_single(graph: dict[int, list[int]], start: int):
    pass


# TODO
def reconstruct_path(start: int, end: int, parents: dict[int, int]) -> list[int]:
    pass

from collections import deque
import heapq
from entorno_db import Node

def breadth_first_search(problem):
    """Búsqueda en Anchura (BFS) - No informada."""
    node = Node(problem.initial)
    if problem.is_goal(node.state):
        return node, 1
    
    frontier = deque([node])
    explored = set()
    nodes_expanded = 0

    while frontier:
        node = frontier.popleft()
        nodes_expanded += 1
        explored.add(node.state)

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                if problem.is_goal(child.state):
                    return child, nodes_expanded
                frontier.append(child)
                
    return None, nodes_expanded


def depth_first_search(problem):
    """Búsqueda en Profundidad (DFS) - No informada."""
    node = Node(problem.initial)
    if problem.is_goal(node.state):
        return node, 1
    
    frontier = [node]
    explored = set()
    nodes_expanded = 0

    while frontier:
        node = frontier.pop()
        nodes_expanded += 1
        explored.add(node.state)

        if problem.is_goal(node.state):
            return node, nodes_expanded

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
                
    return None, nodes_expanded


def heuristic(state):
    """
    Función heurística admisible h(s).
    Estima el costo mínimo restante hacia la meta sin sobreestimar.
    """
    C, M, F, S, I = state
    h_cpu = max(0, C - 40) * 0.05
    h_sec = S * 1.0
    h_frag = F * 0.3
    h_idx = (1 - I) * 4.0
    return h_cpu + h_sec + h_frag + h_idx


def a_star_search(problem):
    """Búsqueda Informada A* utilizando f(n) = g(n) + h(n)."""
    start_node = Node(problem.initial)
    frontier = []
    heapq.heappush(frontier, (heuristic(start_node.state), 0, start_node))
    explored = set()
    nodes_expanded = 0
    counter = 1

    while frontier:
        _, _, node = heapq.heappop(frontier)
        
        if problem.is_goal(node.state):
            return node, nodes_expanded

        if node.state in explored:
            continue

        explored.add(node.state)
        nodes_expanded += 1

        for child in node.expand(problem):
            if child.state not in explored:
                f_child = child.path_cost + heuristic(child.state)
                heapq.heappush(frontier, (f_child, counter, child))
                counter += 1
                
    return None, nodes_expanded
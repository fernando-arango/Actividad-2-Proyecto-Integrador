class DatabaseOptimizationProblem:
    """
    Formalización del espacio de estados para el agente de optimización,
    mantenimiento y seguridad en PostgreSQL.
    Estado: (CPU %, RAM %, Fragmentación [0-10], Amenaza [0-2], Índices [0-1])
    """
    def __init__(self, initial_state):
        self.initial = initial_state

    def actions(self, state):
        C, M, F, S, I = state
        acts = []
        if S > 0:
            acts.append('BLOCK_IP')
        if C > 50 or M > 60:
            acts.append('CANCEL_BACKEND')
        if F > 2:
            acts.append('REINDEX_VACUUM')
        if I == 0:
            acts.append('CREATE_INDEX')
        return acts if acts else ['NOP']

    def result(self, state, action):
        C, M, F, S, I = state
        if action == 'BLOCK_IP':
            return (max(0, C - 20), max(0, M - 10), F, 0, I)
        elif action == 'CANCEL_BACKEND':
            return (max(0, C - 30), max(0, M - 20), F, S, I)
        elif action == 'CREATE_INDEX':
            return (min(100, C + 10), M, max(0, F - 3), S, 1)
        elif action == 'REINDEX_VACUUM':
            return (min(100, C + 10), M, 0, S, I)
        return state

    def is_goal(self, state):
        C, M, F, S, I = state
        return C <= 40 and M <= 50 and F <= 2 and S == 0 and I == 1

    def step_cost(self, state, action):
        costs = {
            'BLOCK_IP': 1,
            'CANCEL_BACKEND': 2,
            'CREATE_INDEX': 4,
            'REINDEX_VACUUM': 5,
            'NOP': 0
        }
        return costs.get(action, 1)


class Node:
    """Representa un nodo dentro del árbol de búsqueda."""
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def expand(self, problem):
        return [
            Node(
                state=problem.result(self.state, action),
                parent=self,
                action=action,
                path_cost=self.path_cost + problem.step_cost(self.state, action)
            )
            for action in problem.actions(self.state)
        ]

    def solution(self):
        """Reconstruye la secuencia de acciones desde el estado inicial hasta este nodo."""
        actions = []
        node = self
        while node.parent is not None:
            actions.append(node.action)
            node = node.parent
        actions.reverse()
        return actions

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)
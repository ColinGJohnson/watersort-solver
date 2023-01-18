from typing import List

from src.solver import WaterSortProblem
from src.solver.PriorityQueue import PriorityQueue
from src.solver.SearchTreeNode import SearchTreeNode
from src.solver.Types import GameState, Action, Tube
from src.solver.WaterSortProblem import is_complete


def best_first_graph_search(problem: WaterSortProblem, f):
    """Search nodes with minimum f(node) value first."""

    node = SearchTreeNode(problem.initial)
    frontier = PriorityQueue([node], key=f)
    reached = {problem.initial: node}

    while frontier:
        node = frontier.pop()
        if is_complete(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)

    raise Exception("Failed to find a solution.")


def expand(problem, node):
    """Expand a node, generating the children nodes."""
    state = node.state
    for action in problem.actions(state):
        next_state = problem.result(state, action)
        cost = node.path_cost + problem.action_cost(state, action, next_state)
        yield SearchTreeNode(next_state, node, action, cost)


def path_actions(node: SearchTreeNode):
    """The sequence of actions to get to this node."""
    if node.parent is None:
        return []
    return path_actions(node.parent) + [node.action]


def path_states(node: SearchTreeNode) -> List[GameState]:
    """The sequence of states to get to this node."""
    return path_states(node.parent) + [node.state]


def astar_search(problem: WaterSortProblem, h=None):
    """Search nodes with minimum f(n) = g(n) + h(n)."""
    h = h or problem.h
    return best_first_graph_search(problem, f=lambda n: g(n) + h(n))

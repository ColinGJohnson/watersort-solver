from typing import List, Callable, Iterable

from watersort.solver.PriorityQueue import PriorityQueue
from watersort.solver import WaterSortProblem
from watersort.solver.WaterSortNode import SearchTreeNode
from watersort.solver.WaterSortTypes import GameState, Action
from watersort.solver.WaterSortProblem import is_complete, get_actions, pour, num_boundaries


def weighted_astar_search(problem: WaterSortProblem) -> SearchTreeNode:
    """Search nodes with minimum (num moves + color boundaries) first, with extra weight on color boundaries."""
    return best_first_graph_search(problem, f=lambda node: node.path_cost + 1.1 * num_boundaries(node.state))


def astar_search(problem: WaterSortProblem) -> SearchTreeNode:
    """Search nodes with minimum (num moves + color boundaries) first."""
    return best_first_graph_search(problem, f=lambda node: node.path_cost + num_boundaries(node.state))


def greedy_search(problem: WaterSortProblem) -> SearchTreeNode:
    """Search nodes with minimum color boundaries first."""
    return best_first_graph_search(problem, f=lambda node: num_boundaries(node.state))


def uniform_cost_search(problem: WaterSortProblem) -> SearchTreeNode:
    """Search nodes with minimum num moves first. This is also a breadth first search since move cost is 1."""
    return best_first_graph_search(problem, f=lambda node: node.path_cost)


def best_first_graph_search(problem: WaterSortProblem, f: Callable[[SearchTreeNode], int]) -> SearchTreeNode:
    """Search nodes with minimum f(node) value first."""

    node = SearchTreeNode(problem.initial_state)
    frontier = PriorityQueue([node], key=f)
    reached = {repr(problem.initial_state): node}

    i = 0

    while frontier:
        i += 1
        node = frontier.pop()
        if is_complete(node.state):
            print("actions checked", i)
            return node
        for child in expand(problem, node):
            child_state_hash = repr(child.state)
            if child_state_hash not in reached or child.path_cost < reached[child_state_hash].path_cost:
                reached[child_state_hash] = child
                frontier.add(child)

    raise Exception("Failed to find a solution.")


def expand(problem: WaterSortProblem, node: SearchTreeNode) -> Iterable[SearchTreeNode]:
    """Expand a node, generating its child nodes."""
    state = node.state
    for action in get_actions(problem.tube_capacity, state):
        next_state = pour(problem.tube_capacity, state, action)
        cost = node.path_cost + 1
        yield SearchTreeNode(next_state, node, action, cost)


def path_actions(node: SearchTreeNode) -> List[Action]:
    """The sequence of actions to get to this node."""
    if node.parent is None:
        return []
    return path_actions(node.parent) + [node.action]


def path_states(node: SearchTreeNode) -> List[GameState]:
    """The sequence of states to get to this node."""
    if node.parent is None:
        return []
    return path_states(node.parent) + [node.state]

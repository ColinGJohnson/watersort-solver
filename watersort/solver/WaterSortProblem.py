import copy
import logging
from typing import Set

from watersort.solver.WaterSortTypes import GameState, Action, Tube


def is_complete(state: GameState):
    """Tests if the given puzzle state is a winner."""
    seen_colors = set()
    for tube in state:
        colors = set(tube)
        if len(colors) == 1:
            color = colors.pop()
            if color in seen_colors:
                return False
            seen_colors.add(color)
        elif len(colors) > 1:
            return False
    return True


def pour(tube_capacity: int, state: GameState, action: Action):
    """Gets the state that results from making a pour (action) on a game state. The last item in state[action[0]] is
    appended to state[action[1]] until there is no more of the same color left in the source, or there is no more
    capacity in the sink."""
    modified = copy.deepcopy(state)
    source_index = action[0]
    sink_index = action[1]

    if len(state[source_index]) == 0:
        logging.warning("Poured from an empty tube.")
        return modified

    top_color = state[source_index][-1]
    while len(modified[source_index]) > 0 \
            and modified[source_index][-1] == top_color \
            and len(modified[sink_index]) < tube_capacity:
        modified[sink_index].append(top_color)
        modified[source_index].pop()

    return modified


def num_boundaries(state: GameState) -> int:
    """Gets the number of boundaries between different colors across all the tubes in the game. A solved puzzle has zero
     such boundaries. This is used as the solver's A* heuristic. """
    boundaries = 0
    for tube in state:
        for i in range(len(tube) - 1):
            if tube[i] != tube[i + 1]:
                boundaries += 1
    return boundaries


def can_pour(tube_capacity: int, source: Tube, sink: Tube) -> bool:
    """Tests a given source tube can be legally poured in to given sink (destination) tube."""
    if tube_capacity < 1:
        raise ValueError("Tube capacity should be greater than or equal to one.")
    elif len(source) == 0:
        return False
    elif len(sink) == 0:
        return True
    elif len(sink) >= tube_capacity or len(source) == 0:
        return False
    return source[-1] == sink[-1]


def get_actions(tube_capacity: int, state: GameState) -> Set[Action]:
    """Gets a list of legal moves from a given state. Moves are represented as 2-tuples
    representing (<index of source tube>, <index of sink tube>)."""
    actions = set()
    for i, source in enumerate(state):
        for j, sink in enumerate(state):
            if i != j and can_pour(tube_capacity, source, sink):
                actions.add((i, j))
    return actions


class WaterSortProblem:
    def __init__(self, tube_capacity: int, initial_state: GameState):
        self.tube_capacity = tube_capacity
        self.initial_state = initial_state

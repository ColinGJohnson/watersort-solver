import copy
from typing import List, Tuple

Tube = List[int]
GameState = List[Tube]
Action = Tuple[int, int]


def is_complete(state):
    """Tests if the given puzzle state is a winner."""
    for tube in state:
        if len(set(tube)) > 1:
            return False
    return True


def pour(state, action):
    """Gets the state that results from making a pour (action) on a game state."""
    modified = copy.deepcopy(state)
    modified[action[1]].append(modified[action[0]][-1])
    modified[action].pop()
    return modified


class WaterSortProblem:
    def __init__(self, initial: GameState, tube_capacity: int):
        self.initial = initial
        self.tube_capacity = tube_capacity

    def get_actions(self, state: GameState) -> List[Action]:
        """Gets a list of legal moves from a given state. Moves are represented as 2-tuples
        representing (<index of source tube>, <index of sink tube>)."""
        actions = []
        for i, source in enumerate(state):
            for j, sink in enumerate(state):
                if i != j and self.can_pour(source, sink):
                    actions.append((i, j))
        return actions

    def can_pour(self, source: Tube, sink: Tube) -> bool:
        """Tests a given source tube can be legally poured in to given sink (destination) tube."""
        if len(source) == 0:
            return False
        elif len(sink) == 0:
            return True
        elif len(sink) >= self.tube_capacity or len(source) == 0:
            return False
        return source[-1] == sink[-1]

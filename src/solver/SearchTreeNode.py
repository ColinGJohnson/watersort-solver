from __future__ import annotations

from src.solver.Types import GameState, Action


class SearchTreeNode:
    def __init__(self, state: GameState, parent: SearchTreeNode = None, action: Action = None, path_cost: int = 0):
        """Create a search tree node representing a water sort puzzle state which originated from
        applying the specified action on the specified parent state."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = 0

    def __repr__(self):
        return "{}".format(self.state)

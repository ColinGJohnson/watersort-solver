from __future__ import annotations


class SearchTreeNode:
    def __init__(self, state, parent: SearchTreeNode, action):
        """Create a search tree node representing a water sort puzzle state which originated from
        applying the specified action on the specified parent state."""
        self.state = state
        self.parent = parent
        self.action = action

    def __repr__(self):
        return "{}".format(self.state)

    
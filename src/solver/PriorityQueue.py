import heapq


class PriorityQueue:
    """A queue in which the item with minimum f(item) is always popped first."""

    def __init__(self, items=(), key=lambda x: x):
        self.key = key
        self.items = []
        for item in items:
            self.add(item)

    def __len__(self):
        return len(self.items)

    def add(self, item):
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        """Pop and return the item with min key(item) value."""
        return heapq.heappop(self.items)[1]

    def top(self):
        return self.items[0][1]

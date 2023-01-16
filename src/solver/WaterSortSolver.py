from src.solver import WaterSortProblem


class WaterSortSolver:

    def best_first_graph_search(self, problem: WaterSortProblem, f, display=False):

        f = memoize(f, 'f')
        node = Node(problem.initial)
        frontier = PriorityQueue('min', f)
        frontier.append(node)
        explored = set()

        while frontier:
            node = frontier.pop()
            if problem.goal_test(node.state):
                return node
            explored.add(node.state)
            for child in node.expand(problem):
                if child.state not in explored and child not in frontier:
                    frontier.append(child)
                elif child in frontier:
                    if f(child) < frontier[child]:
                        del frontier[child]
                        frontier.append(child)

        return None

    def astar_search(problem, h=None, display=False):
        """A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass."""

        h = memoize(h or problem.h, 'h')
        return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

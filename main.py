START_NODES = {
    "house": ["bunny"],
    "bone": [],
    "boat": ["bunny"],
    "flower": [],
    "well": [],
    "carrot": [],
    "tree": ["dog"]
}

TARGET_NODES = {
    "house": [],
    "bone": ["dog"],
    "boat": [],
    "flower": [],
    "well": [],
    "carrot": ["bunny", "bunny"],
    "tree": []
}
# From, To, MustBeOn, MustBeOff
EDGES = [
    ("bone", "boat", (), ()),
    ("bone", "house", ("carrot",), ()),
    ("house", "bone", ("carrot",), ()),
    ("house", "boat", ("tree",), ()),
    ("house", "tree", ("bone", "flower"), ()),
    ("tree", "house", ("bone", "flower"), ()),
    ("tree", "well", (), ()),
    ("carrot", "tree", (), ()),
    ("carrot", "well", (), ("bone",)),
    ("well", "carrot", (), ("bone",)),
    ("well", "tree", (), ()),
    ("well", "flower", (), ()),
    ("flower", "well", (), ()),
    ("flower", "boat", (), ()),
    ("boat", "house", ("tree",), ()),
]

EDGES_OF_NODE = {node: [edge[1:] for edge in EDGES if edge[0] == node] for node in START_NODES}


class DogBunnyGraph:
    def __init__(self, nodes=None, description=""):
        self.nodes = START_NODES if nodes is None else nodes
        self.description = description

    def __str__(self):
        return str({node: self.nodes[node] for node in sorted(self.nodes)})

    def __hash__(self):
        return str(self)

    def copy(self):
        nodes = {node: pieces[:] for node, pieces in self.nodes.items()}
        return DogBunnyGraph(nodes)

    def neighbors(self):
        neighbors = []
        for (node, contents) in self.nodes.items():
            if not len(contents):
                continue  # Nothing to move
            for piece in set(contents):
                for (to_node, on_constraint, off_constraint) in EDGES_OF_NODE[node]:
                    constraints_okay = True
                    for must_be_on in on_constraint:
                        if not len(self.nodes[must_be_on]):
                            constraints_okay = False
                            break
                    for must_be_off in off_constraint:
                        if len(self.nodes[must_be_off]):
                            constraints_okay = False
                            break

                    if not constraints_okay:
                        continue

                    next_nodes = {node: pieces[:] for node, pieces in self.nodes.items()}
                    next_nodes[node].remove(piece)
                    next_nodes[to_node].append(piece)
                    next_nodes[to_node].sort()

                    neighbors.append(DogBunnyGraph(next_nodes, f"Move {piece} from {node} --> {to_node}"))

        return neighbors


from collections import deque


def search():
    init = DogBunnyGraph(START_NODES)
    target = DogBunnyGraph(TARGET_NODES)
    target_str = str(target)
    q = deque([(init, str(init), [])])
    seen = set()
    while len(q):
        (graph, graph_str, history) = q.popleft()
        if graph_str in seen:
            continue
        seen.add(graph_str)
        if graph_str == target_str:
            print("Found! ", len(history))
            for step in history:
                print(step)

            break
        for n in graph.neighbors():
            q.append((n, str(n), history + [graph.description]))


if __name__ == '__main__':
    search()

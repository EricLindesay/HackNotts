# array of nodes, index of which is the id


class Node:
    node_type: int = 0
    id: int = 0
    # list of integers representing the nodes this node connects to
    outputs: list[int] = []

    # list of integers representing the nodes that connect to this node
    inputs: list[int] = []


class Output:
    id: int = 0


class Input:
    id: int = 0

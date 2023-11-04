from constants import *


class Node:
    type_ = "Node"
    node_type: int = 0
    id: int = 0
    # list of integers representing the nodes this node connects to
    outputs: list[int] = []

    # list of integers representing the nodes that connect to this node
    inputs: list[int] = []

    def __str__(self):
        return f"{self.type_}<{self.id=}, {constant_string[self.node_type]}, outputs={self.outputs}"


class Output:
    type_ = "Output"
    id: int = 0

    def __str__(self):
        return f"{self.type_}<{self.id=}"


class Input:
    type_ = "Input"
    id: int = 0

    def __str__(self):
        return f"{self.type_}<{self.id=}"

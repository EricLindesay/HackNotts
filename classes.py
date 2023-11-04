from constants import *


class Node:
    type_ = "Node"
    node_type: int = 0  # AND, NOT, NOR
    id: int = 0
    input_wires: list[int] = []
    output_wire: int = 0

    def __str__(self):
        return f"{self.type_}<{self.id=}, {constant_string[self.node_type]}, input_wires={self.input_wires}, output={self.output_wire}>"


class Output:
    type_ = "Output"
    id: int = 0

    def __str__(self):
        return f"{self.type_}<{self.id=}>"


class Input:
    type_ = "Input"
    id: int = 0

    def __str__(self):
        return f"{self.type_}<{self.id=}>"

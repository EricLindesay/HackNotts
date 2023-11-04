from constants import *



class Node:
    type_ = "Node"
    node_type: int = 0
    id: int = 0
    input_wires = []
    output_wire: int = 0
    def __str__(self):
        return f"{self.type_}<{self.id=}, {constant_string[self.node_type]}, outputs={self.output_wire}, inputs={self.input_wires}"


class Output:
    type_ = "Output"
    id: int = 0
    wire: int = 0
    def __str__(self):
        return f"{self.type_}<{self.id=}, {self.wire=}"


class Input:
    type_ = "Input"
    id: int = 0
    wire: int = 0
    def __str__(self):
        return f"{self.type_}<{self.id=}, {self.wire=}"

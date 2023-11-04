from classes import *
from constants import *
# Get the number of inputs

# Get the number of outputs

# Get the gates we need - put this in a nxn grid (as best as possible)


def route(nodes: list[Node], inputs: list[Input], outputs: list[Output]):
    blocks = [[[]]]


output: Output = Output()
output.id = 0

outputs: list[Output] = [output]


i0: Input = Input()
i0.id = 0

i1: Input = Input()
i1.id = 1

i2: Input = Input()
i2.id = 2

inputs: list[Input] = [i0, i1, i2]


n0: Node = Node()
n0.id = 0
n0.node_type = AND
n0.outputs = [1]

n1: Node = Node()
n1.id = 1
n1.node_type = OR
n1.outputs = [1, 2]

n2: Node = Node()
n2.id = 2
n2.node_type = NAND
n2.outputs = [output]

inputs = 3
outputs = 1
nodes: list[Node] = [n0, n1, n2]


route(nodes, inputs, outputs)

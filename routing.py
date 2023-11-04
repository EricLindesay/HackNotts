from classes import *
from constants import *
from math import ceil, sqrt
# Get the number of inputs

# Get the number of outputs

# Get the gates we need - put this in a nxn grid (as best as possible)


class Block:
    def __init__(self, id, b_type, node):
        self.id: int = id
        self.block_type: int = b_type
        self.node = node


def initialise_blocks(inputs):
    blocks = []
    for i in range(0, 30):
        i_l = []
        for j in range(0, 30):
            j_l = []
            for k in range(0, 2):
                j_l.append(Block(-1, -1, -1))
            i_l.append(j_l)
        blocks.append(i_l)

    for ind, input in enumerate(inputs):
        blocks[0][ind*2][0] = Block(input.id, INPUT, input)

    return blocks


def route(nodes: list[Node], inputs: list[Input], outputs: list[Output]):
    print(inputs)

    blocks = initialise_blocks(inputs)

    # Gates are 3x4
    n: int = ceil(sqrt(len(inputs)))  # this is the grid size, e.g. 2x2 grid

    # Do a 5 block gap between each important thing
    for nodes_done, node in enumerate(nodes):
        divd: int = nodes_done//n  # the x coord
        modd: int = nodes_done % n  # the y coord
        # +4 because the things are 4 long, + 1 for rounding error
        for x in range(divd*9 + 6, divd*9 + 6 + 4):
            # +3 because the things are 3 wide, +1 for rounding error
            for y in range(modd*8, modd*8 + 3):
                block = Block(node.id, node.node_type, node)
                blocks[x][y][0] = block
        nodes_done += 1

    print_blocks(blocks)


def print_blocks(blocks):
    for i in blocks:
        for j in i:
            if (j[0].id == -1):
                print(" ", end='')
            else:
                print(j[0].block_type, end='')
        print()


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

nodes: list[Node] = [n0, n1, n2]


route(nodes, inputs, outputs)

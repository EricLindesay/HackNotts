from classes import *
from constants import *
from math import ceil, sqrt
from gates import *
from parse_input import read_input
# Get the number of inputs

# Get the number of outputs

# Get the gates we need - put this in a nxn grid (as best as possible)


class Block:
    def __init__(self, id, b_type, node):
        self.id: int = id
        self.block_type: int = b_type
        self.node = node
        self.occupied = False


def initialise_blocks(inputs):
    blocks = []
    for i in range(0, 30):
        i_l = []
        for j in range(0, 30):
            j_l = []
            for k in range(0, 3):
                j_l.append(Block(-1, -1, -1))
            i_l.append(j_l)
        blocks.append(i_l)

    for ind, input in enumerate(inputs):
        blocks[0][ind*2][0] = Block(input.id, INPUT, input)
        blocks[0][ind*2][1] = Block(input.wire, INPUT, input)

    return blocks


def add_gates(blocks, nodes):
    # Gates are 3x4
    n: int = ceil(sqrt(len(nodes)))  # this is the grid size, e.g. 2x2 grid

    # Do a 5 block gap between each important thing

    for i, node in enumerate(nodes):
        divd: int = i//n  # the x coord
        modd: int = i % n  # the y coord
        start_x = divd*9 + 6
        end_x = start_x + 4  # the gates are 4 long

        start_y = modd*8
        end_y = start_y + 3  # the gates are 3 wide

        # +4 because the things are 4 long, + 1 for rounding error
        for x in range(start_x, end_x):
            # +3 because the things are 3 wide, +1 for rounding error
            for y in range(start_y, end_y):
                block = Block(node.id, node.node_type, node)
                block.occupied = True
                blocks[x][y][0] = block

        # Add the input and output markers
        gate: Gate = gates[node.node_type]
        for i, gate_input in enumerate(gate.input_locations):
            blocks[start_x + gate_input[0]][start_y +
                                            gate_input[1]][1].id = node.input_wires[i]

        blocks[start_x + gate.output_location[1]][start_y +
                                                  gate.output_location[0]][1].id = -1 * node.output_wire


def route(nodes: list[Node], inputs: list[Input], outputs: list[Output]):
    print(inputs)

    blocks = initialise_blocks(inputs)
    add_gates(blocks, nodes)

    for i, output in enumerate(outputs):
        blocks[len(blocks)-1][i*2][0] = Block(output.id, OUTPUT, output)
        blocks[len(blocks)-1][i*2][1] = Block(output.wire, OUTPUT, output)

    print_blocks(blocks, 1)


def print_blocks(blocks, layer=0):
    for i in blocks:
        for j in i:
            if (j[layer].id == -1):
                print(" ", end='')
            else:
                print(abs(j[layer].id), end='')
        print()

def dijkstras(blocks):



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

if __name__ == "__main__":
    nodes = read_input().read_gates("./yosys/opt6.json")
    inputs = read_input().read_inputs("./yosys/opt6.json")
    outputs = read_input().read_outputs("./yosys/opt6.json")
    route(nodes, inputs, outputs)

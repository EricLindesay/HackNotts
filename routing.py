import math

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

    def __str__(self):
        return f"Block<{self.id=}, {self.block_type=}>"

def initialise_blocks(nodes, inputs, outputs):
    blocks = []
    n: int = ceil(sqrt(len(nodes)))
    input_width = len(inputs) * 2 - 1
    output_width = len(outputs) * 2 - 1
    gate_width = n * 3 + (n - 1) * 5
    width = max(input_width, output_width, gate_width)
    # one for input, one for output. We want 5 gap between them
    # n * 4, they are 4 long, need 5 gap between them

    actual_nodes = n
    while abs(len(nodes) - actual_nodes) <= 0:
        actual_nodes -= 1
    height = 2 + actual_nodes * 4 + (actual_nodes + 1) * 5

    for i in range(0, height):
        i_l = []
        for j in range(0, width):
            j_l = []
            for k in range(0, 3):
                j_l.append(Block(-1, -1, -1))
            i_l.append(j_l)
        blocks.append(i_l)

    for ind, input in enumerate(inputs):
        blocks[0][ind * 2][0] = Block(input.id, INPUT, input)
        blocks[0][ind * 2][1] = Block(input.wire * -1, INPUT, input)

    return blocks


def add_gates(blocks, nodes):
    # Gates are 3x4
    n: int = ceil(sqrt(len(nodes)))  # this is the grid size, e.g. 2x2 grid

    # Do a 5 block gap between each important thing

    for i, node in enumerate(nodes):
        divd: int = i // n  # the x coord
        modd: int = i % n  # the y coord
        start_x = divd * 9 + 6
        end_x = start_x + 4  # the gates are 4 long

        start_y = modd * 8
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
            blocks[start_x + gate_input[0]][start_y +
                                            gate_input[1]][1].block_type = GATE_INPUT

        blocks[start_x + gate.output_location[1]][start_y +
                                                  gate.output_location[0]][1].id = -1 * node.output_wire
        blocks[start_x + gate.output_location[1]][start_y +
                                                  gate.output_location[0]][1].block_type = GATE_INPUT


def route(nodes: list[Node], inputs: list[Input], outputs: list[Output]):
    print(inputs)

    blocks = initialise_blocks(nodes, inputs, outputs)
    add_gates(blocks, nodes)

    for i, output in enumerate(outputs):
        blocks[len(blocks) - 1][i * 2][0] = Block(output.id, OUTPUT, output)
        blocks[len(blocks) - 1][i * 2][1] = Block(output.wire, OUTPUT, output)

    print_blocks(blocks, 1)
    # dijkstras(blocks, [0, 0], [[6,2], [6,8]])
    # print_blocks(blocks, 1)
    print("Inputs")
    for input in inputs:
        goals = goal_finder(blocks, input.wire)
        start = initial_finder(blocks, input.wire)
        print(f"Doing dijkstra on {start}, {goals}")
        dijkstras(blocks, start, goals)


    print("Nodes")
    for node in nodes:
        goals = goal_finder(blocks, node.output_wire)
        start = initial_finder(blocks, node.output_wire)
        dijkstras(blocks, start, goals)

    print_blocks(blocks, 1)

def print_blocks(blocks, layer=0):
    for i in blocks:
        line: str = ""
        for j in i:
            if (j[layer].id == -1):
                line += " "
            else:
                line += str(abs(j[layer].id))
        print(line)


def goal_finder(blocks, goalGateNum):
    goals = []
    for x in range(len(blocks)):
        for y in range(len(blocks[0])):
            if blocks[x][y][1].id == goalGateNum:
                goals.append([x, y])
    return goals

def initial_finder(blocks, initialGateNum):
    for x in range(len(blocks)):
        for y in range(len(blocks[0])):
            if blocks[x][y][1].id == -1 * initialGateNum:
                return [x, y]
    return []

# blocks is area to traverse, initial node is start and goals is a list
def dijkstras(blocks, initial_node, goals):
    i = 0
    unvisited_nodes = []
    # Unvisited nodes list generation
    for layer in blocks:
        if i == 0:
            i += 1
            continue
        for x in layer:
            for y in layer:
                unvisited_nodes.append((x, y, i))
    # instantiate max value for size of blocks
    distance = [[[math.inf for k in range(len(blocks[0][0]) - 1)] for j in range(len(blocks[0]))] for i in
                range(len(blocks))]
    visited = [[[False for k in range(len(blocks[0][0]) - 1)] for j in range(len(blocks[0]))] for i in
                range(len(blocks))]

    to_visit = len(visited) * len(visited[0]) * len(visited[0][0])
    directions = [[1, 0, 0], [0, 0, 1], [0, 0, -1], [-1, 0, 0], [0, 1, 0], [0, -1, 0]]

    # Block off redstone and other pings
    print(blocks[6][0][1])
    print(initial_node, goals)
    for i in range(len(blocks)):
        for j in range(len(blocks[0])):
            # Block off the other inputs
            if blocks[i][j][1].id != -1:
                print(f"{i}, {j}, 1 : {blocks[i][j][1]}")

            dont_block_same_id: bool = ((blocks[i][j][1].block_type == GATE_INPUT or blocks[i][j][1].block_type == OUTPUT) and abs(blocks[i][j][1].id) != abs(blocks[initial_node[0]][initial_node[1]][1].id))
            blockable_type: bool = (dont_block_same_id or blocks[i][j][1].block_type == INPUT)
            is_start_node: bool = (i == initial_node[0] and j == initial_node[1])
            if blockable_type and not is_start_node:
                visited[i][j][0] = True
                to_visit -= 1
                for direction in directions:
                    newX = i + direction[0]
                    newY = j + direction[1]
                    if is_valid(distance, newX, newY, 0):
                        visited[newX][newY][0] = True
                        to_visit -= 1

    # Block off other redstone blocks
    for i in range(len(blocks)):
        for j in range(len(blocks[0])):
            for k in range(len(visited[0][0])):
                blocks_k = k + 1
                # Block off the other redstone
                if blocks[i][j][blocks_k].block_type in [REDSTONE, VIA_UP, VIA_DOWN]:
                    print(f"Redstone blocking {i} {j} {k}")
                    visited[i][j][k] = True
                    to_visit -= 1
                    for direction in directions:
                        newX = i + direction[0]
                        newY = j + direction[1]
                        if is_valid(distance, newX, newY, k):
                            visited[newX][newY][k] = True
                            to_visit -= 1

    distance[initial_node[0]][initial_node[1]][0] = 0
    # Do dijkstras
    while to_visit > 0:
        min_node = []  # 0, 0, 0
        min_dist = 0
        for i in range(len(visited)):
            for j in range(len(visited[0])):
                for k in range(len(visited[0][0])):
                    if not visited[i][j][k]:
                        # if there is no node yet, or the distance is better, choose this node
                        if len(min_node) == 0 or distance[i][j][k] < min_dist:
                            min_dist = distance[i][j][k]
                            min_node = [i, j, k]
        visited[min_node[0]][min_node[1]][min_node[2]] = True
        to_visit -= 1

        for direction in directions:
            newX = min_node[0] + direction[0]
            newY = min_node[1] + direction[1]
            newZ = min_node[2] + direction[2]
            if is_valid(distance, newX, newY, newZ) and not visited[newX][newY][newZ]:
                # update the distances
                distance[newX][newY][newZ] = min(distance[min_node[0]][min_node[1]][min_node[2]]+1, distance[newX][newY][newZ])

    for d in distance:
        print(d)

    # A list of coordinates for each goal

    # Now backtrack from the goal to try to get the best route, then put the redstone on that route
    # if elevation changes, make sure to mark it as a VIAS
    for goal in goals:
        current_node = [goal[0], goal[1], 0]
        # Find the adjacent ones to get the best
        while not (current_node[0] == initial_node[0] and current_node[1] == initial_node[1]):
            best_dist = 0
            next_node = []
            for direction in directions:
                newX = current_node[0] + direction[0]
                newY = current_node[1] + direction[1]
                newZ = current_node[2] + direction[2]
                if is_valid(distance, newX, newY, newZ) and (len(next_node) == 0 or distance[newX][newY][newZ] < best_dist):
                    best_dist = distance[newX][newY][newZ]
                    next_node = [newX, newY, newZ]

            if next_node[0] == initial_node[0] and next_node[1] == initial_node[1] and next_node[2] == 0:
                break

            if blocks[next_node[0]][next_node[1]][next_node[2]+1].block_type in [REDSTONE, VIA_UP, VIA_DOWN]:
                break

            # If you go down, set it as a via instead

            # Work out whether this is a via
            print(f"Update block {next_node}")
            if current_node[0] == next_node[0] and current_node[1] == next_node[1] and current_node[2] != next_node[2]:
                if current_node[2] > next_node[2]:
                    blocks[next_node[0]][next_node[1]][next_node[2] + 1].block_type = VIA_UP
                if current_node[2] < next_node[2]:
                    blocks[next_node[0]][next_node[1]][next_node[2] + 1].block_type = VIA_DOWN
                blocks[next_node[0]][next_node[1]][next_node[2] + 1].id = 1
            else:
                blocks[next_node[0]][next_node[1]][next_node[2]+1].block_type = REDSTONE
                blocks[next_node[0]][next_node[1]][next_node[2]+1].id = 0

            current_node = next_node

    print_blocks(blocks, 1)
    print_blocks(blocks, 2)

def is_valid(distance, x, y, z):
    return not (x >= len(distance) or x < 0 or y >= len(distance[0]) or y < 0 or z >= len(distance[0][0]) or z < 0)


if __name__ == "__main__":
    nodes = read_input().read_gates("./yosys/opt6.json")
    inputs = read_input().read_inputs("./yosys/opt6.json")
    outputs = read_input().read_outputs("./yosys/opt6.json")
    route(nodes, inputs, outputs)

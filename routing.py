import random
import math

from classes import *
from constants import *
from math import ceil, sqrt
from gates import *
from parse_input import read_input


# Get the number of inputs

# Get the number of outputs

# Get the gates we need - put this in a nxn grid (as best as possible)
LAYER_SIZE = 3
PADDING_X = 3
GAP = 7


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
    gate_width = n * 3 + (n - 1) * GAP
    width = max(input_width, output_width, gate_width) + 2 * PADDING_X
    # one for input, one for output. We want 5 gap between them
    # n * 4, they are 4 long, need 5 gap between them

    actual_nodes = n
    while abs(len(nodes) - actual_nodes) <= 0:
        actual_nodes -= 1
    height = 2 + actual_nodes * 4 + (actual_nodes) * GAP

    for i in range(0, height):
        i_l = []
        for j in range(0, width):
            j_l = []
            for k in range(0, LAYER_SIZE):
                j_l.append(Block(-1, -1, -1))
            i_l.append(j_l)
        blocks.append(i_l)

    step_size = width // len(inputs)
    start_offset = step_size // 2
    for ind, input in enumerate(inputs):
        blocks[0][ind * step_size +
                  start_offset][0] = Block(input.id, INPUT, input)
        blocks[0][ind * step_size +
                  start_offset][1] = Block(input.wire * -1, INPUT, input)

    return blocks


def add_gates(blocks, nodes):
    # Gates are 3x4
    n: int = ceil(sqrt(len(nodes)))  # this is the grid size, e.g. 2x2 grid

    # Do a 5 block gap between each important thing

    for i, node in enumerate(nodes):
        divd: int = i // n  # the x coord
        modd: int = i % n  # the y coord
        start_x = divd * (4 + GAP) + 6
        end_x = start_x + 4  # the gates are 4 long

        start_y = modd * (3 + GAP) + PADDING_X
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
        print(gate)
        for i, gate_input in enumerate(gate.input_locations):
            blocks[start_x + gate_input[1]][start_y +
                                            gate_input[0]][1].id = node.input_wires[i]
            blocks[start_x + gate_input[1]][start_y +
                                            gate_input[0]][1].block_type = GATE_INPUT

        blocks[start_x + gate.output_location[1]][start_y +
                                                  gate.output_location[0]][1].id = -1 * node.output_wire
        blocks[start_x + gate.output_location[1]][start_y +
                                                  gate.output_location[0]][1].block_type = GATE_OUTPUT


requires_repeaters = []


def route(nodes: list[Node], inputs: list[Input], outputs: list[Output]):
    blocks = initialise_blocks(nodes, inputs, outputs)
    add_gates(blocks, nodes)

    step_size = len(blocks[0]) // len(outputs)
    start_offset = step_size // 2
    for i, output in enumerate(outputs):
        blocks[len(blocks) - 1][i * step_size +
                                start_offset][0] = Block(output.id, OUTPUT, output)
        blocks[len(blocks) - 1][i * step_size +
                                start_offset][1] = Block(output.wire, OUTPUT, output)

    # dijkstras(blocks, [0, 0], [[6,2], [6,8]])
    # print_blocks(blocks, 1)
    print("Dijkstras on Inputs")
    for input in inputs:
        goals = goal_finder(blocks, input.wire)
        start = initial_finder(blocks, input.wire)
        dijkstras(blocks, start, goals)

    print("Dijkstras on Gates")
    for node in nodes:
        goals = goal_finder(blocks, node.output_wire)
        start = initial_finder(blocks, node.output_wire)
        dijkstras(blocks, start, goals)

    test_via_ups(blocks)
    populate_repeaters(blocks, requires_repeaters)

    print_blocks(blocks, 1)
    print_blocks(blocks, 2)

    return blocks


def populate_repeaters(blocks, requires_repeaters):
    horizontal_directions = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]]
    # Go through the list of repeaters.
    for repeater in requires_repeaters:
        wire_length = 0
        coord = repeater
        prev_wire = []

        next_wire = []
        # Do the initial handling of direction from the source
        for direction in horizontal_directions:
            newX = coord[0] + direction[0]
            newY = coord[1] + direction[1]
            newZ = coord[2] + direction[2]
            # Make sure we aren't cycling
            if not is_valid(blocks, newX, newY, newZ):
                continue

            # Is this redstone/valid?
            if is_redstone_ish(blocks[newX][newY][newZ]):
                next_wire = [newX, newY, newZ]
                break
        prev_wire.append(coord)
        coord = next_wire

        while True:
            if not coord:
                break
            # Go through this circuit, counting the wire length. When you get to 15, step backwards until there is a valid repeater position
            # Do we need to go deeper?
            block = blocks[coord[0]][coord[1]][coord[2]]
            if block.block_type == VIA_UP:
                coord[2] -= 1
                wire_length = 0
            elif block.block_type == VIA_DOWN:
                coord[2] += 1
                wire_length = 0
            elif block.block_type not in [REDSTONE]:  # probs gaate input
                break

            next_wire = None
            wire_length += 1
            stop = False
            if wire_length >= 15:
                # loop backwards until you find a balid position for a repeaty
                while prev_wire:
                    # go to this previous wire
                    # see if the wire before this can be repeated
                    # see if the wire after this can be repeated
                    # repeat
                    next_wire = coord
                    coord = prev_wire[len(prev_wire) - 1]

                    # Remove the last from the array
                    prev_wire.pop(len(prev_wire) - 1)

                    last_wire = prev_wire[len(prev_wire) - 1]
                    # Make sure the x or y coordinates of each of these wires are the same
                    if next_wire[0] == coord[0] and coord[0] == last_wire[0]:
                        # repeate
                        if is_valid(blocks, coord[0], coord[1]+1, coord[2]) and is_redstone_ish(blocks[coord[0]][coord[1]+1][coord[2]]):
                            continue
                        if is_valid(blocks, coord[0], coord[1]-1, coord[2]) and is_redstone_ish(blocks[coord[0]][coord[1]-1][coord[2]]):
                            continue

                        if next_wire[1] - coord[1] == 1:
                            blocks[coord[0]][coord[1]][coord[2]
                                                       ].block_type = REPEATER_EAST
                            blocks[coord[0]][coord[1]][coord[2]].id = 2
                        elif next_wire[1] - coord[1] == -1:
                            blocks[coord[0]][coord[1]][coord[2]
                                                       ].block_type = REPEATER_WEST
                            blocks[coord[0]][coord[1]][coord[2]].id = 2
                        prev_wire.append(coord)
                        coord = next_wire
                        wire_length = 1
                        break
                    if next_wire[1] == coord[1] and coord[1] == last_wire[1]:
                        if is_valid(blocks, coord[0], coord[1]+1, coord[2]) and is_redstone_ish(blocks[coord[0]][coord[1]+1][coord[2]]):
                            continue
                        if is_valid(blocks, coord[0], coord[1]-1, coord[2]) and is_redstone_ish(blocks[coord[0]][coord[1]-1][coord[2]]):
                            continue

                        if next_wire[0] - coord[0] == 1:
                            blocks[coord[0]][coord[1]][coord[2]
                                                       ].block_type = REPEATER_SOUTH
                            blocks[coord[0]][coord[1]][coord[2]].id = 2
                        elif next_wire[0] - coord[0] == -1:
                            blocks[coord[0]][coord[1]][coord[2]
                                                       ].block_type = REPEATER_NORTH
                            blocks[coord[0]][coord[1]][coord[2]].id = 2
                        prev_wire.append(coord)
                        coord = next_wire
                        wire_length = 1
                        break

            horizontal_directions = [[1, 0, 0], [
                0, 1, 0], [-1, 0, 0], [0, -1, 0]]
            next_wire = []
            for direction in horizontal_directions:
                newX = coord[0] + direction[0]
                newY = coord[1] + direction[1]
                newZ = coord[2] + direction[2]
                # Make sure we aren't cycling
                if not is_valid(blocks, newX, newY, newZ) or [newX, newY, newZ] == prev_wire[len(prev_wire) - 1]:
                    continue

                # Is this redstone/valid?
                if is_redstone_ish(blocks[newX][newY][newZ]):
                    next_wire = [newX, newY, newZ]
                    break
                if blocks[newX][newY][newZ].block_type in [GATE_INPUT, OUTPUT]:
                    next_wire = [newX, newY, newZ]
                    stop = True
                    break
            if stop:
                break
            prev_wire.append(coord)
            coord = next_wire


def test_via_ups(blocks):
    horizontal_directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    print("Test VIA_UPs")
    for k in range(len(blocks[0][0])):
        for i in range(len(blocks)):
            for j in range(len(blocks[0])):
                # If you find a VIA_UP or GATE_INPUT if, there is two redstone neighbours, DIE
                if blocks[i][j][k].block_type == VIA_UP or blocks[i][j][k].block_type == GATE_INPUT:
                    red_neighbours = 0
                    # maybe needs to be redstone ish
                    for direction in horizontal_directions:
                        newX = i + direction[0]
                        newY = j + direction[1]
                        newZ = k
                        if is_valid(blocks, newX, newY, newZ) and blocks[newX][newY][newZ].block_type == REDSTONE:
                            red_neighbours += 1
                    if red_neighbours >= 2:
                        raise ValueError("There is redstone through a VIA_UP")


def print_blocks(blocks, layer=0):
    print(f"Layer {layer}")
    for i in blocks:
        line: str = ""
        for j in i:
            if j[layer].id == -1:
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

    directions = [[1, 0, 0], [-1, 0, 0], [0, 1, 0],
                  [0, -1, 0], [0, 0, 1], [0, 0, -1]]

    # Block off redstone and other pings
    for i in range(len(blocks)):
        for j in range(len(blocks[0])):
            # Block off the other inputs

            if i == initial_node[0] and j == initial_node[1]:
                # You don't want to block yourself off
                continue

            # We want to block INPUTs and gate outputs. As well as GATE_INPUTS of different types and OUTPUTS of different type
            # We also don't want to block air
            block = blocks[i][j][1]
            if block.block_type == -1:
                continue

            # We don't want to block GATE_INPUTs if they have the same id as the one we are going to
            if abs(block.id) == abs(blocks[initial_node[0]][initial_node[1]][1].id):
                continue

            # We don't want to block OUTPUTs if they have the same id as the one we are going to
            # if block.block_type == OUTPUT and abs(block.id) == abs(blocks[initial_node[0]][initial_node[1]][1].id):
            #     continue

            # dont_block_same_id: bool = ((blocks[i][j][1].block_type == GATE_INPUT or blocks[i][j][1].block_type == OUTPUT)
            #                             and abs(blocks[i][j][1].id) != abs(blocks[initial_node[0]][initial_node[1]][1].id))
            # blockable_type: bool = (dont_block_same_id or blocks[i][j][1].block_type == INPUT)
            # if blockable_type:

            visited[i][j][0] = True
            for direction in directions:
                newX = i + direction[0]
                newY = j + direction[1]
                if is_valid(distance, newX, newY, 0):
                    visited[newX][newY][0] = True

    # Block off other redstone blocks
    for i in range(len(visited)):
        for j in range(len(visited[0])):
            for k in range(len(visited[0][0])):
                blocks_k = k + 1
                # Block off the other redstone
                if blocks[i][j][blocks_k].block_type in [REDSTONE, VIA_UP, VIA_DOWN]:
                    visited[i][j][k] = True
                    for direction in directions:
                        newX = i + direction[0]
                        newY = j + direction[1]
                        if is_valid(distance, newX, newY, k):
                            visited[newX][newY][k] = True

    # Don't allow an up into an up
    visited[initial_node[0]][initial_node[1]][1] = True

    for goal in goals:
        visited[goal[0]][goal[1]][1] = True

    # Try all of the source's neighbours
    # Try all of the goal's neighbours
    # If they are all blocked, die
    impossible = True
    for direction in directions:
        newX = initial_node[0] + direction[0]
        newY = initial_node[1] + direction[1]
        newZ = direction[2]
        if is_valid(distance, newX, newY, newZ) and not visited[newX][newY][newZ]:
            # update the distances
            impossible = False

    for goal in goals:
        for direction in directions:
            newX = goal[0] + direction[0]
            newY = goal[1] + direction[1]
            newZ = direction[2]
            if is_valid(distance, newX, newY, newZ) and not visited[newX][newY][newZ]:
                # update the distances
                impossible = False

    if impossible:
        raise IndexError("This is an impossible layout")

    distance[initial_node[0]][initial_node[1]][0] = 0

    # Do dijkstras
    while True:
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

        if len(min_node) == 0:
            break  # You have seen everything

        visited[min_node[0]][min_node[1]][min_node[2]] = True

        for direction in directions:
            newX = min_node[0] + direction[0]
            newY = min_node[1] + direction[1]
            newZ = min_node[2] + direction[2]
            if is_valid(distance, newX, newY, newZ) and not visited[newX][newY][newZ]:
                # update the distances
                distance[newX][newY][newZ] = min(distance[min_node[0]][min_node[1]][min_node[2]] + 1,
                                                 distance[newX][newY][newZ])

    # A list of coordinates for each goal

    # Now backtrack from the goal to try to get the best route, then put the redstone on that route
    # if elevation changes, make sure to mark it as a VIA
    # We prefer straight lines
    # a list of coordinates. These coordinates are initial nodes which you should step through
    # Step through this node until you find a place where you require a repeater
    # Then step backwards until you find a place to put it
    # Then continue stepping through until you find another place to put the repeater, or the end

    for goal in goals:
        wire_length: int = 0
        current_node = [goal[0], goal[1], 0]
        # Find the adjacent ones to get the best
        prev_direction = []
        while not (current_node[0] == initial_node[0] and current_node[1] == initial_node[1]):
            best_dist = 0
            next_node = []
            new_directions = []

            # We want to favour going in straight lines, so keep on going in the previous direction
            if prev_direction:
                new_directions.append(prev_direction)

            for d in directions:
                if d not in new_directions:
                    new_directions.append(d)

            for direction in new_directions:
                newX = current_node[0] + direction[0]
                newY = current_node[1] + direction[1]
                newZ = current_node[2] + direction[2]
                if is_valid(distance, newX, newY, newZ) and (
                        len(next_node) == 0 or distance[newX][newY][newZ] < best_dist):
                    best_dist = distance[newX][newY][newZ]
                    next_node = [newX, newY, newZ]
                    prev_direction = direction

            if next_node[0] == initial_node[0] and next_node[1] == initial_node[1] and next_node[2] == 0:
                break

            if blocks[next_node[0]][next_node[1]][next_node[2] + 1].block_type in [REDSTONE, VIA_UP, VIA_DOWN]:
                break

            # If you go down, set it as a via instead

            # Work out whether this is a via
            type_id = blocks[initial_node[0]][initial_node[1]][1].id
            if current_node[0] == next_node[0] and current_node[1] == next_node[1] and current_node[2] != next_node[2]:
                if current_node[2] > next_node[2]:
                    blocks[next_node[0]][next_node[1]
                                         ][next_node[2] + 1].block_type = VIA_DOWN
                if current_node[2] < next_node[2]:
                    blocks[next_node[0]][next_node[1]
                                         ][next_node[2] + 1].block_type = VIA_UP
                blocks[next_node[0]][next_node[1]][next_node[2] + 1].id = 1
                wire_length = 0
            else:
                blocks[next_node[0]][next_node[1]
                                     ][next_node[2] + 1].block_type = REDSTONE
                blocks[next_node[0]][next_node[1]][next_node[2] +
                                                   1].id = blocks[initial_node[0]][initial_node[1]][1].id
                wire_length += 1
                if wire_length >= 15:
                    if type_id not in requires_repeaters:
                        requires_repeaters.append(initial_node + [1])
                    wire_length = 0

            current_node = next_node

    check_redstone_closeness(blocks)

    # ALso have to check repeaters if you have a T junction. Right now it can place a repeater on the T


def check_redstone_closeness(blocks):
    horizontal_directions = [[1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, -1, 0]]
    # Detect for two adjacent redstonies which don't have the same id
    # Loop through the entire
    for k in range(len(blocks[0][0])):
        for i in range(len(blocks)):
            for j in range(len(blocks[0])):
                if blocks[i][j][k].block_type != REDSTONE:
                    continue

                for direction in horizontal_directions:
                    newX = i + direction[0]
                    newY = j + direction[1]
                    newZ = k + direction[2]
                    # Make sure we aren't cycling
                    if not is_valid(blocks, newX, newY, newZ):
                        continue

                    # Is this redstone?
                    if blocks[newX][newY][newZ].block_type != REDSTONE:
                        continue

                    # Are they the same wire?
                    if blocks[newX][newY][newZ].id != blocks[i][j][k].id:
                        raise AssertionError(
                            "Redstone too close together and clashing")


def is_redstone_ish(block):
    return block.block_type == REDSTONE or block.block_type == VIA_UP or block.block_type == VIA_DOWN


def is_valid(distance, x, y, z):
    return not (x >= len(distance) or x < 0 or y >= len(distance[0]) or y < 0 or z >= len(distance[0][0]) or z < 0)


if __name__ == "__main__":
    nodes = read_input().read_gates("./yosys/opt6.json")
    inputs = read_input().read_inputs("./yosys/opt6.json")
    outputs = read_input().read_outputs("./yosys/opt6.json")

    i = 0
    while True:
        try:
            print(f"Trying pass {i}")
            random.shuffle(nodes)
            route(nodes, inputs, outputs)
            break
        except Exception:
            pass
        i += 1

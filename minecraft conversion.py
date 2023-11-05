import random
import mcschematic
from routing import *
redstone_alldir = "minecraft:redstone_wire[north=side,east=side,south=side,west=side]"
redstone_ew = "minecraft:redstone_wire[east=side,west=side]"
redstone_ns = "minecraft:redstone_wire[north=side,south=side]"
repeater_forward = "minecraft:repeater[facing=north]"
repeater_side = "minecraft:repeater[facing=west]"
torch_forward = "minecraft:redstone_wall_torch[facing=south]"
torch_forward_off = "minecraft:redstone_wall_torch[facing=south,lit=false]"
torch_up = "minecraft:redstone_torch"
torch_up_off = "minecraft:redstone_torch[lit=false]"
structure = "minecraft:stone"
piston_down = "minecraft:sticky_piston[facing=down]"
slime = "minecraft:slime_block"
redstone_block = "minecraft:redstone_block"
target_block = "minecraft:target"


class minecraftConverter:
    def __init__(self):
        self.schem = mcschematic.MCSchematic()
        self.gatelayerheight = 1
        self.secondlayerheight = -5  # height for second layer structure
        self.thirdlayerheight = -11  # height for third layer structure
        # self.schem.setBlock((0,-1,0), "minecraft:stone")

    def placeDownFromGate(self, location):
        x = int(location[1])
        y = int(location[0])
        self.schem.setBlock((x, 0, y), piston_down)
        self.schem.setBlock((x, -2, y), redstone_block)
        self.schem.setBlock((x, -1, y), slime)
        self.schem.setBlock((x, -4, y), redstone_alldir)
        self.schem.setBlock((x, -5, y), structure)

    def placeUpToGate(self, location):
        x = int(location[1])
        y = int(location[0])
        self.schem.setBlock((x, -1, y), torch_up_off)
        self.schem.setBlock((x, -2, y), structure)
        self.schem.setBlock((x, -3, y), torch_up)
        self.schem.setBlock((x, -4, y), target_block)

    def placeLayerDust(self, location, layer):
        x = int(location[1])
        y = int(location[0])
        self.schem.setBlock((x, -5 * layer, y), structure)
        self.schem.setBlock((x, (-5 * layer)+1, y), redstone_alldir)
        # if(layer == 2):
        #     self.schem.setBlock((x,-11,y), structure)
        #     self.schem.setBlock((x,-10,y), redstone_alldir)

    def placeViaUp(self, location, layer):  # layer is origin layer
        x = int(location[1])
        y = int(location[0])
        initheight = (-5*layer)+1
        self.schem.setBlock((x, initheight, y), target_block)
        self.schem.setBlock((x, initheight+1, y), torch_up)
        self.schem.setBlock((x, initheight+2, y), target_block)
        self.schem.setBlock((x, initheight+3, y), torch_up_off)

    def placeViaDown(self, location, layer):  # layer is origin layer
        x = int(location[1])
        y = int(location[0])
        initheight = (-5*layer)

        self.schem.setBlock((x, initheight+1, y), redstone_alldir)
        self.schem.setBlock((x, initheight, y), piston_down)
        self.schem.setBlock((x, initheight-2, y), redstone_block)
        self.schem.setBlock((x, initheight-1, y), slime)
        self.schem.setBlock((x, initheight-4, y), redstone_alldir)
        self.schem.setBlock((x, initheight-5, y), structure)

    def doubleDown(self, location):
        x = int(location[1])
        y = int(location[0])
        self.schem.setBlock((x, -6, y), piston_down)
        self.schem.setBlock((x, -7, y), redstone_block)

    def placeAND(self, location):
        x = int(location[1])
        y = int(location[0])
        for i in range(x, x+3):
            for j in range(y, y+4):
                self.schem.setBlock((i, 0, j), structure)

        for i in range(x, x+3):
            self.schem.setBlock((i, 1, y+1), structure)

        self.schem.setBlock((x, 1, y), redstone_alldir)
        self.schem.setBlock((x+2, 1, y), redstone_alldir)
        self.placeUpToGate((y, x))
        self.placeUpToGate((y, x+2))
        self.placeDownFromGate((y+3, x+1))
        self.schem.setBlock((x+1, 1, y+2), torch_forward_off)
        # self.schem.setBlock((x+1,1,y+3), repeater_forward)
        self.schem.setBlock((x, 2, y+1), torch_up)
        self.schem.setBlock((x+1, 2, y+1), redstone_ew)
        self.schem.setBlock((x+2, 2, y+1), torch_up)

    def placeNAND(self, location):
        x = int(location[1])
        y = int(location[0])
        for i in range(x, x+3):
            for j in range(y, y+4):
                self.schem.setBlock((i, 0, j), structure)

        for i in range(x, x+3):
            self.schem.setBlock((i, 1, y+1), structure)

        self.schem.setBlock((x, 1, y), redstone_alldir)
        self.schem.setBlock((x+2, 1, y), redstone_alldir)
        self.schem.setBlock((x+1, 1, y+2), redstone_alldir)
        # self.schem.setBlock((x+1,1,y+3), repeater_forward)

        self.placeUpToGate((y, x))
        self.placeUpToGate((y, x+2))

        self.schem.setBlock((x, 2, y+1), torch_up)
        self.schem.setBlock((x+1, 2, y+1), redstone_ew)
        self.schem.setBlock((x+2, 2, y+1), torch_up)
        self.placeDownFromGate((y+3, x+1))

    def placeOR(self, location):
        x = int(location[1])
        y = int(location[0])
        for i in range(x, x+3):
            for j in range(y, y+4):
                self.schem.setBlock((i, 0, j), "minecraft:stone")

        for i in range(x, x+3):
            self.schem.setBlock((i, 1, y+1), "minecraft:stone")

        self.schem.setBlock((x, 1, y), redstone_alldir)
        self.schem.setBlock((x+2, 1, y), redstone_alldir)
        self.schem.setBlock((x+1, 1, y+2), redstone_alldir)
        # self.schem.setBlock((x+1,1,y+3), repeater_forward)
        self.placeUpToGate((y, x))
        self.placeUpToGate((y, x+2))

        self.schem.setBlock((x, 2, y+1), redstone_alldir)
        self.schem.setBlock((x+1, 2, y+1), redstone_alldir)
        self.schem.setBlock((x+2, 2, y+1), redstone_alldir)
        self.placeDownFromGate((y+3, x+1))

    def placeNOR(self, location):
        x = int(location[1])
        y = int(location[0])
        for i in range(x, x+3):
            for j in range(y, y+4):
                self.schem.setBlock((i, 0, j), "minecraft:stone")

        for i in range(x, x+3):
            self.schem.setBlock((i, 1, y+1), "minecraft:stone")

        self.schem.setBlock((x, 1, y), redstone_alldir)
        self.schem.setBlock((x+2, 1, y), redstone_alldir)
        self.schem.setBlock((x+1, 1, y+2), torch_forward)
        self.schem.setBlock((x+1, 1, y+3), redstone_alldir)
        self.placeUpToGate((y, x))
        self.placeUpToGate((y, x+2))

        self.schem.setBlock((x, 2, y+1), redstone_alldir)
        self.schem.setBlock((x+1, 2, y+1), redstone_alldir)
        self.schem.setBlock((x+2, 2, y+1), redstone_alldir)
        self.placeDownFromGate((y+3, x+1))

    def placeNOT(self, location):
        x = int(location[1])
        y = int(location[0])
        for i in range(x, x+3):
            for j in range(y, y+4):
                self.schem.setBlock((i, 0, j), structure)

        self.schem.setBlock((x+1, 1, y), redstone_alldir)
        self.placeUpToGate((y, x+1))
        self.schem.setBlock((x+1, 1, y+1), structure)
        self.schem.setBlock((x+1, 1, y+2), torch_forward)
        # self.schem.setBlock((x+1,1,y+3),redstone_alldir)
        self.placeDownFromGate((y+3, x+1))

    def placeDFF(self, location):
        x = int(location[1])
        y = int(location[0])
        for i in range(x, x+3):
            for j in range(y, y+4):
                self.schem.setBlock((i, 0, j), structure)

        self.schem.setBlock((x, 1, y), redstone_alldir)
        self.schem.setBlock((x+2, 1, y), redstone_alldir)

        self.schem.setBlock((x, 1, y+1), structure)
        self.schem.setBlock((x+1, 1, y+1), repeater_side)
        self.schem.setBlock((x+2, 1, y+1), repeater_forward)

        self.schem.setBlock((x, 1, y+2), torch_forward)
        self.schem.setBlock((x+1, 1, y+2), repeater_side)
        self.schem.setBlock((x+2, 1, y+2), repeater_forward)

        # self.schem.setBlock((x+2,1,y+3), redstone_alldir)
        self.placeDownFromGate((y+3, x+2))
        self.placeUpToGate((y, x))
        self.placeUpToGate((y, x+2))

    def placeRepeater(self, location, kind, layer):
        x = int(location[1])
        y = int(location[0])
        repeater_north = "minecraft:repeater[facing=south]"
        repeater_south = "minecraft:repeater[facing=north]"
        repeater_east = "minecraft:repeater[facing=west]"
        repeater_west = "minecraft:repeater[facing=east]"
        height = 0
        if layer == 1:
            height = -5
        if layer == 2:
            height = -11

        self.schem.setBlock((x, height, y), structure)
        if (kind == REPEATER_NORTH):
            self.schem.setBlock((x, height+1, y), repeater_north)
        if (kind == REPEATER_SOUTH):
            self.schem.setBlock((x, height+1, y), repeater_south)
        if (kind == REPEATER_EAST):
            self.schem.setBlock((x, height+1, y), repeater_east)
        if (kind == REPEATER_WEST):
            self.schem.setBlock((x, height+1, y), repeater_west)

    def output(self):
        self.schem.save("./", "schematicfile", mcschematic.Version.JE_1_20_1)

    def placeGates(self, Blocks):

        gateIds = []
        gatelocations = []
        gateType = []
        inputIds = []
        inputLocations = []
        outputIds = []
        outputLocations = []
        # identify all the gate ids

        for x in range(len(Blocks)):
            for y in range(len(Blocks[0])):
                curBlock = Blocks[x][y][0]
                if curBlock.block_type <= 5 and curBlock.block_type >= 0 and curBlock.id != -1:
                    if curBlock.id not in gateIds:
                        gateIds.append(curBlock.id)
                        gatelocations.append((x, y))
                        gateType.append(curBlock.block_type)
                if (curBlock.block_type == INPUT):
                    inputLocations.append((x, y))
                    inputIds.append(curBlock.id)
                if (curBlock.block_type == OUTPUT):
                    outputLocations.append((x, y))
                    outputIds.append(curBlock.id)

        for l in range(1, len(Blocks[0][0])):
            for x in range(len(Blocks)):
                for y in range(len(Blocks[0])):
                    curBlock = Blocks[x][y][l]  # dust
                    if (l == 2 and curBlock.id == 1 and curBlock.block_type != VIA_UP):
                        print(
                            "PANICCCCCCCC AAAAAAAAAAAAAAAAAAAAAAAA#############################")
                        print(curBlock)
                    # if(l == 2): print(curBlock)
                    if curBlock.block_type == REDSTONE:  # if its dust
                        self.placeLayerDust((x, y), l)
                    if curBlock.block_type == VIA_UP:  # if its a via up
                        # print("here")
                        self.placeViaUp((x, y), 2)
                    if curBlock.block_type == VIA_DOWN:
                        self.placeViaDown((x, y), 1)
                    if curBlock.block_type == GATE_OUTPUT:
                        # check the surrounding blocks
                        if not is_redstone_ish(Blocks[x+1][y][l]) and not is_redstone_ish(Blocks[x][y+1][l]) and not is_redstone_ish(Blocks[x-1][y][l]) and not is_redstone_ish(Blocks[x][y-1][l]):
                            print("GOT HERE YAAAYYYYY")
                            self.doubleDown((x, y))
                    if curBlock.block_type >= REPEATER_NORTH and curBlock.block_type <= REPEATER_EAST:
                        self.placeRepeater((x, y), curBlock.block_type, l)

        for i in range(len(gateIds)):
            gatetype = int(gateType[i])
            # print(gatetype)
            if (gatetype == 0):
                # print("here")
                # and
                self.placeAND(gatelocations[i])
            if (gatetype == 1):
                # print("Here")
                # OR
                self.placeOR(gatelocations[i])
            if (gatetype == 2):
                # print("Here")
                # NOT
                self.placeNOT(gatelocations[i])
            if (gatetype == 3):
                # print("Here")
                # NOR
                self.placeNOR(gatelocations[i])
            if (gatetype == 4):
                # print("Here")
                # NAND
                self.placeNAND(gatelocations[i])
            if (gatetype == 5):
                # print("Here")
                # DFF
                self.placeDFF(gatelocations[i])

        # print(gateIds)
        # print(gatelocations)
        # print(gateType)
        # print(inputLocations)


nodes = read_input().read_gates("./yosys/opt6.json")
inputs = read_input().read_inputs("./yosys/opt6.json")
outputs = read_input().read_outputs("./yosys/opt6.json")

while True:
    try:
        random.shuffle(nodes)
        blocks = route(nodes, inputs, outputs)
        break
    except Exception:
        pass
converter = minecraftConverter()
converter.placeGates(blocks)
converter.output()

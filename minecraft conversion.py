import mcschematic
from routing import *
redstone_alldir = "minecraft:redstone_wire[north=side,east=side,south=side,west=side]"
redstone_ew = "minecraft:redstone_wire[east=side,west=side]"
redstone_ns = "minecraft:redstone_wire[north=side,south=side]"
repeater_forward = "minecraft:repeater[facing=north]"
torch_forward = "minecraft:redstone_wall_torch[facing=south]"
torch_up = "minecraft:redstone_torch"
structure = "minecraft:stone"
class minecraftConverter:
    def __init__(self):
        self.schem = mcschematic.MCSchematic()
        # self.schem.setBlock((0,-1,0), "minecraft:stone")

    def placeAND(self, location):
        x = int(location[1])
        y = int(location[0])
        print(x,y)
        print("here")
        for i in range(x, x+3):
            for j in range(y, y+4):
                self.schem.setBlock((i,0,j), "minecraft:stone")

        for i in range(x, x+3):
            self.schem.setBlock((i,1,y+1), "minecraft:stone")
        
        self.schem.setBlock((x,1,y), redstone_alldir)
        self.schem.setBlock((x+2,1,y), redstone_alldir)
        self.schem.setBlock((x+1,1,y+2), torch_forward)
        self.schem.setBlock((x+1,1,y+3), repeater_forward)
        
        self.schem.setBlock((x,2,y+1), torch_up)
        self.schem.setBlock((x+1,2,y+1), redstone_ew)
        self.schem.setBlock((x+2,2,y+1), torch_up)

    def placeOR(self, location):
        x = int(location[1])
        y = int(location[0])
        print(x,y)
        print("here")
        for i in range(x, x+3):
            for j in range(y, y+4):
                self.schem.setBlock((i,0,j), "minecraft:stone")
        
        for i in range(x, x+3):
            self.schem.setBlock((i,1,y+1), "minecraft:stone")


        self.schem.setBlock((x,1,y), redstone_alldir)
        self.schem.setBlock((x+2,1,y), redstone_alldir)
        self.schem.setBlock((x+1,1,y+2), redstone_alldir)
        self.schem.setBlock((x+1,1,y+3), repeater_forward)
        
        self.schem.setBlock((x,2,y+1), redstone_alldir)
        self.schem.setBlock((x+1,2,y+1), redstone_alldir)
        self.schem.setBlock((x+2,2,y+1), redstone_alldir)

    
    def placeNOR(self, location):
        x = int(location[1])
        y = int(location[0])
        print(x,y)
        print("here")
        for i in range(x, x+3):
            for j in range(y, y+4):
                self.schem.setBlock((i,0,j), "minecraft:stone")
        
        for i in range(x, x+3):
            self.schem.setBlock((i,1,y+1), "minecraft:stone")


        self.schem.setBlock((x,1,y), redstone_alldir)
        self.schem.setBlock((x+2,1,y), redstone_alldir)
        self.schem.setBlock((x+1,1,y+2), torch_forward)
        self.schem.setBlock((x+1,1,y+3), redstone_alldir)
        
        self.schem.setBlock((x,2,y+1), redstone_alldir)
        self.schem.setBlock((x+1,2,y+1), redstone_alldir)
        self.schem.setBlock((x+2,2,y+1), redstone_alldir)
    def placeNOT(self, location):
        x = int(location[1])
        y = int(location[0])
        for i in range(x, x+3):
            for j in range(y, y+4):
                self.schem.setBlock((i,0,j), "minecraft:stone")

        
        self.schem.setBlock((x+1,1,y),redstone_alldir)
        self.schem.setBlock((x+1,1,y+1),structure)
        self.schem.setBlock((x+1,1,y+2),torch_forward)
        self.schem.setBlock((x+1,1,y+3),redstone_alldir)
        

        
    def output(self):
        self.schem.save("./","schematicfile", mcschematic.Version.JE_1_20_1)
    def placeGates(self,Blocks):
        

        gateIds = []
        gatelocations = []
        gateType = []
        inputIds = []
        inputLocations = []
        outputIds = []
        outputLocations = []
        #identify all the gate ids
        
        for x in range(len(Blocks)):
            for y in range(len(Blocks[0])):
                curBlock = Blocks[x][y][0]
                if curBlock.block_type <= 5 and curBlock.block_type >= 0 and curBlock.id != -1: 
                    if curBlock.id not in gateIds:
                        gateIds.append(curBlock.id)
                        gatelocations.append((x,y))
                        gateType.append(curBlock.block_type)
                if(curBlock.block_type == 8):
                    inputLocations.append((x,y))
                    inputIds.append(curBlock.id)
                if(curBlock.block_type == 9):
                    outputLocations.append((x,y))
                    outputIds.append(curBlock.id)
        
        print(gateIds)
        #print(gatelocations)
        print(gateType)
        #print(inputLocations)
        for i in range(len(gateIds)):
            gatetype = int(gateType[i])
            print(gatetype)
            if(gatetype == 0):
                print("here")
                #and
                self.placeAND(gatelocations[i])
            if(gatetype == 1):
                print("Here")
                #OR
                self.placeOR(gatelocations[i])
            if(gatetype == 2):
                print("Here")
                #NOT
                self.placeNOT(gatelocations[i])
            if(gatetype == 3):
                print("Here")
                #NOR
                self.placeNOR(gatelocations[i])
            if(gatetype == 4):
                print("Here")
                #NAND
                self.placeNAND(gatelocations[i])
            if(gatetype == 5):
                print("Here")
                #DFF
                self.placeDFF(gatelocations[i])
            
            


        
nodes = read_input().read_gates("./yosys/opt6.json")
inputs = read_input().read_inputs("./yosys/opt6.json")
outputs = read_input().read_outputs("./yosys/opt6.json")
blocks = place(nodes, inputs, outputs)

converter = minecraftConverter()
converter.placeGates(blocks)
converter.output()
# array of nodes, index of which is the id
import json
import constants
nodelist = []

class Node:
    node_type: int = 0
    id: int = 0
    # list of integers representing the nodes this node connects to
    #outputs: list[int] = []

    # list of integers representing the nodes that connect to this node
    #inputs: list[int] = []
    input_wires = []
    output_wire: int = 0
class read_input:
    def __init__(self) -> None:
        pass
    def read(self, path):
        print("here")
        f = open("./yosys/opt6.json")
        loaded = json.load(f)
        cells = loaded["modules"]["counter"]["cells"]
        tempNodes = []

        for cellname in cells:
            cell = cells[cellname]
            newNode = Node()
            newNode.node_type = constants.string_constant[cell["type"]]
            connections = cell["connections"]
            input_wires = []
            output_wire = 0
            for connection in connections:
                if(cell["port_directions"][connection] == "input"): input_wires.append(connections[connection][0])
                if(cell["port_directions"][connection] == "output"): output_wire = int(connections[connection][0])
            newNode.temp_input_wires = input_wires
            newNode.temp_output_wire = output_wire
            newNode.id = len(tempNodes)  # Assign the node's id
            tempNodes.append(newNode)
            print(newNode.id, newNode.node_type, newNode.temp_input_wires, newNode.temp_output_wire)
        
        # for node1 in tempNodes:
        #     for node2 in tempNodes:
        #         if(node1.id == node2.id): continue
        #         if(node1.temp_output_wire in node2.temp_input_wires): node1.outputs.append(node2.id)
        #         if(node2.temp_output_wire in node1.temp_input_wires): node1.inputs.append(node2.id)
        #     print(node1.id, node1.outputs, node1.inputs)
        
        for node in tempNodes:
            nodelist.append( node)

        for node in nodelist:
            print()

reader = read_input()
reader.read("thing")

# array of nodes, index of which is the id
import json
nodelist = []
class Node:
    node_type: int = 0
    id: int = 0
    # list of integers representing the nodes this node connects to
    outputs: list[int] = []

    # list of integers representing the nodes that connect to this node
    inputs: list[int] = []

class read_input:
    def __init__(self) -> None:
        pass
    def read(self, path):
        print("here")
        f = open("./yosys/opt6.json")
        loaded = json.load(f)
        cells = loaded["modules"]["counter"]["cells"]
        for cell in cells:
            newNode = Node()
            cells[cell]["type"]

reader = read_input()
reader.read("thing")
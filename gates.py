from constants import *

class Gate:
    input_locations: list[tuple[int]] = []
    output_location: tuple[int] = []

    def __init__(self, inputs, outputs):
        self.input_locations = inputs
        self.output_location = outputs

gates = {
        AND: Gate([(0, 0), (0, 2)], (1, 3)), 
        OR: Gate([(0, 0), (0, 2)], (1, 3)), 
        NOT: Gate([(1, 0)], (1, 3)),
        NOR: Gate([(0, 0), (0, 2)], (1, 3)), 
        NAND: Gate([(0, 0), (0, 2)], (1, 3)), 
        DFF: Gate([(0, 0), (0, 2)], (0,  3)),
        }
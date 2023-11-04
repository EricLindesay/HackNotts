from constants import *

class Gate:
    input_locations: list[tuple[int]] = []
    output_location: tuple[int] = []

    def __init__(self, inputs, outputs):
        self.input_locations = inputs
        self.output_location = outputs

    def __str__(self):
        return f"Gate<{self.input_locations=}, {self.output_location=}>"

gates = {
        AND: Gate([(0, 0), (2, 0)], (1, 3)),
        OR: Gate([(0, 0), (2, 0)], (1, 3)),
        NOT: Gate([(1, 0)], (1, 3)),
        NOR: Gate([(0, 0), (2, 0)], (1, 3)),
        NAND: Gate([(0, 0), (2, 0)], (1, 3)),
        DFF: Gate([(0, 0), (2, 0)], (0,  3)),
        }
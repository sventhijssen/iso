import re

from core.crossbars.SelectorCrossbar import SelectorCrossbar
from core.expressions.BooleanExpression import LITERAL
from core.crossbars.MemristorCrossbar import MemristorCrossbar


class CrossbarReader:

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.crossbar = None

    def read(self):
        rows = 0
        columns = 0
        input_variables = None
        input_nanowires = dict()
        output_nanowires = dict()
        is_selector_crossbar = False
        selectorlines = []

        with open(self.file_name, 'r') as f:
            for line in f.readlines():

                if line.startswith(".type "):
                    (_, raw_value) = line.split()
                    is_selector_crossbar = raw_value == "selector"

                if line.startswith(".rows "):
                    (_, raw_value) = line.split()
                    rows = int(raw_value)

                elif line.startswith(".columns "):
                    (_, raw_value) = line.split()
                    columns = int(raw_value)

                elif line.startswith(".inputs "):
                    raw_values = line.split()
                    input_variables = set(raw_values[1:])

                elif line.startswith(".i "):
                    raw_values = line.split()
                    if len(raw_values) == 3:
                        input_nanowires[raw_values[1]] = (0, int(raw_values[2]))
                    elif len(raw_values) == 4:
                        input_nanowires[raw_values[1]] = (int(raw_values[2]), int(raw_values[3]))
                    else:
                        raise Exception("Length incorrect.")

                elif line.startswith(".o "):
                    raw_values = line.split()
                    if len(raw_values) == 3:
                        output_nanowires[raw_values[1]] = (0, int(raw_values[2]))
                    elif len(raw_values) == 4:
                        output_nanowires[raw_values[1]] = (int(raw_values[2]), int(raw_values[3]))
                    else:
                        raise Exception("Length incorrect.")

                elif line.startswith(".s "):
                    raw_values = line.split()
                    if len(raw_values) == 3:
                        raw_literal = raw_values[2]
                        if raw_literal.startswith("~"):
                            literal = LITERAL(raw_literal[1:], False)
                        else:
                            literal = LITERAL(raw_literal, True)
                        selectorlines.append(literal)
                    else:
                        raise Exception("Length incorrect.")

        if is_selector_crossbar:
            self.crossbar = SelectorCrossbar(rows, columns)
            self.crossbar.selectorlines = selectorlines
        else:
            self.crossbar = MemristorCrossbar(rows, columns)

        self.crossbar.input_variables = input_variables
        self.crossbar.input_nanowires = input_nanowires
        self.crossbar.output_nanowires = output_nanowires

        with open(self.file_name, 'r') as f:
            r = 0
            c = 0
            read = False
            for line in f.read().splitlines():

                if line.startswith(".end"):
                    read = False

                if read:
                    for element in line.split("\t"):
                        raw_literal = re.findall(r'(-|0|1|[\[\]a-z0-9]+|~[\[\]a-z0-9]+)', element)[0]
                        if raw_literal == '0':
                            self.crossbar.set_memristor(r, c, LITERAL('False', False))
                        elif raw_literal == '1':
                            self.crossbar.set_memristor(r, c, LITERAL('True', True))
                        elif raw_literal[0] == '~':
                            self.crossbar.set_memristor(r, c, LITERAL(raw_literal[1:], False))
                        else:
                            self.crossbar.set_memristor(r, c, LITERAL(raw_literal, True))
                        c += 1
                    c = 0
                    r += 1

                if line.startswith(".xbar"):
                    read = True

        return self.crossbar

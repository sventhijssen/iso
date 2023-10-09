from __future__ import annotations

import copy
import json
import random
from pathlib import Path

from typing import Dict, Set, Any

import numpy as np
from networkx import has_path

from core.BooleanFunction import BooleanFunction
from core.crossbars.Crossbar import Crossbar
from core.expressions.BooleanExpression import LITERAL, TRUE, FALSE


class SelectorCrossbar(Crossbar):
    """
    Type of crossbar where selectorlines are assigned to nanowires.
    """

    def __init__(self, rows: int, columns: int, name: str = None, compressed: bool = False):
        super().__init__(rows, columns, name=name, compressed=compressed)
        self.wordlines = []  # Nodes in BDD
        self.selectorlines = []  # Edges in BDD

    def get_input_variables(self) -> Set[str]:
        input_variables = set()
        for selectorline in self.selectorlines:
            if isinstance(selectorline, LITERAL):
                input_variables.add(selectorline.atom)
        return input_variables

    def get_output_variables(self) -> Set[str]:
        output_variables = set()
        for output_variable in self.get_output_nanowires().keys():
            output_variables.add(output_variable)
        return output_variables

    def get_auxiliary_variables(self) -> Set[str]:
        return set()

    def get_log(self) -> Dict:
        return {
            "id": id(self),
            "type":  self.__class__.__name__,
            "name": id(self),  # TODO: Fix name issues
            "rows": self.rows,
            "columns": self.columns,
            "wordlines": list(map(lambda func: str(func), self.wordlines)),
            "selectorlines": list(map(lambda lit: str(lit), self.selectorlines)),
            "layers": self.layers,
            "input_nanowires": self.input_nanowires,
            # A key maps to a set of values. However, JSON cannot encode a set, thus we convert it into a list.
            "output_nanowires": dict(map(lambda item: (item[0], list(item[1])), self.output_nanowires.items()))
        }

    def fix(self, atom: str, positive: bool) -> Crossbar:
        raise NotImplementedError()

    def to_string(self) -> str:
        raise NotImplementedError()

    def to_json(self) -> Dict[Any, Any]:
        graph = self.graph()
        return {
            "type": "crossbar",
            "subtype": "selector",
            "name": self.get_name(),
            "rows": self.rows,
            "columns": self.columns,
            "layers": self.layers,
            "input_nanowires": self.input_nanowires,
            # A key maps to a set of values. However, JSON cannot encode a set, thus we convert it into a list.
            "output_nanowires": dict(map(lambda item: (item[0], list(item[1])), self.output_nanowires.items())),
            "wordlines": list(map(lambda func: str(func), self.wordlines)),
            "selectorlines": list(map(lambda lit: str(lit), self.selectorlines)),
            "graph":
                {
                    "nodes": list(graph.nodes),
                    "edges": list(graph.edges)
                }
        }

    def write(self, file_path: Path):
        json_content = self.to_json()
        json_string = json.dumps(json_content, indent=6)
        with open(file_path, "w") as f:
            f.write(json_string)
            f.write("\n")

    def draw(self, name: str = None) -> Set[str]:

        # We draw a separate crossbar matrix for each layer of memristors.
        # Grid after https://graphviz.org/Gallery/undirected/grid.html
        # Node distance after https://newbedev.com/how-to-manage-distance-between-nodes-in-graphviz
        if name is None:
            name = "g{}".format(random.randint(0, 100))

        if self.get_memristor_layers() > 1:
            raise Exception("Only single memristor layer supported.")

        layer = 0
        content = ''
        content += 'graph {} {{\n'.format(name)
        content += '\tgraph [nodesep="0.2", ranksep="0.2"];\n'
        content += '\tcharset="UTF-8";\n'
        content += '\tratio=fill;\n'
        content += '\tsplines=polyline;\n'
        content += '\toverlap=scale;\n'
        content += '\tnode [shape=circle, fixedsize=true, width=0.4, fontsize=8];\n'
        content += '\n'

        content += '\n\t// Memristors\n'
        for c in range(self.columns):
            for r in range(self.rows):
                if self.get_memristor(r, c, layer).literal.atom == 'False':
                    v = '0'
                    style = 'color="#000000", fillcolor="#eeeeee", style="filled,solid"'
                elif self.get_memristor(r, c, layer).literal.atom == 'True':
                    v = '1'
                    style = 'color="#000000", fillcolor="#cadfb8", style="filled,solid"'
                else:
                    if not self.get_memristor(r, c, layer).literal.positive:
                        v = '¬' + self.get_memristor(r, c, layer).literal.atom
                    else:
                        v = self.get_memristor(r, c, layer).literal.atom
                    style = 'color="#000000", fillcolor="#b4c7e7", style="filled,solid"'
                content += '\tm{}_{} [label="{}" {}]\n'.format(r + 1, c + 1, v, style)

        content += '\n\t// Functions (left y-axis)\n'
        # Functions
        for r in range(len(self.wordlines)):
            input_rows = list(map(lambda i: i[1], self.get_input_nanowires().values()))
            style = 'color="#ffffff", fillcolor="#ffffff", style="filled,solid"'
            if r not in input_rows:
                v = '{}'.format(self.wordlines[r])
                content += '\tm{}_{} [label="{}" {}]\n'.format(r + 1, 0, v, style)
            else:
                v = ''
                for (input_function, (layer, row)) in self.get_input_nanowires().items():
                    if r == row:
                        v = 'Vin<SUB>{}</SUB>'.format(input_function)
                content += '\tm{}_{} [label=<{}> {}]\n'.format(r + 1, 0, v, style)
        for r in range(len(self.wordlines), self.rows):
            style = 'color="#ffffff", fillcolor="#ffffff", style="filled,solid"'
            v = ''
            content += '\tm{}_{} [label="{}" {}]\n'.format(r + 1, 0, v, style)

        content += '\n\t// Outputs (right y-axis)\n'
        # Outputs
        output_variables = dict()
        for (o, (l, r)) in self.output_nanowires.items():
            if (l, r) in output_variables:
                output_variables[(l, r)].append(o)
            else:
                output_variables[(l, r)] = [o]
        for ((l, r), os) in output_variables.items():
            if layer == l:
                for i in range(len(os)):
                    v = os[i]
                    style = 'color="#ffffff", fillcolor="#ffffff", style="filled,solid"'
                    content += '\tm{}_{} [label="{}" {}];\n'.format(r + 1, self.columns + 1, v, style)

        content += '\n\t// Crossbar\n'
        # Important: The description of the grid is transposed when being rendered -> rows and columns are switched
        for r in range(self.rows):
            input_rows = list(map(lambda i: i[1], self.get_input_nanowires().values()))
            content += '\trank=same {\n'
            for c in range(self.columns):
                if r not in input_rows and c == 0:
                    content += '\t\tm{}_{} -- m{}_{} [style=invis];\n'.format(r + 1, c, r + 1, c + 1)
                else:
                    content += '\t\tm{}_{} -- m{}_{};\n'.format(r + 1, c, r + 1, c + 1)

            # TODO: Change layer
            if (0, r) in output_variables:
                content += '\t\tm{}_{} -- m{}_{};\n'.format(r + 1, self.columns, r + 1, self.columns + 1)
            content += '\t}\n'

        for c in range(self.columns):
            content += '\t' + ' -- '.join(["m{}_{}".format(r + 1, c + 1) for r in range(self.rows)]) + '\n'

        content += '\n\t// Literals (bottom x-axis)\n'
        # content += '\tedge [style=invis];\n'
        # Literals
        for c in range(len(self.selectorlines)):
            v = '{}'.format(str(self.selectorlines[c]).replace("\\+", "¬"))
            style = 'color="#ffffff", fillcolor="#ffffff", style="filled,solid"'
            content += '\tm{}_{} [label="{}" {}];\n'.format(self.rows + 1, c + 1, v, style)
            content += '\tm{}_{} -- m{}_{};\n'.format(self.rows, c + 1, self.rows + 1, c + 1)

        for c in range(len(self.selectorlines), self.columns):
            style = 'color="#ffffff", fillcolor="#ffffff", style="filled,solid"'
            v = '—'
            content += '\tm{}_{} [label="{}" {}];\n'.format(self.rows + 1, c + 1, v, style)
            content += '\tm{}_{} -- m{}_{};\n'.format(self.rows, c + 1, self.rows + 1, c + 1)
        content += '\trank=same {' + ' '.join(
            ["m{}_{}".format(self.rows + 1, c + 1) for c in range(self.columns)]) + '}\n'

        # # Outputs
        # output_variables = dict()
        # for (o, (l, r)) in self.output_nanowires.items():
        #     if (l, r) in output_variables:
        #         output_variables[(l, r)].append(o)
        #     else:
        #         output_variables[(l, r)] = [o]
        # for ((l, r), os) in output_variables.items():
        #     if layer == l:
        #         for i in range(len(os)):
        #             v = os[i]
        #             style = 'color="#ffffff", fillcolor="#ffffff", style="filled,solid"'
        #             content += '\t m{}_{} [label="{}" {}];\n'.format(r, self.columns + 2, v, style)
        #         content += '\t m{}_{} -- m{}_{};\n'.format(r, self.columns + 1, r, self.columns + 2)
        # content += '\\draw (n%d_%d) -- (n%d_%d);\n' % (self.columns, self.rows - r, self.columns + 1, self.rows - r)

        content += '}'

        return {content}

    def get_functions(self):
        functions = []
        for (node, _) in self.wordlines:
            functions.append(node)
        return functions

    def __copy__(self):
        crossbar = SelectorCrossbar(self.rows, self.columns)
        for r in range(self.rows):
            for c in range(self.columns):
                crossbar.set_memristor(r, c, self.get_memristor(r, c).literal)
        crossbar.input_variables = self.input_variables.copy()
        crossbar.input_nanowires = self.input_nanowires.copy()
        crossbar.output_nanowires = self.output_nanowires.copy()
        return crossbar

    def instantiate(self, instance: Dict[str, bool]) -> SelectorCrossbar:
        crossbar = copy.deepcopy(self)

        for c in range(len(self.selectorlines)):
            literal = self.selectorlines[c]
            if literal == LITERAL("False", False):
                for r in range(crossbar.rows):
                    crossbar.set_memristor(r, c, LITERAL("False", False))
            elif literal == LITERAL("True", True):
                continue
            else:
                if not instance[literal.atom] and literal.positive:
                    for r in range(crossbar.rows):
                        crossbar.set_memristor(r, c, LITERAL("False", False))
                elif instance[literal.atom] and not literal.positive:
                    for r in range(crossbar.rows):
                        crossbar.set_memristor(r, c, LITERAL("False", False))
        return crossbar

    def eval(self, instance: Dict[str, bool], input_function: str = "1") -> Dict[str, bool]:
        crossbar_instance = self.instantiate(instance)
        graph = crossbar_instance.graph().copy()
        not_stuck_on_edges = [(u, v) for u, v, d in graph.edges(data=True) if
                              not (d['atom'] == 'True' and d['positive'])]
        graph.remove_edges_from(not_stuck_on_edges)

        evaluation = dict()
        for (output_variable, (output_layer, output_nanowire)) in self.output_nanowires.items():
            source = "L{}_{}".format(output_layer, output_nanowire)
            input_layer, input_nanowire = crossbar_instance.get_input_nanowire(input_function)
            sink = "L{}_{}".format(input_layer, input_nanowire)

            is_true = has_path(graph, source, sink)
            evaluation[output_variable] = is_true

        return evaluation

from typing import Dict, Set

from networkx import DiGraph

from core.BooleanFunction import BooleanFunction
from core.BooleanFunctionCollection import BooleanFunctionCollection
from core.DrawInterface import DrawInterface
from core.decision_diagrams.BDD import BDD


class BDDTopology(BooleanFunctionCollection, DrawInterface):

    def __init__(self, topology: DiGraph, bdds: Dict[str, BDD]):
        super().__init__()
        self.topology = topology
        self.bdds = bdds

    def get_input_variables(self) -> Set[str]:
        pass

    def get_output_variables(self) -> Set[str]:
        pass

    def get_auxiliary_variables(self) -> Set[str]:
        pass

    def get_boolean_functions(self) -> Set[BooleanFunction]:
        bdds = set()
        for bdd in self.bdds.values():
            bdds.add(bdd)
        return bdds

    def eval(self, instance: Dict[str, bool]) -> Dict[str, bool]:
        pass

    def draw(self) -> Set[str]:
        contents = set()
        for bdd in self.bdds.values():
            dot = list(bdd.draw())[0]
            contents.add(dot)
        return contents

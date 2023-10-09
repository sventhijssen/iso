from typing import List

from aux import config
from aux.BDDIsomorphism import BDDIsomorphism
from core.decision_diagrams.BDDCollection import BDDCollection
from core.decision_diagrams.BDDTopology import BDDTopology
from cli.Command import Command


class BDDIsomorphismCommand(Command):

    def __init__(self, args: List[str]):
        super().__init__()

        if "-D" not in args:
            self.dimension = None
        else:
            idx = args.index("-D")
            self.dimension = int(args[idx + 1])

    def execute(self):
        context = config.context_manager.get_context()

        bdd_collection = BDDCollection()

        assert isinstance(context, BDDTopology)
        bdd_isomorphism = BDDIsomorphism(context, self.dimension)
        bdd_isomorphism.find()

        config.context_manager.add_context("bdd_collection", bdd_collection)

        return False

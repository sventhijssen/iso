from aux import config
from aux.KLUTParser import KLUTParser
from cli.Command import Command


class KLUTCommand(Command):

    def __init__(self, args):
        super().__init__()

        if "-K" in args:
            idx = args.index("-K")
            self.K = int(args[idx + 1])
        else:
            self.K = None

    def execute(self) -> bool:
        boolean_function_collection = config.context_manager.get_context()

        collection = None
        for boolean_function in boolean_function_collection.boolean_functions:
            parser = KLUTParser(boolean_function, self.K)
            bdd_topology = parser.parse()
            collection = bdd_topology

        config.context_manager.add_context("", collection)

        return False

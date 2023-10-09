from typing import Dict, Any

from aux import config
from aux.BenchmarkReader import BenchmarkReader
from cli.Command import Command
from core.BooleanFunctionCollection import BooleanFunctionCollection


class ReadCommand(Command):

    def __init__(self, args):
        super(ReadCommand).__init__()
        if len(args) < 1:
            raise Exception("No file defined.")
        if "-depr" in args:
            self.deprecated = True
        else:
            self.deprecated = False
        self.relative_file_path = args[0]

    def execute(self):
        benchmark_reader = BenchmarkReader(self.relative_file_path)
        boolean_function_collection = benchmark_reader.read(self.deprecated)
        config.context_manager.add_context("", boolean_function_collection)

        return False

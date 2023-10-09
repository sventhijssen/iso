import os
from pathlib import Path

from cli.Program import Program

benchmarks = [
    # ("c432", True),
    # ("c499", False),
    ("c880", False),
    # ("c1355", False),
    # ("c1908", False),
    # ("c2670", False),
    # ("c3540", False),
    # ("c5315", False),
    # ("c7552", False)
]

current_filepath = Path(os.getcwd())
previous_step_directory = current_filepath.parent.parent.joinpath("benchmarks").joinpath("iscas85")

for benchmark_name, sbdd in benchmarks:
    log_filepath = current_filepath.joinpath("iscas85").joinpath("{}.log".format(benchmark_name))
    benchmark_filepath = previous_step_directory.joinpath("{}.blif".format(benchmark_name))
    bdd_filepath = current_filepath.joinpath("iscas85").joinpath("{}.bdd".format(benchmark_name))

    if sbdd:
        bdd = "sbdd"
    else:
        bdd = "robdd"

    Program.execute("new_log {} | read {} | {} | write {}".format(log_filepath, benchmark_filepath, bdd, bdd_filepath))

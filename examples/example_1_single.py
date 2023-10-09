import os
from pathlib import Path

from cli.Program import Program

benchmark_name = "c432"
sbdd = True

current_filepath = Path(os.getcwd())

benchmark_file_path = current_filepath.joinpath("{}.blif".format(benchmark_name))
log_file_path = current_filepath.joinpath("example_1_{}.log".format(benchmark_name))
bdd_file_path = current_filepath.joinpath("example_1_{}.bdd".format(benchmark_name))

if sbdd:
    bdd = "sbdd"
else:
    bdd = "robdd"

# Recall that each node in the BDD is assigned to a wordline and each edge is assigned to a selectorline
# Source: https://dl.acm.org/doi/pdf/10.1145/3489517.3530596
# Hence, the crossbar dimensions can be deduced from "nodes" and "edges" in the log file.
Program.execute("new_log {} | read {} | {} | write {}".format(log_file_path, benchmark_file_path, bdd, bdd_file_path))

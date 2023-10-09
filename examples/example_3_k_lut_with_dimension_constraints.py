import os
from pathlib import Path

from cli.Program import Program

benchmark_name = "c432"
k = 6
D = 128

current_filepath = Path(os.getcwd())

benchmark_file_path = current_filepath.joinpath("{}.blif".format(benchmark_name))
log_file_path = current_filepath.joinpath("example_3_{}.log".format(benchmark_name))

# Recall that each node in the BDD is assigned to a wordline and each edge is assigned to a selectorline
# Source: https://dl.acm.org/doi/pdf/10.1145/3489517.3530596
# Hence, the crossbar dimensions can be deduced from "nodes" and "edges" in the log file.
Program.execute("new_log {} | read {} | klut -K {} | bddiso -D {}".format(log_file_path, benchmark_file_path, k, D))

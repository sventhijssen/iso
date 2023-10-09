import os
from pathlib import Path

from cli.Program import Program

benchmark_names = [
    "c432",
    "c499",
    "c880",
    "c1355",
    "c1908",
    "c2670",
    "c3540",
    "c5315",
    "c6288",
    "c7552"
]

k = 12

current_directory = Path(os.getcwd())
benchmark_directory = current_directory.joinpath("benchmarks")
k_directory = current_directory.joinpath("k{}".format(k))
log_directory = k_directory.joinpath("logs")

for benchmark_name in benchmark_names:
    print("Benchmark: {}".format(benchmark_name))
    benchmark_file_path = benchmark_directory.joinpath("{}.blif".format(benchmark_name))
    log_file_path = log_directory.joinpath("{}.log".format(benchmark_name))
    program = Program()
    Program.execute("new_log {} | read {} | klut -K {} | bddiso".format(log_file_path, benchmark_file_path, k))

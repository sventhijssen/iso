import os
import shutil
from pathlib import Path

from aux import config
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

Ks = [4, 6, 8]
Ds = [64, 128, 256, 512]

current_directory = Path(os.getcwd())
benchmark_directory = current_directory.joinpath("benchmarks")
abc_directory = config.abc_path

for benchmark_name in benchmark_names:
    print("Benchmark: {}".format(benchmark_name))
    benchmark_file_path = benchmark_directory.joinpath("{}.blif".format(benchmark_name))
    for D in Ds:
        d_directory = current_directory.joinpath("d{}".format(D))
        if not d_directory.exists():
            os.mkdir(d_directory)
        for k in Ks:
            k_directory = d_directory.joinpath("k{}".format(k))
            if not k_directory.exists():
                os.mkdir(k_directory)

            log_directory = k_directory.joinpath("logs")
            lut_directory = k_directory.joinpath("kluts")

            if not log_directory.exists():
                os.mkdir(log_directory)
            if not lut_directory.exists():
                os.mkdir(lut_directory)
            log_file_path = log_directory.joinpath("{}.log".format(benchmark_name))
            program = Program()
            Program.execute("new_log {} | read {} | klut -K {} | bddiso -D {}".format(log_file_path, benchmark_file_path, k, D))

            blif_file_path = abc_directory.joinpath("{}.blif".format(benchmark_name))
            lut_file_path = lut_directory.joinpath("{}.blif".format(benchmark_name))
            if blif_file_path.exists():
                shutil.copy(blif_file_path, lut_file_path)
                os.remove(blif_file_path)
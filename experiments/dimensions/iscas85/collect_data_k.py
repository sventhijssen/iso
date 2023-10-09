import json
import os
from pathlib import Path

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
D = 128

current_directory = Path(os.getcwd())

results = []
for benchmark_name in benchmark_names:
    print(benchmark_name)
    result = []
    for k in Ks:
        print(k)
        d_directory = current_directory.joinpath("d{}".format(D))
        k_directory = d_directory.joinpath("k{}".format(k))
        log_directory = k_directory.joinpath("logs")
        log_file_path = log_directory.joinpath("{}.log".format(benchmark_name))

        if not log_file_path.exists():
            result.append('-')
            result.append('-')
            result.append('-')
            continue

        with open(log_file_path, 'r') as f:
            data = json.load(f)
            bdd2iso = data[-1]
            cycles1 = bdd2iso.get("cycles")
            cycles = cycles1.get("cycles")
            nr_loads = 0
            nr_evals = 0
            nr_cycles = len(cycles)
            for cycle in cycles:
                for instruction in cycle:
                    instruction_type = instruction.get("type")
                    if instruction_type == "LOAD":
                        nr_loads += 1
                    else:
                        nr_evals += 1
            result.append(nr_loads)
            result.append(nr_evals)
            result.append(nr_cycles)
    results.append(result)

with open("iscas85_d{}.csv".format(D), 'w') as f:
    for result in results:
        f.write("{}\n".format("\t".join(map(lambda r: str(r), result))))

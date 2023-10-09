import json
import os
from pathlib import Path

benchmarks = [
    ("c432", True),
    ("c499", False),
    ("c880", False),
    ("c1355", False),
    ("c1908", False),
    ("c2670", False),
    ("c3540", False),
    ("c5315", False),
    ("c7552", False)
]

current_filepath = Path(os.getcwd())

results = dict()
for benchmark_name, sbdd in benchmarks:
    log_filepath = current_filepath.joinpath("iscas85").joinpath("{}.log".format(benchmark_name))

    with open(log_filepath, 'r') as f:
        data = json.load(f)
        nodes = 0
        edges = 0
        for dd in data:
            nodes += dd.get("nodes")
            edges += dd.get("edges")
        results[benchmark_name] = [nodes, edges]

with open("results_iscas85.csv", 'w') as f:
    for benchmark_name, result in results.items():
        f.write("{}\t{}\n".format(result[0], result[1]))

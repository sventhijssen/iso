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

k = 12

current_directory = Path(os.getcwd())
k_directory = current_directory.joinpath("k{}".format(k))
log_directory = k_directory.joinpath("logs")

results = []
for benchmark_name in benchmark_names:
    result = []
    log_file_path = log_directory.joinpath("{}.log".format(benchmark_name))
    with open(log_file_path, 'r') as f:
        data = json.load(f)
        bdd2iso = data[-1]
        patterns = bdd2iso.get("patterns")
        for pattern in patterns:
            bdd_hash = pattern.get("hash")
            nr_bdds = pattern.get("nr_bdds")
            # result.append(bdd_hash)
            result.append(nr_bdds)
    results.append(sorted(result, reverse=True))

with open("iscas85_pattern_frequency_{}.csv".format(k), 'w') as f:
    for result in results:
        f.write("{}\n".format("\t".join(map(lambda r: str(r), result))))

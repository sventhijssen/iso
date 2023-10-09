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

current_directory = Path(os.getcwd())
log_directory = current_directory.joinpath("logs")

results = []
for benchmark_name in benchmark_names:
    result = []
    log_file_path = log_directory.joinpath("{}.log".format(benchmark_name))
    with open(log_file_path, 'r') as f:
        data = json.load(f)
        bdd2iso = data[-1]
        before = bdd2iso.get("before")
        result.append(before.get("rows"))
        result.append(before.get("cols"))
        result.append(before.get("cycles"))
        after = bdd2iso.get("after")
        result.append(after.get("rows"))
        result.append(after.get("cols"))
        result.append(after.get("cycles"))
    results.append(result)

with open("iscas85.csv", 'w') as f:
    for result in results:
        f.write("{}\n".format("\t".join(map(lambda r: str(r), result))))

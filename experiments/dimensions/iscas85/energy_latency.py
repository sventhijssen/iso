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

k = 4
D = 128

reram = {
    "read": {
        "energy": 1.08,
        "latency": 29.31
    },
    "write": {
        "energy": 3910,
        "latency": 50.88
    }
}

sram = {
    "read": {
        "energy": 58.97,
        "latency": 3.397
    },
    "write": {
        "energy": 57.57,
        "latency": 3.397
    }
}


current_directory = Path(os.getcwd())

results = []
for benchmark_name in benchmark_names:
    print(benchmark_name)
    result = []
    d_directory = current_directory.joinpath("d{}".format(D))
    k_directory = d_directory.joinpath("k{}".format(k))
    log_directory = k_directory.joinpath("logs")
    log_file_path = log_directory.joinpath("{}.log".format(benchmark_name))

    with open(log_file_path, 'r') as f:
        data = json.load(f)
        bdd2iso2 = data[-2]
        patterns = bdd2iso2.get("patterns")
        bdd2iso1 = data[-1]
        patterns_dict = dict()
        for pattern in patterns:
            bdd_hash = pattern.get("hash")
            patterns_dict[bdd_hash] = pattern
        cycles1 = bdd2iso1.get("cycles")
        cycles = cycles1.get("cycles")
        energy = 0
        latency = 0
        for cycle in cycles:
            for instruction in cycle:
                instruction_type = instruction.get("type")
                bdd_hash = instruction.get("hash")
                pattern = patterns_dict.get(bdd_hash)
                nodes = pattern.get("nodes")
                edges = pattern.get("edges")
                if instruction_type == "LOAD":
                    # ENERGY
                    energy += 2 * edges * reram.get("write").get("energy")
                else:
                    # ENERGY
                    # For evaluation, we must:
                    # 1. READ the inputs from SRAM
                    # 2. Evaluate the circuit in ReRAM
                    # 3. Write the outputs (always f and f') in ReRAM
                    energy += edges * sram.get("read").get("energy")
                    energy += nodes * reram.get("read").get("energy")
                    energy += 2 * sram.get("write").get("energy")

                    # LATENCY
                    # For evaluation, we must:
                    # 1. READ the inputs from SRAM
                    # 2. Evaluate the circuit in ReRAM
                    # 3. Write the outputs (always f and f') in ReRAM
                    latency += edges * sram.get("read").get("latency")
                    latency += nodes * reram.get("read").get("latency")
                    latency += 2 * sram.get("write").get("latency")
        result.append(energy)
        result.append(latency)
    results.append(result)

with open("iscas85_energy_latency.csv".format(D), 'w') as f:
    for result in results:
        f.write("{}\n".format("\t".join(map(lambda r: str(r), result))))

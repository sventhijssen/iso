### Example 1
In the first example, we will construct a binary decision diagram (BDD) for the benchmark.
The crossbar dimensions for a BDD with DAG G = (V, E) where V is the set of nodes and E is the set of edges are |V| x |E| [1].

For benchmark c432, the crossbar dimensions are 1291 x 2578 according to the log file.

[1] Thijssen, S., Jha, S. K., & Ewetz, R. (2022, July).
Path: Evaluation of boolean logic using path-based in-memory computing.
In Proceedings of the 59th ACM/IEEE Design Automation Conference (pp. 1129-1134).

### Example 2
In the second example, we will construct a k-LUT topology for the benchmark for k=6.

For benchmark c432 and k=6, the crossbar dimensions are 513 x 726 according to the log file.
<br>
When taking graph isomorphism into account, the crossbar dimensions can be reduced to 163 x 242.

### Example 3
In the third example, we consider dimensional constraints for the synthesis.

For benchmark c432, k=6 and D=128, a series of LOAD/EVAL operations are required.
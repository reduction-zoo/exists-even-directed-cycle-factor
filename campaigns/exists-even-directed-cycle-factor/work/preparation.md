# Preparation evidence

Prepared on 2026-09-26 before construction. The fixed corpus contains 113
distinct legal directed two-linkage instances: 13 hand-labelled edge cases
and 100 seeded random cases, with 59 YES and 54 NO decisions and four to
seven vertices. `generate_cases.py` retains seeds and construction rules;
`cases.json` stores checked paths or NO-SOLUTION. The source oracle
enumerates simple directed paths for the two terminal pairs and tests
vertex disjointness. Returned paths are validated directly against arcs,
endpoints and vertex sets. Exhaustion establishes negative answers on this
finite domain.

The target oracle uses Z3 4.16.0 to enumerate successor permutations
consistent with graph arcs, checking each resulting cycle decomposition
for an even cycle. Odd-only factors are blocked and enumeration continues;
UNSAT is conclusive and unknown is an error. Returned factors are checked
again by direct permutation, arc and cycle-parity validation. Independent
exhaustive permutation enumeration agreed on 100 distinct digraphs with
zero to six vertices, including constructed positive factors and random
negative instances. Hand fixtures distinguish an even directed two-cycle
from an odd three-cycle, reject loops and validate disjoint source paths.

[The primary paper](https://arxiv.org/html/2510.18393v1) defines a cycle
factor as vertex-disjoint cycles covering every vertex and explicitly allows
directed two-cycles. This oracle uses that interpretation.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/exists-even-directed-cycle-factor/work/check.py --self-test
```

The self-test starts with the corpus gate, regenerates random source
instances, checks stored labels and witnesses, and compares target decisions
with exhaustive permutation search. The candidate runner uses separate
forward and recovery subprocesses and up to three valid target factors per
source. An incorrect injected candidate was rejected after target solving
and source validation. No actual reduction candidate exists; finite checks
do not establish hardness or a general reduction.

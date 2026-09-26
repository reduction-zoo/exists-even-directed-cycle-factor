# Prepared input and output contract

The directed two-linkage source input is `{"vertices": n, "arcs":
[[u,v], ...], "pairs": [[s1,t1],[s2,t2]]}`. The digraph has distinct
arcs, and the four terminal vertices are distinct. Source loops are harmless
and allowed. A source output is `{"paths": [[s1,...,t1], [s2,...,t2]]}`:
two simple directed paths with no shared vertex. The alternative
`{"status": "NO-SOLUTION"}` is valid exactly when no such pair exists.

The target input is `{"vertices": n, "arcs": [[u,v], ...]}` with distinct
arcs and no loops. A target output is `{"successor": [vertex, ...]}`,
one arc head per tail vertex, forming a permutation of all vertices. Its
cycles are a spanning directed cycle factor. At least one cycle must have
even length; a directed two-cycle qualifies. `{"status": "NO-SOLUTION"}`
is valid only when no such factor exists. The empty digraph has no even
cycle and therefore has no valid positive output.

A candidate `algorithm.py` reads source JSON from stdin and writes legal
target JSON to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes a valid source
output. The commands share no memory, exit nonzero on errors and send
diagnostics to stderr. They must be deterministic and polynomial time;
recovery must work for every valid cycle factor or negative target answer.

`check.py --candidate PATH` independently solves each constructed target on
the fixed source corpus and directly validates recovered source paths.

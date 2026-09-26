"""Fix seeded directed two-linkage instances before construction."""

import json
import random
from pathlib import Path


def source(n,arcs,pairs=None):
    return {"vertices":n,"arcs":arcs,"pairs":pairs or [[0,1],[2,3]]}


EDGE_CASES = [
    (source(4,[[0,1],[2,3]]),True),
    (source(4,[[0,1]]),False),
    (source(4,[]),False),
    (source(4,[[0,1],[2,3],[1,0]]),True),
    (source(4,[[0,1],[1,2],[2,3],[3,0]],[[0,2],[1,3]]),False),
    (source(5,[[0,4],[4,1],[2,3]]),True),
    (source(5,[[0,4],[4,1],[2,4],[4,3]]),False),
    (source(6,[[0,4],[4,1],[2,5],[5,3]]),True),
    (source(6,[[0,4],[4,1],[2,5]]),False),
    (source(4,[[u,v] for u in range(4) for v in range(4) if u != v]),True),
    (source(5,[[0,1],[2,3]]),True),
    (source(5,[[1,0],[3,2]]),False),
    (source(6,[[0,1],[1,2],[2,3],[3,0]],[[0,1],[2,3]]),True),
]


def random_source(seed):
    rng = random.Random(seed)
    n = rng.randint(4,7)
    arcs = [[u,v] for u in range(n) for v in range(n)
            if u != v and rng.random() < 0.22]
    if seed % 2 == 0:
        arcs = [arc for arc in arcs if arc not in ([0,1],[2,3])]
        arcs += [[0,1],[2,3]]
    arcs.sort()
    return source(n,arcs)


def build_cases():
    from check import solve_source
    cases, seen = [], set()

    def add(value,kind,seed=None,hand_answer=None):
        key = json.dumps(value,sort_keys=True,separators=(",", ":"))
        if key in seen:
            return False
        seen.add(key)
        answer = solve_source(value)
        if hand_answer is not None and ("paths" in answer) != hand_answer:
            raise AssertionError(f"Hand label disagrees with oracle: {value}")
        case = {"source":value,"kind":kind,"expected":answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for value,expected in EDGE_CASES:
        add(value,"edge",hand_answer=expected)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed),"random",seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases,indent=2)+"\n")
    print(f"Wrote {len(cases)} cases to {path}")

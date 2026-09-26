"""Independent directed two-linkage and even-cycle-factor oracles."""

import argparse
import json
import random
import subprocess
import sys
from itertools import permutations
from pathlib import Path

import z3


def legal_arcs(n,arcs,loops):
    if type(n) is not int or n < 0 or not isinstance(arcs,list):
        return False
    seen = set()
    for arc in arcs:
        if (not isinstance(arc,list) or len(arc) != 2
                or any(type(v) is not int or not 0 <= v < n for v in arc)
                or (not loops and arc[0] == arc[1])):
            return False
        key = tuple(arc)
        if key in seen:
            return False
        seen.add(key)
    return True


def legal_source(source):
    if not isinstance(source,dict) or not legal_arcs(source.get("vertices"),source.get("arcs"),True):
        return False
    pairs = source.get("pairs")
    n = source["vertices"]
    return (isinstance(pairs,list) and len(pairs) == 2
            and all(isinstance(pair,list) and len(pair) == 2
                    and all(type(v) is int and 0 <= v < n for v in pair)
                    for pair in pairs)
            and len({v for pair in pairs for v in pair}) == 4)


def legal_target(target):
    return (isinstance(target,dict)
            and legal_arcs(target.get("vertices"),target.get("arcs"),False))


def direct_paths(source,paths):
    if not legal_source(source) or not isinstance(paths,list) or len(paths) != 2:
        return False
    arcs = {tuple(arc) for arc in source["arcs"]}
    if not all(isinstance(path,list) and len(path) >= 2
               and path[0] == source["pairs"][i][0]
               and path[-1] == source["pairs"][i][1]
               and all(type(v) is int and 0 <= v < source["vertices"] for v in path)
               and len(set(path)) == len(path)
               and all((u,v) in arcs for u,v in zip(path,path[1:]))
               for i,path in enumerate(paths)):
        return False
    return not (set(paths[0]) & set(paths[1]))


def paths_between(source,start,end):
    outgoing = [[] for _ in range(source["vertices"])]
    for u,v in source["arcs"]:
        if u != v:
            outgoing[u].append(v)

    def visit(path):
        u = path[-1]
        if u == end:
            yield list(path)
            return
        for v in outgoing[u]:
            if v not in path:
                yield from visit(path+[v])

    yield from visit([start])


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal directed two-linkage instance")
    (s1,t1),(s2,t2) = source["pairs"]
    for first in paths_between(source,s1,t1):
        for second in paths_between(source,s2,t2):
            if not (set(first) & set(second)):
                return {"paths":[first,second]}
    return {"status":"NO-SOLUTION"}


def valid_source(source,output):
    if not legal_source(source) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_source(source) == output
    return set(output) == {"paths"} and direct_paths(source,output["paths"])


def direct_factor(target,successor):
    if not legal_target(target) or not isinstance(successor,list):
        return False
    n = target["vertices"]
    if (len(successor) != n or any(type(v) is not int for v in successor)
            or set(successor) != set(range(n))):
        return False
    arcs = {tuple(arc) for arc in target["arcs"]}
    if any((u,v) not in arcs for u,v in enumerate(successor)):
        return False
    unseen = set(range(n))
    has_even = False
    while unseen:
        start = next(iter(unseen))
        u = start
        length = 0
        while u in unseen:
            unseen.remove(u)
            u = successor[u]
            length += 1
        if u != start:
            return False
        has_even |= length % 2 == 0
    return has_even


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Illegal loopless digraph")
    n = target["vertices"]
    outgoing = [set() for _ in range(n)]
    for u,v in target["arcs"]:
        outgoing[u].add(v)
    successor = [z3.Int(f"next_{u}") for u in range(n)]
    solver = z3.Solver()
    if successor:
        solver.add(z3.Distinct(*successor))
    for u,var in enumerate(successor):
        solver.add(z3.Or(*[var == v for v in outgoing[u]]))
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive cycle-factor solver: {result}")
        model = solver.model()
        answer = [model.eval(var).as_long() for var in successor]
        if direct_factor(target,answer):
            outputs.append({"successor":answer})
        solver.add(z3.Or(*[var != value for var,value in zip(successor,answer)]))
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return set(output) == {"successor"} and direct_factor(target,output["successor"])


def exhaustive_target(target):
    for successor in permutations(range(target["vertices"])):
        if direct_factor(target,list(successor)):
            return {"successor":list(successor)}
    return {"status":"NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for source,expected in EDGE_CASES:
        assert ("paths" in solve_source(source)) == expected
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        assert ("paths" in current) == ("paths" in case["expected"])
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    checked, seen_targets, seed = 0, set(), 0
    while checked < 100:
        rng = random.Random(seed)
        if seed % 2 == 0:
            n = rng.choice((2,4,5,6))
            mandatory = {(u,u+1) for u in range(0,n-1,2)} | {(u+1,u) for u in range(0,n-1,2)}
            if n % 2:
                mandatory.discard((n-3,n-2))
                mandatory.discard((n-2,n-3))
                mandatory |= {(n-3,n-2),(n-2,n-1),(n-1,n-3)}
        else:
            n, mandatory = rng.randrange(6), set()
        arcs = [[u,v] for u in range(n) for v in range(n)
                if u != v and ((u,v) in mandatory or rng.randrange(3) == 0)]
        target = {"vertices":n,"arcs":arcs}
        key = json.dumps(target,sort_keys=True)
        seed += 1
        if key in seen_targets:
            continue
        seen_targets.add(key)
        assert ("successor" in solve_target(target)) == ("successor" in exhaustive_target(target))
        checked += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {checked} exhaustive target digraphs")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal cycle-factor target: {target}")
        for output in target_solutions(target):
            if not valid_target(target,output):
                raise AssertionError(f"Invalid target oracle output: {output}")
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)

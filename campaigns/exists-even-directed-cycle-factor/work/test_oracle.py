from check import legal_source, solve_source, valid_source, legal_target, solve_target, valid_target


def test_hand_cases():
    paths = {"vertices":4,"arcs":[[0,1],[2,3]],"pairs":[[0,1],[2,3]]}
    assert valid_source(paths,{"paths":[[0,1],[2,3]]})
    assert not valid_source(paths,{"paths":[[0,1],[0,3]]})
    assert solve_source({**paths,"arcs":[[0,1]]}) == {"status":"NO-SOLUTION"}
    two_cycle = {"vertices":2,"arcs":[[0,1],[1,0]]}
    assert valid_target(two_cycle,{"successor":[1,0]})
    assert "successor" in solve_target(two_cycle)
    three_cycle = {"vertices":3,"arcs":[[0,1],[1,2],[2,0]]}
    assert solve_target(three_cycle) == {"status":"NO-SOLUTION"}
    assert not valid_target(three_cycle,{"successor":[1,2,0]})
    assert not legal_target({"vertices":1,"arcs":[[0,0]]})


if __name__ == "__main__":
    test_hand_cases()

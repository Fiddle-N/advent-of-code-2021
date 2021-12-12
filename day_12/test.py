from day_12 import process


def test_passage_pathing_small_example_all_paths():
    cave_map = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    passage_pathing = process.PassagePathing(cave_map)

    paths = passage_pathing.all_paths(visit_small_cave_twice=False)
    assert paths == {
        ('start', 'A', 'b', 'A', 'c', 'A', 'end'),
        ('start', 'A', 'b', 'A', 'end'),
        ('start', 'A', 'b', 'end'),
        ('start', 'A', 'c', 'A', 'b', 'A', 'end'),
        ('start', 'A', 'c', 'A', 'b', 'end'),
        ('start', 'A', 'c', 'A', 'end'),
        ('start', 'A', 'end'),
        ('start', 'b', 'A', 'c', 'A', 'end'),
        ('start', 'b', 'A', 'end'),
        ('start', 'b', 'end'),
    }
    assert len(paths) == 10


def test_passage_pathing_medium_example_all_paths():
    cave_map = """\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
    passage_pathing = process.PassagePathing(cave_map)

    paths = passage_pathing.all_paths(visit_small_cave_twice=False)
    assert paths == {
        ('start', 'HN', 'dc', 'HN', 'end'),
        ('start', 'HN', 'dc', 'HN', 'kj', 'HN', 'end'),
        ('start', 'HN', 'dc', 'end'),
        ('start', 'HN', 'dc', 'kj', 'HN', 'end'),
        ('start', 'HN', 'end'),
        ('start', 'HN', 'kj', 'HN', 'dc', 'HN', 'end'),
        ('start', 'HN', 'kj', 'HN', 'dc', 'end'),
        ('start', 'HN', 'kj', 'HN', 'end'),
        ('start', 'HN', 'kj', 'dc', 'HN', 'end'),
        ('start', 'HN', 'kj', 'dc', 'end'),
        ('start', 'dc', 'HN', 'end'),
        ('start', 'dc', 'HN', 'kj', 'HN', 'end'),
        ('start', 'dc', 'end'),
        ('start', 'dc', 'kj', 'HN', 'end'),
        ('start', 'kj', 'HN', 'dc', 'HN', 'end'),
        ('start', 'kj', 'HN', 'dc', 'end'),
        ('start', 'kj', 'HN', 'end'),
        ('start', 'kj', 'dc', 'HN', 'end'),
        ('start', 'kj', 'dc', 'end'),
    }
    assert len(paths) == 19


def test_passage_pathing_large_example_all_paths():
    cave_map = """\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""
    passage_pathing = process.PassagePathing(cave_map)

    paths = passage_pathing.all_paths(visit_small_cave_twice=False)
    assert len(paths) == 226


def test_passage_pathing_small_example_all_paths_with_extra_small_cave_visit():
    cave_map = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    passage_pathing = process.PassagePathing(cave_map)

    paths = passage_pathing.all_paths(visit_small_cave_twice=True)
    assert paths == {
        ('start', 'A', 'b', 'A', 'b', 'A', 'c', 'A', 'end'),
        ('start', 'A', 'b', 'A', 'b', 'A', 'end'),
        ('start', 'A', 'b', 'A', 'b', 'end'),
        ('start', 'A', 'b', 'A', 'c', 'A', 'b', 'A', 'end'),
        ('start', 'A', 'b', 'A', 'c', 'A', 'b', 'end'),
        ('start', 'A', 'b', 'A', 'c', 'A', 'c', 'A', 'end'),
        ('start', 'A', 'b', 'A', 'c', 'A', 'end'),
        ('start', 'A', 'b', 'A', 'end'),
        ('start', 'A', 'b', 'd', 'b', 'A', 'c', 'A', 'end'),
        ('start', 'A', 'b', 'd', 'b', 'A', 'end'),
        ('start', 'A', 'b', 'd', 'b', 'end'),
        ('start', 'A', 'b', 'end'),
        ('start', 'A', 'c', 'A', 'b', 'A', 'b', 'A', 'end'),
        ('start', 'A', 'c', 'A', 'b', 'A', 'b', 'end'),
        ('start', 'A', 'c', 'A', 'b', 'A', 'c', 'A', 'end'),
        ('start', 'A', 'c', 'A', 'b', 'A', 'end'),
        ('start', 'A', 'c', 'A', 'b', 'd', 'b', 'A', 'end'),
        ('start', 'A', 'c', 'A', 'b', 'd', 'b', 'end'),
        ('start', 'A', 'c', 'A', 'b', 'end'),
        ('start', 'A', 'c', 'A', 'c', 'A', 'b', 'A', 'end'),
        ('start', 'A', 'c', 'A', 'c', 'A', 'b', 'end'),
        ('start', 'A', 'c', 'A', 'c', 'A', 'end'),
        ('start', 'A', 'c', 'A', 'end'),
        ('start', 'A', 'end'),
        ('start', 'b', 'A', 'b', 'A', 'c', 'A', 'end'),
        ('start', 'b', 'A', 'b', 'A', 'end'),
        ('start', 'b', 'A', 'b', 'end'),
        ('start', 'b', 'A', 'c', 'A', 'b', 'A', 'end'),
        ('start', 'b', 'A', 'c', 'A', 'b', 'end'),
        ('start', 'b', 'A', 'c', 'A', 'c', 'A', 'end'),
        ('start', 'b', 'A', 'c', 'A', 'end'),
        ('start', 'b', 'A', 'end'),
        ('start', 'b', 'd', 'b', 'A', 'c', 'A', 'end'),
        ('start', 'b', 'd', 'b', 'A', 'end'),
        ('start', 'b', 'd', 'b', 'end'),
        ('start', 'b', 'end'),
    }
    assert len(paths) == 36


def test_passage_pathing_medium_example_all_paths_with_extra_small_cave_visit():
    cave_map = """\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
    passage_pathing = process.PassagePathing(cave_map)


    paths = passage_pathing.all_paths(visit_small_cave_twice=True)
    assert len(paths) == 103


def test_passage_pathing_large_example_all_paths_with_extra_small_cave_visit():
    cave_map = """\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""
    passage_pathing = process.PassagePathing(cave_map)

    paths = passage_pathing.all_paths(visit_small_cave_twice=True)
    assert len(paths) == 3509

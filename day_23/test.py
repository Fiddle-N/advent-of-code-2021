from day_23 import process



def test():
    ao = process.AmphipodOrganiser("""\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#  
  #########  """)
    total_energy = ao.organise()
    assert total_energy == 12_521


def test_unfolded():
    ao = process.AmphipodOrganiser("""\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########  """, unfolded=True)
    total_energy = ao.organise()
    assert total_energy == 44169


def test_small():
    ao = process.AmphipodOrganiser("""\
#############
#...........#
###B#A#C#D###
  #A#B#C#D#  
  #########  """)
    total_energy = ao.organise()
    assert total_energy == 46


def test_amphipod_settled_state():
    ao = process.AmphipodOrganiser("""\
#############
#...........#
###A#C#B#B###
  #A#C#D#D#  
  #########  """)
    amphipods = ao.start_state.amphipods
    amphipods_state = ao.start_state.amphipods_state

    # Both Amber amphipods in correct column - settled
    assert amphipods_state[amphipods[process.Coords(3, 2)]] == process.BurrowAmphipodState.SETTLED
    assert amphipods_state[amphipods[process.Coords(3, 3)]] == process.BurrowAmphipodState.SETTLED

    # Both Copper amphipods in wrong column - original
    assert amphipods_state[amphipods[process.Coords(5, 2)]] == process.BurrowAmphipodState.ORIGINAL
    assert amphipods_state[amphipods[process.Coords(5, 3)]] == process.BurrowAmphipodState.ORIGINAL

    # One Desert amphipod in wrong column - original
    assert amphipods_state[amphipods[process.Coords(7, 3)]] == process.BurrowAmphipodState.ORIGINAL

    # One Desert amphipod in correct column - settled
    assert amphipods_state[amphipods[process.Coords(9, 3)]] == process.BurrowAmphipodState.SETTLED


def test_amphipod_settled_state_more():
    ao = process.AmphipodOrganiser("""\
#############
#...........#
###A#C#B#D###
  #A#C#D#B#  
  #########  """)

    amphipods = ao.start_state.amphipods
    amphipods_state = ao.start_state.amphipods_state

    # One Desert amphipod in correct column but with wrong amphipod underneath - original
    assert amphipods_state[amphipods[process.Coords(9, 3)]] == process.BurrowAmphipodState.ORIGINAL


def test_burrow_map_path_coords():

    map = process.BurrowMapGenerator().create(amphipod_rows=2)
    assert map.path_coords(start=process.Coords(3, 3), end=process.Coords(9, 3)) == [
        process.Coords(3, 3),
        process.Coords(3, 2),
        process.Coords(3, 1),
        process.Coords(4, 1),
        process.Coords(5, 1),
        process.Coords(6, 1),
        process.Coords(7, 1),
        process.Coords(8, 1),
        process.Coords(9, 1),
        process.Coords(9, 2),
        process.Coords(9, 3),
    ]


def test_burrow_map_path_coords_cache():

    map = process.BurrowMapGenerator().create(amphipod_rows=2)
    result_1 = map.path_coords(process.Coords(3, 3), process.Coords(9, 3))
    result_2 = map.path_coords(process.Coords(3, 3), process.Coords(9, 3))

    assert result_1 is result_2


def test_burrow_map_path_coords_exclude_true():

    map = process.BurrowMapGenerator().create(amphipod_rows=2)
    assert map.path_coords(process.Coords(3, 3), process.Coords(9, 3), exclude_start=True) == [
        process.Coords(3, 2),
        process.Coords(3, 1),
        process.Coords(4, 1),
        process.Coords(5, 1),
        process.Coords(6, 1),
        process.Coords(7, 1),
        process.Coords(8, 1),
        process.Coords(9, 1),
        process.Coords(9, 2),
        process.Coords(9, 3),
    ]


def test_burrow_map_intrapath_coords_cache():

    map = process.BurrowMapGenerator().create(amphipod_rows=2)
    result_1 = map.path_coords(process.Coords(3, 3), process.Coords(9, 3), exclude_start=True)
    result_2 = map.path_coords(process.Coords(3, 3), process.Coords(9, 3), exclude_start=True)

    assert result_1 is result_2


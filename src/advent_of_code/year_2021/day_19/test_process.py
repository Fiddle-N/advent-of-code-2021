from src.advent_of_code.year_2021.day_19 import process


def test_example_1():
    scanner_data = """\
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""
    beacon_scanner = process.BeaconScanner(scanner_data)
    beacon_scanner.calibrate_scanners()
    assert (
        beacon_scanner.relative_scanner_data[0].beacons
        & beacon_scanner.relative_scanner_data[1].beacons
    ) == {
        process.Coords3D(-618, -824, -621),
        process.Coords3D(-537, -823, -458),
        process.Coords3D(-447, -329, 318),
        process.Coords3D(404, -588, -901),
        process.Coords3D(544, -627, -890),
        process.Coords3D(528, -643, 409),
        process.Coords3D(-661, -816, -575),
        process.Coords3D(390, -675, -793),
        process.Coords3D(423, -701, 434),
        process.Coords3D(-345, -311, 381),
        process.Coords3D(459, -707, 401),
        process.Coords3D(-485, -357, 347),
    }

    assert (
        beacon_scanner.relative_scanner_data[1].beacons
        & beacon_scanner.relative_scanner_data[4].beacons
    ) == {
        process.Coords3D(459, -707, 401),
        process.Coords3D(-739, -1745, 668),
        process.Coords3D(-485, -357, 347),
        process.Coords3D(432, -2009, 850),
        process.Coords3D(528, -643, 409),
        process.Coords3D(423, -701, 434),
        process.Coords3D(-345, -311, 381),
        process.Coords3D(408, -1815, 803),
        process.Coords3D(534, -1912, 768),
        process.Coords3D(-687, -1600, 576),
        process.Coords3D(-447, -329, 318),
        process.Coords3D(-635, -1737, 486),
    }

    relative_beacon_list = beacon_scanner.relative_beacon_list

    assert relative_beacon_list == {
        process.Coords3D(-892, 524, 684),
        process.Coords3D(-876, 649, 763),
        process.Coords3D(-838, 591, 734),
        process.Coords3D(-789, 900, -551),
        process.Coords3D(-739, -1745, 668),
        process.Coords3D(-706, -3180, -659),
        process.Coords3D(-697, -3072, -689),
        process.Coords3D(-689, 845, -530),
        process.Coords3D(-687, -1600, 576),
        process.Coords3D(-661, -816, -575),
        process.Coords3D(-654, -3158, -753),
        process.Coords3D(-635, -1737, 486),
        process.Coords3D(-631, -672, 1502),
        process.Coords3D(-624, -1620, 1868),
        process.Coords3D(-620, -3212, 371),
        process.Coords3D(-618, -824, -621),
        process.Coords3D(-612, -1695, 1788),
        process.Coords3D(-601, -1648, -643),
        process.Coords3D(-584, 868, -557),
        process.Coords3D(-537, -823, -458),
        process.Coords3D(-532, -1715, 1894),
        process.Coords3D(-518, -1681, -600),
        process.Coords3D(-499, -1607, -770),
        process.Coords3D(-485, -357, 347),
        process.Coords3D(-470, -3283, 303),
        process.Coords3D(-456, -621, 1527),
        process.Coords3D(-447, -329, 318),
        process.Coords3D(-430, -3130, 366),
        process.Coords3D(-413, -627, 1469),
        process.Coords3D(-345, -311, 381),
        process.Coords3D(-36, -1284, 1171),
        process.Coords3D(-27, -1108, -65),
        process.Coords3D(7, -33, -71),
        process.Coords3D(12, -2351, -103),
        process.Coords3D(26, -1119, 1091),
        process.Coords3D(346, -2985, 342),
        process.Coords3D(366, -3059, 397),
        process.Coords3D(377, -2827, 367),
        process.Coords3D(390, -675, -793),
        process.Coords3D(396, -1931, -563),
        process.Coords3D(404, -588, -901),
        process.Coords3D(408, -1815, 803),
        process.Coords3D(423, -701, 434),
        process.Coords3D(432, -2009, 850),
        process.Coords3D(443, 580, 662),
        process.Coords3D(455, 729, 728),
        process.Coords3D(456, -540, 1869),
        process.Coords3D(459, -707, 401),
        process.Coords3D(465, -695, 1988),
        process.Coords3D(474, 580, 667),
        process.Coords3D(496, -1584, 1900),
        process.Coords3D(497, -1838, -617),
        process.Coords3D(527, -524, 1933),
        process.Coords3D(528, -643, 409),
        process.Coords3D(534, -1912, 768),
        process.Coords3D(544, -627, -890),
        process.Coords3D(553, 345, -567),
        process.Coords3D(564, 392, -477),
        process.Coords3D(568, -2007, -577),
        process.Coords3D(605, -1665, 1952),
        process.Coords3D(612, -1593, 1893),
        process.Coords3D(630, 319, -379),
        process.Coords3D(686, -3108, -505),
        process.Coords3D(776, -3184, -501),
        process.Coords3D(846, -3110, -434),
        process.Coords3D(1135, -1161, 1235),
        process.Coords3D(1243, -1093, 1063),
        process.Coords3D(1660, -552, 429),
        process.Coords3D(1693, -557, 386),
        process.Coords3D(1735, -437, 1738),
        process.Coords3D(1749, -1800, 1813),
        process.Coords3D(1772, -405, 1572),
        process.Coords3D(1776, -675, 371),
        process.Coords3D(1779, -442, 1789),
        process.Coords3D(1780, -1548, 337),
        process.Coords3D(1786, -1538, 337),
        process.Coords3D(1847, -1591, 415),
        process.Coords3D(1889, -1729, 1762),
        process.Coords3D(1994, -1805, 1792),
    }

    assert len(relative_beacon_list) == 79

    assert beacon_scanner.largest_manhattan_distance == 3621

from day_18 import process


def test_explode_example_1():
    sf1 = process.SnailfishNumber.from_list([[[[[9, 8], 1], 2], 3], 4])
    assert sf1 == process.SnailfishNumber.from_list([[[[0, 9], 2], 3], 4])


def test_explode_example_2():
    sf1 = process.SnailfishNumber.from_list([7, [6, [5, [4, [3, 2]]]]])
    assert sf1 == process.SnailfishNumber.from_list([7, [6, [5, [7, 0]]]])


def test_explode_example_3():
    sf1 = process.SnailfishNumber.from_list([[6, [5, [4, [3, 2]]]], 1])
    assert sf1 == process.SnailfishNumber.from_list([[6, [5, [7, 0]]], 3])


def test_explode_example_4():
    sf1 = process.SnailfishNumber.from_list([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])
    assert sf1 == process.SnailfishNumber.from_list(
        [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
    )


def test_add_simple_example():
    left = process.SnailfishNumber.from_list([[[[4, 3], 4], 4], [7, [[8, 4], 9]]])
    right = process.SnailfishNumber.from_list([1, 1])
    exp_result = process.SnailfishNumber.from_list(
        [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    )
    assert left + right == exp_result


def test_homework_example_1():
    homework = """\
[1,1]
[2,2]
[3,3]
[4,4]"""
    sf_homework = process.sf_homework_part_1(homework)
    while True:
        try:
            next(sf_homework)
        except StopIteration as e:
            result = e.value
            break

    assert result == process.SnailfishNumber.from_list(
        [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]
    )


def test_homework_example_2():
    homework = """\
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]"""
    sf_homework = process.sf_homework_part_1(homework)
    while True:
        try:
            next(sf_homework)
        except StopIteration as e:
            result = e.value
            break

    assert result == process.SnailfishNumber.from_list(
        [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]
    )


def test_homework_example_3():
    homework = """\
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]"""
    sf_homework = process.sf_homework_part_1(homework)
    while True:
        try:
            next(sf_homework)
        except StopIteration as e:
            result = e.value
            break

    assert result == process.SnailfishNumber.from_list(
        [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]
    )


def test_homework_large_example():
    homework = """\
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""

    actual = process.sf_homework_part_1(homework)

    result_1 = next(actual)
    exp_1 = process.SnailfishNumber.from_list(
        [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]]
    )
    assert result_1 == exp_1

    result_2 = next(actual)
    exp_2 = process.SnailfishNumber.from_list(
        [[[[6, 7], [6, 7]], [[7, 7], [0, 7]]], [[[8, 7], [7, 7]], [[8, 8], [8, 0]]]]
    )
    assert result_2 == exp_2

    result_3 = next(actual)
    exp_3 = process.SnailfishNumber.from_list(
        [[[[7, 0], [7, 7]], [[7, 7], [7, 8]]], [[[7, 7], [8, 8]], [[7, 7], [8, 7]]]]
    )
    assert result_3 == exp_3

    result_4 = next(actual)
    exp_4 = process.SnailfishNumber.from_list(
        [[[[7, 7], [7, 8]], [[9, 5], [8, 7]]], [[[6, 8], [0, 8]], [[9, 9], [9, 0]]]]
    )
    assert result_4 == exp_4

    result_5 = next(actual)
    exp_5 = process.SnailfishNumber.from_list(
        [[[[6, 6], [6, 6]], [[6, 0], [6, 7]]], [[[7, 7], [8, 9]], [8, [8, 1]]]]
    )
    assert result_5 == exp_5

    result_6 = next(actual)
    exp_6 = process.SnailfishNumber.from_list(
        [[[[6, 6], [7, 7]], [[0, 7], [7, 7]]], [[[5, 5], [5, 6]], 9]]
    )
    assert result_6 == exp_6

    result_7 = next(actual)
    exp_7 = process.SnailfishNumber.from_list(
        [[[[7, 8], [6, 7]], [[6, 8], [0, 8]]], [[[7, 7], [5, 0]], [[5, 5], [5, 6]]]]
    )
    assert result_7 == exp_7

    result_8 = next(actual)
    exp_8 = process.SnailfishNumber.from_list(
        [[[[7, 7], [7, 7]], [[8, 7], [8, 7]]], [[[7, 0], [7, 7]], 9]]
    )
    assert result_8 == exp_8

    result_9 = next(actual)
    exp_9 = process.SnailfishNumber.from_list(
        [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
    )
    assert result_9 == exp_9


def test_magnitude_example_1():
    assert process.SnailfishNumber.from_list([[1, 2], [[3, 4], 5]]).magnitude() == 143


def test_magnitude_example_2():
    assert (
        process.SnailfishNumber.from_list(
            [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
        ).magnitude()
        == 1384
    )


def test_magnitude_example_3():
    assert (
        process.SnailfishNumber.from_list(
            [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]
        ).magnitude()
        == 445
    )


def test_magnitude_example_4():
    assert (
        process.SnailfishNumber.from_list(
            [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]
        ).magnitude()
        == 791
    )


def test_magnitude_example_5():
    assert (
        process.SnailfishNumber.from_list(
            [[[[5,0],[7,4]],[5,5]],[6,6]]
        ).magnitude()
        == 1137
    )


def test_magnitude_example_6():
    assert (
        process.SnailfishNumber.from_list(
            [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
        ).magnitude()
        == 3488
    )


def test_homework_final_example():
    homework = """\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
    sf_homework = process.sf_homework_part_1(homework)
    while True:
        try:
            next(sf_homework)
        except StopIteration as e:
            result = e.value
            break

    assert result == process.SnailfishNumber.from_list(
        [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
    )

    assert result.magnitude() == 4140


def test_homework_final_example_largest_magnitude():
    homework = """\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
    assert process.sf_homework_part_2(homework) == 3993
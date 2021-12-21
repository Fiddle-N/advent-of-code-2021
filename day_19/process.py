import ast
import collections
import dataclasses
import itertools


@dataclasses.dataclass(frozen=True)
class Coords3D:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Coords3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Coords3D(self.x - other.x, self.y - other.y, self.z - other.z)


@dataclasses.dataclass(frozen=True)
class ScannerResults:
    scanner: Coords3D
    beacons: set[Coords3D]


COORD_TRANSFORMATIONS = [
    lambda coords: Coords3D(coords.x, coords.y, coords.z),
    lambda coords: Coords3D(-coords.y, coords.x, coords.z),
    lambda coords: Coords3D(-coords.x, -coords.y, coords.z),
    lambda coords: Coords3D(coords.y, -coords.x, coords.z),
    lambda coords: Coords3D(-coords.x, coords.y, -coords.z),
    lambda coords: Coords3D(coords.y, coords.x, -coords.z),
    lambda coords: Coords3D(coords.x, -coords.y, -coords.z),
    lambda coords: Coords3D(-coords.y, -coords.x, -coords.z),
    lambda coords: Coords3D(coords.z, coords.y, -coords.x),
    lambda coords: Coords3D(coords.z, -coords.x, -coords.y),
    lambda coords: Coords3D(coords.z, -coords.y, coords.x),
    lambda coords: Coords3D(coords.z, coords.x, coords.y),
    lambda coords: Coords3D(-coords.z, coords.y, coords.x),
    lambda coords: Coords3D(-coords.z, -coords.x, coords.y),
    lambda coords: Coords3D(-coords.z, -coords.y, -coords.x),
    lambda coords: Coords3D(-coords.z, coords.x, -coords.y),
    lambda coords: Coords3D(coords.x, coords.z, -coords.y),
    lambda coords: Coords3D(-coords.y, coords.z, -coords.x),
    lambda coords: Coords3D(-coords.x, coords.z, coords.y),
    lambda coords: Coords3D(coords.y, coords.z, coords.x),
    lambda coords: Coords3D(coords.x, -coords.z, coords.y),
    lambda coords: Coords3D(coords.y, -coords.z, -coords.x),
    lambda coords: Coords3D(-coords.x, -coords.z, -coords.y),
    lambda coords: Coords3D(-coords.y, -coords.z, coords.x),
]


class BeaconScanner:
    def __init__(self, scanner_data):
        self.absolute_scanner_data = []
        for scanner in scanner_data.split("\n\n"):
            scanner_points = set()
            for line in scanner.splitlines():
                if line.startswith("---"):
                    continue
                scanner_points.add(Coords3D(*ast.literal_eval(line)))
            self.absolute_scanner_data.append(scanner_points)

        self.relative_scanner_data = {}

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read().strip())

    def _calculate_beacon_pairs(self, scanner_no, datatype="absolute"):
        if datatype == "absolute":
            data = self.absolute_scanner_data[scanner_no]
        elif datatype == "relative":
            data = self.relative_scanner_data[scanner_no].beacons
        else:
            raise Exception
        vectors = {}
        for beacon_pair in itertools.combinations(data, 2):
            vector = beacon_pair[1] - beacon_pair[0]
            vectors[beacon_pair] = frozenset(
                [abs(vector.x), abs(vector.y), abs(vector.z)]
            )
        return vectors

    def _calibrate_scanner_pairs(self, *scanner_nos):
        assert len(scanner_nos) == 2
        assert scanner_nos[0] in self.relative_scanner_data
        beacon_pairs = [
            self._calculate_beacon_pairs(scanner_nos[0], datatype="relative"),
            self._calculate_beacon_pairs(scanner_nos[1], datatype="absolute"),
        ]

        vectors = []
        for no in (0, 1):
            vector_vals = set(beacon_pairs[no].values())
            assert len(vector_vals) == len(beacon_pairs[no])  # if not we're fucked
            vectors.append(vector_vals)

        overlapping_vectors = vectors[0] & vectors[1]

        vectors_for_beacons_pairs = []
        for no in (0, 1):
            vectors_for_beacons_pairs.append(
                {
                    vector: beacon_pair
                    for beacon_pair, vector in beacon_pairs[no].items()
                    if vector in overlapping_vectors
                }
            )

        matched_beacon_pairs = {
            vectors_for_beacons_pairs[0][vector]: vectors_for_beacons_pairs[1][vector]
            for vector in overlapping_vectors
        }

        left_overlapping_beacons = set()
        for beacon_pair in vectors_for_beacons_pairs[0].values():
            left_overlapping_beacons.update(beacon_pair)

        right_overlapping_beacons = set()
        for beacon_pair in vectors_for_beacons_pairs[1].values():
            right_overlapping_beacons.update(beacon_pair)

        assert len(left_overlapping_beacons) == len(right_overlapping_beacons)

        if len(left_overlapping_beacons) < 12:
            return False  # not enough overlaps

        matched_beacons = {}
        for beacon in left_overlapping_beacons:
            matching_beacon_pairs = [
                beacon_pair_1
                for beacon_pair_0, beacon_pair_1 in matched_beacon_pairs.items()
                if beacon in beacon_pair_0
            ]
            common_beacons = set.intersection(
                *[set(beacon_pair) for beacon_pair in matching_beacon_pairs]
            )
            assert len(common_beacons) == 1
            (common_beacon,) = common_beacons
            matched_beacons[beacon] = common_beacon

        transformation_offsets = None
        for left_beacon, right_beacon in matched_beacons.items():
            transformed_right_beacons = [
                transformation(right_beacon) for transformation in COORD_TRANSFORMATIONS
            ]
            transformation_offset = {
                (transform_no, left_beacon - transformed_right_beacon)
                for transform_no, transformed_right_beacon in enumerate(
                    transformed_right_beacons
                )
            }
            if transformation_offsets is None:
                transformation_offsets = transformation_offset
            else:
                transformation_offsets &= transformation_offset

        assert len(transformation_offsets) == 1
        (transformation_offset,) = transformation_offsets

        right_beacons_relative_to_0 = {
            COORD_TRANSFORMATIONS[transformation_offset[0]](beacon)
            + transformation_offset[1]
            for beacon in self.absolute_scanner_data[scanner_nos[1]]
        }

        self.relative_scanner_data[scanner_nos[1]] = ScannerResults(
            scanner=transformation_offset[1], beacons=right_beacons_relative_to_0
        )

        return True

    def calibrate_scanners(self):
        scanners_to_be_calibrated = collections.deque(
            scanner_no for scanner_no, _ in enumerate(self.absolute_scanner_data)
        )
        while scanners_to_be_calibrated:
            next_scanner_no = scanners_to_be_calibrated.popleft()
            if next_scanner_no == 0:
                self.relative_scanner_data[next_scanner_no] = ScannerResults(
                    scanner=Coords3D(0, 0, 0),
                    beacons=self.absolute_scanner_data[next_scanner_no],
                )
            else:
                for calibrated_scanner_no in self.relative_scanner_data:
                    result = self._calibrate_scanner_pairs(
                        calibrated_scanner_no, next_scanner_no
                    )
                    if result:
                        break
                else:
                    scanners_to_be_calibrated.append(next_scanner_no)  # check later

    @property
    def relative_beacon_list(self):
        return set.union(
            *[results.beacons for results in self.relative_scanner_data.values()]
        )

    @property
    def largest_manhattan_distance(self):
        scanners = [results.scanner for results in self.relative_scanner_data.values()]
        max_val = 0
        for scanner_1, scanner_2 in itertools.combinations(scanners, 2):
            vector = scanner_1 - scanner_2
            scalar = sum(abs(val) for val in (vector.x, vector.y, vector.z))
            if scalar > max_val:
                max_val = scalar
        return max_val


def main():
    beacon_scanner = BeaconScanner.read_file()
    beacon_scanner.calibrate_scanners()
    print("Number of beacons:", len(beacon_scanner.relative_beacon_list))
    print("Largest Manhattan distance between any two scanners:", beacon_scanner.largest_manhattan_distance)


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))

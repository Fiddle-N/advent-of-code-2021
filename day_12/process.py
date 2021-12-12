import collections


class PassagePathing:

    def __init__(self, cave_map):
        self.cave_graph = collections.defaultdict(list)
        for cave_path in cave_map.split('\n'):
            cave_1, cave_2 = cave_path.split('-')
            self.cave_graph[cave_1].append(cave_2)
            self.cave_graph[cave_2].append(cave_1)

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read().strip())

    def all_paths(self, start='start', end='end', visit_small_cave_twice=False):
        all_paths = set()

        def _all_paths(cave=start, path=None, extra_visit=False):
            if path is None:
                path = []
            path.append(cave)
            if cave == end:
                all_paths.add(tuple(path))
            else:
                for cave in self.cave_graph[cave]:
                    path_copy = path.copy()
                    if cave.isupper() or cave not in path:
                        _all_paths(cave, path=path_copy, extra_visit=extra_visit)
                    elif visit_small_cave_twice and not extra_visit and cave not in (start, end):
                        _all_paths(cave, path=path_copy, extra_visit=True)

        _all_paths()
        return all_paths


def main():
    passage_pathing = PassagePathing.read_file()
    print('All paths:', len(passage_pathing.all_paths(visit_small_cave_twice=False)))
    print('All paths with one small cave visited twice:', len(passage_pathing.all_paths(visit_small_cave_twice=True)))


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))

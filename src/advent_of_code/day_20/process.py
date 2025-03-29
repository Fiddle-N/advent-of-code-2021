import dataclasses
import enum
import itertools

import more_itertools
import numpy as np


class Pixel(enum.Enum):
    DARK = "."
    LIGHT = "#"

    def __str__(self):
        return self.value


PIXEL_BIT = {
    Pixel.DARK: "0",
    Pixel.LIGHT: "1",
}


@dataclasses.dataclass
class Image:
    pixels: np.ndarray

    @classmethod
    def from_list(cls, l):
        return cls(np.array(l))

    @classmethod
    def from_str(cls, s):
        l = [[Pixel(px) for px in row] for row in s.split("\n")]
        return cls.from_list(l)

    def __eq__(self, other):
        return np.equal(self.pixels, other.pixels).all()

    def pixel_count(self, px_type):
        """Assumes padding is dark. If padding is white, calculation will not be correct"""
        return np.count_nonzero(self.pixels == px_type)


class ImageEnhancer:
    def __init__(self, input_data):
        algo, image = input_data.split("\n\n")
        self.algo = [Pixel(px) for px in algo]
        self.image = Image.from_str(image)
        if self.algo[0] == Pixel.DARK:
            # padding will always be dark
            self.pad_chars = itertools.cycle([Pixel.DARK])
        elif self.algo[0] == Pixel.LIGHT:
            # padding will cycle between dark and light
            assert self.algo[-1] == Pixel.DARK
            self.pad_chars = itertools.cycle([Pixel.DARK, Pixel.LIGHT])
        else:
            raise Exception

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read().strip())

    def __iter__(self):
        return self

    def __next__(self):
        padded_image = np.pad(
            self.image.pixels,
            pad_width=((2, 2), (2, 2)),
            mode="constant",
            constant_values=next(self.pad_chars),
        )
        next_image = []
        for rows in more_itertools.windowed(padded_image, 3):
            next_row = []
            squares = [more_itertools.windowed(row, 3) for row in rows]
            for square in zip(*squares):
                pixel_str = itertools.chain.from_iterable(square)
                binary = "".join(PIXEL_BIT[pixel] for pixel in pixel_str)
                algo_no = int(binary, base=2)
                algo_px = self.algo[algo_no]
                next_row.append(algo_px)
            next_image.append(next_row)
        self.image = Image.from_list(next_image)
        return self.image


def main():
    image_enhancer = ImageEnhancer.read_file()
    for _ in range(2):
        result = next(image_enhancer)
    print("Lit pixels after 2 times:", result.pixel_count(Pixel.LIGHT))
    for _ in range(50 - 2):
        result = next(image_enhancer)
    print("Lit pixels after 50 times:", result.pixel_count(Pixel.LIGHT))


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))

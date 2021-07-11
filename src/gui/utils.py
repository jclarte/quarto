from enum import Enum
import pygame
import pathlib
from typing import Union
from pygame.locals import RLEACCEL


class Color(Enum):
    BLACK = pygame.Color((0, 0, 0))
    WHITE = pygame.Color((255, 255, 255))
    RED = pygame.Color((255, 0, 0))
    GREEN = pygame.Color((0, 255, 0))
    BLUE = pygame.Color((50, 150, 250))
    YELLOW = pygame.Color((250, 250, 50))





IMAGE_DIR = pathlib.Path(__file__).parent.joinpath('resources')


class Position:

    @staticmethod
    def _square(p1: 'Position', p2: 'Position'):
        return ((p1.x-p2.x)**2 + (p1.y-p2.y)**2)**.5

    @staticmethod
    def _manhattan(p1: 'Position', p2: 'Position'):
        return abs(p1.x-p2.x) + abs(p1.y-p2.y)

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def tuple(self):
        return (self.x, self.y)

    def __getitem__(self, n: int):
        return [self.x, self.y][n]

    def __str__(self):
        return f"Position(x={self.x}, y={self.y})"

    def distance(self, pos: 'Position', norm: str = "square"):
        return {
            "square": self._square,
            "euler": self._square,
            2: self._square,
            "manhattan": self._manhattan,
            1: self._manhattan,
        }[norm](self, pos)

    def __add__(self, vector: 'Position') -> 'Position':
        return Position(self.x + vector.x, self.y + vector.y)

    def __sub__(self, vector: 'Position') -> 'Position':
        return Position(self.x - vector.x, self.y - vector.y)

    def __eq__(self, other: 'Position') -> bool:
        return self.x == other.x and self.y == other.y

    def next_to(self, position: 'Position'):
        if (abs(self.x - position.x) == 1 or abs(self.y - position.y) == 1)\
                and (self.x == position.x or self.y == position.y):
            return True
        return False


class Vector(Position):
    def __init__(self, p1: Union[Position, int], p2: Union[Position, int]):
        if isinstance(p1, Position) and isinstance(p2, Position):
            self.x = p2.x - p1.x
            self.y = p2.y - p1.y
        elif isinstance(p1, int) and isinstance(p2, int):
            self.x = p1
            self.y = p2
        else:
            raise TypeError("expected 2 Positions or 2 int as arguments")

    def norm(self, norm: str = "square"):
        return self.distance(Position(0, 0), norm)


def load_image(name, colorkey=None, scale_to=None):
    fullname = IMAGE_DIR.joinpath(name)
    assert fullname.exists(), f"file {fullname} not found"
    try:
        with fullname.open() as f:
            image = pygame.image.load(f)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    # image = image.convert()
    image = image.convert_alpha()
    if scale_to:
        image = pygame.transform.scale(image, scale_to)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


def load_sound(filename):
    pass

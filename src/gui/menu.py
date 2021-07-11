from typing import Tuple

from .component import Component
from .utils import Position

class Menu(Component):

    def __init__(self, position: Position, size: Tuple[int, int]) -> None:
        super().__init__(position, size)
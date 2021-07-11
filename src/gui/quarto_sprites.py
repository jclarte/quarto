
import logging
import pygame

from .utils import Color, Position, Vector

LOG = logging.getLogger(__file__)

REDUCE = .8

class QuartoPiece(pygame.sprite.DirtySprite):
    def __init__(self, piece_number: int, width: int = 100) -> None:
        """
        instanciate the sprite of a given quarto piece
        :params:
        :piece_number: number from 0 to 15
        :width: width of the squared cell of the sprite
        """

        assert 0 <= piece_number < 16
        super().__init__()
        self.number = piece_number
        self.width = width
        self.image = self._build_image(piece_number, width)
        self.rect = self.image.get_rect()
        self.visible = 0

    @staticmethod
    def _build_image(piece_number, width):
        shape, color, empty, size = map(int, bin(piece_number)[2:].rjust(4, '0'))

        surface = pygame.Surface((width, width))
        surface.fill(Color.WHITE.value)
        surface.set_colorkey(Color.WHITE.value)
        color = Color.BLACK if color else Color.YELLOW
        scale = .75 if size else 1
        radius = width * scale * REDUCE
        offset = int(width*(1 - REDUCE)/2 + .05)

        if shape:
            topleft = (offset, offset) if not size else ((width - radius)/2, (width - radius)/2)
            topleft = tuple(map(int, topleft))
            pygame.draw.rect(surface, color.value, pygame.rect.Rect(topleft, (radius, radius)))
        else:
            center = (width/2, width/2)
            center = tuple(map(int, center))
            pygame.draw.circle(surface, color.value, center, radius/2)

        if empty:
            center = (width/2, width/2)
            center = tuple(map(int, center))
            pygame.draw.circle(surface, Color.WHITE.value, center, radius/5)

        return surface

    def resize(self, new_size: int):
        self.__init__(self.number, new_size)

    def place(self, position: Position) -> None:
        """place the piece at the given position"""
        vector = Vector(Position(*self.rect.topleft), position)
        self.rect.move_ip(vector.tuple)

PIECES = [QuartoPiece(n) for n in range(16)]
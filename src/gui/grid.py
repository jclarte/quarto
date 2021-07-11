import logging
from typing import Tuple

import pygame

from .component import Component
from .utils import Color, Position

LOG = logging.getLogger(__name__)

class Grid(Component):


    def __init__(self, grid_size: Tuple[int, int], cell_size: Tuple[int, int], position: Position):

        self.grid_size = grid_size
        self.cell_size = cell_size

        super().__init__(position, self.rect_size)
        self._draw_init()

    @property
    def n_cells(self):
        x, y = self.grid_size
        return x*y

    @property
    def rect_size(self):
        return (self.cell_size[0] * self.grid_size[0], self.cell_size[1] * self.grid_size[1])

    def _draw_init(self):
        black = Color.BLACK.value
        border = pygame.Rect((0, 0), self.rect_size)
        pygame.draw.rect(self.image, black, border, border_radius=5, width=2)
        for cell_idx in range(1, self.grid_size[0]):
            pygame.draw.line(self.image, black, (cell_idx*self.cell_size[0], 0), (cell_idx*self.cell_size[0], self.rect_size[1]))
        for cell_idx in range(1, self.grid_size[1]):
            pygame.draw.line(self.image, black, (0, cell_idx*self.cell_size[1]), (self.rect_size[0], cell_idx*self.cell_size[1]))

    def draw(self, surface: pygame.Surface) -> None:
        x, y = self.position.tuple
        surface.blit(self.image, (x, y))

    def pos_to_cell(self, pos: Position):

        LOG.debug(f"position: {pos}")
        LOG.debug(f"component position: {self.position}")
        LOG.debug(f"rect position: {self.rect.topleft}")

        return tuple(map(int.__floordiv__, (pos - self.position).tuple, self.cell_size))

    def cell_to_rect(self, cell):
        x, y = self.position.tuple
        return (
            (cell[0]*self.cell_size[0] + x, cell[1]*self.cell_size[1] + y),
            ((cell[0] + 1)*self.cell_size[0] + x, (cell[1] + 1)*self.cell_size[1] + y),
            )

    def reset(self):
        """
        redraw the grid without added stuff
        """
        self.image = pygame.Surface(self.rect_size)
        self.image.fill(self.color)
        self._draw_init()

    def highlight(self, cell: Tuple[int, int]) -> None:
        """hilight cell in red"""
        topleft, _ = self.cell_to_rect(cell)
        border = pygame.Rect((Position(*topleft) - self.position).tuple, self.cell_size)
        pygame.draw.rect(self.image, Color.RED.value, border, border_radius=5, width=3)

    def place_on_cell(self, cell: Tuple[int, int], sprite: pygame.sprite.Sprite) -> None:
        """place a sprite on a given cell"""
        topleft, _ = self.cell_to_rect(cell)
        vector = Position(*topleft) - Position(*sprite.rect.topleft)
        sprite.rect.move_ip(*vector.tuple)


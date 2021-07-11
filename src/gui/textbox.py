import logging

from typing import Tuple

import pygame

from .component import Component
from .utils import Position, Color

LOG = logging.getLogger(__name__)

class TextBox(Component):

    def __init__(self, position: Position, size: Tuple[int, int], color=Color.WHITE.value, border_radius=5, text='text', font_size=12) -> None:
        super().__init__(position, size)
        border = pygame.Rect(0, 0, *size)
        self.rect = pygame.draw.rect(self.image, color, border, border_radius=border_radius)
        self.rect = pygame.draw.rect(self.image, Color.BLACK.value, border, border_radius=border_radius, width=1)
        self.rect.move_ip(*position.tuple)
        self.text = text
        self.font_size = font_size
        self.font_position = (5, 5)

        self.font = pygame.font.SysFont(None, self.font_size)
        img = self.font.render(self.text, True, Color.BLACK.value)
        self.image.blit(img, self.font_position)

    def draw(self, surface):
        self.__init__(self.position, self.size, text=self.text, font_size=self.font_size)
        super().draw(surface)
        
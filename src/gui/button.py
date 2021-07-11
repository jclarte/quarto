from typing import Tuple

import pygame

from .component import Component
from .utils import Position, Color

SCALE = .8

class Button(Component):

    def __init__(self, position: Position, size: Tuple[int, int], color=Color.BLUE.value, border_radius=5, text='Button') -> None:
        super().__init__(position, size)
        border = pygame.Rect(0, 0, *size)
        self.rect = pygame.draw.rect(self.image, color, border, border_radius=border_radius)
        self.rect = pygame.draw.rect(self.image, Color.BLACK.value, border, border_radius=border_radius, width=1)
        self.rect.move_ip(*position.tuple)
        self.text = text
        self.font_size = int(size[1] * SCALE)
        self.font_position = (5, 5)

        font = pygame.font.SysFont(None, self.font_size)
        img = font.render(self.text, True, Color.BLACK.value)
        self.image.blit(img, self.font_position)

    def animate(self):
        pass

    def clicked(self):
        pass
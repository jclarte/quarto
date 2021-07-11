
import logging
from typing import Tuple

import pygame

from .utils import Position, Color

LOG = logging.getLogger(__name__)

class Component(pygame.sprite.Sprite):

    def __init__(self, position: Position, size: Tuple[int, int], color=Color.WHITE.value) -> None:
        super().__init__()

        self.position = position
        self.size = size
        self.children = list()
        self.parent = None
        self.color = color
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(x=self.position.x, y=self.position.y)


    def append(self, component: 'Component', position: Position) -> None:
        component.attach(self)
        self.children.append({'component': component, 'position': position})

    def update(self) -> None:
        super().update()
        for child in self.children:
            child['component'].update()

    def draw(self, surface: pygame.Surface) -> None:
        x, y = self.position.tuple
        surface.blit(self.image, (x, y))
        for child in self.children:
            child['component'].draw(surface)

    def attach(self, component: 'Component') -> None:
        if self.parent:
            for idx in range(len(self.parent.children)):
                if self.parent.children[idx]['component'] is self:
                    self.parent.children.pop(idx)
                    break

        self.parent = component

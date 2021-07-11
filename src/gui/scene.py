from abc import abstractmethod
from typing import Dict, Any

from .component import Component
from .utils import Position

from pygame import Surface
from pygame.event import Event

class Scene:

    def __init__(self, screen: Surface, settings: Dict[str, Any]) -> None:
        self.screen = screen
        screen_settings = settings.get("screen", {})
        self.width = screen_settings.get("width", 0)
        self.height = screen_settings.get("height", 0)
        self.surface = Surface((self.width, self.height))
        self.components = list()

    @abstractmethod
    def handle_event(self, event: Event) -> None:
        """
        handle event, excpecting an event manager
        """

    @abstractmethod
    def update(self) -> None:
        """
        update all sprites in scene
        """


    def draw(self) -> None:
        """
        draw scene on screen
        """
        

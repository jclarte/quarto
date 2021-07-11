"""
implementation of event manager, a class to dispatch event to belonging components
"""
import logging
from typing import Any, Callable, List, Tuple

from pygame.event import Event
from pygame.locals import MOUSEBUTTONDOWN

from .utils import Position

LOG = logging.getLogger(__name__)


class EventParser:

    def __init__(self, argument_list: List[str]) -> None:
        self._args = argument_list

    def __call__(self, event: Event) -> List[Any]:
        return [getattr(event, arg) for arg in self._args]

    def __repr__(self) -> str:
        return f"EventParser(" + ", ".join(self._args) + ")"

class NullParser(EventParser):
    def __init__(self) -> None:
        pass

    def __call__(self, event) -> List[Any]:
        return []

    def __repr__(self) -> str:
        return "NullParser()"

class MousePositionParser(EventParser):

    def __init__(self) -> None:
        pass

    def __call__(self, event) -> List[Any]:
        return [event.pos]

    def __repr__(self) -> str:
        return "MousePositionParser()"


class EventSelector:

    def __init__(self, selector: Callable) -> None:
        self._selector = selector

    def __call__(self, event: Event) -> bool:
        return self._selector(event)

    def __repr__(self) -> str:
        return f"EventSelector({self._selector})"

class AreaSelector(EventSelector):

    def __init__(self, position: Position, size: Tuple[int, int]) -> None:

        self.size= size
        self.position = position
        def selector(event: Event) -> bool:
            
            if (
                event.type == MOUSEBUTTONDOWN
                and self.position.x <= event.pos[0] < self.position.x + self.size[0]
                and self.position.y <= event.pos[1] < self.position.y + self.size[1]
                ):
                return True
            return False
        super().__init__(selector)

    def __repr__(self) -> str:
        return f"AreaSelector(pos={self.position}, size={self.size})"


class Action:

    def __init__(self, callback: Callable, selector: EventSelector, parser: EventParser) -> None:
        self._callback = callback
        self._selector = selector
        self._arg_parser = parser

    def __repr__(self) -> str:
        return f"Action({self._selector}, {self._arg_parser}, Callback({self._callback}))"

    def __call__(self, event: Event) -> None:
        """handle an event"""
        if self._selector(event):
            args = self._arg_parser(event)
            self._callback(*args)


class EventManager:
    def __init__(self) -> None:
        self._actions = list()

    def add_action(self, callback: Callable, selector: EventSelector, parser: EventParser, **kwargs):
        """
        append an action to event manager
        """
        self._actions.append(Action(callback, selector, parser))

    def __call__(self, event: Event) -> None:
        for action in self._actions:
            action(event)
        

    
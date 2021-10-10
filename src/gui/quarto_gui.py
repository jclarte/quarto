
import logging
from typing import Any, Dict, Tuple

import pygame
from pygame import Surface

from .button import Button
from .event_manager import EventManager, EventSelector, EventParser, AreaSelector, MousePositionParser, NullParser
from .grid import Grid
from .quarto_sprites import PIECES
from .scene import Scene
from .textbox import TextBox
from .utils import Position
from ..logic.quarto_logic import Quarto, State
from ..logic.mcts import MCTS

LOG = logging.getLogger(__name__)

DEFAULT_SCREEN_SIZE = (800, 600)
DEFAULT_BOARD_SIZE = (100, 100)
DEFAULT_BOARD_POS = (150, 100)
DEFAULT_POOL_SIZE = (50, 50)
DEFAULT_POOL_POS = (600, 100)
DEFAULT_SELECT_POS = (50, 50)
DEFAULT_SELECT_SIZE = (50, 50)
DEFAULT_BUTTON_POS = (620, 510)
DEFAULT_BUTTON_SIZE = (80, 20)
DEFAULT_TEXT_SIZE = (400, 80)
DEFAULT_TEXT_POS = (150, 10)
DEFAULT_FONT_SIZE = 24

class GameScene(Scene):
    def __init__(self, screen: Surface, settings: Dict[str, Any]) -> None:

        super().__init__(screen, settings)

        scale_factor = (self.width / DEFAULT_SCREEN_SIZE[0], self.height / DEFAULT_SCREEN_SIZE[1])

        self.pool_cell_size = int(DEFAULT_POOL_SIZE[0]*scale_factor[0]), int(DEFAULT_POOL_SIZE[1]*scale_factor[1])
        self.grid_cell_size = int(DEFAULT_BOARD_SIZE[0]*scale_factor[0]), int(DEFAULT_BOARD_SIZE[1]*scale_factor[1])
        self.selected_size = int(DEFAULT_SELECT_SIZE[0]*scale_factor[0]), int(DEFAULT_SELECT_SIZE[1]*scale_factor[1])
        self.button_size = int(DEFAULT_BUTTON_SIZE[0]*scale_factor[0]), int(DEFAULT_BUTTON_SIZE[1]*scale_factor[1])
        self.text_size = int(DEFAULT_TEXT_SIZE[0]*scale_factor[0]), int(DEFAULT_TEXT_SIZE[1]*scale_factor[1])

        self.selected_position = Position(DEFAULT_SELECT_POS[0], DEFAULT_SELECT_POS[1])
        self.pool_position = Position(DEFAULT_POOL_POS[0], DEFAULT_POOL_POS[1])
        self.grid_position = Position(DEFAULT_BOARD_POS[0], DEFAULT_BOARD_POS[1])
        self.button_position = Position(DEFAULT_BUTTON_POS[0], DEFAULT_BUTTON_POS[1])
        self.text_position = Position(DEFAULT_TEXT_POS[0], DEFAULT_TEXT_POS[1])
        
        self.event_manager = EventManager()
        self.game = Quarto()
        self.tmp_game = self.game.copy()

        # DEV
        def printclick(position) -> None:
            LOG.debug(f"clicked on {position}")

        def selectclick(event) -> bool:
            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                return True
            return False

        self.event_manager.add_action(printclick, EventSelector(selectclick), EventParser(["pos"]))

        bot_settings = settings.get('bot', {})

        self.n_iter = bot_settings.get('n_iter', 1000)
        self.bot = MCTS()
        


    def initialize(self) -> None:
        self.grid = Grid((4, 4), self.grid_cell_size, self.grid_position)
        self.pool = Grid((2, 8), self.pool_cell_size, self.pool_position)
        self.selected = Grid((1, 1), self.selected_size, self.selected_position)
        self.button = Button(self.button_position, self.button_size, text='Play')
        self.text = TextBox(self.text_position, self.text_size, text='Starting new game', font_size=DEFAULT_FONT_SIZE)
        self.all_sprites = pygame.sprite.RenderPlain([self.grid, self.pool, self.selected, self.button, self.text])
        self.piece_sprites = pygame.sprite.RenderPlain(PIECES)

        self.update_pieces_position()

        self.event_manager.add_action(
            self.grid_click,
            AreaSelector(self.grid.position, self.grid.rect_size),
            MousePositionParser()
            )

        self.event_manager.add_action(
            self.pool_click,
            AreaSelector(self.pool.position, self.pool.rect_size),
            MousePositionParser()
            )

        self.event_manager.add_action(
            self.button_click,
            AreaSelector(self.button.position, self.button.size),
            NullParser()
            )

    @property
    def handle_event(self):
        return self.event_manager

    def update_pieces_position(self) -> None:
        if self.tmp_game.selected is not None:
            piece = PIECES[self.tmp_game.selected]
            piece.resize(int(self.selected_size[0]))
            self.selected.place_on_cell((0, 0), piece)

        for idx in range(16):
            if self.tmp_game.available[idx]:
                piece = PIECES[idx]
                piece.resize(int(self.pool_cell_size[0]))
                self.pool.place_on_cell((idx % 2, idx // 2), piece)
            
        for cell_idx in range(16):
            piece_idx = self.tmp_game.board_number[cell_idx]

            if piece_idx is not None:
                piece = PIECES[piece_idx]
                piece.resize(int(self.grid_cell_size[0]))
                self.grid.place_on_cell((cell_idx % 4, cell_idx // 4), piece)



    def update(self) -> None:

        # update position of every piece of the game
        self.all_sprites.update()
        self.piece_sprites.update()

        if self.game.player == 1 and self.game.state != State.END:
            for _ in range(self.n_iter):
                self.bot.iterate(self.game)

            action = self.bot.decide(self.game)
            self.game.transition(action)

            self.tmp_game = self.game.copy()
            self.update_pieces_position()
            
        self.draw()

    def draw(self) -> None:
        self.text.text = f"Player {self.tmp_game.player} turn on state {self.tmp_game.state.value}"
        end = self.game.end()
        if end != -1:
            self.text.text = f"Player {end} wins !"
        self.text.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.piece_sprites.draw(self.screen)

    def pool_click(self, position: Tuple[int, int]) -> None:

        if self.game.state == State.PLACE:
            return
        self.tmp_game = self.game.copy()
        cell = self.pool.pos_to_cell(Position(*position))

        LOG.debug(f"Clicked on cell {cell} from position {position}")

        self.action = cell[0] + 2*cell[1]
        if self.game.player == 0 and self.action in self.game.options():
            LOG.debug(f"SELECT action {self.action}")
            self.tmp_game.transition(self.action)
        self.update_pieces_position()

    def grid_click(self, position: Tuple[int, int]) -> None:
        self.grid.reset()
        cell = self.grid.pos_to_cell(Position(*position))
        cell = cell[0], cell[1]
        self.grid.highlight(cell)
        LOG.debug(f"Clicked on cell {cell} from position {position}")
        if self.game.player == 0 and self.tmp_game.state == State.PLACE:
            LOG.debug(f"PLACE action {self.action}")
            self.action = cell[0] + 4*cell[1]

    def button_click(self) -> None:
        if self.game.player == 0 and self.action in self.game.options():
            self.game.transition(self.action)
            self.tmp_game = self.game.copy()
            LOG.debug(f"Playing action {self.action}")
            self.action = None
            self.update_pieces_position()
            





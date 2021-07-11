"""
game runner of pygame version
"""
import sys
import logging
import pygame

from .settings import CONFIGURATION
from .gui.quarto_sprites import PIECES
from .gui import GameScene
from .gui.utils import Color

LOG = logging.getLogger(__name__)

class GameRunner:

    def __init__(self) -> None:

        width = CONFIGURATION["screen"]["width"]
        height = CONFIGURATION["screen"]["height"]

        pygame.init()

        
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('PyQuarto')
        pygame.mouse.set_visible(1)

        # create background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(Color.WHITE.value)

        self.clock = pygame.time.Clock()
        self.pieces = PIECES

        self.scene = GameScene(self.screen, CONFIGURATION)
        self.scene.initialize()
            

        print("Game Runner created")

    def run(self) -> None:
        # raise NotImplementedError("WIP")

        while True:

            # print current player and state
            
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    sys.exit(1)
                else:
                    self.scene.handle_event(event)

            self.screen.blit(self.background, (0, 0))
            self.scene.update()  # update all sprites in scene
            pygame.display.flip()
from config import *
from scene import SceneManager
from utils import *

from pathlib import Path

parent = Path(__file__).parent
sys.path.append(parent.absolute().__str__())

pygame.init()


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.manager = SceneManager()
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    sys.exit(0)
            self.manager.update(events)
            self.manager.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    App().run()

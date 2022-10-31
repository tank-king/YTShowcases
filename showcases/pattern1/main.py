# this part needs to be copy-pasted in every mini-game
# -----------------------------------------------------
import random
import sys

from pathlib import Path

import pygame

try:
    from scene import Scene
except ImportError:
    parent = Path(__file__).parent.parent.parent
    if parent.absolute().__str__() not in sys.path:
        sys.path.append(parent.absolute().__str__())

# -----------------------------------------------------


from scene import Scene, SceneManager
from subtitles import SubtitleManager
from config import *
from pygame.color import THECOLORS


class Showcase(Scene):
    def __init__(self, manager, name):
        super().__init__(manager, name)
        self.circles = [
            [
                [random.randint(0, WIDTH), random.randint(0, HEIGHT)],
                random.choice(list(THECOLORS.keys())),
                random.randint(25, 50)
            ]
            for _ in range(25)
        ]
        from subtitles import SubtitleManager
        self.sub = SubtitleManager()

    def update(self, events: list[pygame.event.Event]):
        for i in self.circles:
            i[0][0] += random.uniform(-1, 1)
            i[0][1] += random.uniform(-1, 1)
        self.sub.update()

    def draw(self, surf: pygame.Surface):
        surf.fill(0)
        for i in self.circles:
            pygame.draw.circle(surf, i[1], i[0], i[2])
        self.sub.draw(surf)


if __name__ == '__main__':
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    p = Showcase(None, 'showcase')
    while True:
        p.update(events=pygame.event.get())
        p.draw(screen)
        pygame.display.update()

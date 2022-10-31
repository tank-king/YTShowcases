import sys

import pygame

from utils import *
from config import *
from transition import TransitionManager
from objects import ObjectManager
from subtitles import SubtitleManager
import os

from typing import Optional


class Scene:
    """
    Base signature for all menus
    """

    def __init__(self, manager: Optional['SceneManager'], name='menu'):
        self.manager = manager
        self.name = name

    def reset(self):
        self.__init__(self.manager, self.name)

    def update(self, events: list[pygame.event.Event]):
        pass

    def draw(self, surf: pygame.Surface):
        surf.fill('#111111')
        surf.blit(text(self.name), (50, 50))


class Preview(Scene):
    def __init__(self, menu: Scene, pos):
        super().__init__(menu.manager, menu.name)
        self.surf = pygame.Surface((WIDTH, HEIGHT))
        self.preview_surf = pygame.Surface((round(WIDTH * PREVIEW_SCALE), round(HEIGHT * PREVIEW_SCALE)))
        self.menu = menu
        self.pos = pos
        self.cached_preview: Optional[pygame.Surface] = None
        self.active = False

    @property
    def rect(self):
        return self.preview_surf.get_rect().move(*self.pos)

    def update(self, events: list[pygame.event.Event]):
        self.active = False
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint(mx, my):
            self.active = True
            self.menu.update(events)
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        self.manager.switch_mode(self.name, reset=True)

    def draw(self, surf: pygame.Surface):
        if self.active:
            self.menu.draw(self.surf)
            self.cached_preview = pygame.transform.smoothscale(self.surf, self.preview_surf.get_size(), self.preview_surf)
            surf.blit(self.cached_preview, self.pos)
        else:
            if self.cached_preview:
                surf.blit(self.cached_preview, self.pos)
            else:
                # pass
                self.menu.draw(self.surf)
                self.cached_preview = pygame.transform.smoothscale(self.surf, self.preview_surf.get_size(), self.preview_surf)
                surf.blit(self.cached_preview, self.pos)
        pygame.draw.rect(surf, 'white' if not self.active else 'blue', self.rect, 5)


class Home(Scene):
    def __init__(self, manager, name):
        super().__init__(manager, name)
        self.manager.load_menu('showcases.pattern1.main')
        # self.switch_mode('showcases.pattern1.main')
        self.preview = Preview(self.manager.menus['showcases.pattern1.main'], (150, 250))

    def update(self, events: list[pygame.event.Event]):
        super().update(events)
        self.preview.update(events)

    def draw(self, surf: pygame.Surface):
        super().draw(surf)
        self.preview.draw(surf)


class SceneManager:
    def __init__(self):
        self.to_switch = 'none'  # to-switch transition
        self.to_reset = False
        self.to_save_in_stack = True
        self._transition_manager = TransitionManager()  # overall transition
        self._objects_manager = ObjectManager()  # to be used across all menus
        self._subtitle_manager = SubtitleManager()  # overall subtitles
        # pre-set menus to be loaded initially
        self.menu_references = {
            'home': Home,
        }
        self.menus = {}
        for i, _ in self.menu_references.items():
            self.menus[i] = self.menu_references.get(i)(self, i)
        self.mode = 'home'
        self.menu = self.menus[self.mode]
        self.mode_stack = []  # for stack based scene rendering
        self._default_reset = False
        self._default_transition = False
        # self.load_menu('showcases.pattern1.main')
        # # self.switch_mode('showcases.pattern1.main')
        # self.preview = Preview(self.menus['showcases.pattern1.main'], (150, 250))

    # def get_all_showcases(self):

    @staticmethod
    def get_path_to_menu(*args):
        from pathlib import Path
        path = Path(__file__).parent.absolute()
        for i in args:
            path /= i
            print(path)
        return path.__str__()

    def load_menu(self, menu):
        print(f'attempting to load {menu}')
        # for dynamically loading menus / scenes
        try:
            import importlib
            module = importlib.import_module(menu)
            # module = __import__(menu)
            # print(dir(module))
            for i in dir(module):
                if i == 'Showcase':
                    self.menus[menu] = getattr(module, i)(self, menu)
                    print(f'loaded {menu}')
                    return
        except ImportError as e:
            print(f'import error: {e}')
            pass

    def switch_to_prev_mode(self):
        try:
            self.switch_mode(self.mode_stack.pop(), self._default_reset, self._default_transition, save_in_stack=False)
        except IndexError:
            sys.exit(0)

    def switch_mode(self, mode, reset=False, transition=False, save_in_stack=True):
        if mode in self.menus:
            if transition:
                self.to_switch = mode
                self.to_reset = reset
                self.to_save_in_stack = save_in_stack
                self._transition_manager.close()
            else:
                if save_in_stack:
                    self.mode_stack.append(self.mode)
                self.mode = mode
                self.menu = self.menus[self.mode]
                if reset:
                    self.menu.reset()
                self._subtitle_manager.clear()

    def update(self, events: list[pygame.event.Event]):
        if self.to_switch != 'none':
            if self._transition_manager.transition.status == 'closed':
                self.switch_mode(self.to_switch, self.to_reset, transition=False, save_in_stack=self.to_save_in_stack)
                self.to_switch = 'none'
                self.to_reset = False
                self._transition_manager.open()
        self.menu.update(events)
        self._transition_manager.update(events)
        self._objects_manager.update(events)
        self._subtitle_manager.update()
        for e in events:
            if e.type == pygame.KEYDOWN:
                # self.switch_mode('game' if self.mode == 'home' else 'home', reset=True, transition=True)
                if e.key == pygame.K_r:
                    self.menu.reset()
                if e.key == pygame.K_ESCAPE:
                    self.switch_to_prev_mode()
        # self.preview.update(events)

    def draw(self, surf: pygame.Surface):
        self.menu.draw(surf)
        self._transition_manager.draw(surf)
        self._objects_manager.draw(surf)
        self._subtitle_manager.draw(surf)
        # self.preview.draw(surf)

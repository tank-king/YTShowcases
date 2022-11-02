"""
Project Configuration
The project structure is meant to be organized but simple at the same time
Because there will be a web version porting of the same game simultanously
using p5.js
Hence the structure needs to be javascript[p5.js] compatible
"""

import os
import sys

# constants declaration
import pygame

WIDTH = 1200  # width of the screen
HEIGHT = 1000  # height of the screen
SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)
BG_COlOR = '#111111'
PREVIEW_SCALE = 0.2
VOLUME = 100  # sound volume
FPS = 60
MAX_SCENES = 10  # max number of scenes that can be loaded simultaneously
ASSETS = 'assets'

# for handling global objects
_global_dict = {}


def set_global(key, value):
    _global_dict[key] = value


def get_global(key):
    return _global_dict.get(key)


def pop_global(key):
    try:
        _global_dict.pop(key)
    except KeyError:
        pass


# for closing pyinstaller splash screen if loaded from bundle

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print('running in a PyInstaller bundle')
    ASSETS = os.path.join(sys._MEIPASS, ASSETS)
    try:
        import pyi_splash

        pyi_splash.close()
    except ImportError:
        pass
else:
    print('running in a normal Python process')

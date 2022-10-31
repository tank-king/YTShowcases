from operator import attrgetter
from typing import Union

from utils import *


class BaseObject:
    def __init__(self):
        self.alive = True
        self.z = 0  # for sorting
        self.object_manager: Union[ObjectManager, None] = None

    def update(self, events: list[pygame.event.Event]):
        pass

    def draw(self, surf: pygame.Surface):
        pass


class ObjectManager:
    def __init__(self):
        self.objects: list[BaseObject] = []
        self._to_add: list[BaseObject] = []
        self.collision_enabled = True

    def get_object_count(self, instance):
        c = 0
        for i in self.objects:
            if type(i) == instance:
                c += 1
        return c

    def clear(self):
        self._to_add.clear()
        self.objects.clear()

    def add(self, _object: BaseObject):
        _object.object_manager = self
        self._to_add.append(_object)

    def add_multiple(self, _objects: list[BaseObject]):
        for i in _objects:
            self.add(i)

    def update(self, events: list[pygame.event.Event]):
        if self._to_add:
            self.objects.extend(self._to_add)
            self._to_add.clear()
        self.objects = [i for i in self.objects if i.alive]
        self.objects.sort(key=attrgetter('z'))

    def draw(self, surf: pygame.Surface):
        for i in self.objects:
            i.draw(surf)

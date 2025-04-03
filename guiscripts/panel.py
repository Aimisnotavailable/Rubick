import pygame
from abc import abstractmethod

class Panel(object):

    def __init__(self, size : list[int],  pos : list[int], color : list[int],  hoverable : bool=False, clickable : bool=False, parent=None):
        self.size = size
        self.parent : Panel = parent
        self.pos = pos
        self.color = color
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.ishoverable = hoverable
        self.isclicakble = clickable

        self.hovered = False

        self.panel_objects : list[Panel] = []

    def render(self, surf : pygame.Surface, offset : list[int] = [0, 0]):
        surf.blit(self.image, [self.pos[0] - offset[0], self.pos[1] - offset[1]])

    def get_world_pos(self):
        if self.parent:
            return [self.pos[0] + self.parent.get_world_pos()[0], self.pos[1] + self.parent.get_world_pos()[1]]
        else:
            return self.pos
    
    def rect(self):
        return pygame.Rect(*self.get_world_pos(), *self.size)
    
    @abstractmethod
    def hover(self):
        raise NotImplementedError
    
    @abstractmethod
    def onclick(self):
        raise NotImplementedError
    
    @abstractmethod
    def update(self):
        raise NotImplementedError
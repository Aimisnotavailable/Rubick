import pygame
from abc import ABC, abstractmethod

class Engine(ABC):

    def __init__(self, dim : tuple[int], font_size : int):
        self.screen = pygame.display.set_mode(dim)
        self.display = pygame.Surface((dim[0]//2, dim[1]//2), pygame.SRCALPHA)

        self.clock = pygame.time.Clock()
        pygame.init()
        
        self.font = pygame.font.Font(size=font_size)
        pygame.font.init()
        
    @abstractmethod
    def run(self):
        raise NotImplementedError

        

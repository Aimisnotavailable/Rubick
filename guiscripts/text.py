import pygame

class Text(object):

    def __init__(self, text, font : str = None, size : int = 20, pos : list[float] = [0, 0]):
        if font:
            self.font = pygame.font.Font(font, size=size)
        else:
            self.font = pygame.font.Font(size=size)
        self.text = text
        self.pos = pos
        
    def render(self, surf : pygame.Surface, color : list[int] = [255, 255, 255], offset:list[float]=[0,0]):
        surf.blit(self.font.render(self.text, True, color), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
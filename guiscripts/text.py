import pygame

class Text(object):

    def __init__(self, text, font : str = None, size : int = 20, pos : list[float]=[0, 0], color : list[int]=[255, 255, 255], parent=None):
        if font:
            self.font = pygame.font.Font(font, size=size)
        else:
            self.font = pygame.font.Font(size=size)
        self.parent = parent
        self.set_text(text, color=color)

        self.text = text
        self.pos = pos

    def set_text(self, text, color : list[int] = [255, 255, 255]):
        self.text_image = self.font.render(text, True, color)

    def get_world_pos(self):
        if self.parent:
            return [self.pos[0] + self.parent.get_world_pos()[0], self.pos[1] + self.parent.get_world_pos()[1]]
        else:
            return self.pos
        
    def rect(self, centered=False):
        if centered:
            return self.text_image.get_rect(center=(self.get_world_pos()))
        
        return pygame.Rect(*self.get_world_pos(), *self.text_image.get_size())
    
    def render(self, surf : pygame.Surface, offset:list[float]=[0,0]):

        surf.blit(self.text_image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
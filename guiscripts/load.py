import pygame
import math
from guiscripts.panel import Panel

class LoadingIndicatorPanel(Panel):

    def __init__(self, size : list[int],  pos : list[int], color : list[int],  hoverable : bool=False, clickable : bool=False, parent = None):
        super().__init__(size, pos, color)
        self.angle = 0

    def update(self):

        self.image.fill(self.color)
        self.angle += 8
        pygame.draw.circle(self.image, (160, 32, 240, 200), (self.size[0] // 2, self.size[1] // 2), 20, 6, True, False, False, False)
        
    def render(self, surf, offset = [0, 0]):
        self.update()
        image = pygame.transform.rotate(self.image, self.angle)
        image_rect = image.get_rect(center=(self.size[0] // 2 + 0.001 * math.cos(math.radians(self.angle)), self.size[1] // 2 + 0.001 * math.sin(math.radians(self.angle))))

        surf.blit(image, (image_rect[0] - offset[0], image_rect[1] - offset[1]))

class LoadingPanel(Panel):
    
    def __init__(self, size : list[int],  pos : list[int], color : list[int],  hoverable : bool=False, clickable : bool=False, parent = None):    
        super().__init__(size, pos, color)
        self.indicator = LoadingIndicatorPanel((40, 40), (0, 0), (0, 0, 0, 0), 20)

    def update(self):
        self.image.fill(self.color)

    def render(self, surf, offset = [0, 0]):
        self.update()

        self.indicator.render(self.image)

        super().render(surf, offset)

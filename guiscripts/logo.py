import pygame
import os
from guiscripts.projection import Cube
from guiscripts.panel import Panel
from guiscripts.text import Text

class LogoPanel(Panel):

    def __init__(self, size : list[int],  pos : list[int], color : list[int],  hoverable : bool=False, clickable : bool=False, parent = None):
        super().__init__(size, pos, color)

        self.x = 0
        self.y = 0
        self.z = 0

        self.cube = Cube()

        self.text = Text("RUBICK", font=f'{os.getcwd()}/gui_resources/RobotoMono-Medium.ttf', size=12, pos=[9, 46])

    def update(self):

        self.image.fill(self.color)

        self.x += 0.018
        self.y += 0.023
        self.z += 0.027

    def render(self, surf : pygame.Surface, offset : list[int] = [0, 0]):
        self.update()
        
        self.cube.render(self.image, self.x, self.y, self.z, scale=10, offset=(20, 15), fill_color=(0, 100, 0))
        self.cube.render(self.image, self.x, self.y, self.z, scale=10, offset=(35,30), fill_color=(0, 100, 0))
        self.cube.render(self.image, self.x, self.y, self.z, scale=10, offset=(20,30), fill_color=(0, 100, 0))
        self.cube.render(self.image, self.x, self.y, self.z, scale=10, offset=(35,15), fill_color=(0, 100, 0))

        self.text.render(self.image)
        super().render(surf, offset)


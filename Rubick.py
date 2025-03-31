
import pygame
import sys
import math
import random
import os
from abc import ABC, abstractmethod
from guiscripts import engine, projection

class Panel(object):

    def __init__(self, size : list[int], pos : list[int], color : list[int], font_size : int):
        self.size = size
        self.pos = pos
        self.color = color
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)

    def render(self, surf : pygame.Surface, offset : list[int] = [0, 0]):
        surf.blit(self.image, [self.pos[0] - offset[0], self.pos[1] - offset[1]])

    @abstractmethod
    def update(self):
        self.image.fill(self.color)
        raise NotImplementedError

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

class LogoPanel(Panel):

    def __init__(self, size : list[int], pos : list[int], color : list[int], font_size : int):
        super().__init__(size, pos, color, font_size)

        self.x = 0
        self.y = 0
        self.z = 0

        self.cube = projection.Cube()

        self.text = Text("RUBICK", size=20, pos=[5, 46])

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


class LoadingIndicatorPanel(Panel):

    def __init__(self, size : list[int], pos : list[int], color : list[int], font_size : int):
        super().__init__(size, pos, color, font_size)
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
    
    def __init__(self, size : list[int], pos : list[int], color : list[int], font_size : int):
        super().__init__(size, pos, color, font_size)
        self.indicator = LoadingIndicatorPanel((40, 40), (0, 0), (0, 0, 0, 0), 20)

    def update(self):
        self.image.fill(self.color)

    def render(self, surf, offset = [0, 0]):
        self.update()

        self.indicator.render(self.image)

        super().render(surf, offset)

class FileTab(Panel):
    def __init__(self, file_type : str, size : list[int], pos : list[int], color : list[int], font_size : int):
        super().__init__(size, pos, color, font_size)
        self.file_type = file_type
        self.text = Text(self.file_type, size=20)

    def update(self):
        self.image.fill(self.color)

    def render(self, surf, offset = [0, 0]):
        self.update()
        self.text.render(self.image, color=(0, 0, 0))
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, *self.size), 2)
        super().render(surf, offset)

class FileExplorer(Panel):

    def __init__(self, size : list[int], pos : list[int], color : list[int], font_size : int):
        super().__init__(size, pos, color, font_size)
        self.current_dir = os.getcwd()
        self.file_tabs : list[FileTab] = []

        self.load_dir()

    def load_dir(self):
        count = 0
        size = [80, 20]

        for dir in os.listdir(self.current_dir):
            if os.path.isdir(dir):
                self.file_tabs.append(FileTab(dir, size, [0, size[1] * count], (255, 255, 255), 20))
                count += 1

    def update(self):
        self.image.fill(self.color)

    def render(self, surf, offset = [0, 0]):
        self.update()

        for file_tab in self.file_tabs:
            file_tab.render(self.image)

        super().render(surf, offset)

class MainPanel(Panel):

    def __init__(self, size : list[int], pos : list[int], color : list[int], font_size : int):
        super().__init__(size, pos, color, font_size)

        self.load = LoadingPanel((40, 40), [self.size[0] // 2, self.size[1] // 2], (0, 0, 0, 0), 20)

        self.file = FileExplorer(size, (0, 0), color, font_size)
    
    def update(self):
        self.image.fill(self.color)

    def render(self, surf, offset = [0, 0]):
        self.update()

        self.load.render(self.image)

        self.file.render(self.image)
        super().render(surf, offset)

class Window(engine.Engine):
    def __init__(self, dim=..., font_size=20):
        super().__init__(dim, font_size)

        pygame.display.set_caption("Rubick")
        # self.cube = projection.Cube()

        self.logo = LogoPanel([60, 60], (0, 0), (160, 32, 240, 100), 20)

        self.main = MainPanel([440, 350], (60, 0), (0, 155, 0, 180), 20)

        self.clicking = False


    def run(self, debug=False):

        while True:

            self.display.fill((0, 0, 0))

            mpos = [pygame.mouse.get_pos()[0] // 2, pygame.mouse.get_pos()[1] // 2]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_d:
                        debug = not debug
            
            self.logo.render(self.display)
            self.main.render(self.display)

            if debug:
                grid_size = 30

                for x in range(0, self.display.get_width(), grid_size):
                    pygame.draw.line(self.display, (0, 0, 0), (x, 0), (x, self.display.get_height()))
                
                for y in range(0, self.display.get_width(), grid_size):
                    pygame.draw.line(self.display, (0, 0, 0), (0, y), (self.display.get_width(), y))

                self.display.blit(self.font.render(f'MPOS : {mpos}', True, (255, 255, 255)), (self.display.get_width() - 200, 0))

                if self.clicking:
                    
                    pygame.draw.line(self.display, (255, 255, 255), (0, mpos[1]), (self.display.get_width(), mpos[1]))
                    pygame.draw.line(self.display, (255, 255, 255), (mpos[0], 0), (mpos[0], self.display.get_height()))

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

Window((1000, 700)).run(debug=False)

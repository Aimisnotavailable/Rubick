import pygame
import sys
from abc import ABC, abstractmethod
from guiscripts import engine, projection

class Panel(object):

    def __init__(self, size : list[int], pos : list[int], color : list[int], font_size : int):
        self.size = size
        self.pos = pos
        self.color = color
        self.font = pygame.font.Font(size=font_size)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)

    def img(self):
        return self.image
    
    def render(self, surf : pygame.Surface, offset : list[int] = [0, 0]):
        surf.blit(self.img(), [self.pos[0] - offset[0], self.pos[1] - offset[1]])

    @abstractmethod
    def update(self):
        raise NotImplementedError

class LogoPanel(Panel):

    def __init__(self, size : list[int], pos : list[int], color : list[int], font_size : int):
        super().__init__(size, pos, color, font_size)

        self.x = 0
        self.y = 0
        self.z = 0

        self.cube = projection.Cube()

    def update(self):

        self.image.fill(self.color)

        self.x += 0.02
        self.y += 0.03
        self.z += 0.02

    def render(self, surf : pygame.Surface, offset : list[int] = [0, 0]):
        self.update()
        
        self.cube.render(self.img(), self.x, self.y, self.z, scale=10, offset=(20, 15), fill_color=(0, 100, 0))
        self.cube.render(self.img(), self.x, self.y, self.z, scale=10, offset=(35,30), fill_color=(0, 100, 0))
        self.cube.render(self.img(), self.x, self.y, self.z, scale=10, offset=(20,30), fill_color=(0, 100, 0))
        self.cube.render(self.img(), self.x, self.y, self.z, scale=10, offset=(35,15), fill_color=(0, 100, 0))

        self.img().blit(self.font.render(f'RUBICK', True, (255, 255, 255)), (5, 46))        
        super().render(surf, offset)

class Window(engine.Engine):
    def __init__(self, dim=..., font_size=20):
        super().__init__(dim, font_size)

        pygame.display.set_caption("Rubick")
        self.cube = projection.Cube()

        self.logo = LogoPanel([60, 60], (0, 0), (255, 0, 0, 100), 20)

        self.clicking = False

    def run(self, debug=False):

        while True:

            self.display.fill((100, 0, 0))

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
            
            self.logo.render(self.display)
            
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

Window((1000, 700)).run(debug=True)

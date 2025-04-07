import pygame
from guiscripts.panel import Panel
from guiscripts.text import Text
from datascripts.handler import Handler

class Button(Panel):

    def __init__(self, size, pos, color, hoverable = False, clickable = False, parent=None, assets=None):
        super().__init__(size, pos, color, hoverable, clickable, parent, assets)

        self.border_color = (0, 0, 0)
        self.hovered = False

        self.text = Text("Continue", font=f'{self.assets.assets_dir["gui_resources"]}\\RobotoMono-Bold.ttf', size=12, pos=(30, 10), parent=self)

    def hover(self):
        if self.ishoverable:
            self.hovered = True
    
    def onclick(self, handler : Handler):
        if self.isclicakble:
            handler.set_status("waiting")

    def draw_border(self):
        pygame.draw.rect(self.image, self.border_color, (0, 0, *self.size), 1)

    def update(self):
        self.image.fill(self.color)

        if self.hovered:
            self.border_color = (0, 255, 0, 255)
        else:
            self.border_color = (0, 0, 0, 0)
    
    def render(self, surf, offset = [0, 0]):
        self.update()

        self.text.render(self.image, offset=[self.text.get_world_pos()[0] - self.text.rect(True)[0], self.text.get_world_pos()[1] - self.text.rect(True)[1]])
        
        self.draw_border()
        super().render(surf, offset)
                
class Prompt(Panel):

    def __init__(self, size, pos, color, hoverable = False, clickable = False, parent=None, assets=None):
        super().__init__(size, pos, color, hoverable, clickable, parent, assets)

        self.button = Button((60, 20), (170, 160), (160, 32, 240, 255), hoverable=True, clickable=True, parent=self, assets=assets)

        self.panel_objects.append(self.button)

        self.text = Text("", font=f'{self.assets.assets_dir["gui_resources"]}\\RobotoMono-Bold.ttf', size=12, pos=[200, 100], parent=self)
    
    def update(self):
        self.image.fill(self.color)

    def render(self, surf, offset = [0, 0], text=""):
        self.update()

        self.text.render(self.image, offset=[self.text.get_world_pos()[0] - self.text.rect(True)[0], self.text.get_world_pos()[1] - self.text.rect(True)[1]])

        self.button.render(self.image)
        super().render(surf, offset)
    
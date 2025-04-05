import pygame
import os
from guiscripts.panel import Panel
from guiscripts.text import Text

class Header(Panel):

    def __init__(self, size, pos, color, hoverable = False, clickable = False, parent=None):
        super().__init__(size, pos, color, hoverable, clickable, parent)
        self.folder_text = Text("Folders", font=f'{os.getcwd()}/gui_resources/RobotoMono-Medium.ttf', size=12, pos=[105, 15], parent=self)
        self.file_text = Text("Files", font=f'{os.getcwd()}/gui_resources/RobotoMono-Medium.ttf', size=12, pos=[330, 15], parent=self)
    
    def update(self):

        self.image.fill(self.color)

    def render(self, surf, offset = [0, 0]):
        self.update()
        self.file_text.render(self.image, offset=[self.file_text.get_world_pos()[0] - self.file_text.rect(True)[0], self.file_text.get_world_pos()[1] - self.file_text.rect(True)[1]])
        self.folder_text.render(self.image, offset=[self.folder_text.get_world_pos()[0] - self.folder_text.rect(True)[0], self.folder_text.get_world_pos()[1] - self.folder_text.rect(True)[1]])

        super().render(surf, offset=offset)
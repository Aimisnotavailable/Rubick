import pygame
from guiscripts.load import LoadingPanel
from guiscripts.file import FileExplorer
from guiscripts.panel import Panel
from guiscripts.header import Header

class MainPanel(Panel):

    def __init__(self, size : list[int],  pos : list[int], color : list[int],  hoverable : bool=False, clickable : bool=False, parent = None, assets=None):
        super().__init__(size, pos, color, assets=assets)

        # self.load = LoadingPanel((40, 40), [self.size[0] // 2, self.size[1] // 2], (0, 0, 0, 0), 20)

        self.header = Header((self.size[0], 30), (0, 0), (0, 255, 0, 200), parent=self)
        self.folder = FileExplorer((220, size[1]-30), (0, 30), color, parent=self, assets=assets)
        self.file = FileExplorer((220, size[1]-30), (220, 30), color, file_type="exe", parent=self, assets=assets)

        self.panel_objects.append(self.folder)
        self.panel_objects.append(self.file)
        self.panel_objects.append(self.header)
    
    def update(self):
        self.image.fill(self.color)
    
    def render(self, surf, offset = [0, 0]):
        
        self.header.render(self.image)
        self.file.render(self.image)
        # self.load.render(self.image)
        self.folder.render(self.image)
        super().render(surf, offset)

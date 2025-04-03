import pygame
from guiscripts.load import LoadingPanel
from guiscripts.file import FileExplorer
from guiscripts.panel import Panel

class MainPanel(Panel):

    def __init__(self, size : list[int],  pos : list[int], color : list[int],  hoverable : bool=False, clickable : bool=False, parent = None):
        super().__init__(size, pos, color)

        self.load = LoadingPanel((40, 40), [self.size[0] // 2, self.size[1] // 2], (0, 0, 0, 0), 20)

        self.file = FileExplorer(size, (0, 0), color, parent=self)
        self.panel_objects.append(self.file)
    
    def update(self):
        self.image.fill(self.color)

    def render(self, surf, window, offset = [0, 0]):
        self.update()

        self.load.render(self.image)

        self.file.render(self.image, window=window)
        super().render(surf, offset)

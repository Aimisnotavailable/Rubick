import pygame
from guiscripts.load import LoadingPanel
from guiscripts.file import FileExplorer
from guiscripts.prompt import Prompt
from guiscripts.panel import Panel
from guiscripts.header import Header


class MainPanel(Panel):

    def __init__(self, size : list[int],  pos : list[int], color : list[int],  hoverable : bool=False, clickable : bool=False, parent = None, assets=None):
        super().__init__(size, pos, color, assets=assets)

        self.load = LoadingPanel((40, 40), [200,155], (0, 0, 0, 0), 20, parent=self)
        self.header = Header((self.size[0], 30), (0, 0), (0, 255, 0, 200), parent=self)
        self.folder = FileExplorer((220, size[1]-30), (0, 30), color, parent=self, assets=assets)
        self.file = FileExplorer((220, size[1]-30), (220, 30), color, file_type="exe", parent=self, assets=assets)

        self.results = Prompt((400, 200), (20, 75), color, parent=self, assets=assets)
        self.results.add_new_text("score", 12, (200, 80))
        self.results.add_new_text("results", 12, (200, 100))

        self.error = Prompt((400, 200), (20, 75), color, parent=self, assets=assets)
        self.error.add_new_text("error", 12, (200, 100))
        
        self.panel_status : dict[str:list[Panel]] = {"fetching" : [self.load], "waiting" : [self.file, self.folder, self.header], "done" : [self.results], "error" : [self.error]}

        self.panel_objects.append(self.folder)
        self.panel_objects.append(self.file)
        self.panel_objects.append(self.header)
        self.panel_objects.append(self.results)

    def update(self):
        self.image.fill(self.color)

    def render(self, surf, offset = [0, 0], status="waiting"):
        self.update()

        for panel in self.panel_status[status]:
            panel.render(self.image)

        super().render(surf, offset)

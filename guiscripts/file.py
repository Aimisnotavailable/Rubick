import pygame
import os
from guiscripts.text import Text
from guiscripts.panel import Panel

class FileTab(Panel):

    def __init__(self, file_type : str, size : list[int],  pos : list[int], color : list[int],  hoverable : bool=False, clickable : bool=False, parent = None):
        super().__init__(size, pos, color, hoverable=hoverable, clickable=clickable)
        self.file_type = file_type
        self.text = Text(self.file_type, size=20)
        self.screen_pos = [0, 0]
        self.border_color = (0, 0, 0)

    def update(self):
        self.image.fill(self.color)

        if self.hovered:
            self.border_color = (255, 0, 0)
        else:
            self.border_color = (0, 0, 0)

    def draw_border(self, color=(0, 0, 0)):
        pygame.draw.rect(self.image, self.border_color, (0, 0, *self.size), 2)

    def hover(self):
        if self.ishoverable:
            self.hovered = True
    
    def onclick(self):
        if self.isclicakble:
            return self.file_type
    
    def rect(self):
        return pygame.Rect(*self.get_screen_pos(), *self.size)

    def set_screen_pos(self, offset):
        self.screen_pos = [self.get_world_pos()[0] - offset[0], self.get_world_pos()[1] - offset[1]]

    def get_screen_pos(self):
        return self.screen_pos
    
    def render(self, surf, offset = [0, 0]):
        self.update()
        
        self.set_screen_pos(offset)
        self.text.render(self.image, color=(0, 0, 0), offset=(-20, 0))
        self.draw_border()
        super().render(surf, offset)

class FileExplorer(Panel):

    def __init__(self, size : list[int],  pos : list[int], color : list[int],  hoverable : bool=False, clickable : bool=False, parent = None):
        super().__init__(size, pos, color)
        os.chdir("C://")
        self.current_dir = os.getcwd()
        self.file_tabs : list[FileTab] = []
        self.tab_size = [240, 20]
        self.max_scroll = 0
        self.load_dir()

    def load_dir(self):
        count = 1
        
        avoid_files = ['config.msi', '$recycle.bin', '$sysreset', 'documents and settings', 'driver', 'recovery', 'system volume information']
        tab = FileTab('..', self.tab_size, [0, 0], (255, 255, 255), hoverable=True, clickable=True)
        self.add_tab(tab)

        for dir in os.listdir(self.current_dir):
            if os.path.isdir(dir) and self.check_file_read_access(dir) and not dir.lower() in avoid_files:
                tab = FileTab(dir, self.tab_size, [0, self.tab_size[1] * count], (255, 255, 255), hoverable=True, clickable=True)
                self.add_tab(tab=tab)
                count += 1

    def add_tab(self, tab : FileTab):
        tab.set_parent(self)
        self.file_tabs.append(tab)
        self.panel_objects.append(tab)

    def check_file_read_access(self, path):
        return os.access(path, os.R_OK)
    
    def check_file_write_access(self, path):
        return os.access(path, os.W_OK)
    
    def reload(self, new_path):
        if self.check_file_read_access(new_path) and self.check_file_write_access(new_path):
            os.chdir(new_path)
            self.current_dir = new_path
            self.file_tabs.clear()
            self.panel_objects.clear()
            self.load_dir()

    def update(self):
        self.image.fill(self.color)

    def render(self, surf, window, offset = [0, 0]):
        self.update()
    
        self.max_scroll = max(0, self.tab_size[1] * len(self.file_tabs) - (window.display.get_height() // self.tab_size[1]) * self.tab_size[1])
        if self.max_scroll > 0:
            for i in range(max(self.tab_size[1], self.tab_size[1] + window.scroll[1]), self.tab_size[1] * len(self.file_tabs), self.tab_size[1]):
                idx = i//self.tab_size[1]
                self.file_tabs[idx].render(self.image, window.scroll)
        else:
            for i in range(1, len(self.file_tabs)):
                self.file_tabs[i].render(self.image)

        self.file_tabs[0]. render(self.image)

        super().render(surf, offset)

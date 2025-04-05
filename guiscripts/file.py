import pygame
import os
from guiscripts.text import Text
from guiscripts.panel import Panel

class FileTab(Panel):

    def __init__(self, file_name : str, size : list[int],  pos : list[int], color : list[int],  hoverable : bool=False, clickable : bool=False, parent=None, assets=None):
        super().__init__(size, pos, color, hoverable=hoverable, clickable=clickable, parent=parent, assets=assets)
        self.file_name = file_name
        self.text = Text(self.file_name if len(file_name) <= 20 else self.file_name[:20] + '..', font=f'{self.assets.assets_dir["gui_resources"]}\\RobotoMono-Bold.ttf', size=12, color=(0, 0, 0))
        self.screen_pos = [0, 0]
        self.border_color = (0, 0, 0)

    def update(self):
        self.image.fill(self.color)

        if self.hovered:
            self.border_color = (0, 255, 0, 255)
        else:
            self.border_color = (0, 0, 0, 0)

    def draw_border(self, color=(0, 0, 0)):
        pygame.draw.rect(self.image, self.border_color, (0, 0, *self.size), 1)

    def hover(self):
        if self.ishoverable:
            self.hovered = True
    
    def onclick(self):
        if self.isclicakble:
            return self.file_name
    
    def rect(self):
        return pygame.Rect(*self.get_screen_pos(), *self.size)

    def set_screen_pos(self, offset):
        self.screen_pos = [self.get_world_pos()[0] - offset[0], self.get_world_pos()[1] - offset[1]]

    def get_screen_pos(self):
        return self.screen_pos
    
    def render(self, surf, offset = [0, 0]):
        self.update()
        
        self.set_screen_pos(offset)
        self.text.render(self.image, offset=(-20, -5))

        self.draw_border()
        super().render(surf, offset)

class FileExplorer(Panel):

    def __init__(self, size : list[int],  pos : list[int], color : list[int], file_type="dir",  hoverable : bool=False, clickable : bool=False, parent = None, assets=None):
        super().__init__(size, pos, color, parent=parent, assets=assets)
        os.chdir("C://")
        self.current_dir = os.getcwd()
        self.file_tabs : list[FileTab] = []
        self.tab_size = [210, 20]
        self.tab_color = (0, 255, 0, 200)
        self.max_scroll = 0
        self.file_type = file_type
        self.scroll = [0, 0]
        self.load_dir()

    def load_dir(self):
        count = 1
        
        # avoid_files = [] #= ['config.msi', '$recycle.bin', '$sysreset', 'documents and settings', 'driver', 'recovery', 'system volume information']
        if self.file_type=="dir":
            tab = FileTab('..', self.tab_size, [0, 0], self.tab_color, hoverable=True, clickable=True, parent=self, assets=self.assets)
            self.add_tab(tab)

            for dir in os.listdir(self.current_dir):
                if os.path.isdir(dir) and self.check_file_read_access(dir):
                    tab = FileTab(dir, self.tab_size, [0, self.tab_size[1] * count], self.tab_color, hoverable=True, clickable=True, parent=self, assets=self.assets)
                    self.add_tab(tab=tab)
                    count += 1
            if len(self.file_tabs) == 1:
                self.add_tab(FileTab("No Folders Found", self.tab_size, [0, self.tab_size[1] * count], self.tab_color, hoverable=False, clickable=False, parent=self, assets=self.assets))
        else:
            tab = FileTab(f'Filetype : {self.file_type}', self.tab_size, [0, 0], self.tab_color, hoverable=True, clickable=True, parent=self, assets=self.assets)
            self.add_tab(tab)

            for dir in os.listdir(self.current_dir):
                if dir.endswith(self.file_type):
                    tab = FileTab(dir, self.tab_size, [0, self.tab_size[1] * count], self.tab_color, hoverable=True, clickable=True, parent=self, assets=self.assets)
                    self.add_tab(tab=tab)
                    count += 1
            if len(self.file_tabs) == 1:
                self.add_tab(FileTab("No Files Found", self.tab_size, [0, self.tab_size[1] * count], self.tab_color, hoverable=False, clickable=False, parent=self, assets=self.assets))

    def add_tab(self, tab : FileTab):
        self.file_tabs.append(tab)
        self.panel_objects.append(tab)

    def check_file_read_access(self, path):
        return os.access(path, os.R_OK)
    
    def check_file_write_access(self, path):
        return os.access(path, os.W_OK)
    
    def reload_objects(self):
        self.file_tabs.clear()
        self.panel_objects.clear()
        self.load_dir()

    def reload(self, new_path):
        if self.check_file_read_access(new_path) and self.check_file_write_access(new_path):
            old_path : str = self.current_dir
            try:
                os.chdir(new_path)
                self.current_dir = new_path
                self.reload_objects()
            except PermissionError:
                os.chdir(old_path)
                self.current_dir = old_path
                self.reload_objects()
                

    def update(self):
        self.image.fill(self.color)

    def scroll_up(self):
        self.scroll[1] = min(self.max_scroll, self.scroll[1] + self.file_tabs[0].size[1])
    
    def scroll_down(self):
        self.scroll[1] = max(0, self.scroll[1] - self.file_tabs[0].size[1])
    
    def render(self, surf, offset = [0, 0]):
        self.update()

        # Calculate max scroll based on the excess size of the entire file tab image by computing (tab size * no of tabs) - the window height
        # Set 0 as the maximum value for downward scroll and the excess as the upward scroll
        # Scrolls are applied negatively -> to move up and down we have to subtract the scroll from the current position of the tab
        self.max_scroll = max(0, self.tab_size[1] * len(self.file_tabs) - (self.size[1] // self.tab_size[1]) * self.tab_size[1])

        if self.max_scroll > 0:
            for i in range(max(self.tab_size[1], self.tab_size[1] + self.scroll[1]), self.tab_size[1] * len(self.file_tabs), self.tab_size[1]):
                idx = i//self.tab_size[1]
                self.file_tabs[idx].render(self.image, self.scroll)
        else:
            for i in range(1, len(self.file_tabs)):
                self.file_tabs[i].render(self.image)

        self.file_tabs[0]. render(self.image)

        super().render(surf, offset)

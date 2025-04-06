
import pygame
import sys
import math
import random
import os
import threading
from abc import ABC, abstractmethod

from scripts.ember_api import EmberModel
from datascripts.handler import Handler

from guiscripts import engine, projection
from guiscripts.panel import Panel
from guiscripts.file import FileExplorer, FileTab
from guiscripts.load import LoadingPanel
from guiscripts.logo import LogoPanel
from guiscripts.assets import Assets
from guiscripts.mainpanel import MainPanel


class Window(engine.Engine):

    def __init__(self, dim=..., font_size=20):
        super().__init__(dim, font_size)

        pygame.display.set_caption("Rubick")
        # self.cube = projection.Cube()
        self.assets = Assets()

        self.logo = LogoPanel([60, 60], (0, 0), (160, 32, 240, 100), 20)

        self.main = MainPanel([440, 350], (60, 0), (0, 155, 0, 180), 20, assets=self.assets)

        self.clicking = False

        self.click = False

        self.scroll = ""
        
        self.ember = EmberModel(self.assets)
        self.ember_thread : threading.Thread = None

        self.data_handler = Handler()

    def parse(self, panel_objects : list[Panel]) -> list[Panel]:
        panel_objects_list = []

        for panel_object in panel_objects:
            if panel_object.panel_objects:
                panel_objects_list = panel_objects_list + self.parse(panel_object.panel_objects)
            else:
                panel_objects_list.append(panel_object)

        return panel_objects_list
    
    def run(self, debug=False):

        while True:
            self.click = False
            self.display.fill((0, 0, 0))

            mpos = [pygame.mouse.get_pos()[0] // 2, pygame.mouse.get_pos()[1] // 2]
            m_rect = pygame.Rect(*mpos, 1, 1)

            self.scroll = ""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        self.click = True

                    if event.button == 4:
                        self.scroll = "down"
                    if event.button == 5:
                        self.scroll = "up"

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_d:
                        debug = not debug

            if m_rect.colliderect(self.main.rect()):
                panel_objects : list[FileTab] = self.parse(self.main.folder.panel_objects)

                for panel_object in panel_objects:
                    if m_rect.colliderect(panel_object.rect()):
                        panel_object.hover()
                        if self.click:
                            new_path = f'{self.main.folder.current_dir}\\{panel_object.onclick()}'
                            self.main.folder.reload(new_path=new_path)
                            self.main.file.reload(new_path=new_path)
                            self.main.folder.scroll = [0, 0]
                            self.main.file.scroll = [0, 0]
                            break
                    else:
                        panel_object.hovered = False
                panel_objects : list[FileTab] = self.parse(self.main.file.panel_objects)

                for panel_object in panel_objects:
                    if m_rect.colliderect(panel_object.rect()):
                        panel_object.hover()
                        if self.click:
                            if panel_object.isclicakble:
                                if self.ember_thread and self.ember_thread.is_alive():
                                    print("Process is still running")
                                else:
                                    self.ember_thread = threading.Thread(target=self.ember.get_prediction, args=(self.data_handler, f"{self.main.folder.current_dir}\\{panel_object.onclick()}",))
                                    self.ember_thread.start()
                    else:
                        panel_object.hovered = False
                print(self.data_handler.get_result())
                if m_rect.colliderect(self.main.folder.rect()):
                    if self.scroll == "up":
                        self.main.folder.scroll_up()
                    elif self.scroll == "down":
                        self.main.folder.scroll_down()
                
                if m_rect.colliderect(self.main.file.rect()):
                    if self.scroll == "up":
                        self.main.file.scroll_up()
                    elif self.scroll == "down":
                        self.main.file.scroll_down()

            self.logo.render(self.display)
            self.main.render(self.display, load=(self.ember_thread and self.ember_thread.is_alive()))

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



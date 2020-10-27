import pygame
import sys
import os
import pygame_gui
from pygame_gui import UIManager, PackageResource
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UIButton
from pygame_gui.elements import UIHorizontalSlider
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UIDropDownMenu
from pygame_gui.elements import UIScreenSpaceHealthBar
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIImage
from pygame_gui.elements import UIPanel
from pygame_gui.elements import UISelectionList
from pygame_gui.windows import UIMessageWindow
from entidades import DataBlock, Modulos, MainWorker
from gui_manager import GuiManager
from pygame.locals import *


LIGHTGRAY = (192, 192, 192)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)


class PGData:
    """
    Clase para trabajar con pygame
    """
    def __init__(self, window_size=(1000, 650)):
        self.initialize_pygame()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 40)
        self.WINDOW_SIZE = window_size  # Tamaño ventana principal
        self.window_surface = pygame.display.set_mode(self.WINDOW_SIZE)        
        self.is_running = True
        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('#000000'))
        
    @staticmethod
    def initialize_pygame():
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centra la interfaz
        pygame.display.set_caption('Data analysis')

    def run(self):
        worker = MainWorker()
        modulo = Modulos(1)
        worker.modulos.add(modulo)
        gui_manager = GuiManager()
        while self.is_running:
            keys = pygame.key.get_pressed()  # Obtencion de tecla presionada
            time_delta = self.clock.tick(60)/1000.0
            position_mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif keys[K_ESCAPE]:  # Acciones al presionar tecla escape
                    gui_manager.cancel()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if gui_manager.selected_block:
                        for modulo in worker.modulos:
                            if modulo.id == 1:
                                datablock = DataBlock(position_mouse, gui_manager.selected_item)
                                modulo.data_ingesta.add(datablock)
                if event.type == pygame.USEREVENT:                    
                    gui_manager.check_event(event, position_mouse, worker)
                gui_manager.manager.process_events(event)
            self.window_surface.fill(BLACK)
            abs_position = pygame.mouse.get_pos()  # Posición actual mouse
            gui_manager.manager.update(time_delta)
            self.window_surface.blit(self.background, (0, 0))
            gui_manager.manager.draw_ui(self.window_surface)
            gui_manager.draw_workspace(self.window_surface)
            worker.draw_all(self.window_surface, abs_position)
            gui_manager.workspace.fill(LIGHTGRAY)
            if gui_manager.selected_block:
                gui_manager.draw_selected(self.window_surface, abs_position)
            pygame.display.update()
        

if __name__ == '__main__':
    app = PGData()
    app.run()
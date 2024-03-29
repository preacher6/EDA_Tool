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
from entidades import DataBlock, Modulos, MainWorker, Conexion
from gui_manager import GuiManager
from pygame.locals import *


LIGHTGRAY = (192, 192, 192)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
ANCHO = 1000
ALTO = 600
size_alert = (300, 150)

class PGData:
    """
    Clase para trabajar con pygame
    """
    def __init__(self, window_size=(ANCHO, ALTO)):
        self.initialize_pygame()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 49)
        self.logo = pygame.image.load(os.path.join('pics', 'logo.png')) # Carga logo utp
        self.WINDOW_SIZE = window_size  # Tamaño ventana principal
        self.window_surface = pygame.display.set_mode(self.WINDOW_SIZE)        
        self.is_running = True
        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('#000000'))

    @staticmethod
    def initialize_pygame():
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centra la interfaz
        pygame.display.set_caption('BlockEDA')

    def run(self):
        worker = MainWorker()
        worker.num_modulos+=1
        modulo = Modulos(worker.num_modulos)        
        worker.modulos.add(modulo)
        gui_manager = GuiManager(window_size=(ANCHO, ALTO))
        position_mouse = (0, 0)  # Inicializar posicion presionad
        init_pos = (0, 0)  # Posicion inicial de la conexion
        draw_wire = False
        draw_blue = False
        elem_ini = None
        while self.is_running:
            keys = pygame.key.get_pressed()  # Obtencion de tecla presionada
            time_delta = self.clock.tick(60)/1000.0            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif keys[K_ESCAPE]:  # Acciones al presionar tecla escape
                    gui_manager.cancel(worker.modulos)
                    draw_wire = False
                    draw_blue = False         
                    for modulo in worker.modulos:
                        if modulo.id == gui_manager.selected_model:
                            for bloque in modulo.data_blocks:
                                bloque.selected = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position_mouse = pygame.mouse.get_pos()
                    #
                    if pygame.mouse.get_pressed()[0]:
                        """Tareas dependientes del click izquierdo"""
                        for modulo in worker.modulos:
                                if modulo.name == gui_manager.selected_model:  ## Selecciona el módulo
                                    for bloque in modulo.data_blocks:
                                        if bloque.rect.collidepoint(position_mouse):
                                            if not bloque.selected: 
                                                for bloque_2 in modulo.data_blocks:                                                    
                                                    bloque_2.selected = False
                                                bloque.selected = True
                                            else:
                                                bloque.selected = False
                        if gui_manager.selected_block:  # Poner bloque en modulo
                            for modulo in worker.modulos:
                                
                                if modulo.name == gui_manager.selected_model:
                                    print(modulo.id)
                                    if gui_manager.rect_workspace.collidepoint(position_mouse):
                                        datablock = DataBlock(position_mouse, gui_manager.selected_item,
                                        type=gui_manager.selected_type, action=gui_manager.selected_action)
                                        modulo.data_blocks.add(datablock)
                                        gui_manager.selected_block = False
                        
                        if draw_wire:
                            for modulo in worker.modulos:
                                if modulo.name == gui_manager.selected_model:
                                    for bloque in modulo.data_blocks:
                                        for nodo in bloque.nodos:
                                            if nodo.rect.collidepoint(position_mouse):
                                                bloque.in_elements.add(elem_ini)
                                                # print(bloque.bloque.data)
                                                print(bloque.bloque.id)
                                                join = False  # Flag para 2 dataframes (caso de join)
                                                if not bloque.bloque.data.empty:
                                                    if bloque.bloque.id == 'Transformacion':
                                                        bloque.bloque.cargar_data2(data2=elem_ini.bloque.data)
                                                        join = True
                                                        for bloque_ini in modulo.data_blocks:
                                                            if bloque_ini == elem_ini:
                                                                bloque_ini.out_elements.add(bloque)
                                                        elem_fin = bloque
                                                        conexion = Conexion((init_pos, position_mouse),
                                                        elem_ini, elem_fin)
                                                        modulo.conections.add(conexion)
                                                        draw_wire = False
                                                        gui_manager.hold_line = False
                                                else:
                                                    if bloque.bloque.data.empty:
                                                        bloque.bloque.cargar_data(data=elem_ini.bloque.data)
                                                        for bloque_ini in modulo.data_blocks:
                                                            if bloque_ini == elem_ini:
                                                                bloque_ini.out_elements.add(bloque)
                                                        elem_fin = bloque
                                                        conexion = Conexion((init_pos, position_mouse),
                                                        elem_ini, elem_fin)
                                                        modulo.conections.add(conexion)
                                                        draw_wire = False
                                                        gui_manager.hold_line = False
                                                
                                                if bloque.bloque.data.empty or join:
                                                    print('une')
                                                    
                                                else:
                                                    ('no une')
                                                
                        if draw_blue:
                            for modulo in worker.modulos:
                                if modulo.name == gui_manager.selected_model:
                                    for bloque in modulo.data_blocks:
                                        for nodo_v in bloque.nodos_v:
                                            if nodo_v.rect.collidepoint(position_mouse):
                                                bloque.in_elements.add(elem_ini)
                                                bloque.bloque.cargar_data(data=elem_ini.bloque.data)
                                                for bloque_ini in modulo.data_blocks:
                                                    if bloque_ini == elem_ini:
                                                        bloque_ini.out_elements.add(bloque)
                                                elem_fin = bloque
                                                conexion = Conexion((init_pos, position_mouse),
                                                elem_ini, elem_fin)
                                                modulo.conections.add(conexion)
                                                draw_blue = False
                                                gui_manager.hold_line = False

                        if gui_manager.hold_line and not draw_wire:  # Iniciar conexión
                            
                            for modulo in worker.modulos:
                                if modulo.name == gui_manager.selected_model:
                                    for bloque in modulo.data_blocks:                                        
                                        for nodo in bloque.nodos:
                                            if nodo.rect.collidepoint(position_mouse):
                                                if not bloque.bloque.data.empty:
                                                    draw_wire = True
                                                    init_pos = pygame.mouse.get_pos()
                                                    elem_ini = bloque
                                                else:
                                                    UIMessageWindow(pygame.Rect((self.WINDOW_SIZE[0]/2-size_alert[0]/2, 
                                                                                self.WINDOW_SIZE[1]/2-size_alert[1]/2), size_alert),
                                                                                html_message='El elemento no puede\n ser conectado.', window_title='Error', manager=gui_manager.manager)
                                                    gui_manager.hold_line = False
                                                    gui_manager.editar[0] = 0
                                                        
                        if gui_manager.hold_line and not draw_blue:  # Iniciar conexión
                            for modulo in worker.modulos:
                                if modulo.name == gui_manager.selected_model:
                                    for bloque in modulo.data_blocks:                                                            
                                        for nodo_v in bloque.nodos_v:
                                            if nodo_v.rect.collidepoint(position_mouse):
                                                if not bloque.bloque.data.empty:
                                                    draw_blue = True
                                                    init_pos = pygame.mouse.get_pos()
                                                    elem_ini = bloque
                                                else:
                                                    UIMessageWindow(pygame.Rect((self.WINDOW_SIZE[0]/2-size_alert[0]/2, 
                                                                                self.WINDOW_SIZE[1]/2-size_alert[1]/2), size_alert),
                                                                                html_message='El bloque no ha sido procesado', window_title='Error', manager=gui_manager.manager)
                                                    gui_manager.hold_line = False
                                                    gui_manager.editar[0] = 0
                                            
                    elif pygame.mouse.get_pressed()[2]:
                        """Tareas dependientes del click derecho"""
                        for modulo in worker.modulos:
                                if modulo.name == gui_manager.selected_model:
                                    for bloque in modulo.data_blocks:
                                        if bloque.rect.collidepoint(position_mouse):
                                            if not bloque.out_elements:
                                                if not bloque.selected: 
                                                    for bloque_2 in modulo.data_blocks:                                                    
                                                        bloque_2.selected = False
                                                    bloque.selected = True
                                                else:
                                                    bloque.selected = False
                                                gui_manager.properties = False
                                                gui_manager.check_block(bloque, (ANCHO, ALTO))  
                                            else:
                                                    UIMessageWindow(pygame.Rect((self.WINDOW_SIZE[0]/2-size_alert[0]/2, 
                                                                                self.WINDOW_SIZE[1]/2-size_alert[1]/2), size_alert),
                                                                                html_message='El bloque no puede tener elementos conectados a su salida si se desea modificar', window_title='Error', manager=gui_manager.manager)
                                                    gui_manager.hold_line = False                                          

                if event.type == pygame.USEREVENT: 
                    gui_manager.check_event(event, position_mouse, worker)
                    gui_manager.check_actions(position_mouse, worker)
                gui_manager.manager.process_events(event)
            abs_position = pygame.mouse.get_pos()  # Posición actual mouse            
            self.window_surface.fill(BLACK)            
            
            gui_manager.manager.update(time_delta)
            self.window_surface.blit(self.background, (0, 0))   
            self.window_surface.blit(self.logo, (65, 40))         
            gui_manager.draw_workspace(self.window_surface)
            gui_manager.exec_actions(self.window_surface, abs_position, worker)
            gui_manager.workspace.fill(LIGHTGRAY)
            worker.draw_all(self.window_surface, abs_position, gui_manager.selected_model)   
            
            if gui_manager.selected_block:
                gui_manager.draw_selected(self.window_surface, abs_position)
            gui_manager.manager.draw_ui(self.window_surface) # Dibujar elementos pygame_gui
            if draw_wire:
                gui_manager.draw_wire(self.window_surface, init_pos, abs_position)
            if draw_blue:
                gui_manager.draw_wire(self.window_surface, init_pos, abs_position)
            self.window_surface.blit(self.font.render('BlockEDA', True, (255, 255, 255)), (730, 40))
            pygame.display.update()

   
if __name__ == '__main__':
    app = PGData()
    app.run()

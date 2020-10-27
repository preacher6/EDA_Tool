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


LIGHTGRAY = (192, 192, 192)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)


class GuiManager:
    """Maneja todo lo relacionado a la estructura de la GUI y manejo de eventos"""
    def __init__(self, workspace_size=(700, 450)):
        self.manager = pygame_gui.UIManager((1000, 650), PackageResource(package='data.themes', resource='theme_1.json'))
        self.manager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
                                            {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
                                            {'name': 'fira_code', 'point_size': 10, 'style': 'italic'},
                                            {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
                                            {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
                                            ])
        self.SIZE_WORKSPACE = workspace_size  # Tamaño del espacio de trabajo        
        self.items_choose = ['Ingesta', 'Exploración', 'Limpieza', 'Análisis', 'Transformación', 'Exportar']        
        self.ing_datos = ['Fichero', 'SQL', 'URL', 'Data toy']
        self.explor_datos = ['Descripción', 'Tabla', 'Tipos de datos','Comportamiento']
        self.limp_datos = ['Eliminar Nan', 'Reemplazar Nan']
        self.anali_datos = ['Univariante', 'Multivariante', 'Correlación']
        self.transf_data = ['Agregar', 'Unir', 'Pivote', 'Filtrar', 'Particionar', 'PCA', 'ICA']
        self.expor_datos = ['CSV']
        self.selected_item = 'CSV'
        self.items_list = [self.items_choose[0], self.ing_datos[0]]
        self.proc_datos = ['Explorar datos', 'Limpiar datos', 'Transformar datos']
        
        self.validar = []

        self.selected_block = False  # Indica si se esta dibujando algun bloque en pantalla

        self.init_elements()

    def init_elements(self):
        self.panel_objects  = UIPanel(pygame.Rect(10, 160, 235, 300),
                            starting_layer_height=4,
                            manager=self.manager)
        self.ini_primenu = 'Ingesta'
        self.primer_menu = UIDropDownMenu(self.items_choose,
                                            self.ini_primenu,
                                            pygame.Rect((10, 10),
                                                        (210, 30)),
                                            self.manager,
                                            container=self.panel_objects)
        self.ini_segmenu = 'Ficheros'
        self.segundo_menu = UIDropDownMenu(self.ing_datos,
                                            self.ini_segmenu,
                                            pygame.Rect((10, 50),
                                                        (210, 30)),
                                            self.manager,
                                            container=self.panel_objects)
        self.accion = UISelectionList(pygame.Rect(10, 100, 210, 140),
                                    item_list=self.ing_datos,
                                    manager=self.manager,
                                    container=self.panel_objects,
                                    allow_multi_select=False)
        self.select = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((60, 250), (100, 30)),
                                            text='Seleccionar',
                                            manager=self.manager,
                                            container=self.panel_objects)

        self.panel_modulos  = UIPanel(pygame.Rect(10, 470, 235, 120),
                            starting_layer_height=4,
                            manager=self.manager)
        self.ini_modulo = 'Modelo 1'
        self.modelo = UIDropDownMenu(['Modelo 1'],
                                            self.ini_modulo,
                                            pygame.Rect((10, 10),
                                                        (210, 30)),
                                            self.manager,
                                            container=self.panel_modulos)
        self.new = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 60), (35, 35)),
                                            text='',
                                            manager=self.manager,
                                            container=self.panel_modulos,
                                            object_id='#new')
        self.delete = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 60), (35, 35)),
                                            text='',
                                            manager=self.manager,
                                            container=self.panel_modulos,
                                            object_id='#del')
        self.rename = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((160, 60), (35, 35)),
                                            text='',
                                            manager=self.manager,
                                            container=self.panel_modulos,
                                            object_id='#rename')

        button_row_width = 40
        button_row_height = 40  
        spacing = 10
        self.panel_tareas  = UIPanel(pygame.Rect(270, 90, 270, 55),
                            starting_layer_height=4,
                            manager=self.manager)
        y_pos = 5
        for ind_x in range(1, 6):
            x_pos = ind_x*spacing + (ind_x-1)*button_row_width
            pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x_pos, y_pos), (button_row_width, button_row_height)),
                                        text='',
                                        manager=self.manager,
                                        container=self.panel_tareas,
                                        object_id='#p'+str(ind_x))

        self.panel_editar  = UIPanel(pygame.Rect(550, 90, 300, 55),
                            starting_layer_height=4,
                            manager=self.manager)
        y_pos = 5
        for ind_x in range(1, 5):
            x_pos = ind_x*spacing + (ind_x-1)*button_row_width
            pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x_pos, y_pos), (button_row_width, button_row_height)),
                                        text='',
                                        manager=self.manager,
                                        container=self.panel_editar,
                                        object_id='#e'+str(ind_x))

        self.workspace = pygame.Surface(self.SIZE_WORKSPACE)
        self.workspace.fill(LIGHTGRAY)
        self.pos_workspace = (270, 160)

    def reasign2(self, lista1, lista2):
        #self.segundo_menu.kill() Esto permitia eliminar un objeto e instanciarlo de nuevo
        self.ini_segmenu = lista1[0]
        self.segundo_menu = UIDropDownMenu(lista1,
                                            self.ini_segmenu,
                                            pygame.Rect((10, 50),
                                                        (210, 30)),
                                            self.manager,
                                            container=self.panel_objects)
        self.accion.set_item_list(lista2)

    def reasign1(self, lista):
        self.accion.set_item_list(lista)

    def draw_workspace(self, screen):
        screen.blit(self.workspace, self.pos_workspace)
    
    def check_event(self, event, position, worker, image=None):
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_object_id == 'panel.#2':
                self.accion.set_item_list(['23', '3'])
            if event.ui_element == self.select:  # Selecciona un objeto
                self.selected_block = True
                self.datablock = DataBlock(position, self.selected_item)
                """for modulo in worker.modulos:
                    if modulo.id == 1:
                        modulo.data_ingesta.add(self.datablock)"""
        if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.primer_menu:  # Elección primera acción
                if event.text == self.items_choose[0]:
                    self.reasign1(self.ing_datos)
                elif event.text == self.items_choose[1]:
                    self.reasign1(self.explor_datos)
                elif event.text == self.items_choose[2]:
                    self.reasign1(self.limp_datos)
                elif event.text == self.items_choose[3]:
                    self.reasign1(self.anali_datos)
                elif event.text == self.items_choose[4]:
                    self.reasign1(self.transf_data)
                elif event.text == self.items_choose[5]:
                    self.reasign1(self.expor_datos)

            if event.ui_element == self.segundo_menu:  # Elección segunda acción
                if event.text == self.ing_datos[0]:  # ingesta datos
                    self.selected_item = 'csv'
                    self.reasign1(self.ficheros)
                elif event.text == self.ing_datos[1]:
                    self.selected_item = 'csv'
                    self.reasign1(self.data_toy)
                elif event.text == self.ing_datos[2]:
                    self.items_list[1] = self.ing_datos[2]
                    self.reasign1(self.ficheros)    

                if event.text == self.proc_datos[0]:  # Procesamiento data
                    self.selected_item = 'describir'
                    self.reasign1(self.exp_datos)
                elif event.text == self.proc_datos[1]:
                    self.reasign1(self.limp_datos)
                elif event.text == self.proc_datos[2]:
                    self.reasign1(self.transf_data)
                
                if event.text == self.entrenar[0]:  # Entrenar
                    self.reasign1(self.clasificar)
                elif event.text == self.entrenar[1]:
                    self.reasign1(self.regresion)
                elif event.text == self.entrenar[2]:
                    self.reasign1(self.agrupar)

    def draw_selected(self, screen, position):
        self.datablock.hot_draw(screen, position)

    def cancel(self):
        self.selected_block = False
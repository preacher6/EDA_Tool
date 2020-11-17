import pygame
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIButton
from pygame_gui.elements import UISelectionList, UIDropDownMenu


class ProperLoad(UIWindow):
    def __init__(self, rect, ui_manager):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_load',
                         resizable=True)

        loaded_test_image = pygame.image.load('data/images/splat.bmp').convert_alpha()
        top_margin = 2
        top_left = 10
        self.entry_text =  UITextEntryLine(pygame.Rect((70, top_margin), (120, 20)),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)
        
        self.search_label = UILabel(pygame.Rect((10, top_margin),
                                                (56, self.entry_text.rect.height)),
                                                    "Nombre:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.rename = UIButton(relative_rect=pygame.Rect((top_left, 50), (35, 35)),
                                            text='',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#folder')
        self.path_label = UITextEntryLine(pygame.Rect((50, 50),
                                                (340, self.entry_text.rect.height)),
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self,
                                                object_id='pathdir')
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+120, 100), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        self.path_label.disable()
        self.set_blocking(True)


class ProperDropnan(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_dropnan',
                         resizable=True)
        top_margin = 2
        top_left = 10
        
        self.entry_text =  UITextEntryLine(pygame.Rect((70, top_margin), (120, 20)),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)
        
        self.search_label = UILabel(pygame.Rect((10, top_margin),
                                                (56, self.entry_text.rect.height)),
                                                    "Nombre:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.eje_name = UILabel(pygame.Rect((10, top_margin+35),
                                                (60, self.entry_text.rect.height)),
                                                    "Eje:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.eje = UIDropDownMenu(['Fila', 'Columna'],
                                    'Fila',
                                    pygame.Rect((10+50, 35),
                                                (100, 30)),
                                    ui_manager,
                                    container=self)

        self.criterio_name = UILabel(pygame.Rect((170, top_margin+35),
                                                (70, self.entry_text.rect.height)),
                                                    "Criterio:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.criterio = UIDropDownMenu(['Alguno', 'Todos', 'Valor'],
                                        'Alguno',
                                            pygame.Rect((190+50, 35),
                                                        (100, 30)),
                                            ui_manager,
                                            container=self)
        
        self.lista_columnas = UISelectionList(pygame.Rect(top_left+80, 70, 210, 120),
                                    item_list=bloque.bloque.data.columns,
                                    manager=ui_manager,
                                    container=self,
                                    allow_multi_select=True)
        
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+120, 200), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        
        self.set_blocking(True)

class ProperDelCol(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_del_col',
                         resizable=True)
        top_margin = 2
        top_left = 10
        
        self.entry_text =  UITextEntryLine(pygame.Rect((70, top_margin), (120, 20)),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)
        
        self.search_label = UILabel(pygame.Rect((10, top_margin),
                                                (56, self.entry_text.rect.height)),
                                                    "Nombre:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.eti_columnas = UILabel(pygame.Rect((10, top_margin+35),
                                                (160, self.entry_text.rect.height)),
                                                    "Columnas a eliminar:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        
        self.lista_columnas = UISelectionList(pygame.Rect(top_left+80, 70, 210, 120),
                                    item_list=bloque.bloque.data.columns,
                                    manager=ui_manager,
                                    container=self,
                                    allow_multi_select=True)
        
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+120, 200), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        
        self.set_blocking(True)
        
class ProperRenCol(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_ren_col',
                         resizable=True)
        top_margin = 2
        top_left = 10
        
        self.entry_text =  UITextEntryLine(pygame.Rect((70, top_margin), (120, 20)),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)
        
        self.search_label = UILabel(pygame.Rect((10, top_margin),
                                                (56, self.entry_text.rect.height)),
                                                    "Nombre:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.eti_columnas = UILabel(pygame.Rect((10, top_margin+35),
                                                (190, self.entry_text.rect.height)),
                                                    "Columna(s) a renombrar:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        
        self.lista_columnas = UISelectionList(pygame.Rect(top_left+190, 40, 210, 120),
                                    item_list=bloque.bloque.data.columns,
                                    manager=ui_manager,
                                    container=self,
                                    allow_multi_select=True)
        
        self.eti_name = UILabel(pygame.Rect((10, top_margin+165),
                                                (160, self.entry_text.rect.height)),
                                                    "Nombre(s) a asignar:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        
        self.new_name =  UITextEntryLine(pygame.Rect((170, top_margin+165), (220, 20)),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)
        
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+140, 200), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        
        self.set_blocking(True)

import pygame
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIButton
from pygame_gui.elements import UISelectionList


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
        self.path_label = UILabel(pygame.Rect((50, 50),
                                                (340, self.entry_text.rect.height)),
                                                    "Dirección archivo",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self,
                                                object_id='label2')
        self.set_blocking(True)


class ProperDelCol(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_del_col',
                         resizable=True)
        top_margin = 2
        top_left = 10
        bloque = bloque.bloque.data
        
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
        
        self.accion = UISelectionList(pygame.Rect(10, 100, 210, 140),
                                    item_list=self.ing_datos,
                                    manager=ui_manager,
                                    container=self,
                                    allow_multi_select=True)
        
        self.rename = UIButton(relative_rect=pygame.Rect((top_left, 50), (35, 35)),
                                            text='',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#folder')
        self.path_label = UILabel(pygame.Rect((50, 50),
                                                (340, self.entry_text.rect.height)),
                                                    "Dirección archivo",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self,
                                                object_id='label2')
        self.set_blocking(True)
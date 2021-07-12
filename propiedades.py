import pygame
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIButton
from pygame_gui.elements import UISelectionList, UIDropDownMenu

##### INGESTA

class ProperLoad(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
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
        self.path_label.set_text(bloque.bloque.path)
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+120, 100), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        print(self.path_label)
        self.path_label.disable()
        self.set_blocking(True)


### EXPLORAR


class ProperUnique(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_unique',
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
                                                (170, self.entry_text.rect.height)),
                                                    "Columnas a explorar:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        
        elementos = bloque.bloque.data.columns
        self.elementos = UIDropDownMenu(elementos,
                                      elementos[0],
                                    pygame.Rect((top_left+80, 40),
                                                (190, 30)),
                                    ui_manager,
                                    container=self)
        
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+120, 200), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        
        self.set_blocking(True)       

        
class ProperPlotBar(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_plotbar',
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
        self.atributo_name = UILabel(pygame.Rect((10, top_margin+35),
                                                (70, self.entry_text.rect.height)),
                                                    "Atributo:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.atributo = UIDropDownMenu(bloque.bloque.data.columns,
                                    bloque.bloque.data.columns[0],
                                    pygame.Rect((90, top_margin+35),
                                                (150, 30)),
                                    ui_manager,
                                    container=self)

        self.criterio_name = UILabel(pygame.Rect((10, top_margin+75),
                                                (70, self.entry_text.rect.height)),
                                                    "Criterio:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.criterio = UIDropDownMenu(['Conteo', 'Suma', 'Media'],
                                        'Conteo',
                                            pygame.Rect((90, top_margin+75),
                                                        (100, 30)),
                                            ui_manager,
                                            container=self)
        
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+120, 200), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        
        self.set_blocking(True)


class ProperTabDin(UIWindow):
    """Clase para generar tablas dinámicas
    Args:
        UIWindow ([type]): [description]
    """
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_tabdin',
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
        self.eti_index = UILabel(pygame.Rect((10-5, top_margin+40),
                                                (70, self.entry_text.rect.height)),
                                                    "Índice:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        elementos = bloque.bloque.data.columns
        self.indice = UIDropDownMenu(elementos,
                                      elementos[0],
                                    pygame.Rect((top_left+60, 40),
                                                (140, 30)),
                                    ui_manager,
                                    container=self)
        self.eti_col = UILabel(pygame.Rect((10-5, top_margin+80),
                                                (70, self.entry_text.rect.height)),
                                                    "Columna:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        
        self.columna = UIDropDownMenu(elementos,
                                      elementos[1],
                                    pygame.Rect((top_left+70, 80),
                                                (140, 30)),
                                    ui_manager,
                                    container=self)
        
        self.eti_valor = UILabel(pygame.Rect((10+195, top_margin+40),
                                                (70, self.entry_text.rect.height)),
                                                    "Valor:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)        
        
        self.valor = UIDropDownMenu(elementos,
                                      elementos[0],
                                    pygame.Rect((top_left+255, top_margin+40),
                                                (140, 30)),
                                    ui_manager,
                                    container=self)
        
        self.eti_oper = UILabel(pygame.Rect((240, top_margin+80),
                                                (80, self.entry_text.rect.height)),
                                                    "Operación:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        
        self.operacion = UISelectionList(pygame.Rect(top_left+240, 130, 120, 70),
                            item_list=['Media', 'Contar', 'Sumar'],
                            manager=ui_manager,
                            container=self,
                            allow_multi_select=True)
                
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+140, 200), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        
        self.set_blocking(True)






### LIMPIEZA    

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
        
class ReplaceNan(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_repnan',
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
        self.eje_name = UILabel(pygame.Rect((10, top_margin+40),
                                                (60, self.entry_text.rect.height)),
                                                    "Valor:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.value =  UITextEntryLine(pygame.Rect((70, top_margin+40), (80, 20)),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)

        self.columnas = UILabel(pygame.Rect((220, top_margin+35),
                                                (80, self.entry_text.rect.height)),
                                                    "Atributos:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        
        self.lista_columnas = UISelectionList(pygame.Rect(top_left+140, 70, 210, 120),
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

class ReplaceValue(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_repval',
                         resizable=True)
        top_margin = 2
        top_left = 10
        
        self.entry_text =  UITextEntryLine(pygame.Rect((70, top_margin), (120, 20)),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)
        
        self.label1 = UILabel(pygame.Rect((10, top_margin),
                                                (56, self.entry_text.rect.height)),
                                                    "Nombre:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.label2 = UILabel(pygame.Rect((10, top_margin+40),
                                                (60, self.entry_text.rect.height)),
                                                    "Valor a reemplazar:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.old_value =  UITextEntryLine(pygame.Rect((70, top_margin+40), (80, 20)),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)
        self.label3 = UILabel(pygame.Rect((10, top_margin+90),
                                                (60, self.entry_text.rect.height)),
                                                    "Nuevo valor:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)

        self.value =  UITextEntryLine(pygame.Rect((70, top_margin+90), (80, 20)),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)

        self.columnas = UILabel(pygame.Rect((220, top_margin+35),
                                                (80, self.entry_text.rect.height)),
                                                    "Atributos:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        
        self.lista_columnas = UISelectionList(pygame.Rect(top_left+140, 70, 210, 120),
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
        
class ProperTurnDate(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_turn_date',
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
                                                (170, self.entry_text.rect.height)),
                                                    "Columnas a modificar:",
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

class ProperTurnNum(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_turn_num',
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
                                                (170, self.entry_text.rect.height)),
                                                    "Columnas a modificar:",
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


class ProperTurnCat(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_turn_cat',
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
                                                (170, self.entry_text.rect.height)),
                                                    "Columnas a modificar:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        
        self.lista_columnas = UIDropDownMenu(bloque.bloque.data.columns,
                                            bloque.bloque.data.columns[0],
                                            pygame.Rect(top_left+80, 70, 160, 30),
                                            ui_manager,
                                            container=self)
           
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+120, 200), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        
        self.set_blocking(True)       


class ProperSetIndex(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_set_index',
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
                                                (170, self.entry_text.rect.height)),
                                                    "Nuevo indice:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        
        self.lista_columnas = UISelectionList(pygame.Rect(top_left+80, 70, 210, 120),
                                    item_list=bloque.bloque.data.columns,
                                    manager=ui_manager,
                                    container=self)
        
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+120, 200), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        
        self.set_blocking(True)        





class ProperSave(UIWindow):
    def __init__(self, rect, ui_manager):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_save',
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
        

####### ANÁLISIS

class ProperAnaUni(UIWindow):
    """Clase para generar tablas dinámicas
    Args:
        UIWindow ([type]): [description]
    """
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_anauni',
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

        elementos = bloque.bloque.data.columns
        self.elementos = UIDropDownMenu(elementos,
                                      elementos[0],
                                    pygame.Rect((top_left+80, 40),
                                                (190, 30)),
                                    ui_manager,
                                    container=self)
        self.eti_elementos = UILabel(pygame.Rect((10, top_margin+40),
                                                (75, self.entry_text.rect.height)),
                                                    "Atributo:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)

        graficos = ['Distribución', 'Caja', 'Conteo']
        self.graficos = UIDropDownMenu(graficos,
                                      graficos[0],
                                    pygame.Rect((top_left+130, 90),
                                                (140, 30)),
                                    ui_manager,
                                    container=self)
        
        self.eti_valor = UILabel(pygame.Rect((10, top_margin+90),
                                                (130, self.entry_text.rect.height)),
                                                    "Tipo de gráfico:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)  
                
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+90, 140), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        
        self.set_blocking(True)

        
class ProperAnaBi(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_anabi',
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
        self.eti_x = UILabel(pygame.Rect((10, top_margin+40),
                                                (70, self.entry_text.rect.height)),
                                                    "Eje X:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.eti_y = UILabel(pygame.Rect((10, top_margin+80),
                                                (70, self.entry_text.rect.height)),
                                                    "Eje Y:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        elementos = bloque.bloque.data.columns
        self.x_value = UIDropDownMenu(elementos,
                                      elementos[0],
                                    pygame.Rect((top_left+70, 40),
                                                (140, 30)),
                                    ui_manager,
                                    container=self)
        
        self.y_value = UIDropDownMenu(elementos,
                                      elementos[1],
                                    pygame.Rect((top_left+70, 80),
                                                (140, 30)),
                                    ui_manager,
                                    container=self)
        tipo_grafico = ['Relación', 'Regresión', 'Conteo']
        self.tipo = UILabel(pygame.Rect((10, top_margin+120),
                                                (140, self.entry_text.rect.height)),
                                                    "Tipo de gráfico:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        
        self.grafico = UIDropDownMenu(tipo_grafico,
                                      tipo_grafico[0],
                                    pygame.Rect((top_left+150, top_margin+120),
                                                (140, 30)),
                                    ui_manager,
                                    container=self)
                
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+140, 200), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        
        self.set_blocking(True)


class ProperAnaMult(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_anamult',
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
        self.eti_atributo = UILabel(pygame.Rect((10, top_margin+35),
                                                (70, self.entry_text.rect.height)),
                                                    "Atributo:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.atributo = UIDropDownMenu(['Algunas', 'Todas'],
                                    'Algunas',
                                    pygame.Rect((35+50, 35),
                                                (100, 30)),
                                    ui_manager,
                                    container=self,
                                    object_id='#atributo')
        
        self.lista_columnas = UISelectionList(pygame.Rect(top_left+80, 70, 210, 120),
                                    item_list=bloque.bloque.data.columns,
                                    manager=ui_manager,
                                    container=self,
                                    allow_multi_select=True,
                                    object_id='#columnas')
        
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+120, 200), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        
        self.set_blocking(True)


### TRANSFORMAR


class ProperJoin(UIWindow):
    def __init__(self, rect, ui_manager, bloque):
        super().__init__(rect, ui_manager,
                         window_display_title='Propiedades',
                         object_id='#proper_join',
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
        self.union_name = UILabel(pygame.Rect((10, top_margin+35),
                                                (70, self.entry_text.rect.height)),
                                                    "Columna unión:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.union = UIDropDownMenu(bloque.bloque.data.columns,
                                    bloque.bloque.data.columns[0],
                                    pygame.Rect((90, top_margin+35),
                                                (150, 30)),
                                    ui_manager,
                                    container=self)

        self.tipo_label = UILabel(pygame.Rect((10, top_margin+75),
                                                (70, self.entry_text.rect.height)),
                                                    "Tipo de unión:",
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        self.tipo = UIDropDownMenu(['Izquierda', 'Derecha', 'Interna'],
                                        'Externa',
                                            pygame.Rect((90, top_margin+75),
                                                        (100, 30)),
                                            ui_manager,
                                            container=self)
        
        self.aceptar = UIButton(relative_rect=pygame.Rect((top_left+120, 200), (90, 35)),
                                            text='Aceptar',
                                            manager=ui_manager,
                                            container=self,
                                            object_id='#aceptar')
        
        self.set_blocking(True)

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
from pygame_gui.windows import UIFileDialog
from pygame_gui.windows import UIMessageWindow
from entidades import DataBlock, Modulos, MainWorker
import propiedades
from pygame_gui.core.utility import create_resource_path


LIGHTGRAY = (192, 192, 192)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
FUENTE = BLACK
SIZE_ALERT = (300, 150)


class AlertWindow(UIWindow):
    def __init__(self, message, rect, ui_manager):
        super().__init__(rect, ui_manager,
                         window_display_title='Advertencia',
                         object_id='#warning_window',
                         resizable=True)
        altura = 40
        message_size = 280
        self.warn_label = UILabel(pygame.Rect((0, 12),
                                            (self.get_container().get_size()[0], 20)),
                                                message,
                                                manager=ui_manager,
                                                container=self,
                                                parent_element=self)
        #self.set_dimensions((self.warn_label.rect.width, 200))
        button_size = (100, 30)
        self.accept_warn = UIButton(relative_rect=pygame.Rect((self.warn_label.rect.width/2-button_size[0]/2,
                                                                                 altura+10), button_size),
                                                                                text='Aceptar',
                                                                                manager=self.ui_manager,
                                                                                container=self)
        self.set_blocking(True)

class GuiManager:
    """Maneja todo lo relacionado a la estructura de la GUI y manejo de eventos"""
    def __init__(self, window_size=(1000, 650), workspace_size=(700, 450)):
        self.window_size = window_size
        self.manager = pygame_gui.UIManager(window_size, PackageResource(package='data.themes', resource='theme_1.json'))
        self.manager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
                                            {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
                                            {'name': 'fira_code', 'point_size': 10, 'style': 'italic'},
                                            {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
                                            {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
                                            ])
        self.SIZE_WORKSPACE = workspace_size  # Tamaño del espacio de trabajo        
        self.items_choose = ['Ingesta', 'Exploración', 'Limpieza', 'Análisis', 'Transformación', 'Exportar']        
        self.ing_datos = ['Fichero', 'SQL', 'URL', 'Data toy', 'Carpeta', 'Temporal']
        self.explor_datos = ['Tabla', 'Descripción', 'Tabla dinámica', 'Tipos de datos', 'Diagrama de barras',
                             'Cabecera', 'Cola', 'Elementos únicos']
        self.limp_datos = ['Eliminar Nan', 'Reemplazar Nan', 'Eliminar columnas', 'Eliminar filas',
                            'Renombrar columnas', 'Reemplazar valor', 'Cambiar indice',
                            'Convertir a fecha', 'Convertir a número', 'Convertir a categoría']
        self.anali_datos = ['Análisis univariante', 'Análisis bivariante',
                            'Análisis multivariante', 'Correlación']
        self.transf_data = ['Crear columna', 'Operar una columna', 'Operar dos columnas', 'Unir',
                             'Agrupar', 'Filtrar una columna', 'Filtrar dos columnas', 'Seleccionar columnas', 'Ordenar', 'Particionar',
                            'Normalizar', 'Estandarizar', 'Muestra', 'Remodelar']
        self.expor_datos = ['CSV', 'Temporal']
        self.selected_type = self.items_choose[0]
        self.selected_item = 'database'
        self.selected_action = ''
        self.items_list = [self.items_choose[0], self.ing_datos[0]]
        self.proc_datos = ['Explorar datos', 'Limpiar datos', 'Transformar datos']
        self.properties = False
        self.validar = []
        self.selected_model = 'Modelo 1'  # Modelo seleccionado
        self.selected_id = 1
        self.selected_block = False  # Indica si se esta dibujando algun bloque en pantalla
        self.tareas = [0]*5
        self.editar = [0]*4
        self.hold_line = False  # Dibujar arco para conectar elementos
        self.path = ''  # Direccion de archivo a procesar
        self.panel_proper = None  # Panel de propiedades del bloque elegido
        self.del_line = False  # Borrar líneas
        self.delete_line = pygame.image.load(os.path.join('pics', 'icons', 'erase.png'))
        self.init_elements()

    def init_elements(self):
        self.bloque = []
        self.alert_wi = []
        self.panel_objects  = UIPanel(pygame.Rect(10, 130, 235, 300),
                            starting_layer_height=4,
                            manager=self.manager)
        self.ini_primenu = 'Ingesta'
        self.primer_menu = UIDropDownMenu(self.items_choose,
                                            self.ini_primenu,
                                            pygame.Rect((10, 10),
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

        self.panel_modulos  = UIPanel(pygame.Rect(10, 440, 235, 120),
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
        spacing = 15
        self.panel_tareas  = UIPanel(pygame.Rect(270, 40, 405, 55),
                            starting_layer_height=4,
                            manager=self.manager)
        y_pos = 5
        for ind_x in range(1, 8):
            x_pos = ind_x*spacing + (ind_x-1)*button_row_width
            pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x_pos, y_pos), (button_row_width, button_row_height)),
                                        text='',
                                        manager=self.manager,
                                        container=self.panel_tareas,
                                        object_id='#p'+str(ind_x))

        # self.panel_editar  = UIPanel(pygame.Rect(550, 90, 300, 55),
        #                     starting_layer_height=4,
        #                     manager=self.manager)
        # y_pos = 5
        # for ind_x in range(1, 5):
        #     x_pos = ind_x*spacing + (ind_x-1)*button_row_width
        #     pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x_pos, y_pos), (button_row_width, button_row_height)),
        #                                 text='',
        #                                 manager=self.manager,
        #                                 container=self.panel_editar,
        #                                 object_id='#e'+str(ind_x))

        self.workspace = pygame.Surface(self.SIZE_WORKSPACE)
        self.workspace.fill(LIGHTGRAY)
        self.pos_workspace = (270, 120)
        datab = DataBlock((0, 0), 'database') # La recta sobre la que se pueden poner bloques
        x, y = datab.image.get_size()
        self.rect_workspace = pygame.Rect((self.pos_workspace[0]+x/2, self.pos_workspace[1]+y/2),
                                            (self.SIZE_WORKSPACE[0]-x, self.SIZE_WORKSPACE[1]-y))


    def reasign1(self, lista):
        self.accion.set_item_list(lista)

    def draw_workspace(self, screen):
        screen.blit(self.workspace, self.pos_workspace)
    
    def check_event(self, event, position, worker, image=None):
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            # print(event.ui_object_id)
            if event.ui_object_id == '#warning_window.button':
                self.alert_wi.kill()
            if event.ui_object_id == '#proper_load.#folder':
                self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 440, 500),
                                                    self.manager,
                                                    window_title='Cargar datos...',
                                                    initial_file_path='data/',
                                                    allow_existing_files_only=False)
            #### Grabar archivos
            if event.ui_object_id == '#proper_save.#folder_csv':
                self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 440, 500),
                                                    self.manager,
                                                    window_title='Almacenar archivo en...',
                                                    initial_file_path='data/',
                                                    allow_existing_files_only=False, 
                                                    allow_picking_directories=True)
                # print(1)
                # print(self.file_dialog)
            if event.ui_object_id == '#file_dialog.#ok_button':
                # print(self.file_dialog.file_selection_list)
                # print(self.file_dialog.file_path_text_line)
                # print(self.file_dialog.current_file_path)
                # print(self.file_dialog.current_file_list)
                # print(self.file_dialog.current_directory_path)
                self.panel_proper.path_label.set_text(create_resource_path(self.file_dialog.current_file_path))
                self.file_dialog.kill()

            if event.ui_object_id == '#proper_load.#aceptar':                
                self.bloque.status = False
                self.bloque.selected = False
                self.bloque.bloque.define_data(self.panel_proper.path_label.text)
                self.bloque.bloque.sep = self.panel_proper.elementos.selected_option
                self.panel_proper.kill()
                self.selected_type = self.items_choose[0]
                self.reasign1(self.ing_datos)
                self.selected_item = 'database'
                self.selected_action = ''
            if event.ui_object_id == '#proper_url.#aceptar':
                self.bloque.status = False
                self.bloque.selected = False
                self.bloque.bloque.define_data(self.panel_proper.path_label.text)
                self.panel_proper.kill()
                self.selected_type = self.items_choose[0]
                self.reasign1(self.ing_datos)
                self.selected_item = 'database'
                self.selected_action = ''
            if event.ui_object_id == '#proper_toy.#aceptar':
                self.bloque.status = False
                self.bloque.selected = False
                option_path = self.panel_proper.elementos.selected_option
                self.bloque.bloque.define_path(option_path)
                self.panel_proper.kill()
                self.selected_type = self.items_choose[0]
                self.reasign1(self.ing_datos)
                self.selected_item = 'database'
                self.selected_action = ''


            ##---- Limpieza
            if event.ui_object_id == '#proper_del_col.#aceptar':
                self.bloque.status = False                
                self.bloque.bloque.selected_columns = self.panel_proper.lista_columnas.get_multi_selection()
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_dropnan.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.axis = 0 if self.panel_proper.eje.selected_option == 'Fila' else 1 \
                                         if self.panel_proper.eje.selected_option == 'Columna' else 2
                self.bloque.bloque.thresh = 1 if self.panel_proper.eje.selected_option == 'Valor' else None
                self.bloque.bloque.how = 'all' if self.panel_proper.eje.selected_option == 'Todos' else 'any'
                self.bloque.bloque.selected_columns = self.panel_proper.lista_columnas.get_multi_selection()
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_ren_col.#aceptar':
                self.bloque.status = False
                viejos = self.panel_proper.lista_columnas.get_multi_selection()
                nuevos = self.panel_proper.new_name.text
                self.bloque.bloque.new_names(nuevos, viejos)
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_turn_date.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.elementos_fecha = self.panel_proper.lista_columnas.get_multi_selection()
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_turn_num.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.selected_columns = self.panel_proper.lista_columnas.get_multi_selection()
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_turn_cat.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.selected_columns = self.panel_proper.lista_columnas.selected_option
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_set_index.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.index = self.panel_proper.lista_columnas.get_single_selection()
                self.panel_proper.kill()
            
            # Carga
            if event.ui_object_id == '#proper_tabdin.#aceptar':
                self.bloque.status = False
                # self.bloque.bloque.index_barra = self.panel_proper.indice.selected_option
                #self.bloque.bloque.type_barra = 0 if self.panel_proper.criterio.selected_option == 'Conteo' else 1 if self.panel_proper.criterio.selected_option == 'Suma' else 2
                self.bloque.bloque.columna = self.panel_proper.columna.selected_option
                self.bloque.bloque.valor = self.panel_proper.valor.selected_option
                self.bloque.bloque.agg = self.panel_proper.operacion.get_multi_selection()
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_repnan.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.value = self.panel_proper.value.text
                self.bloque.bloque.selected_columns = self.panel_proper.lista_columnas.get_multi_selection()
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_repval.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.value = self.panel_proper.value.text
                self.bloque.bloque.old_value = self.panel_proper.old_value.text
                self.bloque.bloque.selected_columns = self.panel_proper.lista_columnas.get_multi_selection()
                self.panel_proper.kill()

            if event.ui_object_id == '#proper_unique.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.selected_column = self.panel_proper.elementos.selected_option
                self.panel_proper.kill()

            ##### Exploración
            if event.ui_object_id == '#proper_unique.#aceptar':
                pass
            
            if event.ui_object_id == '#proper_plotbar.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.columna = self.panel_proper.atributo.selected_option
                self.bloque.bloque.columna2 = self.panel_proper.atributo2.selected_option
                self.bloque.bloque.type_barra = 0 if self.panel_proper.criterio.selected_option == 'Conteo' else 1 
                self.panel_proper.kill()

            #### Análisis 
            if event.ui_object_id == '#proper_anauni.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.ejex = self.panel_proper.elementos.selected_option
                self.bloque.bloque.kind = self.panel_proper.graficos.selected_option
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_anabi.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.ejex = self.panel_proper.x_value.selected_option
                self.bloque.bloque.ejey = self.panel_proper.y_value.selected_option
                self.bloque.bloque.kind = self.panel_proper.grafico.selected_option
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_anamult.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.atributo = self.panel_proper.atributo.selected_option
                self.bloque.bloque.columnas = self.panel_proper.lista_columnas.get_multi_selection()
                self.panel_proper.kill()

            #### Transformación
            if event.ui_object_id == '#proper_operone.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.new_variable = self.panel_proper.new_name.text
                print('####')
                self.bloque.bloque.operation = self.panel_proper.operacion.selected_option
                self.bloque.bloque.selected_variable = self.panel_proper.variable.selected_option
                self.bloque.bloque.valor = self.panel_proper.valor.text
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_opertwo.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.new_variable = self.panel_proper.new_name.text
                self.bloque.bloque.operation = self.panel_proper.operacion.selected_option
                self.bloque.bloque.selected_variable = self.panel_proper.variable1.selected_option
                self.bloque.bloque.selected_variable2 = self.panel_proper.variable2.selected_option
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_filterone.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.selected_variable = self.panel_proper.variable.selected_option
                self.bloque.bloque.condicion = self.panel_proper.condicion_op.get_single_selection()
                self.bloque.bloque.tipo_cond = self.panel_proper.tipo_data.selected_option
                self.bloque.bloque.valor = self.panel_proper.valor.text                
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_filtertwo.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.selected_variable = self.panel_proper.variable1.selected_option
                self.bloque.bloque.tipo_cond = self.panel_proper.tipo_data1.selected_option
                self.bloque.bloque.condicion = self.panel_proper.condicion_op1.get_single_selection()
                self.bloque.bloque.valor = self.panel_proper.valor1.text 
                self.bloque.bloque.selected_variable2 = self.panel_proper.variable2.selected_option
                self.bloque.bloque.tipo_cond2 = self.panel_proper.tipo_data2.selected_option
                self.bloque.bloque.condicion2 = self.panel_proper.condicion_op2.get_single_selection()
                self.bloque.bloque.valor2 = self.panel_proper.valor2.text               
                self.bloque.bloque.operation = self.panel_proper.operacion.selected_option
                self.panel_proper.kill()
            if event.ui_object_id == '#proper_selectcols.#aceptar':
                self.bloque.status = False
                self.bloque.bloque.selected_variables = self.panel_proper.lista_columnas.get_multi_selection() 
                self.panel_proper.kill()
                        
            
            if event.ui_object_id == 'panel.#new':  # Crear nuevo módulo
                worker.num_modulos+=1
                modulo = Modulos(worker.num_modulos)
                worker.modulos.add(modulo)
                elementos = [modelo.name for modelo in worker.modulos]
                self.modelo.kill()
                self.modelo = UIDropDownMenu(elementos,
                                            elementos[worker.num_modulos-1],
                                            pygame.Rect((10, 10),
                                                        (210, 30)),
                                            self.manager,
                                            container=self.panel_modulos)

                self.selected_model = elementos[worker.num_modulos-1]
                                        
            if event.ui_object_id == 'panel.#del':  # Eliminar módulo
                [worker.modulos.remove(modulo) for modulo in worker.modulos if modulo.name == self.selected_model]
                
                self.modelo.kill()
                
                if not worker.modulos:
                    worker.num_modulos+=1
                    modulo = Modulos(worker.num_modulos)
                    worker.modulos.add(modulo)

                elementos = [modelo.name for modelo in worker.modulos]
                self.modelo = UIDropDownMenu(elementos,
                                            elementos[0],
                                            pygame.Rect((10, 10),
                                                        (210, 30)),
                                            self.manager,
                                            container=self.panel_modulos)

                self.selected_model = elementos[0]
            
            if event.ui_object_id == 'panel.#rename':  # Renombrar módulo
                pass
                
            for ind_x in range(1, 6):
                """Recorrer acciones"""
                if event.ui_object_id == 'panel.#p'+str(ind_x):
                    self.cancel(worker.modulos)
                    self.tareas[ind_x-1] = 1

            for ind_x in range(1, 5):
                """Recorrer edicion"""
                if event.ui_object_id == 'panel.#e'+str(ind_x):
                    self.cancel(worker.modulos)
                    self.editar[ind_x-1] = 1

            if event.ui_element == self.select and self.selected_action:  # Selecciona un objeto
                self.selected_block = True
                print(self.selected_action)
                self.datablock = DataBlock(position, self.selected_item, type=self.selected_action)
        
        # if event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
        #     self.path = create_resource_path(event.text)
        #     self.bloque.bloque.path = self.path

        if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.primer_menu:  # Elección primera acción                
                if event.text == self.items_choose[0]:
                    self.selected_type = self.items_choose[0]
                    self.reasign1(self.ing_datos)
                    self.selected_item = 'database'
                    self.selected_action = ''
                elif event.text == self.items_choose[1]:
                    self.selected_type = self.items_choose[1]
                    self.reasign1(self.explor_datos)
                    self.selected_item = 'describir'
                    self.selected_action = ''
                elif event.text == self.items_choose[2]:
                    self.selected_type = self.items_choose[2]
                    self.reasign1(self.limp_datos)
                    self.selected_item = 'limpiar'
                    self.selected_action = ''
                elif event.text == self.items_choose[3]:
                    self.selected_type = self.items_choose[3]
                    self.reasign1(self.anali_datos)
                    self.selected_item = 'analizar'
                    self.selected_action = ''
                elif event.text == self.items_choose[4]:
                    self.selected_type = self.items_choose[4]
                    self.reasign1(self.transf_data)
                    self.selected_item = 'transformar'
                    self.selected_action = ''
                elif event.text == self.items_choose[5]:
                    self.selected_type = self.items_choose[5]
                    self.reasign1(self.expor_datos)
                    self.selected_item = 'exportar'
                    self.selected_action = ''
            
            if event.ui_object_id == '#proper_anamult.#atributo':
                if event.text == 'Todas':
                    self.panel_proper.lista_columnas.disable()
                else:
                    self.panel_proper.lista_columnas.enable()

            if event.ui_object_id == '#proper_dropnan.#eje':
                if event.text == 'Fila':
                    self.panel_proper.lista_columnas.disable()
                else:
                    self.panel_proper.lista_columnas.enable()

            if event.ui_object_id == '#proper_filterone.#data':
                if event.text == 'Texto':
                    lista_str = ['Igual', 'Contiene', 'Empieza por', 'Termina en']
                    self.panel_proper.condicion_op.set_item_list(lista_str)
                else:
                    lista_oper = ['==', '!=', '>', '<', '>=', '<=']
                    self.panel_proper.condicion_op.set_item_list(lista_oper)
            
            if event.ui_object_id == '#proper_filtertwo.#data1':
                if event.text == 'Texto':
                    lista_str = ['Igual', 'Contiene', 'Empieza por', 'Termina en']
                    self.panel_proper.condicion_op1.set_item_list(lista_str)
                else:
                    lista_oper = ['==', '!=', '>', '<', '>=', '<=']
                    self.panel_proper.condicion_op1.set_item_list(lista_oper)
            
            if event.ui_object_id == '#proper_filtertwo.#data2':
                if event.text == 'Texto':
                    lista_str = ['Igual', 'Contiene', 'Empieza por', 'Termina en']
                    self.panel_proper.condicion_op2.set_item_list(lista_str)
                else:
                    lista_oper = ['==', '!=', '>', '<', '>=', '<=']
                    self.panel_proper.condicion_op2.set_item_list(lista_oper)


            if event.ui_element == self.modelo:
                self.selected_model = event.text

            if event.ui_object_id == '#proper_plotbar.#criterio_name': ## Criterio plot bar
                if self.panel_proper.criterio.selected_option == 'Conteo':
                    self.panel_proper.atributo2.disable()
                else:
                    self.panel_proper.atributo2.enable()

        if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.text:
                self.bloque.action = event.text
            else:
                size_alert = (300, 150)
                UIMessageWindow(pygame.Rect((self.window_size[0]/2-size_alert[0]/2, 
                                             self.window_size[1]/2-size_alert[1]/2), size_alert), html_message='hhola', window_title='fin', manager=self.manager)
                # self.alert_wi = AlertWindow('El nombre no puede estar vacio', pygame.Rect((self.window_size[0]/2-size_alert[0]/2,
                #                             self.window_size[1]/2-size_alert[1]/2), size_alert), self.manager)

        if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            self.selected_action = event.text            

    def draw_selected(self, screen, position):
        self.datablock.hot_draw(screen, position)

    def exec_actions(self, screen, position, worker):
        if self.del_line:
            pygame.mouse.set_visible(False)
            screen.blit(self.delete_line, position)
            for modulo in worker.modulos:
                for conexion in modulo.conections:
                    if self.delete_line.rect.collidepoint(conexion):
                        print('ola')


    def check_actions(self, position, worker):
        if self.tareas[2]:
            self.del_line = True
        if self.tareas[1]:
            self.hold_line = True            
        if self.tareas[0]:
            for modulo in worker.modulos:
                # if modulo.id == 1:
                for bloque in modulo.data_blocks:
                    if bloque.selected:
                        bloque.bloque.procesar()
                        if not bloque.bloque.error:
                            print('inp')
                            bloque.status = True
                        else:
                            print('op')
                            size_alert = (300, 150)
                            UIMessageWindow(pygame.Rect((self.window_size[0]/2-size_alert[0]/2, 
                                            self.window_size[1]/2-size_alert[1]/2), size_alert), html_message=bloque.bloque.msg, window_title='Error', manager=self.manager)
                        """if not bloque.in_elements:
                            lista_iniciales.append(bloque)   
                    modulo.dict_rutas['nivel1'] = lista_iniciales
                    modulo.build_rutas(lista_iniciales)     
                print(modulo.dict_rutas)  
                for ruta, mod in modulo.dict_rutas.items():
                    if mod:
                        for bloque in mod:
                            #print(bloque.bloque.procesar())
                            #print(ruta, bloque.action)    
                            #print(ruta, bloque.type)   
                            print('--')    """   
            self.tareas[0] = 0 
    def check_block(self, bloque, position, size=(400, 300)):
        """Acá entra si se hace click derecho"""
        print(bloque.id)
        self.bloque = bloque
        if bloque.action=='Fichero':
            self.panel_proper = propiedades.ProperLoad(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+130, size[1]-100)), self.manager, bloque)
        if bloque.action=='URL':
            self.panel_proper = propiedades.ProperURL(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+130, size[1]-100)), self.manager, bloque)
        if bloque.action=='Data toy':
            self.panel_proper = propiedades.ProperToy(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0], size[1]-100)), self.manager, bloque)
        

        if bloque.action==self.limp_datos[0]:
            self.panel_proper = propiedades.ProperDropnan(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0], size[1])), self.manager, bloque)            
        if bloque.action==self.limp_datos[2]:
            self.panel_proper = propiedades.ProperDelCol(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0], size[1])), self.manager, bloque)
        if bloque.action==self.limp_datos[4]:
            self.panel_proper = propiedades.ProperRenCol(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)
        if bloque.action=='Cambiar indice':
            self.panel_proper = propiedades.ProperSetIndex(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)
        if bloque.action=='Convertir a número':
            self.panel_proper = propiedades.ProperTurnNum(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)
        if bloque.action=='Convertir a categoría':
            self.panel_proper = propiedades.ProperTurnCat(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)                                                
        if bloque.action=='Reemplazar valor':
            self.panel_proper = propiedades.ReplaceValue(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)            
        if bloque.action==self.limp_datos[7]:
            self.panel_proper = propiedades.ProperTurnDate(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)
        if bloque.action==self.limp_datos[1]:
            self.panel_proper = propiedades.ReplaceNan(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)           
        if bloque.action=='Análisis bivariante':
            self.panel_proper = propiedades.ProperAnaBi(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)                                                            
        if bloque.action==self.explor_datos[4]:
            self.panel_proper = propiedades.ProperPlotBar(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)                
        if bloque.action==self.explor_datos[2]:
            self.panel_proper = propiedades.ProperTabDin(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)
        if bloque.action==self.explor_datos[4]:
            #self.panel_proper = propiedades.ProperDataType(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)
            pass
        if bloque.action=='Elementos únicos':
            self.panel_proper = propiedades.ProperUnique(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)

        ### Análisis
        if bloque.action=='Análisis univariante':
            self.panel_proper = propiedades.ProperAnaUni(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]-70, size[1]-50)), self.manager, bloque)
        if bloque.action=='Análisis multivariante':
            self.panel_proper = propiedades.ProperAnaMult(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]-60, size[1]-20)), self.manager, bloque)

        ### Transformar
        if bloque.action=='Unir':
            self.panel_proper = propiedades.ProperJoin(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)
        if bloque.action=='Operar una columna':
            self.panel_proper = propiedades.ProperOperateOne(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)
        if bloque.action=='Operar dos columnas':
            self.panel_proper = propiedades.ProperOperateTwo(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)
        if bloque.action=='Filtrar una columna':
            self.panel_proper = propiedades.ProperFilterOne(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)
        if bloque.action=='Filtrar dos columnas':
            self.panel_proper = propiedades.ProperFilterTwo(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+150, size[1]+70)), self.manager, bloque)
        if bloque.action=='Seleccionar columnas':
            self.panel_proper = propiedades.ProperSelectColumns(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0]+50, size[1])), self.manager, bloque)

        if bloque.action=='CSV':
            self.panel_proper = propiedades.ProperSave(pygame.Rect((position[0]/2-size[0]/2, position[1]/2-size[1]/2), (size[0], size[1]-100)), self.manager, bloque)
    
    def draw_wire(self, screen, init_pos, end_line):
        pygame.draw.aaline(screen, BLACK, init_pos, end_line)
        
    def run_pipeline(self):
        self.routes()
        
    def cancel(self, modulos):
        # for modulo in modulos:
        #         for bloque in modulo.data_blocks:
        #             bloque.selected = False
        self.selected_block = False
        self.tareas = [0]*5

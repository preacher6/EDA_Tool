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

LIGHTGRAY = (192, 192, 192)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)


class DataBlock(pygame.sprite.Sprite):
    """Maneja cada bloque"""
    def __init__(self, position, name, id='', status=False, type=None):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.name = name  # Indica el nombre del icono
        self.id = id
        self.status = status
        self.type = type
        self.dir_images = {'database': 'pics/icons/database.png',
                            'describir': 'pics/icons/describir.png',
                            'limpiar': 'pics/icons/limpiar.png',
                            'analizar': 'pics/icons/analizar.png',
                            'transformar': 'pics/icons/transformar.png',
                            'exportar': 'pics/icons/exportar.png'}
        self.image = pygame.image.load(os.path.join('pics', 'images', 'block.png'))
        self.path_status = {'on': 'pics/images/on.png',
                            'off': 'pics/images/off.png',
                            'bad': 'pics/images/bad.png'}
        self.image_status = pygame.image.load(os.path.join(self.path_status['off']))        
        self.agregar = pygame.image.load(os.path.join('pics/icons/agregar.png'))
        self.quitar = pygame.image.load(os.path.join('pics/icons/quitar.png'))
        self.botones = []
        self.selected = False  # Indica si el elemento esta seleccionado
        self.image_nodo = pygame.image.load(os.path.join('pics', 'images', 'nodo.png'))
        self.rect_nodo = self.image_nodo.get_rect()
        self.nodos = pygame.sprite.Group()
        self.rect_image()
        self.definir_nodos()   

    def definir_nodos(self):
        if self.type != 'Ingesta':
            self.nodos.add(Nodo((self.rect.x-self.rect_nodo.width/2, self.rect.y+15)))
        if self.type != 'Exportar':
            self.nodos.add(Nodo((self.rect.x+self.rect.width+self.rect_nodo.width/2, self.rect.y+15)))

    def rect_botones(self):        
        self.botones = []        
        if self.type == 'Ingesta':
            posiciones = [(46, 3)]
        else:
            posiciones = [(5, 3), (46, 3)]
        lista = ['poner1', 'poner2']
        for poner, pos in zip(lista, posiciones):
            rect_agregar = self.agregar.get_rect()
            rect_agregar.x = self.rect.x+pos[0]
            rect_agregar.y = self.rect.y+pos[1]
            self.botones.append([poner, rect_agregar])
            self.image.blit(self.agregar, pos)

        if self.type == 'Ingesta':
            posiciones = [(46, 17)]
        else:
            posiciones = [(5, 17), (46, 17)]
        lista = ['quitar1', 'quitar2']
        for quitar, pos in zip(lista, posiciones):
            rect_quitar = self.agregar.get_rect()
            rect_quitar.x = self.rect.x+pos[0]
            rect_quitar.y = self.rect.y+pos[1]
            self.botones.append([quitar, rect_quitar])
            self.image.blit(self.quitar, pos)   
        
    def rect_image(self):
        self.icon = pygame.image.load(self.dir_images[self.name])
        self.rect_icon = self.icon.get_rect()
        self.rect_status = self.image_status.get_rect()
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def draw(self, screen):        
        self.image = pygame.image.load(os.path.join('pics', 'images', 'block.png'))
        if self.status:
            self.image_status = pygame.image.load(os.path.join(self.path_status['on']))
        else:
            self.image_status = pygame.image.load(os.path.join(self.path_status['off']))
        self.rect_image()
        self.rect_botones()
        
        #self.image.blit(self.quitar, (5, 17))
        self.image.blit(self.image_status, (27, 10))
        self.image.blit(self.icon, (18, 53))        
        screen.blit(self.image, self.rect)
        for nodo in self.nodos:
            nodo.draw(screen)

    def hot_draw(self, screen, position):
        """Dibujar el bloque en caliente"""
        self.image = pygame.image.load(os.path.join('pics', 'images', 'block.png'))
        self.hot_rect_image(position)
        self.image.blit(self.icon, (18, 50))
        screen.blit(self.image, self.rect)

    def hot_rect_image(self, position):
        self.icon = pygame.image.load(self.dir_images[self.name])
        self.rect_icon = self.icon.get_rect()
        self.rect = self.image.get_rect()
        self.rect.center = position

class Nodo(pygame.sprite.Sprite):
    """Maneja cada modulo que se crea como una entidad independiente"""
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('pics', 'images', 'nodo_off.png'))
        self.rect = self.image.get_rect()
        self.rect.center = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Conexion(pygame.sprite.Sprite):
    def __init__(self, puntos, elem1, elem2):
        pygame.sprite.Sprite.__init__(self)
        self.puntos = puntos
        print(self.puntos)
        self.elem1 = elem1
        self.elem2 = elem2  # Este elemento es una etiqueta si pertenece a las conexiones de propiedades, y es un numero si pertence a un elemento
        self.puntos_internos = self.build_rect_points(puntos)
    
    def build_rect_points(self, puntos, num_points=20):  # Funcion recta. Construye los puntos de la recta para cada linea de una conexion
        x1, y1 = puntos[0]
        x2, y2 = puntos[1]
        x_spacing = (x2-x1)/(num_points+1)
        y_spacing = (y2 - y1) / (num_points + 1)
        return [[x1+i*x_spacing, y1+i*y_spacing] for i in range(1, num_points+1)]
    
    def draw(self, screen):
        pygame.draw.aaline(screen, BLACK, self.puntos[0], self.puntos[1])

class Modulos(pygame.sprite.Sprite):
    """Maneja cada modulo que se crea como una entidad independiente"""
    def __init__(self, identidad):
        pygame.sprite.Sprite.__init__(self)
        self.data_blocks = pygame.sprite.Group()
        self.conections = pygame.sprite.Group()  # Guarda las conexiones del contenedor
        self.id = identidad


class MainWorker(pygame.sprite.Sprite):
    """Maneja todo lo relacionado al accionar de los objetos"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.modulos = pygame.sprite.Group()

    def draw_all(self, screen, position):
        for modulo in self.modulos:
            for data in modulo.data_blocks:
                data.draw(screen)
                for boton in data.botones:
                    if boton[1].collidepoint(position):
                        print('in')
            for conexion in modulo.conections:
                conexion.draw(screen)

    def add_nodo(self, screen, position, modulo):
        for bloque in modulo.data_blocks:
            for boton in bloque.botones:
                pass

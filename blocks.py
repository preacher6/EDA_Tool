import pandas as pd

class OwnPipeline():
    def __init__(self):
        self.grupo_ingesta = {}
    
    def add_ingesta(self, name):
        self.grupo_ingesta[name] = Ingesta()
    
class Ingesta:
    def __init__(self, action) -> None:
        self.items = ['Fichero', 'SQL', 'URL', 'Data toy', 'Carpeta']
        self.action = action
        self.data = ''
        self.path = ''

    def define_data(self, path):
        self.path = path
        
    def procesar(self):
        if self.action == self.items[0]:
            self.data = pd.read_csv(self.path)
            print(self.data.head())
    

class Limpieza:
    def __init__(self, action) -> None:
        self.items = ['Eliminar Nan', 'Reemplazar Nan', 'Eliminar columnas', 'Eliminar filas',
                    'Renombrar columnas', 'Reemplazar valores', 'Cambiar indices']
        self.action = action
        self.data = ''
        self.path = ''
    
    def procesar(self):
        if self.action == self.items[0]:
            pass
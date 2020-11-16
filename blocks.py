import pandas as pd

class OwnPipeline():
    def __init__(self):
        self.grupo_ingesta = {}
    
    def add_ingesta(self, name):
        self.grupo_ingesta[name] = Ingesta()
    
class Ingesta:
    def __init__(self) -> None:
        self.data = ''
        self.path = ''
    
    def define_data(self, path):
        self.path = path
        
    def cargar_datos(self):
        self.data = pd.read_csv(self.path)
        print(self.data.head())
    
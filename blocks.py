import pandas as pd

class OwnPipeline():
    def __init__(self):
        self.grupo_ingesta = {}
    
    def add_ingesta(self, name):
        self.grupo_ingesta[name] = Ingesta()
    
class Ingesta:
    def __init__(self) -> None:
        self.data = ''
    
    def cargar_datos(self, archivo):
        self.data = pd.read_csv(archivo)
    
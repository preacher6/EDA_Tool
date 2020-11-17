import pandas as pd
import build_table


class OwnPipeline():
    def __init__(self):
        self.grupo_ingesta = {}
    
    def add_ingesta(self, name):
        self.grupo_ingesta[name] = Ingesta()


class Ingesta:
    def __init__(self, action) -> None:
        self.items = ['Fichero', 'SQL', 'URL', 'Data toy', 'Carpeta']
        self.action = action
        self.data = pd.DataFrame()
        self.path = ''

    def define_data(self, path):
        self.path = path
        
    def procesar(self, **kwargs):
        if self.action == self.items[0]:
            self.data = pd.read_csv(self.path)
            #print(self.data.head())
    

class Limpieza:
    def __init__(self, action) -> None:
        self.items = ['Eliminar Nan', 'Reemplazar Nan', 'Eliminar columnas', 'Eliminar filas',
                    'Renombrar columnas', 'Reemplazar valores', 'Cambiar indices']
        self.action = action
        self.selected_columns = []
        self.own_dicto = {}
        self.axis=1
        self.how='any'
        self.thresh=None
        self.subset=None
        self.asign_names={}
    
    def cargar_data(self, data):
        self.data = data
        print(self.data.head())
        print('----')
    
    def new_names(self, nuevos, viejos):
        self.asign_names = dict(zip(viejos, nuevos.split(',')))
        print(self.asign_names)
        
        
    def procesar(self, **kwargs):
        if self.action == self.items[0]:
            self.data = self.data.dropna(how=self.how, axis=self.axis, thresh=self.thresh, subset=None)
            print(self.data.head())
            print(self.data.shape)
        if self.action == self.items[2]:
            self.data = self.data.drop(self.selected_columns, axis=self.axis)
            print(self.data.head())
            print(self.data.shape)
        if self.action == self.items[4]:
            self.data.rename(columns=self.asign_names, inplace=True)
            print(self.data.head())
            
class Explorar:
    def __init__(self) -> None:
        pass
    
    def cargar_data(self, data):
        self.data = data
    
    def procesar(self):
        app = build_table.MyApp(self.data)
        app.mainloop()
import pandas as pd
import build_table
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class OwnPipeline():
    def __init__(self):
        self.grupo_ingesta = {}
    
    def add_ingesta(self, name):
        self.grupo_ingesta[name] = Ingesta()
        x = 5


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
                            'Renombrar columnas', 'Reemplazar valores', 'Cambiar indices',
                            'Convertir a fecha', 'Convertir a número']
        self.action = action
        self.selected_columns = []
        self.own_dicto = {}
        self.axis=1
        self.how='any'
        self.thresh=None
        self.subset=None
        self.asign_names={}
        self.elementos_fecha = []
    
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
        if self.action == self.items[7]:
            print(self.elementos_fecha[0])
            print(self.data[self.elementos_fecha[0]])
            self.data = self.data[self.data[self.elementos_fecha[0]].str[0:2] != 'Or']
            self.data[self.elementos_fecha[0]] = pd.to_datetime(self.data[self.elementos_fecha[0]])
            print(self.data.head())


class Explorar:
    def __init__(self, action) -> None:
        self.data = pd.DataFrame()
        self.action = action
        self.items = ['Tabla', 'Descripción', 'Tipos de datos', 'Diagrama de barras', 'Cabecera', 'Cola']
        self.index_barra = None
        self.type_barra = None
        self.columna = None
        self.valor = None
    
    def cargar_data(self, data):
        self.data = data
    
    def procesar(self):
        if self.action == self.items[0]:
            app = build_table.MyApp(self.data)
            app.mainloop()
        if self.action == self.items[1]:
            app = build_table.MyApp(self.data.describe())
            app.mainloop()
        if self.action == self.items[3]:
            print(self.data.dtypes)
            print(type(print(self.data.dtypes)))
            print(pd.DataFrame(self.data.dtypes))
            data = pd.DataFrame(self.data.dtypes).rename(columns={0:'Tipo'})
            app = build_table.MyApp(data)
            app.mainloop()
        if self.action == self.items[4]:  # Diagrama de barras
            print(self.type_barra)
            sns.set_theme()
            new_df = self.data.copy()
            if self.type_barra==0:
                new_df = new_df.groupby(self.index_barra).count()
            elif self.type_barra==1:
                new_df = new_df.groupby(self.index_barra).sum()
            else:
                new_df = new_df.groupby(self.index_barra).mean()
            new_df.plot(kind='bar')
            plt.show()
        if self.action == 'Tabla dinámica':
            new_df = self.data.pivot_table(values=self.valor, index=self.index_barra,
                                           columns=self.columna, aggfunc=[np.sum, np.mean]).stack()
            print(new_df)
            app = build_table.MyApp(new_df)
            app.mainloop()
            
class Analisis:
    def __init__(self, action) -> None:
        self.items = ['Univariante', 'Multivariante', 'Correlación']
        self.data = pd.DataFrame()
        self.action = action
        self.ejex = None
        self.ejey = None
        self.kind = 'plot'
    
    def cargar_data(self, data):
        self.data = data
        print(self.data.head())
        print('----')
    
    def procesar(self):
        if self.action == self.items[0]:
            self.data = self.data[self.data['Order Date'].str[0:2] != 'Or']
            sns.set_theme()
            plt.plot(pd.to_numeric(self.data[self.ejex]), pd.to_numeric(self.data[self.ejey]))
            plt.show()

class Exportar:
    def __init__(self, action):
        self.items = ['Univariante', 'Multivariante', 'Correlación']
        self.data = pd.DataFrame()
        self.action = action
        self.path = ''
        self.nombre = ''
    
    def cargar_data(self, data):
        self.data = data
        print(self.data.head())
        print('----')
        
    def procesar(self):
        if self.action == self.items[0]:
            self.data.to_csv(self.nombre, index=False)
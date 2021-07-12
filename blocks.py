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
        self.id = 'Ingesta'
        self.items = ['Fichero', 'SQL', 'URL', 'Data toy', 'Carpeta']
        self.action = action
        self.data = pd.DataFrame()
        self.path = ''
        self.error = False
        self.msg = ''

    def define_data(self, path):
        self.path = path
        
    def procesar(self, **kwargs):
        if self.action == self.items[0]:
            try:
                self.data = pd.read_csv(self.path)
                print(self.data)
            except:
                self.error = True
                self.msg = 'El archivo no existe o es inválido'

class Limpieza:
    def __init__(self, action) -> None:
        self.id = 'Limpieza'
        self.data = pd.DataFrame()
        self.items = ['Eliminar Nan', 'Reemplazar Nan', 'Eliminar columnas', 'Eliminar filas',
                            'Renombrar columnas', 'Reemplazar valores', 'Cambiar indice',
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
        self.value = None
        self.index = None
        self.old_value = None  # Valor a reemplazar
        self.error = False
    
    def cargar_data(self, data):
        self.data = data
        print(self.data.head())
        print('----')
    
    def new_names(self, nuevos, viejos):
        self.asign_names = dict(zip(viejos, nuevos.split(',')))
        print(self.asign_names)        
        
    def procesar(self, **kwargs):
        if self.action == 'Eliminar Nan':
            self.data = self.data.dropna(how=self.how, axis=self.axis, thresh=self.thresh, subset=None)
            print(self.data.head())
            print(self.data.shape)
        if self.action == 'Eliminar columnas':
            self.data = self.data.drop(self.selected_columns, axis=self.axis)
            print(self.data.head())
            print(self.data.shape)
        if self.action == 'Renombrar columnas':
            self.data.rename(columns=self.asign_names, inplace=True)
            print(self.data.head())
        if self.action == 'Reemplazar Nan':
            print(self.value)
            self.data[self.selected_columns] = self.data[self.selected_columns].fillna(float(self.value))
        if self.action == 'Cambiar indice':
            self.data.set_index(self.index, inplace=True)
        if self.action == 'Convertir a fecha':
            print(self.elementos_fecha[0])
            print(self.data[self.elementos_fecha[0]])
            self.data = self.data[self.data[self.elementos_fecha[0]].str[0:2] != 'Or']
            self.data[self.elementos_fecha[0]] = pd.to_datetime(self.data[self.elementos_fecha[0]])
            print(self.data.head())
        if self.action == 'Convertir a número':
            self.data[self.selected_columns] = self.data[self.selected_columns].apply(pd.to_numeric)
        if self.action == 'Convertir a categoría':
            print(self.data[self.selected_columns].unique())
            self.data[self.selected_columns] = pd.Categorical(self.data[self.selected_columns])
            self.data[self.selected_columns] = self.data[self.selected_columns].cat.as_ordered()
            print(self.data[self.selected_columns].unique())
        if self.action == 'Reemplazar valor':
            try:
                float(self.old_value)
                self.old_value = float(self.old_value)
            except ValueError:
                pass
            try:
                float(self.value)
                self.value = float(self.value)
            except ValueError:
                pass

            self.data[self.selected_columns].replace(self.old_value, self.value)


class Explorar:
    def __init__(self, action) -> None:
        self.id = 'Explorar'
        self.data = pd.DataFrame()
        self.action = action
        self.items = ['Tabla', 'Descripción', 'Tabla dinámica', 'Tipos de datos', 'Diagrama de barras', 'Cabecera', 'Cola']
        self.index_barra = None
        self.type_barra = None
        self.columna = None
        self.valor = None
        self.agg = None
        self.selected_column = None
        self.error = False
    
    def cargar_data(self, data):
        self.data = data
    
    def procesar(self):
        if self.action == self.items[0]:  # Tabla completa
            app = build_table.MyApp(self.data)
            app.mainloop()
        if self.action == self.items[1]: # Descripción
            app = build_table.MyApp(self.data.describe())
            app.mainloop()
        if self.action == 'Tipos de datos':
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
            lista_agg = []
            if 'Media' in self.agg:
                lista_agg.append(np.mean)
            if 'Contar' in self.agg:
                lista_agg.append("count")
            if 'Sumar' in self.agg:
                lista_agg.append(np.sum)
            print(self.agg)
            new_df = self.data.pivot_table(values=self.valor, index=self.index_barra,
                                           columns=self.columna, aggfunc=lista_agg).stack()
            print(new_df)
            app = build_table.MyApp(new_df)
            app.mainloop()
        if self.action == 'Cabecera':
            app = build_table.MyApp(self.data.head())
            app.mainloop()
        if self.action == 'Cola':
            app = build_table.MyApp(self.data.tail())
            app.mainloop()
        if self.action == 'Elementos únicos':
            print(self.data[self.selected_column].unique())
            app = build_table.MyApp(pd.DataFrame(self.data[self.selected_column].unique()))
            app.mainloop()
            
class Analisis:
    def __init__(self, action) -> None:
        self.id = 'Analisis'
        self.items = ['Análisis univariante', 'Análisis bivariante',
                        'Análisis multivariante', 'Correlación']
        self.data = pd.DataFrame()
        self.action = action
        self.ejex = None
        self.ejey = None
        self.kind = 'plot'
        self.atributo = None
        self.columnas = []
        self.error = False
    
    def cargar_data(self, data):
        self.data = data
        print(self.data.head())
        print('----')
    
    def procesar(self):
        if self.action == 'Análisis univariante':
            #self.data = self.data[self.data['Order Date'].str[0:2] != 'Or']
            sns.set_theme()
            if self.kind == 'Distribución':
                sns.displot(data=self.data, x=self.ejex)
            elif self.kind == 'Caja':
                sns.boxplot(data=self.data, x=self.ejex)
            elif self.kind == 'Conteo':
                sns.countplot(data=self.data, x=self.ejex)

            #plt.plot(pd.to_numeric(self.data[self.ejex]), pd.to_numeric(self.data[self.ejey]))
            plt.show()
        if self.action == 'Análisis bivariante':
            sns.set_theme()
            if self.kind == 'Relación':
                sns.jointplot(x=self.ejex, y=self.ejey, data=self.data)
            elif self.kind == 'Regresión':
                sns.lmplot(x=self.ejex, y=self.ejey, data=self.data)
            elif self.kind == 'Conteo':
                sns.countplot(x=self.ejex, hue=self.ejey, data=self.data)
            
            plt.show()

        if self.action == 'Análisis multivariante':
            if self.atributo == 'Todas':
                sns.pairplot(self.data)
            else:
                sns.pairplot(self.data[self.columnas])
            
            plt.show()


class Transformacion:
    def __init__(self):
        self.data = pd.DataFrame()
        self.data2 = pd.DataFrame()
        self.id = 'Transformacion'
        self.error = False

    def cargar_data(self, data):
        self.data = data
        print(self.data.head())
        print('----')

    def procesar(self):
        if self.action == 'Unir':
            pass

class Exportar:
    def __init__(self, action):
        self.items = ['Univariante', 'Multivariante', 'Correlación']
        self.data = pd.DataFrame()
        self.action = action
        self.path = ''
        self.nombre = ''
        self.error = False
    
    def cargar_data(self, data):
        self.data = data
        print(self.data.head())
        print('----')
        
    def procesar(self):
        if self.action == self.items[0]:
            self.data.to_csv(self.nombre, index=False)
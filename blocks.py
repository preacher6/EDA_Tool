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
        self.sep = ','

    def define_data(self, path):
        print(path)
        self.path = path

    def define_path(self, option_path):
        if option_path == 'Titanic':
            self.path = 'D:\proyectos_git\Auto_EDA\EDA_Tool\data\titanic.csv'
        elif option_path == 'Flores':
            self.path = ''
        
    def procesar(self, **kwargs):
        if self.action == self.items[0] or self.action == self.items[2]:
            try:
                print(self.sep)
                self.data = pd.read_csv(self.path, sep=self.sep)
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
        self.selected_columns = None
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
    
    def new_names(self, nuevos, viejos):
        self.asign_names = dict(zip(viejos, nuevos.split(',')))
        
    def procesar(self, **kwargs):
        if self.action == 'Eliminar Nan':
            if self.axis == 2:
                self.data = self.data.dropna(how=self.how, axis=0, thresh=self.thresh, subset=self.selected_columns)
            else:
                self.data = self.data.dropna(how=self.how, axis=self.axis, thresh=self.thresh)
        if self.action == 'Eliminar columnas':
            self.data = self.data.drop(self.selected_columns, axis=self.axis)
        if self.action == 'Renombrar columnas':
            self.data.rename(columns=self.asign_names, inplace=True)
        if self.action == 'Reemplazar Nan':
            self.data[self.selected_columns] = self.data[self.selected_columns].fillna(float(self.value))
        if self.action == 'Cambiar indice':
            self.data.set_index(self.index, inplace=True)
        if self.action == 'Convertir a fecha':
            self.data = self.data[self.data[self.elementos_fecha[0]].str[0:2] != 'Or']
            self.data[self.elementos_fecha[0]] = pd.to_datetime(self.data[self.elementos_fecha[0]])
            
        if self.action == 'Convertir a número':
            self.data[self.selected_columns] = self.data[self.selected_columns].apply(pd.to_numeric)
        if self.action == 'Convertir a categoría':
            
            self.data[self.selected_columns] = pd.Categorical(self.data[self.selected_columns])
            self.data[self.selected_columns] = self.data[self.selected_columns].cat.as_ordered()
            
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
        self.columna2 = None
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
            data = pd.DataFrame(self.data.dtypes).rename(columns={0:'Tipo'})
            app = build_table.MyApp(data)
            app.mainloop()
        if self.action == self.items[4]:  # Diagrama de barras
            sns.set_theme()
            new_df = self.data.copy()
            if self.type_barra==0:
                new_serie = new_df[self.columna].value_counts()
            elif self.type_barra==1:
                new_serie =  pd.crosstab(new_df[self.columna], new_df[self.columna2])
            new_serie.plot(kind='bar')
            plt.show()
        if self.action == 'Tabla dinámica':
            lista_agg = []
            if 'Media' in self.agg:
                lista_agg.append(np.mean)
            if 'Contar' in self.agg:
                lista_agg.append("count")
            if 'Sumar' in self.agg:
                lista_agg.append(np.sum)
            new_df = self.data.pivot_table(values=self.valor, columns=self.columna,
                                            aggfunc=lista_agg).stack()
            app = build_table.MyApp(new_df)
            app.mainloop()
        if self.action == 'Cabecera':
            app = build_table.MyApp(self.data.head())
            app.mainloop()
        if self.action == 'Cola':
            app = build_table.MyApp(self.data.tail())
            app.mainloop()
        if self.action == 'Elementos únicos':
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
    def __init__(self, action):
        self.data = pd.DataFrame()
        self.data2 = pd.DataFrame()
        self.id = 'Transformacion'
        self.error = False
        self.action = action
        self.new_variable = ''
        self.selected_variable = ''
        self.selected_variable2 = ''
        self.operation = None
        self.valor = None
        self.valor2= None
        self.condicion = None
        self.condicion2 = None
        self.tipo_cond = None
        self.tipo_cond2 = None
        self.selected_variables = []

    def cargar_data(self, data):
        self.data = data
        
    def cargar_data2(self, data2):
        self.data2 = data2

    def procesar(self):
        if self.action == 'Unir':
            pass
        if self.action == 'Operar dos columnas':
            if self.operation == 'Sumar':
                funco = lambda x: x[0] + x[1]
            elif self.operation == 'Restar':
                funco = lambda x: x[0] - x[1]
            elif self.operation == 'Multiplicar':
                funco = lambda x: x[0] * x[1]
            elif self.operation == 'Dividir':
                funco = lambda x: x[0] / x[1]
            self.data[self.new_variable] = self.data[[self.selected_variable, self.selected_variable2]].apply(funco, axis=1)

        if self.action == 'Operar una columna':
            self.valor = float(self.valor)
            if self.operation == 'Sumar':
                funco = lambda x: x + self.valor
            elif self.operation == 'Restar':
                funco = lambda x: x - self.valor
            elif self.operation == 'Multiplicar':
                funco = lambda x: x * self.valor
            elif self.operation == 'Dividir':
                funco = lambda x: x / self.valor
            elif self.operation == 'Elevar':
                funco = lambda x: x ** self.valor
            self.data[self.new_variable] = self.data[self.selected_variable].apply(funco)

        if self.action == 'Filtrar una columna':
            if self.tipo_cond == 'Numérico':
                self.valor = float(self.valor)
                if self.condicion == '==':
                    self.data = self.data[self.data[self.selected_variable] == self.valor]
                if self.condicion == '!=':
                    self.data = self.data[self.data[self.selected_variable] != self.valor]
                if self.condicion == '>':
                    self.data = self.data[self.data[self.selected_variable] > self.valor]
                if self.condicion == '<':
                    self.data = self.data[self.data[self.selected_variable] < self.valor]
                if self.condicion == '>=':
                    self.data = self.data[self.data[self.selected_variable] >= self.valor]
                if self.condicion == '<=':
                    self.data = self.data[self.data[self.selected_variable] <= self.valor]
            else:
                if self.condicion == 'Igual':
                    self.data = self.data[self.data[self.selected_variable] == self.valor]
                if self.condicion == 'Empieza por':
                    self.data = self.data[self.data[self.selected_variable].astype(str).str.startswith(self.valor)]
                if self.condicion == 'Termina en':
                    self.data = self.data[self.data[self.selected_variable].astype(str).str.endswith(self.valor)]
                if self.condicion == 'Contiene':
                    self.data = self.data[self.data[self.selected_variable].astype(str).str.contains(self.valor)]
        if self.action == 'Seleccionar columnas':
            self.data = self.data[self.selected_variables]

        if self.action == 'Filtrar dos columnas':
            if self.tipo_cond == 'Numérico':
                self.valor = float(self.valor)
                if self.condicion == '==':
                    cond1 = self.data[self.selected_variable] == self.valor
                if self.condicion == '!=':
                    cond1 = self.data[self.selected_variable] != self.valor
                if self.condicion == '>':
                    cond1 = self.data[self.selected_variable] > self.valor
                if self.condicion == '<':
                    cond1 = self.data[self.selected_variable] < self.valor
                if self.condicion == '>=':
                    cond1 = self.data[self.selected_variable] >= self.valor
                if self.condicion == '<=':
                    cond1 = self.data[self.selected_variable] <= self.valor
            else:
                if self.condicion == 'Igual':
                    cond1 = self.data[self.selected_variable] == self.valor
                if self.condicion == 'Empieza por':
                    cond1 = self.data[self.selected_variable].astype(str).str.startswith(self.valor)
                if self.condicion == 'Termina en':
                    cond1 = self.data[self.selected_variable].astype(str).str.endswith(self.valor)
                if self.condicion == 'Contiene':
                    cond1 = self.data[self.selected_variable].astype(str).str.contains(self.valor)

            if self.tipo_cond2 == 'Numérico':
                self.valor2 = float(self.valor2)
                if self.condicion2 == '==':
                    cond2 = self.data[self.selected_variable2] == self.valor2
                if self.condicion2 == '!=':
                    cond2 = self.data[self.selected_variable2] != self.valor2
                if self.condicion2 == '>':
                    cond2 = self.data[self.selected_variable2] > self.valor2
                if self.condicion2 == '<':
                    cond2 = self.data[self.selected_variable2] < self.valor2
                if self.condicion2 == '>=':
                    cond2 = self.data[self.selected_variable2] >= self.valor2
                if self.condicion2 == '<=':
                    cond2 = self.data[self.selected_variable2] <= self.valor2
            else:
                if self.condicion2 == 'Igual':
                    cond2 = self.data[self.selected_variable2] == self.valor2
                if self.condicion2 == 'Empieza por':
                    cond2 = self.data[self.selected_variable2].astype(str).str.startswith(self.valor2)
                if self.condicion2 == 'Termina en':
                    cond2 = self.data[self.selected_variable2].astype(str).str.endswith(self.valor2)
                if self.condicion2 == 'Contiene':
                    cond2 = self.data[self.selected_variable2].astype(str).str.contains(self.valor2)

            if self.operation == 'AND':
                self.data = self.data[cond1 & cond2]
            else:
                self.data = self.data[cond1 | cond2]

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
        
    def procesar(self):
        if self.action == self.items[0]:
            self.data.to_csv(self.nombre, index=False)
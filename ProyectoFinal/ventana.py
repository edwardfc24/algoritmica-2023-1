import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pandastable import Table, TableModel

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np


class Ventana():
    def __init__(self):
        self.frame = None
        self.frame_tabla = None
        self.frame_buttons = None
        self.frame_predict = None
        self.tabla = None

        self.columnas_entrenamiento = []
        self.columna_objetivo = None

        self.df = None
        self.df_limpio = None
        self.labels = {}
        self.modelo = None
        self.score = None
        self.entry = None

    def cargar_ventana(self):
        root = tk.Tk()
        root.title('Proyecto final - Algoritmica avanzada')

        self.frame = tk.Frame(root)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.pack()

        self.frame_predict = tk.Frame(self.frame)
        self.frame_buttons = tk.Frame(self.frame)
        self.frame_buttons.grid(padx=5, pady=5, row=0, column=0)
        self.frame_buttons.grid_rowconfigure(0, weight=1)
        self.frame_buttons.grid_rowconfigure(1, weight=1)
        self.frame_buttons.grid_rowconfigure(2, weight=1)
        self.frame_buttons.grid_rowconfigure(3, weight=1)
        self.frame_buttons.grid_rowconfigure(4, weight=1)
        self.frame_buttons.grid_rowconfigure(5, weight=1)
        self.frame_buttons.grid_columnconfigure(0, weight=1)

        self.frame_tabla = tk.Frame(self.frame)
        self.frame_tabla.grid(padx=5, pady=5, row=0, column=1)

        table_model = TableModel(dataframe=pd.DataFrame())
        self.tabla = Table(self.frame_tabla, model=table_model,
                           editable=False, enable_menus=False)
        self.tabla.show()

        btn_cargar = tk.Button(
            self.frame_buttons, text="Cargar archivo", width=30, command=self.cargar_archivo)
        btn_cargar.grid(padx=10, pady=10, row=0, column=0)

        btn_guardar_col_train = tk.Button(
            self.frame_buttons, text="Seleccionar columna de entrenamiento", width=30, command=self.guardar_columnas_entrenamiento)
        btn_guardar_col_train.grid(padx=10, pady=10, row=1, column=0)

        btn_guardar_col_objetivo = tk.Button(
            self.frame_buttons, text="Seleccionar columna objetivo", width=30, command=self.guardar_columna_objetivo)
        btn_guardar_col_objetivo.grid(padx=10, pady=10,  row=2, column=0)

        btn_eliminar_seleccion = tk.Button(
            self.frame_buttons, text="Eliminar columna seleccionada", width=30, command=self.eliminar_columna_seleccionada)
        btn_eliminar_seleccion.grid(padx=10, pady=10, row=3, column=0)

        self.combobox = ttk.Combobox(
            self.frame_buttons, width=30, state='readonly')
        self.combobox['values'] = self.cargar_modelos()
        self.combobox.current(0)
        self.combobox.grid(padx=10, pady=10, row=4, column=0)

        btn_usar = tk.Button(
            self.frame_buttons, text="Usar modelo", width=30, command=self.entrenar)
        btn_usar.grid(padx=10, pady=10, row=5, column=0)

        root.mainloop()

    def cargar_modelos(self):
        self.modelos_predictivos = {
            'Regresión lineal - (Predictivo)': linear_model.LinearRegression(),
            'Ridge - (Predictivo)': linear_model.Ridge(alpha=.5),
            'Lasso - (Predictivo)': linear_model.Lasso(alpha=0.1),
        }
        self.modelos_clasificatorios = {
            'Arbol de decisión - (Clasificatorio)': DecisionTreeClassifier(),
            'Vecinos más cercanos - (Clasificatorio)': KNeighborsClassifier(),
            'Bosque aleatorio - (Clasificatorio)': RandomForestClassifier(),
        }

        lista_predictivos = list(self.modelos_predictivos.keys())
        lista_clasificatorios = list(self.modelos_clasificatorios.keys())
        return lista_predictivos + lista_clasificatorios

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(
            filetypes=[("Archivos CSV", "*.csv")])
        if archivo:
            self.columnas_entrenamiento = []
            self.columna_objetivo = None
            self.df = pd.read_csv(archivo)
            self.limpiar_datos()
            self.mostrar_datos(self.df)

    def limpiar_datos(self):
        self.df_limpio = self.df.copy()
        columnas = self.df.columns
        columnas_eliminadas = []

        for columna in columnas:
            if self.df[columna].dtype == "object" and self.df[columna].isnull().values.any():
                self.df.drop(columna, axis=1, inplace=True)
                self.df_limpio.drop(columna, axis=1, inplace=True)
                columnas_eliminadas.append(columna)
                continue

            if self.df[columna].dtype == "object":
                le = LabelEncoder()
                self.df_limpio[columna] = le.fit_transform(self.df[columna])
                self.labels[str(columna)] = le

            if self.df_limpio[columna].isnull().values.any():
                media = self.df_limpio[columna].mean()
                self.df_limpio[columna] = self.df_limpio[columna].fillna(media)

        valores = [str(elemento) for elemento in columnas_eliminadas]
        columnas_eliminadas_str = ", ".join(valores)

        if (len(columnas_eliminadas) > 0):
            messagebox.showinfo(
                "Aviso", f"Se eliminaron las siguientes columnas. \n{columnas_eliminadas_str}")

    def mostrar_datos(self, df):
        table_model = TableModel(dataframe=df)
        self.tabla.updateModel(table_model)
        self.tabla.redraw()

    def guardar_columnas_entrenamiento(self):
        if self.tabla is None and self.df is None:
            return

        columna_seleccionada = self.tabla.getSelectedColumn()
        nombre_columna = self.df.columns.values[columna_seleccionada]

        # print(f"Columna seleccionada: {nombre_columna}")

        if columna_seleccionada is not None and nombre_columna not in self.columnas_entrenamiento and nombre_columna != self.columna_objetivo:
            self.tabla.setColumnColors(
                cols=[columna_seleccionada], clr='#00ff00')
            self.columnas_entrenamiento.append(nombre_columna)
            print(f"Columnas seleccionadas: {self.columnas_entrenamiento}")
            print(f"Columna objetivo: {self.columna_objetivo}")

    def guardar_columna_objetivo(self):
        if (self.tabla is None) and (self.df is None):
            return

        columna_seleccionada = self.tabla.getSelectedColumn()
        nombre_columna = self.df.columns.values[columna_seleccionada]

        # print(f"Columna seleccionada: {nombre_columna}")

        if (nombre_columna in self.columnas_entrenamiento):
            respuesta = messagebox.showinfo("Aviso",
                                            "La columna objetivo no debe ser la misma que una columna de entrenamiento.")
            return

        if (columna_seleccionada is not None):
            if self.columna_objetivo is not None:
                indice = self.df.columns.get_loc(self.columna_objetivo)
                self.tabla.setColumnColors(cols=[indice], clr='#f4f4f3')
            self.tabla.setColumnColors(
                cols=[columna_seleccionada], clr='#0000ff')
            self.columna_objetivo = nombre_columna
            print(f"Columnas seleccionadas: {self.columnas_entrenamiento}")
            print(f"Columna objetivo: {self.columna_objetivo}")

    def eliminar_columna_seleccionada(self):
        if (self.tabla is None) and (self.df is None):
            return

        columna_seleccionada = self.tabla.getSelectedColumn()
        nombre_columna = self.df.columns.values[columna_seleccionada]

        print(f"Columna a eliminar: {nombre_columna}")

        if (columna_seleccionada is not None) and (nombre_columna in self.columnas_entrenamiento):
            self.tabla.setColumnColors(
                cols=[columna_seleccionada], clr='#f4f4f3')
            self.columnas_entrenamiento.remove(nombre_columna)
            print(f"Columnas seleccionadas: {self.columnas_entrenamiento}")
            print(f"Columna objetivo: {self.columna_objetivo}")

        if nombre_columna == self.columna_objetivo:
            self.tabla.setColumnColors(
                cols=[columna_seleccionada], clr='#f4f4f3')
            self.columna_objetivo = None
            print(f"Columnas seleccionadas: {self.columnas_entrenamiento}")
            print(f"Columna objetivo: {self.columna_objetivo}")

    def cargar_entries(self):
        self.frame_buttons.grid_forget()
        self.frame_predict.grid(padx=5, pady=5, row=0, column=0)
        self.frame_predict.grid_rowconfigure(0, weight=1)
        self.frame_predict.grid_rowconfigure(1, weight=1)
        self.frame_predict.grid_rowconfigure(2, weight=1)
        self.frame_predict.grid_rowconfigure(3, weight=1)
        self.frame_predict.grid_rowconfigure(4, weight=1)
        self.frame_predict.grid_rowconfigure(5, weight=1)
        self.frame_predict.grid_rowconfigure(6, weight=1)
        self.frame_predict.grid_columnconfigure(0, weight=1)

        btn_volver = tk.Button(
            self.frame_predict, text="Volver", command=self.volver)
        btn_volver.grid(padx=10, pady=10, row=0, column=0)

        valores = [str(elemento) for elemento in self.columnas_entrenamiento]
        columnas_entrenamiento_str = ", ".join(valores)
        self.label_columnas_entrenamiento = tk.Label(
            self.frame_predict, text=f"Columnas de entrenamiento: \n [{columnas_entrenamiento_str}]")
        self.label_columnas_entrenamiento.grid(
            padx=10, pady=10, row=1, column=0)

        self.entry = tk.Entry(self.frame_predict, width=40)
        self.entry.insert(0, "Inserte los valores separados por comas")
        self.entry.grid(padx=10, pady=10, row=2, column=0)

        btn_prededir = tk.Button(
            self.frame_predict, text="Predecir", width=30, command=self.predecir)
        btn_prededir.grid(padx=10, pady=10, row=3, column=0)

        self.label_predicted = tk.Label(self.frame_predict, text="Predicted")

        score = round(self.score*100, 2)
        self.label_score = tk.Label(
            self.frame_predict, text=f"Score: {score}%")
        self.label_score.grid(padx=10, pady=10, row=6, column=0)

    def volver(self):
        self.score = None
        self.modelo = None
        self.label_columnas_entrenamiento.grid_forget()
        self.label_predicted.grid_forget()
        self.label_score.grid_forget()
        self.frame_predict.grid_forget()
        self.frame_buttons.grid(padx=5, pady=5, row=0, column=0)

    def entrenar(self):
        if (self.df_limpio is None) or (self.columna_objetivo is None) or (len(self.columnas_entrenamiento) == 0):
            messagebox.showinfo("Aviso",
                                "Necesitas seleccionar una columna objetivo y al menos una columna de entrenamiento.")
            return

        lista_modelos_clasificatorios = list(
            self.modelos_clasificatorios.keys())

        if (self.df_limpio[self.columna_objetivo].unique().size > 10) and (self.combobox.get() in lista_modelos_clasificatorios):
            respuesta = messagebox.askyesno("Advertencia",
                                            "Se ha seleccionado un modelo clasificatorio, pero la columna objetivo tiene más de 10 valores únicos. ¿Desea continuar?")
            if not respuesta:
                return
        elif (self.df_limpio[self.columna_objetivo].unique().size <= 10) and (self.combobox.get() not in lista_modelos_clasificatorios):
            respuesta = messagebox.askyesno("Advertencia",
                                            "Se ha seleccionado un modelo predictivo, pero la columna objetivo es una columna categórica. ¿Desea continuar?")
            if not respuesta:
                return

        data_x = None

        for columna in self.columnas_entrenamiento:
            if data_x is None:
                data_x = self.df_limpio[columna]
            else:
                data_x = pd.concat([data_x, self.df_limpio[columna]], axis=1)

        data_y = self.df_limpio[self.columna_objetivo]

        train_x, test_x, train_y, test_y = train_test_split(
            data_x, data_y, test_size=0.1)

        if len(self.columnas_entrenamiento) == 1:
            test_x = test_x.values.reshape(-1, 1)
            train_x = train_x.values.reshape(-1, 1)

        if self.combobox.get() in lista_modelos_clasificatorios:
            self.modelo = self.modelos_clasificatorios[self.combobox.get()].fit(
                train_x, train_y)
        else:
            self.modelo = self.modelos_predictivos[self.combobox.get()].fit(
                train_x, train_y)

        print(f"Score: {self.modelo.score(test_x, test_y)}")
        self.score = self.modelo.score(test_x, test_y)
        messagebox.showinfo("Aviso",
                            "El modelo ha sido entrenado exitosamente.")
        self.cargar_entries()

    def predecir(self):
        texto_input = self.entry.get().strip()

        if texto_input == "":
            messagebox.showinfo(
                "Aviso", "Se deben ingresar un valores, la caja de texto no puede estar vacia.")
            return

        valores_predict = []

        if len(self.columnas_entrenamiento) > 1:
            valores_split = texto_input.split(",")
            if len(valores_split) != len(self.columnas_entrenamiento):
                messagebox.showinfo(
                    "Aviso", "La cantidad de valores ingresados no coincide con la cantidad de columnas seleccionadas.")
                return

            for i in range(len(valores_split)):
                valor = valores_split[i].strip()
                if valor == "":
                    messagebox.showinfo(
                        "Aviso", "Se deben ingresar todos los valores, no puede haber valores vacios.")
                    return

                if ((self.df[self.columnas_entrenamiento[i]].dtype == np.float64) or (self.df[self.columnas_entrenamiento[i]].dtype == np.int64)) and (not self.esNumero(valor)):
                    messagebox.showinfo(
                        "Aviso", "Se ha ingresado un texto donde se esperaba un valor numerico")
                    return

                if self.df[self.columnas_entrenamiento[i]].dtype == 'object':
                    llaves_labels = list(
                        self.labels[self.columnas_entrenamiento[i]].classes_)
                    if valor not in llaves_labels:
                        mensaje = f"En la columna '{self.columnas_entrenamiento[i]}' se ha ingresado un valor que no se encuentra en el conjunto de datos."
                        messagebox.showinfo("Aviso", mensaje)
                        return
                    valor = self.labels[self.columnas_entrenamiento[i]].transform([valor])[
                        0]
                    valores_predict.append(valor)
                else:
                    valores_predict.append(float(valor))
        else:
            if texto_input == "":
                messagebox.showinfo(
                    "Aviso", "Se deben ingresar todos los valores, no puede haber valores vacios.")
                return

            if ((self.df[self.columnas_entrenamiento[0]].dtype == np.float64) or (self.df[self.columnas_entrenamiento[0]].dtype == np.int64)) and (not self.esNumero(texto_input)):
                messagebox.showinfo(
                    "Aviso", "Se ha ingresado un valor numerico donde se esperaba un texto")
                return

            if self.df[self.columnas_entrenamiento[0]].dtype == 'object':
                llaves_labels = list(
                    self.labels[self.columnas_entrenamiento[0]].classes_)
                if texto_input not in llaves_labels:
                    mensaje = f"En la columna '{self.columnas_entrenamiento[0]}' se ha ingresado un valor que no se encuentra en el conjunto de datos."
                    messagebox.showinfo("Aviso", mensaje)
                    return
                valor = self.labels[self.columnas_entrenamiento[0]].transform([texto_input])[
                    0]
                valores_predict.append(valor)
            else:
                valores_predict.append(float(texto_input))

        predicted = self.modelo.predict([valores_predict])

        if self.modelo in self.modelos_clasificatorios.values():
            if (self.df[self.columna_objetivo].dtype == np.float64) or (self.df[self.columna_objetivo].dtype == np.int64):
                self.label_predicted.config(text=f"Prediccion: {predicted[0]}")
                self.label_predicted.grid(padx=10, pady=10, row=5, column=0)
                return
            predicted = self.labels[self.columna_objetivo].inverse_transform(
                predicted)

        if self.modelo in self.modelos_predictivos.values():
            self.label_predicted.config(
                text=f"Prediccion: {round(predicted[0],2)}")
        else:
            self.label_predicted.config(text=f"Prediccion: {predicted[0]}")

        self.label_predicted.grid(padx=10, pady=10, row=5, column=0)

        print(f"Prediccion: {predicted[0]}")

    def esNumero(self, string):
        esInt = True
        esFloat = True
        try:
            int(string)
            esInt = True
        except ValueError:
            esInt = False
        try:
            float(string)
            esFloat = True
        except ValueError:
            esFloat = False
        return esInt or esFloat

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier

class Proyecto:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('PROYECTO ALGORITMICA')
        self.ventana.configure(bg='white')

        self.data = None # Datos del archivo CSV
        self.columns = None # Nombres de las columnas del archivo CSV
        self.selected_columns = [] # Columnas seleccionadas para entrenar
        self.feature_columns = [] # Columnas de entrenamiento
        self.target_column = None # Columna objetivo
        self.model = None # Modelo de clasificación o predicción

        # Botón para cargar archivo CSV
        self.boton_cargar = tk.Button(self.ventana, text='Cargar CSV', command=self.cargar_archivo_csv)
        self.boton_cargar.pack()

        self.ventana.mainloop()

    def cargar_archivo_csv(self):
        # Ventana para seleccionar archivo CSV
        ruta_archivo = filedialog.askopenfilename(filetypes=[('Archivo CSV', '*.csv')])

        if ruta_archivo:
            # Cargar archivo CSV en un DataFrame de pandas
            self.data = pd.read_csv(ruta_archivo)
            self.columns = self.data.columns
            print(self.columns)# Verificar los nombres de las columnas

            
            ventana_entrenamiento = tk.Toplevel(self.ventana)
            ventana_entrenamiento.title('Columnas de entrenamiento')
            ventana_entrenamiento.configure(bg='white')

            
            screen_width = self.ventana.winfo_screenwidth()
            screen_height = self.ventana.winfo_screenheight()
            width = int(screen_width * 0.4)
            height = int(screen_height * 0.4)
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            ventana_entrenamiento.geometry(f'{width}x{height}+{x}+{y}')

            
            self.etiqueta_entrenamiento = tk.Label(ventana_entrenamiento, text='Columnas Para Entrenar:', bg='white')
            self.etiqueta_entrenamiento.pack()

            
            self.training_listbox = tk.Listbox(ventana_entrenamiento, selectmode=tk.MULTIPLE)
            for column in self.columns:
                self.training_listbox.insert(tk.END, column)
            self.training_listbox.pack()

            
            boton_siguiente = tk.Button(ventana_entrenamiento, text='Siguiente', command=self.analizar_datos)
            boton_siguiente.pack()

    def analizar_datos(self):
        self.selected_columns = []
        mapping_table_data = []

        for column in self.columns:
            data_type = str(self.data[column].dtype) 
            if data_type == "object": 
                
                self.data[column].fillna("", inplace=True) 
                label_encoder = LabelEncoder() 
                self.data[column] = label_encoder.fit_transform(self.data[column])
                mapping_table_data.extend(
                    ((column, label_encoder.classes_[i], i) for i in range(len(label_encoder.classes_))))

            elif data_type == "float64" or data_type == "int64": 
                
                self.data[column].fillna(self.data[column].mean(), inplace=True)
                self.selected_columns.append(column)

        
        ventana_entrenamiento = tk.Toplevel(self.ventana)
        ventana_entrenamiento.title('Entrenamiento')
        ventana_entrenamiento.configure(bg='white')

        
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        width = int(screen_width * 0.4)
        height = int(screen_height * 0.4)
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        ventana_entrenamiento.geometry(f'{width}x{height}+{x}+{y}')

        
        self.etiqueta_objetivo = tk.Label(ventana_entrenamiento, text='Columna objetivo:', bg='white')
        self.etiqueta_objetivo.pack()

        
        self.target_combobox = tk.OptionMenu(ventana_entrenamiento, tk.StringVar(), *self.selected_columns)
        self.target_combobox.pack()

        # Menú desplegable para seleccionar tipo de modelo (Clasificación o Predicción)
        self.model_combobox = tk.OptionMenu(ventana_entrenamiento, tk.StringVar(), "Clasificación", "Predicción")
        self.model_combobox.pack()

        # Botón para entrenar el modelo
        self.train_button = tk.Button(ventana_entrenamiento, text="Entrenar Modelo", command=self.entrenar_modelo)
        self.train_button.pack()

    def entrenar_modelo(self):
        self.feature_columns = self.training_listbox.curselection()
        self.target_column = self.target_combobox.cget("text")
        self.model = self.model_combobox.cget("text")

        if self.feature_columns and self.target_column and self.model:
            if self.model == "Clasificación":
                # Crear modelo de clasificación RandomForestClassifier
                self.model = RandomForestClassifier()
            elif self.model == "Predicción":
                # Crear modelo de predicción LinearRegression
                self.model = LinearRegression()

            X = self.data.iloc[:, list(self.feature_columns)]
            y = self.data[self.target_column]

            # Entrenar el modelo con los datos de entrenamiento
            self.model.fit(X, y)

            # Mostrar mensaje de entrenamiento exitoso
            messagebox.showinfo("Entrenamiento Exitoso", "Modelo Entrenado")

            # Calcular y mostrar el score
            self.calcular_puntuacion()

    def calcular_puntuacion(self):
        # Calcular el score utilizando el método score() del modelo entrenado
        score = self.model.score(self.data.iloc[:, list(self.feature_columns)], self.data[self.target_column])
        messagebox.showinfo("Score", f"Valor calculado es: {score}")


if __name__ == '__main__':
    app = Proyecto()


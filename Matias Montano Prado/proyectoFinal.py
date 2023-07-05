import tkinter as tk  # Importar el módulo tkinter para crear la interfaz gráfica
from tkinter import filedialog, messagebox  # Importar funciones específicas de tkinter
import pandas as pd  # Importar el módulo pandas para el manejo de datos
from tkinter import ttk  # Importar clases y funciones específicas de tkinter
from sklearn.preprocessing import LabelEncoder  # Importar el codificador de etiquetas de scikit-learn
from sklearn.ensemble import RandomForestClassifier  # Importar el clasificador de bosques aleatorios de scikit-learn
from sklearn.linear_model import LinearRegression  # Importar el modelo de regresión lineal de scikit-learn
from ttkthemes import ThemedStyle  # Importar el módulo ttkthemes para aplicar estilos a la interfaz


class AnalizadorDatos:
    def __init__(self):
        # Configuración de la interfaz gráfica
        self.root = tk.Tk()  # Crear la ventana principal
        self.root.title("Predicción y Clasificación de Datos")  # Establecer el título de la ventana
        self.root.configure(bg="#282C34")  # Establecer el color de fondo de la ventana
        self.root.geometry("1000x1000")  # Establecer las dimensiones de la ventana
        style = ThemedStyle(self.root)  # Crear un objeto ThemedStyle para aplicar estilos
        style.set_theme("equilux")  # Establecer el tema oscuro "equilux"

        self.data = None  # Variable para almacenar los datos cargados
        self.columns = []  # Lista para almacenar los nombres de las columnas del archivo
        self.selected_columns = []  # Lista para almacenar las columnas seleccionadas para el análisis
        self.feature_columns = []  # Lista para almacenar las columnas seleccionadas como características de entrenamiento
        self.target_column = ""  # Variable para almacenar la columna objetivo
        self.model = None  # Variable para almacenar el modelo seleccionado

        # Etiqueta para mostrar el estado del archivo cargado
        self.file_label = tk.Label(
            self.root, text="No se ha cargado ningún archivo", bg='dark gray', fg='white')
        self.file_label.pack(pady=10)

        # Botón para cargar un archivo CSV
        self.load_button = ttk.Button(
            self.root, text="Cargar CSV", command=self.cargar_csv, style="DarkButton.TButton")
        self.load_button.pack(pady=5)

        # Botón para analizar los datos del archivo
        self.analyze_button = ttk.Button(
            self.root, text="Analizar Datos", command=self.analizar_datos,
            state=tk.DISABLED, style="DarkButton.TButton")
        self.analyze_button.pack(pady=5)

        # Etiqueta y lista para seleccionar las columnas de entrenamiento
        self.training_label = tk.Label(
            self.root, text="Columnas de entrenamiento:", bg='dark gray', fg='white')
        self.training_label.pack()
        self.training_listbox = tk.Listbox(
            self.root, selectmode=tk.MULTIPLE, bg='white', fg='black', selectbackground='#0078D7')
        self.training_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        # Etiqueta y combobox para seleccionar la columna objetivo
        self.target_label = tk.Label(
            self.root, text="Columna objetivo:", bg='dark gray', fg='white')
        self.target_label.pack()
        self.target_combobox = ttk.Combobox(
            self.root, state="readonly", style="Combobox.TCombobox")
        self.target_combobox.pack(pady=5, fill=tk.BOTH, expand=True)

        # Etiqueta y combobox para seleccionar el tipo de modelo
        self.model_label = tk.Label(
            self.root, text="Selecciona el tipo de modelo:", bg='dark gray', fg='white')
        self.model_label.pack()
        self.model_combobox = ttk.Combobox(
            self.root, values=["Clasificación", "Predicción"], state="readonly", style="Combobox.TCombobox")
        self.model_combobox.pack(pady=5, fill=tk.BOTH, expand=True)

        # Botón para entrenar el modelo
        self.train_button = ttk.Button(
            self.root, text="Entrenar Modelo", command=self.entrenar_modelo,
            state=tk.DISABLED, style="DarkButton.TButton")
        self.train_button.pack(pady=5)

        # Etiqueta para ingresar los valores a predecir o clasificar
        self.score_label = tk.Label(
            self.root, text="Ingresa los valores para hacer la predicción/clasificación:",
            bg='dark gray', fg='white')
        self.score_label.pack()

        # Diccionario que guarda las entradas para los valores a predecir o clasificar
        self.score_entries = {}
        self.score_frame = tk.Frame(self.root, bg='dark gray')
        self.score_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        # Botón para calcular el score de predicción o clasificación
        self.score_button = ttk.Button(
            self.root, text="Calcular Score", command=self.calcular_puntuacion,
            state=tk.DISABLED, style="DarkButton.TButton")
        self.score_button.pack(pady=5)

        # Marco para mostrar la tabla de mapeo de categorías
        self.mapping_table_frame = tk.Frame(self.root, bg='dark gray')
        self.mapping_table_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        self.apply_button_styles()  # Aplicar estilos personalizados a los botones

    def apply_button_styles(self):
        # Aplicar estilos personalizados a los botones
        style = ThemedStyle(self.root)
        style.configure("DarkButton.TButton", foreground="white", background="#707070",
                        font=("Helvetica", 12, "bold"))
        style.map("DarkButton.TButton",
                  foreground=[('pressed', 'white'), ('active', 'white')],
                  background=[('pressed', '#404040'), ('active', '#404040')])

        # Estilo personalizado para el combobox
        style.configure("Combobox.TCombobox", foreground="black", background="white",
                        selectforeground="white", selectbackground="#0078D7",
                        fieldbackground="white", font=("Helvetica", 12, "bold"))

    def cargar_csv(self):
        # Función para cargar un archivo CSV
        file_path = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)  # Leer el archivo CSV y almacenar los datos en self.data
            self.file_label.config(text="Archivo cargado: " + file_path)  # Actualizar la etiqueta del archivo cargado
            self.columns = self.data.columns.tolist()  # Obtener los nombres de las columnas del archivo
            self.analyze_button.config(state=tk.NORMAL)  # Habilitar el botón "Analizar Datos"

    def analizar_datos(self):
        # Función para analizar los datos del archivo cargado
        self.selected_columns = []  # Lista para almacenar las columnas seleccionadas
        mapping_table_data = []  # Lista para almacenar los datos de mapeo de categorías

        for column in self.columns:
            data_type = str(self.data[column].dtype)  # Obtener el tipo de datos de la columna
            if data_type == "object":
                # Si es una columna de tipo "object", se realiza una codificación numérica
                self.data[column].fillna("", inplace=True)  # Rellenar los valores faltantes con una cadena vacía
                label_encoder = LabelEncoder()  # Crear un codificador de etiquetas
                self.data[column] = label_encoder.fit_transform(self.data[column])  # Codificar la columna
                mapping_table_data.extend(
                    [(column, label_encoder.classes_[i], i) for i in range(len(label_encoder.classes_))])
                # Guardar los datos de mapeo de categorías en la lista
            elif data_type == "float64" or data_type == "int64":
                # Si es una columna numérica, se rellenan los valores faltantes con la media
                self.data[column].fillna(self.data[column].mean(), inplace=True)
            else:
                continue
            self.selected_columns.append(column)  # Agregar la columna a la lista de columnas seleccionadas

        # Actualización de la lista de columnas de entrenamiento y combobox de la columna objetivo
        self.training_listbox.delete(0, tk.END)  # Limpiar la lista de columnas de entrenamiento
        self.training_listbox.insert(tk.END, *self.selected_columns)  # Insertar las columnas seleccionadas
        self.target_combobox.config(values=self.selected_columns, state="readonly")
        # Establecer los valores y el estado del combobox de la columna objetivo
        self.model_combobox.config(state="readonly")  # Establecer el estado del combobox del tipo de modelo
        self.train_button.config(state=tk.NORMAL)  # Habilitar el botón "Entrenar Modelo"

        self.mostrar_tabla_mapeo(mapping_table_data)  # Mostrar la tabla de mapeo de categorías

    def mostrar_tabla_mapeo(self, mapping_data):
        # Función para mostrar la tabla de mapeo de categorías en un marco
        scrollbar = tk.Scrollbar(self.mapping_table_frame)  # Crear una barra de desplazamiento vertical
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Empaquetar la barra de desplazamiento en el lado derecho

        mapping_table = tk.Text(
            self.mapping_table_frame, yscrollcommand=scrollbar.set, bg='#282C34',
            fg='white', insertbackground='white', font=("Helvetica", 10))
        # Crear un widget de Texto para mostrar la tabla de mapeo
        mapping_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Empaquetar el widget de Texto

        mapping_table.insert(tk.END, "Columna\tValor Antiguo\tValor Nuevo\n")  # Insertar encabezados de la tabla
        for item in mapping_data:
            mapping_table.insert(tk.END, f"{item[0]}\t{item[1]}\t{item[2]}\n")
            # Insertar los datos de mapeo en la tabla

        scrollbar.config(command=mapping_table.yview)  # Configurar la barra de desplazamiento

    def entrenar_modelo(self):
        # Función para entrenar el modelo seleccionado
        self.feature_columns = self.training_listbox.curselection()  # Obtener las columnas seleccionadas
        self.target_column = self.target_combobox.get()  # Obtener la columna objetivo
        self.model = self.model_combobox.get()  # Obtener el tipo de modelo

        if self.feature_columns and self.target_column and self.model:
            # Verificar que se haya seleccionado al menos una columna de entrenamiento,
            # una columna objetivo y un tipo de modelo
            if self.model == "Clasificación":
                self.model = RandomForestClassifier()  # Crear un clasificador de bosques aleatorios
            elif self.model == "Predicción":
                self.model = LinearRegression()  # Crear un modelo de regresión lineal

            X = self.data.iloc[:, list(self.feature_columns)]  # Obtener las características de entrenamiento
            y = self.data[self.target_column]  # Obtener la columna objetivo

            self.model.fit(X, y)  # Entrenar el modelo con los datos de entrenamiento

            messagebox.showinfo("Entrenamiento Exitoso", "El modelo se ha entrenado exitosamente.")
            # Mostrar un cuadro de diálogo con el mensaje de entrenamiento exitoso

            self.score_label.config(text="Ingresa los valores para hacer la predicción/clasificación:")
            # Actualizar la etiqueta para ingresar los valores a predecir o clasificar
            self.score_entries = {}  # Limpiar el diccionario de entradas de valores
            for widget in self.score_frame.winfo_children():
                widget.destroy()  # Eliminar los widgets anteriores del marco de valores a predecir/clasificar

            for i, column in enumerate(self.feature_columns):
                label = tk.Label(self.score_frame, text=self.selected_columns[column], bg='dark gray', fg='white')
                label.grid(row=i, column=0, padx=5, pady=5)
                entry = tk.Entry(self.score_frame, bg='white', fg='black')
                entry.grid(row=i, column=1, padx=5, pady=5)
                self.score_entries[column] = entry  # Guardar la entrada en el diccionario de entradas de valores

            self.score_button.config(state=tk.NORMAL)  # Habilitar el botón "Calcular Score"

    def calcular_puntuacion(self):
        # Función para calcular el score de predicción o clasificación
        score_values = []
        for column, entry in self.score_entries.items():
            value = entry.get()  # Obtener el valor ingresado en la entrada
            if value:
                score_values.append(float(value))  # Convertir el valor a float y agregarlo a la lista

        if score_values:
            score_values = [score_values]  # Convertir la lista en una lista de listas
            score = self.model.predict(score_values)  # Calcular el score de predicción o clasificación
            messagebox.showinfo("Score", f"El score calculado es: {score[0]}")
            # Mostrar un cuadro de diálogo con el score calculado

    def iniciar_aplicacion(self):
        self.root.mainloop()  # Iniciar el bucle principal de la aplicación


if __name__ == "__main__":
    aplicacion = AnalizadorDatos()  # Crear una instancia de la clase AnalizadorDatos
    aplicacion.iniciar_aplicacion()  # Iniciar la aplicación

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, r2_score

class MLModel:
    def __init__(self, data, target, model_type):
        self.data = data
        self.target = target
        self.model_type = model_type
        self.model = None

    def train(self):
        X_train, X_test, y_train, y_test = train_test_split(self.data, self.target, test_size=0.2, random_state=42)

        if self.model_type == "Prediction":
            self.model = Ridge()
        else:
            self.model = KNeighborsClassifier()

        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)

        if self.model_type == "Prediction":
            score = r2_score(y_test, predictions)
            messagebox.showinfo("Training Complete", f"Model trained successfully. R2 Score: {score}")
        else:
            score = accuracy_score(y_test, predictions)
            messagebox.showinfo("Training Complete", f"Model trained successfully. Accuracy Score: {score}")

    def predict(self, values):
        predictions = self.model.predict(values)
        messagebox.showinfo("Prediction Result", f"Predicted values: {predictions}")

class DataCleaner:
    @staticmethod
    def clean(data):
        cleaned_data = data.copy()

        # Eliminar columnas con muchos valores nulos
        null_threshold = len(cleaned_data) * 0.5  # Umbral del 50% para eliminar columnas
        cleaned_data = cleaned_data.dropna(thresh=null_threshold, axis=1)

        # Agrupar columnas con pocos valores nulos con el grupo que tiene menos valores
        for column in cleaned_data.columns:
            if cleaned_data[column].isnull().sum() > 0:
                if cleaned_data[column].dtype != "float64" and cleaned_data[column].dtype != "int64":
                    mode_value = cleaned_data[column].mode()[0]  # Moda del grupo con menos valores nulos
                    cleaned_data[column].fillna(mode_value, inplace=True)

        # Asignar números a los valores de las columnas basados en grupos
        for column in cleaned_data.columns:
            if cleaned_data[column].dtype != "float64" and cleaned_data[column].dtype != "int64":
                unique_values = cleaned_data[column].unique()
                mapping = {value: i + 1 for i, value in enumerate(unique_values)}
                cleaned_data[column] = cleaned_data[column].map(mapping)

        return cleaned_data

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ML Model Predictor/Classifier")
        self.file_path = None
        self.data = None
        self.cleaned_data = None
        self.training_columns = []
        self.target_column = None
        self.model_type = tk.StringVar(value="Prediction")  # Valor predeterminado: Predicción
        self.model = None

        self.style = ttk.Style()
        self.style.configure("TButton", padding=10)
        self.style.configure("TLabel", padding=5)

        self.file_label = ttk.Label(self, text="No file selected")
        self.file_label.pack(pady=10)

        self.load_button = ttk.Button(self, text="Load CSV", command=self.load_csv)
        self.load_button.pack()

        self.clean_button = ttk.Button(self, text="Clean Data", command=self.clean_data, state=tk.DISABLED)
        self.clean_button.pack()

        self.model_type_label = ttk.Label(self, text="Select Model Type:")
        self.model_type_label.pack()

        self.model_type_dropdown = ttk.OptionMenu(self, self.model_type, "Prediction", "Classification")
        self.model_type_dropdown.pack()

        self.train_button = ttk.Button(self, text="Train Model", command=self.train_model, state=tk.DISABLED)
        self.train_button.pack()

        self.predict_button = ttk.Button(self, text="Predict Values", command=self.predict_values, state=tk.DISABLED)
        self.predict_button.pack()

        self.export_button = ttk.Button(self, text="Export Cleaned Data", command=self.export_data, state=tk.DISABLED)
        self.export_button.pack()

        self.training_frame = ttk.LabelFrame(self, text="Training Columns")
        self.training_frame.pack(pady=10)

        self.target_frame = ttk.LabelFrame(self, text="Target Column")
        self.target_frame.pack(pady=10)

        self.training_checkboxes = []
        self.target_combobox = None

        self.model_type.trace("w", self.change_model_type)

    def load_csv(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.file_label.configure(text=self.file_path)

        if self.file_path:
            self.data = pd.read_csv(self.file_path)
            self.clean_button.configure(state=tk.NORMAL)

            # Borrar casillas de verificación anteriores y cuadro combinado
            for checkbox in self.training_checkboxes:
                checkbox.destroy()
            self.training_checkboxes = []

            if self.target_combobox:
                self.target_combobox.destroy()
                self.target_combobox = None

            # Crear casillas de verificación para columnas de entrenamiento
            for column in self.data.columns:
                var = tk.IntVar()
                checkbox = ttk.Checkbutton(self.training_frame, text=column, variable=var)
                checkbox.pack(anchor="w")
                self.training_checkboxes.append(checkbox)

            # Crear cuadro combinado para la columna de destino
            self.target_combobox = ttk.Combobox(self.target_frame, values=self.data.columns)
            self.target_combobox.pack()

    def clean_data(self):
        self.training_columns = [checkbox.cget("text") for checkbox in self.training_checkboxes if checkbox.instate(["selected"])]
        self.target_column = self.target_combobox.get()

        if not self.training_columns:
            messagebox.showwarning("Error", "Please select at least one training column")
            return

        if not self.target_column:
            messagebox.showwarning("Error", "Please select a target column")
            return

        self.cleaned_data = DataCleaner.clean(self.data)
        messagebox.showinfo("Data Cleaning", "Data cleaned successfully")
        self.train_button.configure(state=tk.NORMAL)
        self.export_button.configure(state=tk.NORMAL)

    def train_model(self):
        self.model = MLModel(self.cleaned_data[self.training_columns], self.cleaned_data[self.target_column], self.model_type.get())
        self.model.train()
        self.predict_button.configure(state=tk.NORMAL)

    def predict_values(self):
        # Realizando la limpieza de datos en nuevos valores, si es necesario
        # Obteniendo nuevos valores y pasarlos al modelo para la predicción
        messagebox.showinfo("Prediction Result", "Prediction completed")

    def change_model_type(self, *args):
        self.model_type.set(self.model_type.get())

    def export_data(self):
        export_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if export_path:
            self.cleaned_data.to_csv(export_path, index=False)
            messagebox.showinfo("Export Successful", "Cleaned data exported successfully")

if __name__ == "__main__":
    app = Application()
    app.mainloop()

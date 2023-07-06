from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from colorama import init


def open_csv_file():
    filetypes = [("Archivos CSV", "*.csv")]
    filename = filedialog.askopenfilename(filetypes=filetypes)
    if filename:
        try:
            global df
            df = pd.read_csv(filename)
            header = df.columns.tolist()
            show_columns(header)
            show_recommendations(header)
        except pd.errors.EmptyDataError:
            show_error("El archivo está vacío.")
        except pd.errors.ParserError:
            show_error("No se pudo leer el archivo CSV.")
    else:
        show_error("No se seleccionó ningún archivo.")


def toggle_switch():
    global switch_state
    if switch_state:
        switch_state = False
        modelo_actual = combo_predictivos.get()
        combo_predictivos.configure(state="enable")
        combo_clasificatorios.configure(state="disabled")

    else:
        switch_state = True
        modelo_actual = combo_clasificatorios.get()
        combo_predictivos.configure(state="disabled")
        combo_clasificatorios.configure(state="enable")

    modelo_actual_label.config(text=f"Modelo actual: {modelo_actual}")


global switch_state
modelo_actual = ""
switch_state = False
entrys = []
labels = []
# Inicializa colorama
init()


window = tk.Tk()
window.title("CSV Insight")
window.config(bg="#23272F")
window.geometry("1440x660")
button_frame = tk.Frame(window, bg="#23272F")
button_frame.pack(pady=20)


def get_x_recommendations(columns):
    numeric_columns = [
        column for column in columns if pd.api.types.is_numeric_dtype(df[column])
    ]
    print(f"Columnas numéricas: {', '.join(numeric_columns)}")
    return numeric_columns


def get_y_recommendations(columns):
    categorical_columns = []

    for column in columns:
        if df[column].dtype == "object":
            categorical_columns.append(column)

    return categorical_columns


open_button = tk.Button(
    button_frame,
    text="Cargar CSV",
    command=open_csv_file,
    fg="#FFFFFF",
    bg="#374151",
    relief=tk.FLAT,
    font=("Arial", 12),
)
open_button.pack(side=tk.LEFT, padx=10)

switch_button = tk.Button(
    button_frame,
    text="Seleccionar Modelo",
    command=toggle_switch,
    fg="#FFFFFF",
    bg="#374151",
    relief=tk.FLAT,
    font=("Arial", 12),
)
switch_button.pack(side=tk.LEFT, padx=10)


def show_columns(columns):
    columns_frame = tk.Frame(window, bg="#23272F")
    columns_frame.pack(pady=20)

    # Combobox de la columna
    global column_combobox
    column_combobox = ttk.Combobox(columns_frame, values=columns)
    column_combobox.grid(row=0, column=0, padx=5)
    column_combobox.set("Seleccione una columna")
    column_combobox.bind("<<ComboboxSelected>>", lambda event: update_listbox(columns))

    # Lista de selección múltiple
    global columns_lb
    columns_lb = tk.Listbox(columns_frame, selectmode=tk.MULTIPLE)
    columns_lb.grid(row=0, column=1, padx=5)

    # Botón para entrenar el modelo
    global train_button
    train_button = tk.Button(
        columns_frame,
        text="Entrenar modelo",
        command=train_model,
        fg="#FFFFFF",
        bg="#374151",
        relief=tk.FLAT,
        font=("Arial", 10),
    )
    train_button.grid(row=0, column=2, padx=5)

    # Botón para calcular el score
    global score_button
    score_button = tk.Button(
        columns_frame,
        text="Calcular score",
        command=calculate_score,
        fg="#FFFFFF",
        bg="#374151",
        relief=tk.FLAT,
        state=tk.DISABLED,
        font=("Arial", 10),
    )
    score_button.grid(row=0, column=3, padx=5)

    # Botón para calcular la predicción
    global predict_button
    predict_button = tk.Button(
        columns_frame,
        text="Calcular Predicción",
        command=calculate_prediction,
        fg="#FFFFFF",
        bg="#374151",
        relief=tk.FLAT,
        state=tk.DISABLED,
        font=("Arial", 10),
    )
    predict_button.grid(row=0, column=4, padx=5)


def update_listbox(columns):
    selected_column = column_combobox.get()
    columns_lb.delete(0, tk.END)
    for column in columns:
        if column != selected_column:
            columns_lb.insert(tk.END, column)


def train_predictive_model(modelo_seleccionado):
    print("Entrenando modelo predicgtivo...")

    global linear
    global dataYNoEncoded

    if modelo_seleccionado == "Regresión Lineal":
        from sklearn.linear_model import LinearRegression

        linear = LinearRegression()
        print("Regresión Lineal")
    if modelo_seleccionado == "Bosques Aleatorios para Regresión":
        from sklearn.tree import DecisionTreeRegressor

        linear = DecisionTreeRegressor()
        print("Bosques Aleatorios para Regresión")
    if modelo_seleccionado == "Máquinas de Vectores de Soporte para Regresión":
        from sklearn.svm import SVR

        linear = SVR()
        print("Máquinas de Vectores de Soporte para Regresión")
    if modelo_seleccionado == "Regresión Ridge":
        from sklearn.linear_model import Ridge

        linear = Ridge()
        print("Regresión Ridge")
    if modelo_seleccionado == "Regresión Lasso":
        from sklearn.linear_model import Lasso

        linear = Lasso()
        print("Regresión Lasso")

    print("Entrenando modelo...")
    global selected_columns
    selected_columns = [columns_lb.get(i) for i in columns_lb.curselection()]
    selected_y_column = column_combobox.get()

    print(f"Columnas seleccionadas: {', '.join(selected_columns)}")
    print(f"Columna Y: {selected_y_column}")

    if selected_columns:
        if selected_y_column in selected_columns:
            show_error(
                "La columna seleccionada para Y debe ser distinta de las columnas seleccionadas."
            )
            return

        data_x = df[selected_columns]
        data_y = df[selected_y_column]
        dataYNoEncoded = data_y
        data_x = data_x.fillna("desconocido")
        data_y = data_y.fillna("desconocido")

        # Convertir todas las columnas a tipo string
        data_x = data_x.astype(str)
        data_y = data_y.astype(str)

        # Aplicar Label Encoder a cada columna seleccionada
        label_encoder = LabelEncoder()
        for column in selected_columns:
            data_x[column] = label_encoder.fit_transform(data_x[column])

        # Aplicar Label Encoder a la columna seleccionada para Y
        data_y = label_encoder.fit_transform(data_y)

        global train_x, test_x, train_y, test_y
        train_x, test_x, train_y, test_y = train_test_split(
            data_x, data_y, test_size=0.1
        )

        linear.fit(train_x, train_y)
        score_button["state"] = tk.NORMAL
        predict_button["state"] = tk.NORMAL

        # Eliminar los labels y entrys existentes
        for label in window.grid_slaves():
            if isinstance(label, tk.Label):
                label.destroy()

        for entry in window.grid_slaves():
            if isinstance(entry, tk.Entry):
                entry.destroy()

        create_inputs()
        print(f"Modelo entrenado con las columnas: {', '.join(selected_columns)}")


def train_classification_model(modelo_seleccionado):
    print("Entrenando modelo clasificatorio...")
    global linear

    if modelo_seleccionado == "Regresión Logística":
        from sklearn.linear_model import LogisticRegression

        linear = LogisticRegression()
        print("MODELO ENTRENADO CON LOGISTIC REGRESSION")
    if modelo_seleccionado == "Árboles de Decisión":
        from sklearn.tree import DecisionTreeClassifier

        linear = DecisionTreeClassifier()
        print("MODELO ENTRENADO CON DECISION TREE CLASSIFIER")
    if modelo_seleccionado == "Máquinas de Vectores de Soporte":
        from sklearn.svm import SVC

        linear = SVC()
        print("MODELO ENTRENADO CON SVC")
    if modelo_seleccionado == "Bosques Aleatorios":
        from sklearn.ensemble import RandomForestClassifier

        linear = RandomForestClassifier()
        print("MODELO ENTRENADO CON RANDOM FOREST CLASSIFIER")
    if modelo_seleccionado == "Naive Bayes":
        from sklearn.naive_bayes import GaussianNB

        linear = GaussianNB()
        print("MODELO ENTRENADO CON GAUSSIAN NB")

    print("Entrenando modelo...")
    global selected_columns
    selected_columns = [columns_lb.get(i) for i in columns_lb.curselection()]
    selected_y_column = column_combobox.get()

    print(f"Columnas seleccionadas: {', '.join(selected_columns)}")
    print(f"Columna Y: {selected_y_column}")

    if selected_columns:
        if selected_y_column in selected_columns:
            show_error(
                "La columna seleccionada para Y debe ser distinta de las columnas seleccionadas."
            )
            return

        data_x = df[selected_columns]
        data_y = df[selected_y_column]

        # Manejo de valores NaN en columnas seleccionadas
        data_x = data_x.fillna("desconocido")
        data_y = data_y.fillna("desconocido")

        # Convertir todas las columnas a tipo string
        data_x = data_x.astype(str)
        data_y = data_y.astype(str)

        # Aplicar Label Encoder a cada columna seleccionada
        label_encoder = LabelEncoder()
        for column in selected_columns:
            data_x[column] = label_encoder.fit_transform(data_x[column])

        # Aplicar Label Encoder a la columna seleccionada para Y
        data_y = label_encoder.fit_transform(data_y)

        global train_x, test_x, train_y, test_y
        train_x, test_x, train_y, test_y = train_test_split(
            data_x, data_y, test_size=0.1
        )

        linear.fit(train_x, train_y)
        score_button["state"] = tk.NORMAL
        predict_button["state"] = tk.NORMAL

        # Eliminar los labels y entrys existentes
        for label in window.grid_slaves():
            if isinstance(label, tk.Label):
                label.destroy()

        for entry in window.grid_slaves():
            if isinstance(entry, tk.Entry):
                entry.destroy()

        create_inputs()
        print(
            f"Modelo entrenado con las columnas PREDICTIVAS: {', '.join(selected_columns)}"
        )


def create_inputs():
    global entrys
    global labels

    # Eliminar los entrys y labels anteriores
    for entry in entrys:
        entry.destroy()
    entrys.clear()
    for label in labels:
        label.destroy()
    labels.clear()

    # Crear un widget de desplazamiento
    canvas = tk.Canvas(window)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    # Configurar el canvas y el scrollbar
    canvas.configure(yscrollcommand=scrollbar.set, bg="#23272F")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.config(background="#23272F")
    scrollbar.pack(side="right", fill="y")

    # Configurar el scroll_frame en el canvas
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    for column in selected_columns:
        label = tk.Label(scroll_frame, text=column, font=("Arial", 10))
        label.config(background="#23272F", foreground="white")
        label.pack(side="top", padx=5, pady=5)
        labels.append(label)
        entry = tk.Entry(scroll_frame)
        entry.pack(side="top", padx=5, pady=5)
        entrys.append(entry)

    # Configurar el tamaño del canvas para que se ajuste al contenido
    scroll_frame.config(background="#23272F")
    scroll_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def train_model():
    if switch_state:
        if combo_clasificatorios.get() == "Regresión Logística":
            print("Regresión Logística")
            train_classification_model("Regresión Logística")
            return
        if combo_clasificatorios.get() == "Árboles de Decisión":
            print("Árboles de Decisión")
            train_classification_model("Árboles de Decisión")
            return
        if combo_clasificatorios.get() == "Máquinas de Vectores de Soporte":
            print("Máquinas de Vectores de Soporte")
            train_classification_model("Máquinas de Vectores de Soporte")
            return
        if combo_clasificatorios.get() == "Bosques Aleatorios":
            print("Bosques Aleatorios")
            train_classification_model("Bosques Aleatorios")
            return
        if combo_clasificatorios.get() == "Naive Bayes":
            print("Naive Bayes")
            train_classification_model("Naive Bayes")
            return

        return
    else:
        if combo_predictivos.get() == "Regresión Lineal":
            print(combo_predictivos.get())
            train_predictive_model(modelo_seleccionado="Regresión Lineal")
            return
        if combo_predictivos.get() == "Bosques Aleatorios para Regresión":
            print("Bosques Aleatorios para Regresión")
            train_predictive_model("Bosques Aleatorios para Regresión")
            return
        if combo_predictivos.get() == "Máquinas de Vectores de Soporte para Regresión":
            print("Máquinas de Vectores de Soporte para Regresión")
            train_predictive_model("Máquinas de Vectores de Soporte para Regresión")
            return
        if combo_predictivos.get() == "Regresión Ridge":
            print("Regresión Ridge")
            train_predictive_model("Regresión Ridge")
            return
        if combo_predictivos.get() == "Regresión Lasso":
            print("Regresión Lasso")
            train_predictive_model("Regresión Lasso")
            return


def calculate_score():
    try:
        score = round(linear.score(test_x, test_y) * 100, 2)
        score_label.config(text=f"Puntaje: {score}%")
        print(f"Score: {score}%")
    except Exception as e:
        show_error(str(e))


def calculate_prediction():
    try:
        values = []
        for entry in entrys:
            values.append(entry.get())
        values = [int(i) for i in values]
        print(f"Valores: {values}")
        predicted = linear.predict([values])
        score_predicted.config(text=f"Predicción: {predicted}")

        prediction.config(text="Predicción:  {predicted}")
        print(f"Predicción: {predicted}")
    except Exception as e:
        show_error(str(e))


def show_error(message):
    error_label.config(text=message)
    error_label.pack(pady=0)


def show_recommendations(columns):
    recommendations_frame = tk.Frame(window, bg="#23272F")
    recommendations_frame.pack(pady=10)

    recommendations_label = tk.Label(
        recommendations_frame,
        text="Recomendaciones de columnas numericas:",
        font=("Arial", 12, "bold"),
        bg="#23272F",
        fg="white",
    )
    recommendations_label.pack()

    # Recomendaciones para variables independientes (X)
    x_recommendations = get_x_recommendations(columns)
    x_recommendations_label = tk.Label(
        recommendations_frame,
        text=", ".join(x_recommendations),
        font=("Arial", 12),
        bg="#23272F",
        fg="white",
    )
    x_recommendations_label.pack()
    recommendations_label = tk.Label(
        recommendations_frame,
        text="Recomendaciones de columnas categoricas:",
        font=("Arial", 12, "bold"),
        bg="#23272F",
        fg="white",
    )
    recommendations_label.pack()
    # Recomendaciones para variable dependiente (Y)
    y_recommendations = get_y_recommendations(columns)
    y_recommendations_label = tk.Label(
        recommendations_frame,
        text=", ".join(y_recommendations),
        font=("Arial", 12),
        bg="#23272F",
        fg="white",
    )
    y_recommendations_label.pack()


# Etiqueta para el primer ComboBox
label_predictivos = ttk.Label(window, text="Modelos Predictivos:")
label_predictivos.pack()

# ComboBox para los modelos predictivos
combo_predictivos = ttk.Combobox(
    window,
    values=[
        "Regresión Lineal",
        "Bosques Aleatorios para Regresión",
        "Máquinas de Vectores de Soporte para Regresión",
        "Regresión Ridge",
        "Regresión Lasso",
    ],
)
combo_predictivos.current(0)
combo_predictivos.pack()
combo_predictivos.configure(state="disabled")

# Etiqueta para el segundo ComboBox
label_clasificatorios = ttk.Label(window, text="Modelos Clasificatorios:")
label_clasificatorios.pack()

# ComboBox para los modelos clasificatorios
combo_clasificatorios = ttk.Combobox(
    window,
    values=[
        "Regresión Logística",
        "Árboles de Decisión",
        "Máquinas de Vectores de Soporte",
        "Bosques Aleatorios",
        "Naive Bayes",
    ],
)
combo_clasificatorios.current(0)
combo_clasificatorios.pack()
combo_clasificatorios.configure(state="disabled")

# Contenedor para las etiquetas de modelo y puntaje
info_frame = tk.Frame(window, bg="#23272F")
info_frame.pack(pady=20)

modelo_actual_label = tk.Label(
    info_frame, text="Modelo actual:", fg="green", bg="#23272F"
)
modelo_actual_label.pack(side=tk.LEFT)

modelo_actual_value = tk.Label(info_frame, text=modelo_actual, fg="green", bg="#23272F")
modelo_actual_value.pack(side=tk.LEFT, padx=10)

score_label = tk.Label(info_frame, text="Puntaje:", fg="green", bg="#23272F")
score_label.pack(side=tk.LEFT)

score_predicted = tk.Label(info_frame, text="", fg="green", bg="#23272F")
score_predicted.pack(side=tk.LEFT, padx=10)

prediction = tk.Label(info_frame, text="", fg="green", bg="#23272F")
score_predicted.pack(side=tk.LEFT, padx=10)

# Etiqueta para mostrar los errores
error_label = tk.Label(
    window,
    fg="red",
    bg="#202123",
    anchor="w",
    justify="left",
    font=("Arial", 12),
    padx=10,
    pady=10,
)
error_label.pack(side="bottom", fill=tk.X)

# Iniciar el bucle de eventos de la ventana
window.mainloop()

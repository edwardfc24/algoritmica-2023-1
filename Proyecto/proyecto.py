import tkinter as tk
from tkinter import Tk, Label, Button, Frame, messagebox, filedialog, ttk, Scrollbar, VERTICAL, HORIZONTAL, Listbox
import pandas as pd
from tkinter import *
from cleaner import Cleaner
from sklearn import neighbors
from sklearn import linear_model
from sklearn.model_selection import train_test_split

global datos
datos = pd.DataFrame()
global indices_x
indices_x = []
global columnas_x
columnas_x = pd.DataFrame()
global columna_y
columna_y = None
global modelo
modelo = None
global modelo_entrenado
modelo_entrenado = None
global lista_entries 
lista_entries = []
global labels_columnas_x
labels_columnas_x = []

color_principal = '#230903'
color_secundario = '#F2A900'
color_texto = '#FFFFFF'

ventana = tk.Tk()
ventana.title("Analizador de Datos")
ventana.geometry("500x500")
ventana.configure(background= color_principal)
ventana.minsize(700, 600)

ventana.columnconfigure(0, weight=1)

frame_cargar_archivo = Frame(ventana, bg= color_principal)
frame_cargar_archivo.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

frame_cargar_archivo.columnconfigure(0, weight=1)
frame_cargar_archivo.rowconfigure(1, weight=1)
frame_cargar_archivo.columnconfigure(1, weight=3)
frame_cargar_archivo.rowconfigure(1, weight=3)

label_subir_archivo = Label(frame_cargar_archivo, fg='white', bg=color_principal, text='Ubicación del archivo', font=('Arial', 10, 'bold'))
label_subir_archivo.grid(column=1, row=0)

frame_options = Frame(ventana, bg= color_principal)
frame_options.grid(row=1, column=0, padx=10, pady=10)

frame_seleccion_modelo = Frame(frame_options, bg= color_principal)
frame_seleccion_modelo.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
frame_seleccion_modelo.columnconfigure(0, weight=1)
frame_seleccion_modelo.rowconfigure(1, weight=1)


label_modelo = Label(frame_seleccion_modelo, fg='white', bg=color_principal, text='Seleccionar Tipo de modelo',
                    font=('Arial', 10, 'bold'))
label_modelo.grid(column=0, row=0)


combobox_modelo = ttk.Combobox(frame_seleccion_modelo, state='readonly')
combobox_modelo['values'] = ('Clasificatorio', 'Prediccion')
combobox_modelo.grid(column=0, row=1)

frame_seleccion_columna_objetivo = Frame(frame_options, bg= color_principal)
frame_seleccion_columna_objetivo.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
frame_seleccion_columna_objetivo.columnconfigure(0, weight=1)
frame_seleccion_columna_objetivo.rowconfigure(1, weight=1)

label_seleccionar_columna_y = Label(frame_seleccion_columna_objetivo, fg='white', bg= color_principal, text='Seleccionar Columna Objetivo',
                                font=('Arial', 10, 'bold'))
label_seleccionar_columna_y.grid(column=0, row=0)

combobox_columna_y = ttk.Combobox(frame_seleccion_columna_objetivo, state='readonly')
combobox_columna_y.grid(column=0, row=1)

frame_seleccion_columnas_x = Frame(ventana, bg= color_principal)
frame_seleccion_columnas_x.grid(row=2, column=0)

label_columnas_x = Label(frame_seleccion_columnas_x, fg='white', bg= color_principal, text='Seleccionar Columnas de Entrenamiento', font=('Arial', 10, 'bold'))
label_columnas_x.grid(column=0, row=0)

listbox_columnas_x = tk.Listbox(frame_seleccion_columnas_x, selectmode=tk.MULTIPLE, bg= 'white', fg='black')

frame_entries = Frame(ventana, bg= color_principal)
frame_entries.grid(row=5, column=0)

frame_entries.columnconfigure(1, weight=1)

label_ingresar_datos = Label(frame_entries, fg='white', bg=color_principal, text='Ingresar Datos Para Predecir/Clasificar', font=('Arial', 10, 'bold'))
label_ingresar_datos.grid(column=0, row=0)

def abrir_archivo():
    archivo = filedialog.askopenfilename(initialdir='/', title='Selecione archivo',
                                        filetype=(('csv files', '*.csv*'), ('All files', '*.*')))
    label_subir_archivo['text'] = archivo
    datos_excel()


def datos_excel():
    datos_obtenidos = label_subir_archivo['text']
    df = None
    try:
        archivoexcel = r'{}'.format(datos_obtenidos)
        df = pd.read_csv(archivoexcel)
    except ValueError:
        messagebox.showerror('Informacion', 'Formato incorrecto')
        return None
    except FileNotFoundError:
        messagebox.showerror('Informacion', 'El archivo esta \n malogrado')
        return None

    clean = Cleaner(df)
    clean.clean_df()
    global datos
    datos = clean.get_df()

    lista_columnas = []
    # Carga todas las columnas del dataframe ya limpio en el combobox y en el listbox
    for column in datos.columns:
        listbox_columnas_x.insert(tk.END, column)
        lista_columnas.append(column)
    listbox_columnas_x.grid(column=0, row=1)
    combobox_columna_y['values'] = lista_columnas


def on_listbox_columnas_select(event):
    # Guarda los indices en el listbox de las columnas seleccionadas
    global indices_x
    indices_x = event.widget.curselection()

def entrenar_modelo():
    global indices_x
    global columnas_x
    global labels_columnas_x
    global lista_entries
    global modelo
    global modelo_entrenado
    global columna_y
    labels_columnas_x = []
    # Saca los nombres de las columnas seleccionadas, guardados en el listbox
    for index in indices_x:
        labels_columnas_x.append(listbox_columnas_x.get(index))
    # Validaciones para que se seleccionen todos los datos antes de entrenar el modelo
    if len(labels_columnas_x) == 0:
        messagebox.showerror('Informacion', 'No se ha seleccionado ninguna columna de entrenamiento')
        return None
    elif combobox_columna_y.get() == '':
        messagebox.showerror('Informacion', 'No se ha seleccionado una columna objetivo')
        return None
    elif combobox_modelo.get() == '':
        messagebox.showerror('Informacion', 'No se ha seleccionado un tipo de modelo')
        return None
    elif combobox_columna_y.get() in labels_columnas_x:
        messagebox.showerror('Informacion', 'La columna objetivo no puede ser una columna de entrenamiento')
        return None
    
    contador = 1
    # Se crea los entries para ingresar los datos a predecir o clasificar y se guarda las columnas de entrenamiento
    for label in labels_columnas_x:
        columnas_x[label] = datos[label]
        rango = " (" + str(datos[label].min()) + " - " + str(datos[label].max()) +  ")"
        Label(frame_entries, fg='white', bg=color_principal, text=label + rango, font=('Arial', 10, 'bold')).grid(column=0, row=contador)
        entry = Entry(frame_entries, fg='black', bg='white', font=('Arial', 10, 'bold'))
        entry.grid(column=1, row=contador)
        lista_entries.append(entry)
        contador += 1
    
    modelo = combobox_modelo.get()
    columna_y = combobox_columna_y.get()
    columna_y = datos[columna_y]
    # Se crea el modelo de acuerdo al tipo de modelo seleccionado, se lo entrena y se crea un label para mostrar su score
    if modelo == 'Clasificatorio':
        modelo_entrenado = neighbors.KNeighborsClassifier(n_neighbors=7)
        train_x, test_x, train_y, test_y = train_test_split(columnas_x, columna_y, test_size=0.1)
        modelo_entrenado.fit(train_x, train_y)
        label_score = Label(ventana, fg='white', bg= color_principal,
                            text=f'Grado de Confianza: {round(modelo_entrenado.score(test_x, test_y), 2) * 100}%',
                            font=('Arial', 10, 'bold'))
    else:
        modelo_entrenado = linear_model.LinearRegression()
        train_x, test_x, train_y, test_y = train_test_split(columnas_x, columna_y, test_size=0.1)
        modelo_entrenado.fit(train_x, train_y)
        label_score = Label(ventana, fg='white', bg= color_principal,
                            text=f'Grado de Confianza: {round(modelo_entrenado.score(test_x, test_y), 2) * 100}%',
                            font=('Arial', 10, 'bold'))
    label_score.grid(column=0, row=4)


def calcular():
    valores = []
    for entry in lista_entries:
        if entry.get() == '':
            messagebox.showerror('Informacion', 'Debe rellenar todos los campos')
            return None
        valores.append(float(entry.get()))
    prediccion = modelo_entrenado.predict([valores])
    label_resultado = Label(ventana, fg='white', bg=color_principal, text=f'El resultado es: {prediccion}', font=('Arial', 10, 'bold'))
    label_resultado.grid(column=0, row=7)



boton_cargar = Button(frame_cargar_archivo, text='Abrir', bg= color_secundario, command=abrir_archivo)
boton_cargar.grid(column=0, row=0, padx=40, pady=10, sticky='nsew')

boton_entrenar = Button(ventana, text='Entrenar', bg= color_secundario, command=entrenar_modelo)
boton_entrenar.grid(column=0, row=3, padx=250, pady=10, sticky='nsew')

boton_calcular = Button(ventana, text='Calcular', bg= color_secundario, command=calcular)
boton_calcular.grid(column=0, row=6, padx=250, pady=10, sticky='nsew')

listbox_columnas_x.bind('<<ListboxSelect>>', on_listbox_columnas_select)

def cerrar_ventana():
    ventana.destroy()


ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)

ventana.mainloop()
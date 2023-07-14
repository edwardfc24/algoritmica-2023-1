import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel, config
from tkinter import filedialog
from tkinter import messagebox

import pandas as pd
import math


class SelecterPanel:

    def __init__(self, window, self_window):
        self.window = window
        self.self_window = self_window
        self.window.geometry("1400x700")
        self_window.center_window(self.window)
        self.type = "predicted"

        self.x_columns = []
        self.y_column = None
        self.model_table = None
        self.table = None

        self.file = self.self_window.file
        self.model_predicted = tk.StringVar()
        self.model_classifier = tk.StringVar()
        self.is_predicted = tk.BooleanVar()
        self.is_classifier = tk.BooleanVar()
        self.is_predicted.set(True)
        self.model_predicted.set("Linear Regression")
        self.model_classifier.set("KNieghbors")

        models_predictted = ["Linear Regression", "Lasso", "Ridge"]
        models_classifier = ["KNieghbors", "Decision Tree", "Random Forest"]

        self.panel = tk.Frame(self.window)

        # Predicted
        self.cbox_predicted = tk.Checkbutton(self.panel, text="Predecir", bg=None, fg="black", font="none 16 bold", command=self.predicted_selected, variable=self.is_predicted)
        self.menu_predicted = tk.OptionMenu(self.panel, self.model_predicted, *models_predictted)
        # Classifier
        self.cbox_classifier = tk.Checkbutton(self.panel, text="Clasificar", bg=None, fg="black", font="none 16 bold", command=self.classifier_selected, variable=self.is_classifier)
        self.menu_classifier = tk.OptionMenu(self.panel, self.model_classifier, *models_classifier)
        # Table
        self.table_container = tk.Frame(self.panel)
        # x, y
        self.btn_x = tk.Button(self.panel, text="X", command=self.select_x)
        self.btn_y = tk.Button(self.panel, text="Y", command=self.select_y)
        self.x_columns_container = tk.Frame(self.panel, bg=None)
        self.y_columns_container = tk.Frame(self.panel, bg=None)
        # Train
        self.btn_train = tk.Button(self.panel, text="Entrenar Modelo", command=self.train_model)
        # File
        self.btn_select_file = tk.Button(self.panel, text="Seleccionar archivo", command=self.open_file_chooser)
        # Columns
        self.x_columns_list = tk.Listbox(self.x_columns_container, bg=None, font="none 16 bold")
        self.y_columns_list = tk.Listbox(self.y_columns_container, bg=None, font="none 16 bold")

        self.panel.pack(fill=tk.BOTH, expand=True)
        self.cbox_predicted.pack()
        self.menu_predicted.pack()
        self.cbox_classifier.pack()
        self.menu_classifier.pack()
        self.table_container.pack()
        self.btn_x.pack()
        self.btn_y.pack()

        self.x_columns_container.pack()
        self.y_columns_container.pack()
        self.x_columns_list.pack()
        self.y_columns_list.pack()

        self.btn_train.pack()
        self.btn_select_file.pack()

        self.cbox_predicted.place(x=50, y=50, width=150, height=30)
        self.menu_predicted.place(x=50, y=100, width=150, height=30)

        self.cbox_classifier.place(x=50, y=200, width=150, height=30)
        self.menu_classifier.place(x=50, y=250, width=150, height=30)

        self.table_container.place(x=250, y=50, width=800, height=600)

        self.btn_x.place(x=50, y=350, width=150, height=30)
        self.btn_y.place(x=50, y=400, width=150, height=30)
        self.x_columns_container.place(x=1100, y=50, width=250, height=500)
        self.y_columns_container.place(x=1100, y=600, width=250, height=50)
        self.x_columns_list.place(x=0, y=0, width=250, height=500)
        self.y_columns_list.place(x=0, y=0, width=250, height=50)
        self.btn_train.place(x=50, y=550, width=150, height=30)
        self.btn_select_file.place(x=50, y=600, width=150, height=30)

        self.upload_file()
        self.recommend_predicted_y_columns()

    def train_model(self):
        # VERIFICAR las columnas seleccionadas
        if len(self.x_columns) == 0 or self.y_column is None:
            messagebox.showerror("Error", "No se han seleccionado las columnas")
            return
        model_selected = None
        if self.type == "predicted":
            model_selected = self.model_predicted.get()
        elif self.type == "classifier":
            model_selected = self.model_classifier.get()

        self.self_window.open_results_panel(self.type, model_selected, self.x_columns, self.y_column, self.df)

    def predicted_selected(self):
        if not self.is_predicted.get():
            self.recommend_classifier_y_columns()
            self.is_classifier.set(True)
            self.type = "classifier"
        else:
            self.recommend_predicted_y_columns()
            self.is_classifier.set(False)
            self.type = "predicted"

    def classifier_selected(self):
        if not self.is_classifier.get():
            self.recommend_predicted_y_columns()
            self.is_predicted.set(True)
            self.type = "predicted"
        else:
            self.recommend_classifier_y_columns()
            self.is_predicted.set(False)
            self.type = "classifier"

    def upload_file(self):
        file = open(self.file, 'r')
        self.df = pd.read_csv(file)
        self.clean_df()
        self.verify_columns_sequence()
        if self.model_table is None and self.table is None:
            self.model_table = TableModel(self.df)
            self.table = Table(
                self.table_container, model=self.model_table, editable=False, enable_menus=False)
            self.table.bind("<Button-1>", self.column_selected)
            self.table.show()
        else:
            self.model_table.df = self.df
            self.table.redraw()
            self.recommend_y()
        file.close()

    def open_file_chooser(self):
        new_file = filedialog.askopenfilename(
            initialdir="/", title="Seleccione el CSV", filetypes=[("Archivo CSV", ".csv")])
        if new_file != "":
            self.file = new_file
            self.upload_file()

    def column_selected(self, event):
        column = self.table.get_col_clicked(event)
        column_name = self.df.columns[column]
        self.add_column(column_name)

    def add_column(self, column_name):
        if self.btn_x["state"] == "disabled":
            if column_name in self.x_columns:
                self.x_columns.remove(column_name)
                self.reload_list()
                return
            if column_name == self.y_column:
                return
            self.x_columns.append(column_name)
            self.x_columns_list.insert(tk.END, column_name)
        elif self.btn_y["state"] == "disabled":
            if column_name == self.y_column:
                self.y_column = None
                self.y_columns_list.delete(0, tk.END)
                return
            if column_name in self.x_columns:
                return
            self.y_column = column_name
            self.y_columns_list.delete(0, tk.END)
            self.y_columns_list.insert(tk.END, column_name)

    def reload_list(self):
        self.x_columns_list.delete(0, tk.END)
        for header in self.x_columns:
            self.x_columns_list.insert(tk.END, header)

    def select_x(self):
        self.btn_x["state"] = "disabled"
        self.btn_y["state"] = "normal"

    def select_y(self):
        self.btn_x["state"] = "normal"
        self.btn_y["state"] = "disabled"

    def clean_df(self):
        total_row_count = len(self.df.index)
        for column in self.df.columns:
            column_type = self.df[column].dtype
            row_count = self.df[column].count()
            if row_count < total_row_count * 0.70:
                self.df = self.df.drop(column, axis=1)
                continue
            if column_type == "object":
                if self.df[column].unique().size > 10:
                    self.df = self.df.drop(column, axis=1)

    def verify_columns_sequence(self):
        is_sequence = True
        for column in self.df.columns:
            if self.df[column].dtype == "object":
                continue
            limit = math.ceil(len(self.df[column].index) * 0.25)
            for i in range(1, limit):
                if self.df[column][i] + 1 != self.df[column][i + 1]:
                    is_sequence = False
            if is_sequence:
                self.df = self.df.drop(column, axis=1)

    def recommend_y(self):
        if self.is_predicted.get():
            self.recommend_predicted_y_columns()
        elif self.is_classifier.get():
            self.recommend_classifier_y_columns()

    def recommend_predicted_y_columns(self):
        self.remove_all_color_columns()
        for column_name in self.df.columns:
            column_type = self.df[column_name].dtype
            if column_type != "object" and self.df[column_name].unique().size > 10:
                self.paint_column(column_name)

    def recommend_classifier_y_columns(self):
        self.remove_all_color_columns()
        for column_name in self.df.columns:
            column_type = self.df[column_name].dtype
            if column_type == "object":
                self.paint_column(column_name)
            elif self.df[column_name].unique().size <= 10:
                self.paint_column(column_name)

    def remove_all_color_columns(self):
        for column_name in self.df.columns:
            self.table.columncolors[column_name] = '#ffffff'
            self.table.redraw()

    def paint_column(self, column_name):
        self.table.columncolors[column_name] = '#ebc034'
        self.table.redraw()

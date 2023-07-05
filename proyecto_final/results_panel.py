from sklearn import linear_model, neighbors, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from tkinter import messagebox

import tkinter as tk
import pandas as pd
import numpy as np
from math import ceil

class ResultsPanel:

    def __init__(self, window, self_window, type, model, x_columns, y_column, df):
        self.window = window
        self.window_self = self_window
        self.window.geometry("500x700")
        self_window.center_window(self.window)
        self.y_labels = {}
        self.all_map_values = {}
        self.button_result_pressed = False

        # Models
        self.predicted_models = {
            "Linear Regression": linear_model.LinearRegression(),
            "Lasso": linear_model.Lasso(),
            "Ridge": linear_model.Ridge()
        }
        self.classifier_models = {
            "KNieghbors": neighbors.KNeighborsClassifier(),
            "Decision Tree": tree.DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier()
        }

        self.predicted_scores_and_results = {
            "Linear Regression": {
                "score": None,
                "result": None
            },
            "Lasso": {
                "score": None,
                "result": None
            },
            "Ridge": {
                "score": None,
                "result": None
            }
        }

        self.classifier_scores_and_results = {
            "KNieghbors": {
                "score": None,
                "result": None
            },
            "Decision Tree": {
                "score": None,
                "result": None
            },
            "Random Forest": {
                "score": None,
                "result": None
            }
        }

        self.df = df
        self.x_columns = x_columns
        self.y_column = y_column
        self.type = type
        self.model = model
        self.y_column_type = self.df[y_column].dtype

        self.inputs_value = {}
        self.panel = tk.Frame(self.window)
        self.lblTitle = tk.Label(self.panel, text=model, bg=None, fg="black", font="none 18 bold")

        self.lblResult = tk.Label(self.panel, text="Resultado", bg="white", fg="black", font="none 14 bold")
        self.btnMoreResults = tk.Button(self.panel, text="+", command=self.open_more_results)
        self.lblScore = tk.Label(self.panel, text="Score")

        # Inputs
        self.container = tk.Frame(self.panel, bg='white')
        self.scrollbar = tk.Scrollbar(self.container, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas = tk.Canvas(self.container, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.inputs_container = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inputs_container, anchor=tk.NW)
        self.scrollbar.config(command=self.canvas.yview)

        # Se agregan los inputs
        self.upload_inputs(x_columns)
        self.inputs_container.update_idletasks()
        self.inputs_container.pack(fill=tk.BOTH, expand=True)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        self.btnAction = tk.Button(self.panel, text="Predecir", bg="blue", fg="white", font="none 16 bold", command=self.model_action)

        self.panel.pack(fill=tk.BOTH, expand=True)
        self.lblTitle.pack()
        self.lblResult.pack()
        self.btnMoreResults.pack()
        self.lblScore.pack()
        self.container.pack(fill=tk.BOTH, expand=True)
        self.btnAction.pack()

        self.lblResult.place(x=100, y=50, width=300, height=40)
        self.btnMoreResults.place(x=410, y=50, width=40, height=40)
        self.lblScore.place(x=0, y=100, width=500, height=40)
        self.container.place(x=50, y=200, width=400, height=400)
        self.btnAction.place(x=150, y=625, width=200, height=50)

        if type == "predicted":
            self.btnAction["text"] = "Predecir"
        elif type == "classifier":
            self.btnAction["text"] = "Clasificar"
        self.train_df()
        # self.show_df()

    def open_more_results(self):
        data = ""
        if not self.button_result_pressed:
            messagebox.showinfo("Resultados", "Primero debe presionar el botón de predecir o clasificar")
            return
        if self.type == "predicted":
            for model_name in self.predicted_scores_and_results:
                model_data = self.predicted_scores_and_results[model_name]
                data += f'{model_name}: Score: {model_data["score"]}, Resultado: {model_data["result"]}\n'
        elif self.type == "classifier":
            for model_name in self.classifier_scores_and_results:
                model_data = self.classifier_scores_and_results[model_name]
                data += f'{model_name}: Score: {model_data["score"]}, Resultado: {model_data["result"]}\n'
        messagebox.showinfo("Resultados", data)


    def upload_inputs(self, x_columns):
        for column_name in x_columns:
            lblInput = tk.Label(self.inputs_container, text=column_name, bg="white", fg="black", font="none 12 bold")
            column_type = self.df[column_name].dtype
            input_value = None
            if column_type == "object":
                input_value = tk.StringVar()
            elif column_type == "int64":
                input_value = tk.IntVar()
            elif column_type == "float64":
                input_value = tk.DoubleVar()
            else:
                input_value = tk.StringVar()
            lblInput.pack(fill=tk.X)
            # Se verifica si tiene menos de 10 valores unicos
            if self.is_classifier(column_name):
                options = self.df[column_name].unique()
                input_value.set(options[0])
                dropdown = tk.OptionMenu(self.inputs_container, input_value, *options)
                dropdown.pack(fill=tk.X, pady=10)
            else:
                entry = tk.Entry(self.inputs_container, textvariable=input_value, bg="white", fg="black", font="none 12 bold")
                entry.pack(fill=tk.X, pady=10)
            self.inputs_value[column_name] = input_value

    def is_classifier(self, column):
        return self.df[column].unique().size <= 10
    
    def clean_df(self):
        # X
        for column_name in self.x_columns:
            if self.df[column_name].dtype == "object":
                self.df[column_name] = self.df[column_name].map(self.map_column(column_name))
            self.df[column_name] = self.df[column_name].fillna(ceil(self.df[column_name].mean()))
        # Y
        if self.df[self.y_column].dtype == "object":
            map_values = self.map_column(self.y_column)
            if self.type == 'classifier':
                self.y_labels = self.set_y_labels(map_values)
            self.df[self.y_column] = self.df[self.y_column].map(map_values)
        self.df[self.y_column] = self.df[self.y_column].fillna(ceil(self.df[self.y_column].mean()))

    def map_column(self, column_name):
        unique_values = self.df[column_name].unique()
        unique_without_nan = unique_values[~pd.isnull(unique_values)]
        map_values = {}
        for i in range(len(unique_without_nan)):
            map_values[unique_without_nan[i]] = i
        self.all_map_values[column_name] = map_values
        return map_values
    
    def set_y_labels(self, map_values):
        labels = {}
        for key in map_values:
            labels[map_values[key]] = key
        return labels
    
    def train_df(self):
        self.clean_df()
        colunms_drop = []
        colunms_drop.append(self.y_column)
        for column in self.df.columns:
            if column not in self.x_columns:
                colunms_drop.append(column)
        X = self.df.drop(colunms_drop, axis=1)
        Y = self.df[self.y_column]

        train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.1)
        if self.type == "predicted":
            for model_name in self.predicted_models:
                model = self.predicted_models[model_name]
                model.fit(train_x, train_y)
                score = round(model.score(test_x, test_y), 4) * 100
                if self.model == model_name:
                    self.lblScore["text"] = "Score: " + str(score) + "%"
                self.predicted_scores_and_results[model_name]["score"] = score
        elif self.type == "classifier":
            for model_name in self.classifier_models:
                model = self.classifier_models[model_name]
                model.fit(train_x, train_y)
                score = round(model.score(test_x, test_y), 4) * 100
                if self.model == model_name:
                    self.lblScore["text"] = "Score: " + str(score) + "%"
                self.classifier_scores_and_results[model_name]["score"] = score

    def show_df(self):
        print(self.df.describe())

    def model_action(self):
        values = []
        count = 0
        for value in self.inputs_value.values():
            if type(value.get()).__name__ == "str":
                input_map = self.all_map_values[self.x_columns[count]]
                value_mapped = input_map[value.get()]
                values.append(value_mapped)
            else:
                values.append(value.get())
            count += 1
        if self.type == "predicted":
            self.predict(values, self.predicted_models)
        elif self.type == "classifier":
            self.predict(values, self.classifier_models)

    def predict(self, values, models_dict):
        self.button_result_pressed = True
        for model_name in models_dict:
                model = models_dict[model_name]
                prediction = model.predict([values])
                prediction_value = prediction[0]
                if self.type == "classifier":
                    if self.model == model_name and self.y_column_type == "object":
                        self.lblResult["text"] = "Resultado: " + self.y_labels[prediction_value]
                        self.classifier_scores_and_results[model_name]["result"] = self.y_labels[prediction_value]
                    elif self.model == model_name:
                        self.lblResult["text"] = "Resultado: " + str(round(prediction_value, 4))
                        self.classifier_scores_and_results[model_name]["result"] = str(round(prediction_value, 4))
                    else :
                        self.classifier_scores_and_results[model_name]["result"] = str(round(prediction_value, 4))
                elif self.type == "predicted":
                    if self.model == model_name:
                        self.lblResult["text"] = "Resultado: " + str(round(prediction_value, 4))
                    self.predicted_scores_and_results[model_name]["result"] = str(round(prediction_value, 4))

    def get_column_name(self, index):
        return self.df.columns[index]
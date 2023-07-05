import pandas as pd
from sklearn.preprocessing import LabelEncoder


class Cleaner:
    def __init__(self, df):
        self.df = df

    def clean_df(self):
        na_columns = []
        for column in self.df.columns:
            if self.df[column].isna().sum() > len(self.df) * 0.15:
                na_columns.append(column)
            elif self.df[column].unique().size == self.df[column].size:
                na_columns.append(column)
            else:
                if self.df[column].dtype == "object":
                # Si es una columna de tipo "object", se realiza una codificación numérica
                    self.df[column].fillna("", inplace=False)
                    label_encoder = LabelEncoder()
                    self.df[column] = label_encoder.fit_transform(self.df[column])
                    # mapping_table_data.extend(
                    #     [(column, label_encoder.classes_[i], i) for i in range(len(label_encoder.classes_))])
                elif self.df[column].dtype == "float64" or self.df[column].dtype == "int64":
                    # Si es una columna numérica, se rellenan los valores faltantes con la media
                    self.df[column] = self.df[column].fillna(self.df[column].mean(), inplace=False)
                else:
                    na_columns.append(column)
        self.df = self.df.drop(na_columns, axis=1, inplace=False)

    def get_df(self):
        print(self.df)
        return self.df

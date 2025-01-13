import os
import logging
import mlflow
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from file_handler import FileHandler
class TrainModel():
    def __init__(self, model, name):
        self.model = model
        self.name = name
        self.file_handler = FileHandler()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def scaler(self):
        scaler = StandardScaler()
        return scaler

    def train(self, X, y, model_type):
        mlflow.set_experiment(self.name)
        mlflow.sklearn.autolog()

        train_pipe = Pipeline(
            [('Scaling', self.scaler()),
             (self.name, self.model)])

        pipe = train_pipe.fit(X, y)
        self.file_handler.save_model(pipe.steps[1][1], str(self.name + "_" + model_type))

    def train_sales(self):
        train_features_path = os.path.join(self.base_dir, '../features/train_features.csv')
        target_sales_path = os.path.join(self.base_dir, '../features/target_sales.csv')
        X = pd.read_csv(train_features_path)
        y = pd.read_csv(target_sales_path)
        self.train(X, y, 'Sales')

    def train_customers(self):
        train_features_path = os.path.join(self.base_dir, '../features/train_features.csv')
        target_customers_path = os.path.join(self.base_dir, '../features/target_customers.csv')
        X = pd.read_csv(train_features_path)
        y = pd.read_csv(target_customers_path)
        self.train(X, y, 'Customers')

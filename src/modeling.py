import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

class ModelBuilder:
    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.models = {}
        self.results = {}

    def train_linear_regression(self):
        print("Training Linear Regression...")
        model = LinearRegression()
        model.fit(self.X_train, self.y_train)
        self.models['LinearRegression'] = model
        return model

    def train_random_forest(self):
        print("Training Random Forest (this may take time)...")
        # n_estimators=50 to save time, use 100+ for production
        model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
        model.fit(self.X_train, self.y_train)
        self.models['RandomForest'] = model
        return model

    def train_xgboost(self):
        print("Training XGBoost...")
        model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42, n_jobs=-1)
        model.fit(self.X_train, self.y_train)
        self.models['XGBoost'] = model
        return model

    def evaluate_models(self):
        print("\n--- Model Evaluation ---")
        metrics_list = []
        
        for name, model in self.models.items():
            preds = model.predict(self.X_test)
            
            mse = mean_squared_error(self.y_test, preds)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(self.y_test, preds)
            r2 = r2_score(self.y_test, preds)
            
            metrics_list.append({
                'Model': name,
                'RMSE': rmse,
                'MAE': mae,
                'R2 Score': r2
            })
            print(f"{name} -> RMSE: {rmse:.2f}, R2: {r2:.4f}")
            
        return pd.DataFrame(metrics_list)
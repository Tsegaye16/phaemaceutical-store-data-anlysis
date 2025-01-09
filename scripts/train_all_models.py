from train_model import TrainModel
from lightgbm import LGBMRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

def train_all_models():
    models = [
        (LGBMRegressor(), "Light GBM Regressor"),
        (LinearRegression(), "Linear Regression"),
        (RandomForestRegressor(n_jobs=-1, n_estimators=15, verbose=True, max_depth=15, min_samples_split=2, min_samples_leaf=1), "Random Forest Regressor"),
        (XGBRegressor(), "XGB Regressor")
    ]
    
    # Train models for sales
    for model, name in models:
        train_model = TrainModel(model, name)
        train_model.train_sales()

    # Train models for customers
    for model, name in models:
        train_model = TrainModel(model, name)
        train_model.train_customers()

if __name__ == "__main__":
    train_all_models()

##//////////////////////////////////

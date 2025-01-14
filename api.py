from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import pickle
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Initialize FastAPI
app = FastAPI()

# Load models
models = {
    "LightGBM": "models/Light GBM Regressor_Sales 2025-01-10-09_05_43.pkl",
    "Random Forest": "models/Random Forest Regressor_Sales 2025-01-10-09_07_20.pkl",
    "Linear Regression": "models/Linear Regression_Sales 2025-01-10-09_06_17.pkl",
    "XGBoost": "models/XGB Regressor_Sales 2025-01-10-09_07_48.pkl"
}

loaded_models = {}
for name, path in models.items():
    try:
        with open(path, "rb") as f:
            loaded_models[name] = pickle.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Model file for {name} not found at {path}")

@app.get("/")
def root():
    return {"message": "Welcome to the ML Model Comparison API"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not (file.filename.endswith(".csv") or file.filename.endswith(".xlsx")):
        raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported.")

    try:
        if file.filename.endswith(".csv"):
            data = pd.read_csv(file.file)
        else:
            data = pd.read_excel(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

    # Strip column names and handle case sensitivity
    data.columns = data.columns.str.strip()
    if "Sales".lower() not in map(str.lower, data.columns):
        raise HTTPException(status_code=400, detail=f"'Sales' column not found. Columns: {data.columns.tolist()}")

    # Process features and target
    feature_cols = [col for col in data.columns if col.lower() != "sales"]
    if not feature_cols:
        raise HTTPException(status_code=400, detail="No features found in the file.")

    X = data[feature_cols]
    y = data["Sales"]

    results = {}
    for model_name, model in loaded_models.items():
        try:
            predictions = model.predict(X)
            mae = mean_absolute_error(y, predictions)
            mse = mean_squared_error(y, predictions)
            r2 = r2_score(y, predictions)

            results[model_name] = {
                "MAE": mae,
                "MSE": mse,
                "R2": r2,
                "Predictions": predictions.tolist()
            }
        except Exception as e:
            results[model_name] = {"error": str(e)}

    best_model = max(results, key=lambda m: results[m]["R2"] if "R2" in results[m] else float("-inf"))
    response = {
        "best_model": best_model,
        "best_model_metrics": results[best_model],
        "all_models": results
    }
    return JSONResponse(content=response)


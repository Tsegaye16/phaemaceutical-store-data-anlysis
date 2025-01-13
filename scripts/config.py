import os
from pathlib import Path

class Config:
    RANDOM_SEED = 42
    ASSETS_PATH = Path("E:/Development/10-Accademy/phaemaceutical-store-data-anlysis")
    REPO = "E:/Development/10-Accademy/phaemaceutical-store-data-anlysis"
    DATASET_FILE_PATH = "data/train.csv"
    DATASET_PATH = ASSETS_PATH / "data"
    FEATURES_PATH = ASSETS_PATH / "features"
    MODELS_PATH = ASSETS_PATH / "models"
    LOGS_PATH = ASSETS_PATH / "logs"
    OUTPUT_PATH = ASSETS_PATH / "output"
       

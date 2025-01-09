from pathlib import Path

class Config:
    # Seed for reproducibility
    RANDOM_SEED = 42  # Adjust as needed
    
    # Base path for the project
    ASSETS_PATH = Path("E:/Development/10-Accademy/phaemaceutical-store-data-anlysis")
    
    # Repository path
    REPO = "E:/Development/10-Accademy/phaemaceutical-store-data-anlysis"
    
    # Dataset paths
    DATASET_FILE_PATH = "data/train.csv"  # Assuming your dataset is named 'train.csv'
    DATASET_PATH = ASSETS_PATH / "data"
    
    # Features and models paths
    FEATURES_PATH = ASSETS_PATH / "features"
    MODELS_PATH = ASSETS_PATH / "models"
    
    # Additional paths (optional)
    LOGS_PATH = ASSETS_PATH / "logs"  # Directory for log files
    OUTPUT_PATH = ASSETS_PATH / "output"  # Directory for output files

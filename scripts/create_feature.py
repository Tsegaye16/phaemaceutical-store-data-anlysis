import os
import sys
import pandas as pd
from config import Config
from sklearn.preprocessing import LabelEncoder

sys.path.append(os.path.abspath(os.path.join('../scripts')))
from file_handler import FileHandler

# Ensure output directory exists
Config.FEATURES_PATH.mkdir(parents=True, exist_ok=True)

file_handler = FileHandler()

# Load datasets
train_df = file_handler.read_csv(str(Config.DATASET_PATH / "train.csv"))
test_df = file_handler.read_csv(str(Config.DATASET_PATH / "test.csv"))
store_df = file_handler.read_csv(str(Config.DATASET_PATH / "store.csv"))

def merge(df, store):
    """Merge dataset with store information."""
    return pd.merge(df, store, on='Store', how='left')

def get_part_of_month(day):
    """Determine part of the month."""
    if day < 10:
        return 0
    elif day < 20:
        return 1
    else:
        return 2

def preprocess_dataframe(df):
    """Preprocess and create new features."""
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['DayOfMonth'] = df['Date'].dt.day
    df['WeekOfYear'] = df['Date'].apply(lambda x: x.isocalendar().week)
    df['weekday'] = df['DayOfWeek'].apply(lambda x: 0 if x in [6, 7] else 1)
    df.loc[:, "part_of_month"] = df["DayOfMonth"].apply(get_part_of_month)
    return df

def encode_categorical_columns(df, columns):
    """Encode categorical columns using LabelEncoder."""
    lb = LabelEncoder()
    for col in columns:
        df[col] = df[col].astype(str)
        df[col] = lb.fit_transform(df[col])
    return df

def extract_test_features(df):
    """Extract features for the test set."""
    df = merge(df, store_df)
    df = preprocess_dataframe(df)
    df = encode_categorical_columns(df, ['StateHoliday', 'Assortment', 'StoreType'])
    df = df.drop(columns=['Id', 'PromoInterval', 'Date'], axis=1, errors='ignore')
    return df

def extract_features(df):
    """Extract features for the training set."""
    df = preprocess_dataframe(df)
    df = encode_categorical_columns(df, ['StateHoliday', 'Assortment', 'StoreType'])
    df = df.drop(columns=['Sales', 'Customers', 'PromoInterval', 'Date'], axis=1, errors='ignore')
    return df

def extract_target(df, target_column):
    """Extract target column."""
    return df[[target_column]]

# Preprocess and extract features
train_df = train_df[train_df['Open'] == 1]
train_features = extract_features(train_df)
test_features = extract_test_features(test_df)

target_sales = extract_target(train_df, "Sales")
target_customers = extract_target(train_df, "Customers")

# Save preprocessed data
train_features.to_csv(str(Config.FEATURES_PATH / "train_features.csv"), index=False)
test_features.to_csv(str(Config.FEATURES_PATH / "test_features.csv"), index=False)
target_sales.to_csv(str(Config.FEATURES_PATH / "target_sales.csv"), index=False)
target_customers.to_csv(str(Config.FEATURES_PATH / "target_customers.csv"), index=False)

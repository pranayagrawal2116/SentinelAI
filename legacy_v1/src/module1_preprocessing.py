import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.datasets import make_classification
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')

def get_iot_data(filepath=None, use_synthetic=False, max_rows=2500000):
    '''
    Loads IoT Network Traffic Data.
    If use_synthetic is False, it loads real data from 'filepath'.
    max_rows=2500000 loads approximately 1 GB of text/CSV data into memory.
    '''
    if use_synthetic:
        print("[Module 1] Generating synthetic IoT Network Traffic data...")
        X, y = make_classification(
            n_samples=10000, 
            n_features=40, 
            n_informative=15, 
            n_redundant=10, 
            n_classes=4, 
            weights=[0.6, 0.2, 0.1, 0.1], # Imbalanced data
            random_state=42
        )
        
        feature_names = [f'flow_feature_{i}' for i in range(1, 41)]
        df = pd.DataFrame(X, columns=feature_names)
        
        target_mapping = {0: 'Benign', 1: 'DDoS', 2: 'Recon', 3: 'BruteForce'}
        df['label'] = pd.Series(y).map(target_mapping)
        return df
    else:
        if filepath is None:
            raise ValueError("Please provide a valid filepath to the dataset.")
        
        print(f"[Module 1] Loading real data from {filepath}...")
        print(f"  -> Limiting to {max_rows} rows (approx. 1GB of CSV data) to save memory.")
        
        try:
            df = pd.read_csv(filepath, nrows=max_rows)
        except FileNotFoundError:
            print(f"Error: Could not find {filepath}. Please ensure the dataset is downloaded and in the right folder.")
            raise
        
        print("  -> Shuffling data to ensure an even distribution of attack classes...")
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        return df

def preprocess_data(df, target_col='label'):
    if target_col not in df.columns:
        possible_targets = ['Label', 'attack_type', 'Attack_type']
        for p_t in possible_targets:
            if p_t in df.columns:
                target_col = p_t
                break
                
    print(f"[Module 1] Starting Data Preprocessing (Target column: '{target_col}')...")
    
    # 1. Clean Data (Handle NaN and Inf)
    print(f"  -> Initial shape: {df.shape}")
    df.drop_duplicates(inplace=True)
    
    # CRITICAL FIX: IoT network features often contain Infinity due to divide-by-zero errors in Flow Rate calculations.
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    print(f"  -> Shape after cleaning (removed Inf and NaN): {df.shape}")
    
    # 2. Separate Features and Target
    X = df.drop(columns=[target_col])
    
    cols_to_drop = [c for c in ['id', 'ID', 'flow_id', 'timestamp', 'Flow ID', 'Timestamp'] if c in X.columns]
    if cols_to_drop:
        print(f"  -> Dropping irrelevant identifiers/timestamps to prevent data leakage: {cols_to_drop}")
        X.drop(columns=cols_to_drop, inplace=True)
        
    y_raw = df[target_col]
    
    # 3. Encode Categorical Target
    le = LabelEncoder()
    y = le.fit_transform(y_raw)
    class_names = le.classes_
    print(f"  -> Classes detected: {len(class_names)} unique classes")
    
    # 4. Train-Test Split (Prevent Data Leakage)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # 5. Feature Scaling
    print("  -> Scaling features using StandardScaler...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X.columns)
    
    # 6. Address Class Imbalance
    if len(y_train) > 200000:
        print("  -> Dataset is very large! Skipping SMOTE to avoid RAM crash (OOM error).")
        print("  -> Imbalance will be handled dynamically by the models in Module 3 using class weights.")
        X_train_res, y_train_res = X_train_scaled, y_train
    else:
        print("  -> Addressing class imbalance with SMOTE (Synthetic Data Generation)...")
        smote = SMOTE(random_state=42)
        X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)
    
    print("[Module 1] Preprocessing Complete.")
    return X_train_res, X_test_scaled, y_train_res, y_test, X.columns, class_names

if __name__ == "__main__":
    df = get_iot_data(use_synthetic=True)
    X_train, X_test, y_train, y_test, feats, classes = preprocess_data(df)

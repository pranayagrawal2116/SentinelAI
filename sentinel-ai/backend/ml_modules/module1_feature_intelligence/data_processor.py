import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

class DataProcessor:
    """
    Handles data loading, inspection, cleaning, and leakage-safe preprocessing.
    """
    def __init__(self, target_column: str = 'label'):
        self.target_column = target_column
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
        # Track statistics for explainability and dashboard
        self.stats: Dict[str, Any] = {}

    def load_and_clean_data(self, filepath: str) -> pd.DataFrame:
        """Loads data, performs missing/duplicate analysis, and removes leak-prone fields."""
        print(f"[Module 1] Loading dataset from {filepath}...")
        df = pd.read_csv(filepath)
        
        # 1. Dataset Inspection & Statistics
        original_shape = df.shape
        self.stats['original_records'] = original_shape[0]
        self.stats['original_features'] = original_shape[1] - 1  # Excluding target
        
        # 2. Missing value analysis
        missing_counts = df.isnull().sum().sum()
        self.stats['missing_values_found'] = int(missing_counts)
        
        # Infinite values handling (common in flow data due to divide by zero)
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)
        
        # 3. Duplicate analysis
        duplicates = df.duplicated().sum()
        self.stats['duplicates_found'] = int(duplicates)
        df.drop_duplicates(inplace=True)
        
        self.stats['clean_records'] = df.shape[0]
        
        # 4. Identification of irrelevant/leakage-prone fields
        leakage_fields = [col for col in ['id', 'flow_id', 'timestamp', 'src_ip', 'dst_ip'] if col.lower() in [c.lower() for c in df.columns]]
        if leakage_fields:
            print(f"[Module 1] Removing leakage-prone fields: {leakage_fields}")
            # Case insensitive drop
            drop_cols = [c for c in df.columns if c.lower() in [l.lower() for l in leakage_fields]]
            df.drop(columns=drop_cols, inplace=True)
            
        self.stats['final_features_pre_selection'] = df.shape[1] - 1
        
        # 5. Class distribution analysis
        if self.target_column not in df.columns:
            # Fallback auto-detect target
            for col in ['Label', 'attack_type', 'Attack_type']:
                if col in df.columns:
                    self.target_column = col
                    break
                    
        self.stats['class_distribution'] = df[self.target_column].value_counts().to_dict()
        print(f"[Module 1] Cleaned data shape: {df.shape}")
        
        return df

    def split_and_preprocess(self, df: pd.DataFrame, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, List[str]]:
        """
        CRITICAL REQUIREMENT: Prevent data leakage.
        Learned preprocessing must be fitted ONLY on training data.
        """
        print("[Module 1] Performing leakage-safe train/test split...")
        X = df.drop(columns=[self.target_column])
        y_raw = df[self.target_column]
        
        # Encode targets
        y = pd.Series(self.label_encoder.fit_transform(y_raw), index=y_raw.index)
        self.stats['classes'] = self.label_encoder.classes_.tolist()
        
        # Stratified Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        feature_names = X_train.columns.tolist()
        
        # Fit scaler ONLY on training data, then transform both
        print("[Module 1] Applying Training-only preprocessing (Scaling)...")
        X_train_scaled = pd.DataFrame(self.scaler.fit_transform(X_train), columns=feature_names, index=X_train.index)
        X_test_scaled = pd.DataFrame(self.scaler.transform(X_test), columns=feature_names, index=X_test.index)
        
        return X_train_scaled, X_test_scaled, y_train, y_test, feature_names

    def get_stats(self) -> Dict[str, Any]:
        return self.stats

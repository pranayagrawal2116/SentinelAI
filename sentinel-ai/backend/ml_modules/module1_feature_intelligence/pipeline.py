import os
import json
import joblib
from typing import Dict, Any, List
from .data_processor import DataProcessor
from .feature_selectors import HybridFeatureSelector

class Module1Pipeline:
    """
    Orchestrates Module 1: Hybrid Network Feature Intelligence.
    Loads data, cleans it, splits, runs hybrid feature selection, and saves state.
    """
    def __init__(self, data_path: str, target_features: int = 20, output_dir: str = None):
        self.data_path = data_path
        self.target_features = target_features
        if output_dir is None:
            if os.path.exists('experiments') or not os.path.exists('sentinel-ai/backend'):
                self.output_dir = 'experiments'
            else:
                self.output_dir = 'sentinel-ai/backend/experiments'
        else:
            self.output_dir = output_dir
        self.processor = DataProcessor()
        self.selector = HybridFeatureSelector(target_features=target_features)
        
    def run(self) -> Dict[str, Any]:
        print("\n" + "="*50)
        print(" MODULE 1: HYBRID NETWORK FEATURE INTELLIGENCE")
        print("="*50)
        
        # 1. Load and clean
        df = self.processor.load_and_clean_data(self.data_path)
        
        # 2. Prevent Data Leakage via safe split and preprocessing
        X_train, X_test, y_train, y_test, all_features = self.processor.split_and_preprocess(df)
        
        # 3. Hybrid Feature Selection
        # To avoid RAM crashes and massive delays on huge datasets, we can sample down for RFE/Tree training 
        # (This is an optimization for Module 1 speed, actual training uses all records)
        sample_size = min(100000, X_train.shape[0])
        X_train_sample = X_train.sample(n=sample_size, random_state=42)
        y_train_sample = y_train.loc[X_train_sample.index]
        
        final_features = self.selector.select_features(X_train_sample, y_train_sample)
        
        # 4. Apply selection
        X_train_selected = X_train[final_features]
        X_test_selected = X_test[final_features]
        
        # 5. Compile Statistics
        stats = {
            "data_stats": self.processor.get_stats(),
            "feature_selection_stats": self.selector.get_stats()
        }
        
        # 6. Save artifacts (Reproducibility requirement)
        self._save_artifacts(X_train_selected, X_test_selected, y_train, y_test, all_features, final_features, stats)
        
        print("\n[Module 1] Pipeline complete. Artifacts saved for Module 2.")
        return stats

    def _save_artifacts(self, X_train, X_test, y_train, y_test, all_features, final_features, stats):
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Save datasets to disk (so Module 2 and 3 can pick them up)
        X_train.to_parquet(os.path.join(self.output_dir, 'X_train.parquet'))
        X_test.to_parquet(os.path.join(self.output_dir, 'X_test.parquet'))
        y_train.to_frame(name='label').to_parquet(os.path.join(self.output_dir, 'y_train.parquet'))
        y_test.to_frame(name='label').to_parquet(os.path.join(self.output_dir, 'y_test.parquet'))
        
        # Save full feature test set as well for Experiment 1 & 3
        # We need the pre-selected data to compare Full vs Selected
        full_output_dir = os.path.join(self.output_dir, 'full_features')
        os.makedirs(full_output_dir, exist_ok=True)
        
        # We'll just save the scaler and encoders for full data, we'll let Module 2 handle the Full data if needed,
        # but to save disk space, let's just serialize the processor objects.
        joblib.dump(self.processor.scaler, os.path.join(self.output_dir, 'scaler.pkl'))
        joblib.dump(self.processor.label_encoder, os.path.join(self.output_dir, 'label_encoder.pkl'))
        
        # Save run stats
        with open(os.path.join(self.output_dir, 'module1_stats.json'), 'w') as f:
            json.dump(stats, f, indent=4)
        
        # Save feature lists
        with open(os.path.join(self.output_dir, 'features.json'), 'w') as f:
            json.dump({
                "all_features": all_features,
                "selected_features": final_features
            }, f, indent=4)

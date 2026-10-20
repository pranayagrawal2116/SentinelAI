import time
import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, HistGradientBoostingClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from catboost import CatBoostClassifier

class DetectionEngine:
    def __init__(self, models_dir: str = None):
        if models_dir is None:
            if os.path.exists('models') or not os.path.exists('sentinel-ai/backend'):
                self.models_dir = 'models'
            else:
                self.models_dir = 'sentinel-ai/backend/models'
        else:
            self.models_dir = models_dir
        os.makedirs(self.models_dir, exist_ok=True)
        
    def _get_base_models(self) -> Dict[str, Any]:
        """Returns instantiated base models with class weighting."""
        # Using HistGradientBoosting as a cross-platform LightGBM equivalent
        return {
            'Random Forest': RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1),
            'CatBoost': CatBoostClassifier(iterations=100, auto_class_weights='Balanced', random_state=42, verbose=0),
            'LightGBM_equiv': HistGradientBoostingClassifier(class_weight='balanced', random_state=42),
            'SVM_Baseline': CalibratedClassifierCV(LinearSVC(class_weight='balanced', random_state=42))
        }

    def train_models(self, X_train: pd.DataFrame, y_train: pd.Series, experiment_id: str) -> Dict[str, Any]:
        print(f"[Module 2] Training models for experiment {experiment_id}...")
        base_models = self._get_base_models()
        trained_models = {}
        training_stats = {}
        
        for name, model in base_models.items():
            print(f"  -> Training {name}...")
            start_time = time.time()
            model.fit(X_train, y_train)
            train_time = time.time() - start_time
            
            trained_models[name] = model
            training_stats[name] = {"train_time_ms": int(train_time * 1000)}
            
            # Serialize model
            model_path = os.path.join(self.models_dir, f"{experiment_id}_{name.replace(' ', '_')}.pkl")
            joblib.dump(model, model_path)
            training_stats[name]["model_path"] = model_path

        # Create and train Soft Voting Ensemble
        print("  -> Training Soft Voting Ensemble...")
        estimators = [(name, model) for name, model in trained_models.items() if name != 'SVM_Baseline']
        ensemble = VotingClassifier(estimators=estimators, voting='soft')
        
        start_time = time.time()
        ensemble.fit(X_train, y_train)
        train_time = time.time() - start_time
        
        ensemble_path = os.path.join(self.models_dir, f"{experiment_id}_Ensemble.pkl")
        joblib.dump(ensemble, ensemble_path)
        
        training_stats['Ensemble'] = {
            "train_time_ms": int(train_time * 1000),
            "model_path": ensemble_path
        }
        
        return training_stats

    def predict(self, model_path: str, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Loads a model and generates predictions and probabilities."""
        model = joblib.load(model_path)
        preds = model.predict(X)
        probs = model.predict_proba(X) if hasattr(model, 'predict_proba') else None
        return preds, probs

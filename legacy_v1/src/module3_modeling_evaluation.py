import time
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, HistGradientBoostingClassifier
from catboost import CatBoostClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
from sklearn.calibration import CalibratedClassifierCV
import warnings
warnings.filterwarnings('ignore')

def train_and_evaluate_models(X_train, X_test, y_train, y_test, class_names, experiment_name=""):
    print(f"\n[Module 3] Running Modeling & Evaluation: {experiment_name}")
    
    results = []
    
    # Define Classifiers with built-in class weight balancing
    # This prevents the models from ignoring rare attacks even if SMOTE was skipped
    rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1)
    
    # Replaced XGBoost/LightGBM with CatBoost and HistGradientBoosting (Scikit-Learn's LightGBM equivalent) 
    # to ensure compatibility with Mac OSX environments missing 'libomp'.
    cat = CatBoostClassifier(iterations=100, auto_class_weights='Balanced', random_state=42, verbose=0)
    
    hgboost = HistGradientBoostingClassifier(class_weight='balanced', random_state=42)
    
    # LinearSVC baseline with balanced class weights
    svm_base = LinearSVC(class_weight='balanced', random_state=42)
    # Wrapped in CalibratedClassifierCV to get probabilities required for soft voting ensemble
    svm = CalibratedClassifierCV(svm_base)
    
    # Ensemble (Soft Voting)
    ensemble = VotingClassifier(
        estimators=[('RF', rf), ('CatBoost', cat), ('HGBoost', hgboost)],
        voting='soft'
    )
    
    models = {
        'Random Forest': rf,
        'CatBoost': cat,
        'HistGradBoost (LightGBM equivalent)': hgboost,
        'SVM (Baseline)': svm,
        'Ensemble (Soft Voting)': ensemble
    }
    
    for name, model in models.items():
        print(f"  -> Training {name}...")
        
        # Training Time
        start_time = time.time()
        model.fit(X_train, y_train)
        train_time = time.time() - start_time
        
        # Inference Time
        start_time = time.time()
        y_pred = model.predict(X_test)
        inference_time = time.time() - start_time
        
        # Metrics
        acc = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
        
        results.append({
            'Experiment': experiment_name,
            'Model': name,
            'Accuracy': acc,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1,
            'Training Time (s)': round(train_time, 4),
            'Inference Time (s)': round(inference_time, 4)
        })
        
        print(f"     Accuracy: {acc:.4f} | F1: {f1:.4f}")
        
    results_df = pd.DataFrame(results)
    return results_df

def print_final_comparison(full_results_df):
    print("\n===========================================================")
    print("                FINAL EXPERIMENTAL RESULTS                 ")
    print("===========================================================")
    print(full_results_df.to_string(index=False))
    print("===========================================================\n")
    print("[Module 3] Evaluation complete.")

if __name__ == "__main__":
    from module1_preprocessing import get_iot_data, preprocess_data
    from module2_feature_selection import hybrid_feature_selection, apply_feature_selection
    
    df = get_iot_data(use_synthetic=True)
    X_train, X_test, y_train, y_test, feats, classes = preprocess_data(df)
    
    res = train_and_evaluate_models(X_train, X_test, y_train, y_test, classes, "Full Features Test")
    print_final_comparison(res)

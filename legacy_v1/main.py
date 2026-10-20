"""
Main script for IoT Intrusion Detection Project.
This script combines all 3 modules to run the complete pipeline.
"""

from src.module1_preprocessing import get_iot_data, preprocess_data
from src.module2_feature_selection import hybrid_feature_selection, apply_feature_selection
from src.module3_modeling_evaluation import train_and_evaluate_models, print_final_comparison
import pandas as pd

def main():
    print("=====================================================")
    print("  IoT Intrusion Detection Machine Learning Pipeline  ")
    print("=====================================================")

    # ---------------------------------------------------------
    # MODULE 1: Data Engineering & Preprocessing
    # ---------------------------------------------------------
    # We set use_synthetic=False to load real data.
    # Provide the exact path to your dataset CSV file here.
    # max_rows=2500000 ensures it only pulls ~1GB of data from the massive CSV.
    try:
        df = get_iot_data(
            filepath='ciciot2023.csv', # <-- Replace with your downloaded dataset name if different
            use_synthetic=False,       # Set to False to use the real dataset
            max_rows=2500000           # Limits the load to roughly 1 GB of data
        )
    except FileNotFoundError:
        print("\n[!] Dataset 'ciciot2023.csv' not found. Falling back to synthetic data for demonstration...\n")
        df = get_iot_data(use_synthetic=True)
    
    X_train, X_test, y_train, y_test, feature_names, class_names = preprocess_data(df)

    # ---------------------------------------------------------
    # MODULE 2: Hybrid Feature Selection
    # ---------------------------------------------------------
    # Select top 15 features out of the total features
    selected_features = hybrid_feature_selection(X_train, y_train, feature_names, k=15)
    
    # Apply to train and test sets
    X_train_selected, X_test_selected = apply_feature_selection(X_train, X_test, selected_features)

    # ---------------------------------------------------------
    # MODULE 3: Modeling, Ensemble Learning & Evaluation
    # ---------------------------------------------------------
    # Experiment A: All Features
    results_full = train_and_evaluate_models(
        X_train, X_test, y_train, y_test, class_names, 
        experiment_name="Exp 1: Full Features"
    )
    
    # Experiment B: Selected Features
    results_selected = train_and_evaluate_models(
        X_train_selected, X_test_selected, y_train, y_test, class_names, 
        experiment_name="Exp 2: Hybrid Selected Features"
    )

    # Combine Results and Display
    final_results = pd.concat([results_full, results_selected], ignore_index=True)
    print_final_comparison(final_results)


if __name__ == "__main__":
    main()

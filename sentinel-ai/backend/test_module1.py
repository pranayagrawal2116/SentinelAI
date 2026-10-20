import sys
import os

# Add backend to path for direct testing
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ml_modules.module1_feature_intelligence.pipeline import Module1Pipeline
import pandas as pd
from sklearn.datasets import make_classification

def generate_mock_data():
    """Generates a small mock dataset for testing."""
    print("Generating mock dataset...")
    X, y = make_classification(
        n_samples=5000, 
        n_features=40, 
        n_informative=15, 
        n_redundant=10, 
        n_classes=4, 
        random_state=42
    )
    feature_names = [f'flow_feature_{i}' for i in range(1, 41)]
    df = pd.DataFrame(X, columns=feature_names)
    df['id'] = range(len(df)) # Irrelevant column
    df['src_ip'] = '192.168.1.1' # Leakage column
    target_mapping = {0: 'Benign', 1: 'DDoS', 2: 'Recon', 3: 'BruteForce'}
    df['label'] = pd.Series(y).map(target_mapping)
    
    # Introduce some NaNs and Infs
    df.loc[0, 'flow_feature_1'] = float('inf')
    df.loc[1, 'flow_feature_2'] = float('nan')
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/mock_ciciot.csv', index=False)
    return 'data/mock_ciciot.csv'

if __name__ == "__main__":
    data_path = generate_mock_data()
    
    pipeline = Module1Pipeline(
        data_path=data_path,
        target_features=15,
        output_dir='experiments/run_test'
    )
    
    stats = pipeline.run()
    
    print("\n--- Summary of Module 1 ---")
    print(f"Original Records: {stats['data_stats']['original_records']}")
    print(f"Clean Records: {stats['data_stats']['clean_records']}")
    print(f"Features before selection: {stats['data_stats']['final_features_pre_selection']}")
    print(f"Features after hybrid selection: {stats['feature_selection_stats']['hybrid_consensus_count']}")

import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import time

def split_massive_dataset(input_csv: str, train_out: str, frontend_out: str, chunk_size: int = 100000):
    """
    Safely processes massive datasets (e.g., 5GB+) without causing Out-of-Memory (OOM) crashes.
    Splits the data 50/50 randomly into a Training Set and a Frontend Simulation Set.
    """
    print(f"🚀 Initializing Massive Data Splitter for: {input_csv}")
    print(f"📦 Training Destination: {train_out}")
    print(f"🌐 Frontend Destination: {frontend_out}")
    
    # Check file size
    file_size_gb = os.path.getsize(input_csv) / (1024 ** 3)
    print(f"📊 Detected File Size: {file_size_gb:.2f} GB")
    
    # Initialize files with headers
    first_chunk = True
    
    # Count rows for progress bar (rough estimate: 1GB ~ 2.5M rows)
    estimated_rows = int(file_size_gb * 2500000)
    
    print("\n⏳ Processing and splitting data in chunks to save RAM...")
    
    try:
        # We use chunking to ensure a 5GB file doesn't consume 15GB of RAM in Pandas
        for chunk in tqdm(pd.read_csv(input_csv, chunksize=chunk_size), total=estimated_rows//chunk_size):
            # Shuffle the chunk
            chunk = chunk.sample(frac=1, random_state=42).reset_index(drop=True)
            
            # Split 50/50
            split_idx = len(chunk) // 2
            train_chunk = chunk.iloc[:split_idx]
            frontend_chunk = chunk.iloc[split_idx:]
            
            # Append to disk
            mode = 'w' if first_chunk else 'a'
            header = first_chunk
            
            train_chunk.to_csv(train_out, mode=mode, header=header, index=False)
            frontend_chunk.to_csv(frontend_out, mode=mode, header=header, index=False)
            
            first_chunk = False
            
        print("\n✅ Success! Dataset successfully split.")
        print(f"-> Model Training Data: ~{file_size_gb/2:.2f} GB")
        print(f"-> Frontend Simulator Data: ~{file_size_gb/2:.2f} GB")
        
    except FileNotFoundError:
        print(f"\n❌ Error: Could not find {input_csv}.")
        print("Please ensure your 5GB dataset is placed in the backend folder and named correctly.")

if __name__ == "__main__":
    # Create directories if they don't exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('demo_scenarios', exist_ok=True)
    
    # Example usage: Replace 'raw_5gb_ciciot.csv' with your actual downloaded file name
    # You can download the 5GB CSV manually via Kaggle or HuggingFace, put it in the backend folder, and run this.
    
    # Create a dummy file for testing the script if the real one doesn't exist yet
    if not os.path.exists('raw_5gb_ciciot.csv'):
        print("⚠️ 'raw_5gb_ciciot.csv' not found. Please download your 5GB dataset and name it 'raw_5gb_ciciot.csv'.")
        print("For now, this script is ready to run as soon as your file is downloaded!")
    else:
        split_massive_dataset(
            input_csv='raw_5gb_ciciot.csv',
            train_out='data/training_set.csv',
            frontend_out='demo_scenarios/frontend_test_set.csv'
        )

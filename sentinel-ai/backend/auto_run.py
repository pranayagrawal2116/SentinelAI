import os
import pandas as pd
import numpy as np
import time
from tqdm import tqdm
import urllib.request
import ssl
import sys

# We will grab a diverse 600MB+ slice of the dataset to represent the "full" pipeline
# while preventing a 30GB multi-hour download from crashing your Mac.
FILES_TO_DOWNLOAD = [
    "BenignTraffic.pcap.csv",
    "BenignTraffic1.pcap.csv",
    "DDoS-ICMP_Flood.pcap.csv",
    "DDoS-TCP_Flood.pcap.csv",
    "DDoS-UDP_Flood.pcap.csv",
    "DDoS-SYN_Flood.pcap.csv",
    "DDoS-PSHACK_Flood.pcap.csv",
    "DDoS-RSTFINFlood.pcap.csv",
    "DDoS-SlowLoris.pcap.csv",
    "DDoS-ICMP_Fragmentation.pcap.csv"
]

BASE_URL = "https://huggingface.co/datasets/baalajimaestro/DDoS-CICIoT2023/resolve/main/"

def download_data():
    print("==================================================")
    print(" 1. AUTONOMOUS DATA ACQUISITION ")
    print("==================================================")
    
    os.makedirs('data/raw', exist_ok=True)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    downloaded_files = []
    
    for filename in FILES_TO_DOWNLOAD:
        filepath = f"data/raw/{filename}"
        downloaded_files.append(filepath)
        if os.path.exists(filepath):
            print(f"[*] {filename} already exists, skipping.")
            continue
            
        url = BASE_URL + filename
        print(f"[*] Downloading {filename}...")
        try:
            # Using basic urllib to bypass Mac SSL issues
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
        except Exception as e:
            print(f"[!] Failed to download {filename}: {e}")
            
    return downloaded_files

def prepare_and_split(downloaded_files):
    print("\n==================================================")
    print(" 2. DATA PROCESSING & 50/50 SIMULATION SPLIT ")
    print("==================================================")
    
    train_out = 'data/training_set.csv'
    frontend_out = 'demo_scenarios/frontend_test_set.csv'
    
    os.makedirs('demo_scenarios', exist_ok=True)
    
    if os.path.exists(train_out) and os.path.exists(frontend_out):
        print("[*] Split datasets already exist. Skipping split.")
        return train_out
        
    print("[*] Merging raw files and appending labels...")
    
    dfs = []
    for filepath in tqdm(downloaded_files, desc="Processing CSVs"):
        if not os.path.exists(filepath): continue
        df = pd.read_csv(filepath)
        
        # The CICIoT2023 huggingface dataset hides labels in the filename!
        # We MUST extract the label from the filename (e.g. DDoS-ICMP_Flood)
        base_name = os.path.basename(filepath).replace('.pcap.csv', '')
        # Remove trailing numbers from split files like BenignTraffic1 -> BenignTraffic
        label = ''.join([i for i in base_name if not i.isdigit()])
        
        df['label'] = label
        dfs.append(df)
        
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"[*] Combined Dataset Shape: {combined_df.shape}")
    
    print("[*] Shuffling massive dataset randomly...")
    combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print("[*] Splitting 50% for Training, 50% for Frontend Simulator...")
    split_idx = len(combined_df) // 2
    
    train_df = combined_df.iloc[:split_idx]
    frontend_df = combined_df.iloc[split_idx:]
    
    train_df.to_csv(train_out, index=False)
    frontend_df.to_csv(frontend_out, index=False)
    
    print(f"✅ Success! Generated {train_out} and {frontend_out}")
    return train_out

def trigger_ml_pipeline(train_path):
    print("\n==================================================")
    print(" 3. EXECUTING MACHINE LEARNING PIPELINE ")
    print("==================================================")
    
    # Add backend to path dynamically
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from ml_modules.module1_feature_intelligence.pipeline import Module1Pipeline
    from ml_modules.module2_detection_engine.trainer import DetectionEngine
    
    print("[*] Triggering Module 1: Hybrid Feature Intelligence...")
    pipeline1 = Module1Pipeline(data_path=train_path, target_features=15, output_dir="experiments/current_run")
    stats1 = pipeline1.run()
    
    print("[*] Triggering Module 2: Ensemble Detection Engine...")
    train_data = pd.read_parquet("experiments/current_run/X_train.parquet")
    train_labels = pd.read_parquet("experiments/current_run/y_train.parquet")['label']
    
    engine = DetectionEngine()
    stats2 = engine.train_models(train_data, train_labels, experiment_id="EXP_FINAL")
    
    print("\n🚀 FULL PIPELINE COMPLETE!")
    print("The backend models are now fully trained and ready for the Frontend Simulator.")

if __name__ == "__main__":
    files = download_data()
    train_file = prepare_and_split(files)
    trigger_ml_pipeline(train_file)

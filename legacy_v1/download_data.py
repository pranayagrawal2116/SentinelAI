import pandas as pd
import urllib.request
import os

base_url = "https://huggingface.co/datasets/baalajimaestro/DDoS-CICIoT2023/resolve/main/"
files_to_download = [
    "BenignTraffic.pcap.csv",
    "DDoS-ICMP_Flood.pcap.csv",
    "DDoS-TCP_Flood.pcap.csv",
    "DDoS-UDP_Flood.pcap.csv"
]

print("Downloading and merging real CICIoT2023 dataset files from HuggingFace...")
dfs = []
for file in files_to_download:
    url = base_url + file
    print(f"Downloading {file}...")
    try:
        urllib.request.urlretrieve(url, file)
        df = pd.read_csv(file)
        dfs.append(df)
        print(f"Loaded {file} shape: {df.shape}")
        # Clean up to save disk space
        os.remove(file)
    except Exception as e:
        print(f"Failed to download {file}: {e}")

if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"Combined dataset shape: {combined_df.shape}")
    combined_df.to_csv("ciciot2023.csv", index=False)
    print("Saved to ciciot2023.csv successfully!")
else:
    print("No data downloaded.")

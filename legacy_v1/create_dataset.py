import pandas as pd
import os

urls = {
    'Benign': 'https://huggingface.co/datasets/baalajimaestro/DDoS-CICIoT2023/resolve/main/BenignTraffic.pcap.csv',
    'DDoS-ICMP': 'https://huggingface.co/datasets/baalajimaestro/DDoS-CICIoT2023/resolve/main/DDoS-ICMP_Flood.pcap.csv',
    'DDoS-TCP': 'https://huggingface.co/datasets/baalajimaestro/DDoS-CICIoT2023/resolve/main/DDoS-TCP_Flood.pcap.csv'
}

print("Redownloading and mapping labels...")
dfs = []
for label, url in urls.items():
    print(f"Fetching {label}...")
    os.system(f'curl -kL -s -o temp.csv "{url}"')
    df = pd.read_csv('temp.csv')
    df['label'] = label # ADDING THE MISSING LABEL COLUMN!
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)
combined_df.to_csv('ciciot2023.csv', index=False)
print("Saved to ciciot2023.csv. Shape:", combined_df.shape)
if os.path.exists('temp.csv'):
    os.remove('temp.csv')

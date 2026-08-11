from processing.tshark_processor import pcap_to_csv
from processing.dataset_builder import load_dataset
from processing.feature_extractor import prepare_features
import pandas as pd


datasets = [
    ("output/pcap/normal_traffic.pcap", "output/csv/normal.csv", "normal"),
    ("output/pcap/port_scan.pcap", "output/csv/port_scan.csv", "port_scan"),
    ("output/pcap/mqtt_flood.pcap", "output/csv/mqtt_flood.csv", "mqtt_flood"),
    ("output/pcap/dns_exfiltration.pcap", "output/csv/dns_exfiltration.csv", "dns_exfiltration"),
    ("output/pcap/mirai_like.pcap", "output/csv/mirai_like.csv", "mirai_like")
]

all_dataframes = []

for pcap_path, csv_path, label in datasets:
    pcap_to_csv(pcap_path, csv_path)

    df = load_dataset(csv_path, label=label)
    df = prepare_features(df)

    all_dataframes.append(df)

final_df = pd.concat(all_dataframes, ignore_index=True)

print(final_df["label"].value_counts())
print()
print(final_df.shape)

final_df.to_csv(
    "output/csv/final_dataset.csv",
    index=False
)

print("Final dataset saved successfully.")
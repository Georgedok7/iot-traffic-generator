import os
import matplotlib.pyplot as plt

LABEL_NAMES = {
    "normal": "Normal",
    "port_scan": "Port Scan",
    "mirai_like": "Mirai-like",
    "dns_exfiltration": "DNS Exfiltration",
    "mqtt_flood": "MQTT Flood"
}
def create_dataset_plots(flow_df, burst_df):
    output_dir = "output/plots"
    os.makedirs(output_dir, exist_ok=True)

    create_label_distribution(flow_df, output_dir)
    create_protocol_distribution(flow_df, output_dir)
    create_attack_timing_plot(burst_df, output_dir)
    create_port_distribution(flow_df, output_dir)


def create_label_distribution(df, output_dir):
    counts = df["label"].value_counts()

    counts.index = [
        LABEL_NAMES.get(label, label)
        for label in counts.index
    ]

    plt.figure(figsize=(8, 5))
    counts.plot(kind="bar")

    plt.title("Flow Distribution by Label")
    plt.xlabel("Traffic Label")
    plt.ylabel("Number of Flows")
    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig(
        f"{output_dir}/label_distribution.png",
        dpi=300
    )

    plt.close()


def create_protocol_distribution(df, output_dir):
    counts = df["protocol"].value_counts()

    plt.figure(figsize=(6, 5))
    counts.plot(kind="bar")

    plt.title("Protocol Distribution")
    plt.xlabel("Protocol")
    plt.ylabel("Number of Flows")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(
        f"{output_dir}/protocol_distribution.png",
        dpi=300
    )

    plt.close()


def create_attack_timing_plot(burst_df, output_dir):
    timing = (
        burst_df.groupby("attack_type")
        ["avg_inter_arrival"]
        .mean()
        .sort_values()
    )
    timing.index = [
        LABEL_NAMES.get(label, label)
        for label in timing.index
    ]
    plt.figure(figsize=(8, 5))
    timing.plot(kind="bar")

    plt.title("Average Inter-Arrival Time by Attack Type")
    plt.xlabel("Attack Type")
    plt.ylabel("Average Inter-Arrival Time (seconds)")
    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig(
        f"{output_dir}/attack_inter_arrival.png",
        dpi=300
    )

    plt.close()


def create_port_distribution(df, output_dir):
    ports = (
        df["dst_port"]
        .value_counts()
        .head(10)
    )

    plt.figure(figsize=(8, 5))
    ports.plot(kind="bar")

    plt.title("Top 10 Destination Ports")
    plt.xlabel("Destination Port")
    plt.ylabel("Number of Flows")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(
        f"{output_dir}/destination_ports.png",
        dpi=300
    )

    plt.close()
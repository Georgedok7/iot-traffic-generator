import subprocess
from pathlib import Path
import pandas as pd

def run_zeek(pcap_path, output_dir):
    pcap_path = Path(pcap_path).resolve()
    output_dir = Path(output_dir).resolve()

    output_dir.mkdir(parents=True, exist_ok=True)

    windows_pcap = str(pcap_path)
    windows_output = str(output_dir)

    command = [
        "wsl",
        "-d",
        "Ubuntu",
        "bash",
        "-lc",
        (
            f'cd "$(wslpath \'{windows_output}\')" && '
            f'/opt/zeek/bin/zeek -r "$(wslpath \'{windows_pcap}\')"'
        )
    ]

    subprocess.run(command, check=True)

  


def load_conn_log(conn_log_path, label=None):
    fields = []

    with open(conn_log_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#fields"):
                fields = line.strip().split("\t")[1:]
                break

    df = pd.read_csv(
        conn_log_path,
        sep="\t",
        comment="#",
        names=fields
    )

    selected_columns = [
        "id.orig_h",
        "id.orig_p",
        "id.resp_h",
        "id.resp_p",
        "proto",
        "service",
        "duration",
        "orig_bytes",
        "resp_bytes",
        "orig_pkts",
        "resp_pkts"
    ]

    df = df[selected_columns].rename(columns={
        "id.orig_h": "src_ip",
        "id.orig_p": "src_port",
        "id.resp_h": "dst_ip",
        "id.resp_p": "dst_port",
        "proto": "protocol"
    })
    numeric_columns = [
        "src_port",
        "dst_port",
        "duration",
        "orig_bytes",
        "resp_bytes",
        "orig_pkts",
        "resp_pkts"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    if label is not None:
        df["label"] = label

    return df
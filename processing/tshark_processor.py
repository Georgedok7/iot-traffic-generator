import subprocess

TSHARK_PATH = r"C:\Program Files\Wireshark\tshark.exe"

def pcap_to_csv(pcap_path, csv_path):
    command = [
        TSHARK_PATH,
        "-r", pcap_path,
        "-T", "fields",
        "-E", "header=y",
        "-E", "separator=,",
        "-E", "quote=d",
        "-e", "frame.time_epoch",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "ip.proto",
        "-e", "tcp.srcport",
        "-e", "tcp.dstport",
        "-e", "udp.srcport",
        "-e", "udp.dstport",
        "-e", "frame.len",
    ]

    with open(csv_path, "w", encoding="utf-8") as output_file:
        subprocess.run(
            command,
            stdout=output_file,
            check=True
        )
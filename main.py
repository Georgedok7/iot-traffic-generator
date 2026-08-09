from scapy.all import wrpcap
from generators.dns_generator import generate_dns_traffic


packets = generate_dns_traffic(count=10)

wrpcap("output/pcap/dns_traffic.pcap", packets)
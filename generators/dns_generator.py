from scapy.all import IP, UDP, DNS, DNSQR, DNSRR
import random


domains = [
    "sensor.local",
    "camera.local",
    "thermostat.local",
    "gateway.local"
]


def generate_dns_traffic(
    count=10,
    dns_server="8.8.8.8",
    source_ip="192.168.1.10"
):
    packets = []

    for _ in range(count):
        source_port = random.randint(49152, 65535)
        domain = random.choice(domains)

        query = IP(
            src=source_ip,
            dst=dns_server
        ) / UDP(
            sport=source_port,
            dport=53
        ) / DNS(
            rd=1,
            qd=DNSQR(qname=domain)
        )

        packets.append(query)

        response = IP(
            src=dns_server,
            dst=source_ip
        ) / UDP(
            sport=53,
            dport=source_port
        ) / DNS(
            id=query[DNS].id,
            qr=1,
            aa=1,
            qd=query[DNS].qd,
            an=DNSRR(
                rrname=domain,
                type="A",
                rdata="192.168.1.100"
            )
        )

        packets.append(response)

    return packets
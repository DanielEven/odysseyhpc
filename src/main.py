import argparse
import os
import sys
from typing import NamedTuple, Optional

from loguru import logger
from scapy.utils import rdpcap


class Endpoint:
    def __init__(self, ip_port: str):
        ip, port = ip_port.split(':')
        self.ip = ip
        self.port = int(port)

    def __str__(self):
        return f"{self.ip}:{self.port}"


class Connection(NamedTuple):
    client: Endpoint
    server: Endpoint

    def __str__(self):
        return f"{str(self.client)}->{str(self.server)}"


# this is en example of reading packets from a pcap file using scapy
def count_packets(pcap_path: str):
    count = 0
    packets = rdpcap(pcap_path)
    for pkt in packets:
        count += 1
    return count


def count_ipv4_tcp_packets(pcap_path: str):
    count = 0
    # TODO implement (stage 1)
    return count


def count_connection_packets(pcap_path: str, client: EndpointDetails, server: EndpointDetails):
    count = 0
    # TODO implement (stage 1)
    return count


def log_results(pcap_path: str, total: int, ipv4_tcp: int, connections: Optional[int] = None,
                connection: Optional[Connection] = None):
    logger.info(f"{pcap_path} contains {total} packets")
    logger.info(f"{pcap_path} contains {ipv4_tcp} IPv4 TCP packets")
    if connection:
        logger.info(f"{pcap_path} contains {connections} packets for connection {connection}")


def process_pcap_single(pcap_path: str, connection: Optional[Connection]):
    logger.info(f"Processing {pcap_path}...")
    total = count_packets(pcap_path)
    ipv4_tcp = count_ipv4_tcp_packets(pcap_path)
    connections = count_connection_packets(pcap_path, connection.client, connection.server) if connection else None
    log_results(pcap_path, total, ipv4_tcp, connections, connection)
    logger.info("Done!")


def process_pcap_multi(pcap_path: str, connection: Optional[Connection]):
    # TODO implement (stage 3)
    pass


def main():
    parser = argparse.ArgumentParser(description='HPC packet processor')
    parser.add_argument('--pcap', help='pcap file to parse', required=True)
    parser.add_argument('--client', help='client ip:port')
    parser.add_argument('--server', help='server ip:port')
    parser.add_argument('--multi', help='run multi core', action='store_true')
    args = parser.parse_args()
    pcap_path = args.pcap

    if not os.path.isfile(pcap_path):
        logger.warning(f"{pcap_path} does not exist")
        sys.exit(-1)

    connection = None
    if args.client and args.server:
        client = Endpoint(args.client)
        server = Endpoint(args.server)
        connection = Connection(client, server)

    logger.info(f"{connection}")

    if args.multi:
        process_pcap_multi(pcap_path, connection)
    else:
        process_pcap_single(pcap_path, connection)


if __name__ == '__main__':
    logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
    main()

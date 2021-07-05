import argparse
import os
import sys
import socket

from loguru import logger

RECV_BUFFER_SIZE = 1024


class Endpoint:
    def __init__(self, ip_port: str):
        ip, port = ip_port.split(':')
        self.ip = ip
        self.port = int(port)

    def __str__(self):
        return f"{self.ip}:{self.port}"


def send(jobs: list[int], lb: Endpoint):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    logger.info(f"Connecting to {lb}")
    s.connect((lb.ip, lb.port))

    logger.info(f"Sending jobs {jobs}")
    for job in jobs:
        s.send(job.encode())

    logger.info(f"Waiting for resutls...")
    for _ in jobs:
        result = s.recv(RECV_BUFFER_SIZE).decode().rstrip()
        logger.info(f"got result: {result}")

    s.close()
    logger.info("Done!")


def main():
    parser = argparse.ArgumentParser(description='A very demanding client app')
    parser.add_argument('--lb', help='load balancer ip:port', required=True)
    parser.add_argument('--jobs', help='a comma-separated list of jobs to run, e.g. 1,2,1,1,1,2', type=str)
    parser.add_argument('--f', help='a file containing a comma-separated list of jobs to run', type=str)
    args = parser.parse_args()
    jobs_str = args.jobs
    jobs_file = args.f

    if (not jobs_str and not jobs_file) or (jobs_str and jobs_file):
        logger.warning("Please use *exactly one* of the options, run with -h for more information")
        sys.exit(-1)

    if jobs_file:
        if not os.path.isfile(jobs_file):
            logger.warning(f"{jobs_file} does not exist")
            sys.exit(-1)
        with open(jobs_file, "r") as f:
            jobs_str = f.readlines()[0]

    jobs = jobs_str.split(',')
    lb = Endpoint(args.lb)

    send(jobs, lb)


if __name__ == '__main__':
    main()

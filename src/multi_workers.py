import psutil
import argparse
from sys import argv
from subprocess import Popen

parser = argparse.ArgumentParser(description="A multi-worker")
parser.add_argument('--lb', help='load balancer ip:port', required=True)
args = parser.parse_args()
print(str(args.lb))
 
CORE_NUMBER = psutil.cpu_count(logical=False)

# https://docs.python.org/3/library/subprocess.html#subprocess.Popen
procs = []
for i in range(CORE_NUMBER):
    procs.append(Popen(["python3", "bitcoin_worker.py", *argv[1:]]))

print("Opened "+str(CORE_NUMBER)+" Workers! Good luck!🍀")

for proc in procs:
    proc.wait()
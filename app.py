# def main():
#      try:
#     # Taking User Input for the hostname or ip address
#         target = input("Enter Target's IP Address or Hostname: ")

#     # checking if the ip address is valid or not
#         ip = ipaddress.ip_address(target)
#         print('%s is a correct IP%s address.' % (ip, ip.version))
#     except ValueError:
#         print('address/netmask is invalid: %s' % target)
#     except:
#         print('Usage : %s  ip' % sys.argv[0])


# try:
#     start_port = int(input("Enter a port number: "))
#     end_port = int(input("Enter Ending Port: "))
#     if 1 <= start_port <= 65535:
#         print("This is a VALID port number.")
#     else:
#         raise ValueError
# except ValueError:
#     print("This is NOT a VALID port number.")

import socket
import ipaddress
from queue import Queue
import sys
import threading
from netaddr import *
import logging
import time


print('''
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!-- ~ _____           _      _____                 _   ~ -->
<!-- ~|  __ \         | |    / ____|               | |  ~ -->
<!-- ~| |__) |__  _ __| |_  | (___   ___ __ _ _ __ | |  ~ -->
<!-- ~|  ___/ _ \| '__| __|  \___ \ / __/ _` | '_ \| |  ~ -->
<!-- ~| |  | (_) | |  | |_   ____) | (_| (_| | | | |_|_ ~ -->
<!-- ~|_|   \___/|_|   \__| |_____/ \___\__,_|_| |_(_|_)~ -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->       
      ''')


time.sleep(2)


target = input("Enter Target's IP Address or Hostname: ")

# checking if the ip address is valid or not
try:
    ip = ipaddress.ip_address(target)
    print("%s is a correct IP%s address." % (ip, ip.version))
except ValueError:
    print("address/netmask is invalid: %s" % target)

# Variables
start_port = 1
end_port = 1024
customPortStart = 0
customPortEnd = 0
allPort = 1
allPortEnd = 65535

# scan modes and custom port option.
print("Select your scan type: ")
print("[+] Select 1 for 1 to 1024 port scaning")
print("[+] Select 2 for 1 to 65535 port scaning")
print("[+] Select 3 for custom port scaning")
print("[+] Select 4 for Scanning Ip Ranges [Ex : 1.1.1.1 - 3.3.3.3]")
print("[+] Select 5 for exit \n")

mode = int(input("[+] Select any option: "))
print()

# Custom Ports
if mode == 3:
    customPortStart = int(input("[+] Enter starting port number: "))
    customPortEnd = int(input("[+] Enter Ending port number: "))

    print("_" * 50)
    print(f"Scanning Ports from {customPortStart} to {customPortEnd} on {target}....\n")


# Ip Range Scanning 
if mode == 4:     
    ipStart, ipEnd = int(input("Enter IP-IP: ").split("-"))

    iprange = IPRange(ipStart , ipEnd)



# Main Scan Function
def scan_port(port):
    s = socket.socket()
    s.settimeout(5)
    result = s.connect_ex((target, port))
    if result == 0:
        print("port open", port)
    s.close()


queue = Queue()

# Scan Modes Config
def get_ports(mode):
    if mode == 1:
        print("\n Scanning ..\n")
        for port in range(start_port, end_port + 1):
            queue.put(port)
    elif mode == 2:
        print("\n Scanning ..\n")
        for port in range(allPort, allPortEnd + 1):
            queue.put(port)
    elif mode == 3:
        print("\n Scanning ..\n")
        for port in range(customPortStart, customPortEnd + 1):
            queue.put(port)
    elif mode == 4:
        print("[-] Exiting...")
        sys.exit()
    elif mode == 5:
        print("[-] Exiting...")
        sys.exit()


open_ports = []

def worker():
    while not queue.empty():
        port = queue.get()
        if scan_port(port):
            print("Port {} is open!".format(port))
            open_ports.append(port)



# Threading for running multiple ports
def run_scan(threads, mode):
    get_ports(mode)

    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


run_scan(1021, mode)
print("Scanning complete")


# If user asks for Output File [ Output Customization]
file_output = input(print("Do You Want to Save the Scan Results ?: "))
if file_output == "YES" or "yes":

    stdOut_Origin = sys.stdout
    sys.stdout = open("output.txt" , "w")


    sys.stdout.close()
    sys.stdout=stdOut_Origin

    #file = open('output.txt' , 'a')
    #sys.stdout = file
    #file.close()


# Log File 
logger = logging.getLogger('Scanning')
logger.setLevel(logging.DEBUG)

# File Handler
fh = logging.FileHandler('run.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


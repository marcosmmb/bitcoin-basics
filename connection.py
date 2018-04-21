
import struct
import time
import random
from hashlib import sha256
import socket

HOST = "177.190.148.9"
PORT = 8333
BLOCK_HEIGHT = 519202
PROTOCOL_VERSION = 70015

def return_payload(block_height, protocol_version):
    version = struct.pack("i", protocol_version)
    services = struct.pack("Q", 0)
    timestamp = struct.pack("q", time.time())
    addr_recv_services = struct.pack("Q", 0)
    addr_recv_ip = struct.pack(">16s", "127.0.0.1")
    addr_recv_port = struct.pack(">H", 8333)
    addr_trans_services = struct.pack("Q", 0)
    addr_trans_ip = struct.pack(">16s", "127.0.0.1")
    addr_trans_port = struct.pack(">H", 8333)
    nonce = struct.pack("Q", random.getrandbits(64))
    user_agent_bytes = struct.pack("B", 0)
    start_height = struct.pack("i", block_height)
    relay = struct.pack("?", False)

    payload = version + services + timestamp + addr_recv_services + \
    addr_recv_ip + addr_recv_port + addr_trans_services + addr_trans_ip + \
    addr_trans_port + nonce + user_agent_bytes + start_height + relay
    
    return payload

def return_msg():
    payload = return_payload(BLOCK_HEIGHT, PROTOCOL_VERSION)
    magic = "F9BEB4D9".decode("hex")
    command = "version" + 5 * "\00"
    length = struct.pack("I" ,len(payload))
    checksum = sha256(sha256(payload).digest()).digest()[:4]

    msg = magic + command + length + checksum + payload


msg = return_msg

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

s.send(msg)

s.recv(1024)
import struct
import time
import random
from hashlib import sha256
import socket

DEFAULT_HOST                = "177.190.148.9"
DEFAULT_PORT                = 8333
DEFAULT_BLOCK_HEIGHT        = 519202
DEFAULT_PROTOCOL_VERSION    = 70015

class Connection:

    def __init__(self,  
                host = DEFAULT_HOST, 
                port = DEFAULT_PORT, 
                block_height = DEFAULT_BLOCK_HEIGHT, 
                protocol_version = DEFAULT_PROTOCOL_VERSION): 
                # https://bitcoin.org/en/developer-reference#protocol-versions

        self.host               = host
        self.port               = port
        self.block_height       = block_height
        self.protocol_version   = protocol_version

    def return_payload(self):
        # https://bitcoin.org/en/developer-reference#version
        # https://docs.python.org/2/library/struct.html
        version                 = struct.pack("i", self.protocol_version)
        services                = struct.pack("Q", 0)
        timestamp               = struct.pack("q", time.time())
        addr_recv_services      = struct.pack("Q", 0)
        addr_recv_ip            = struct.pack(">16s", "127.0.0.1")
        addr_recv_port          = struct.pack(">H", 8333)
        addr_trans_services     = struct.pack("Q", 0)
        addr_trans_ip           = struct.pack(">16s", "127.0.0.1")
        addr_trans_port         = struct.pack(">H", 8333)
        nonce                   = struct.pack("Q", random.getrandbits(64))
        user_agent_bytes        = struct.pack("B", 0)
        start_height            = struct.pack("i", self.block_height)
        relay                   = struct.pack("?", False)

        payload = version + services + timestamp + addr_recv_services + \
        addr_recv_ip + addr_recv_port + addr_trans_services + addr_trans_ip + \
        addr_trans_port + nonce + user_agent_bytes + start_height + relay
        
        return payload

    def return_msg(self):
        # https://bitcoin.org/en/developer-reference#message-headers
        payload     = self.return_payload()
        magic       = "F9BEB4D9".decode("hex")
        command     = "version" + 5 * "\00"
        length      = struct.pack("I" ,len(payload))
        checksum    = sha256(sha256(payload).digest()).digest()[:4]

        msg         = magic + command + length + checksum + payload
        
        return msg

    def start_connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        return s

    def send_msg(self):
        msg = self.return_msg()
        s = self.start_connection()
        s.send(msg)
        r = s.recv(1024)
        return r

conn = Connection()
conn.send_msg()
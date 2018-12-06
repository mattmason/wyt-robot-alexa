from array import array
import struct
import socket
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class mesh():
    def __init__(self):
        HOST = "localhost"
        PORT = 42001
        logger.info("Connecting...")
        print("Connecting...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("localhost", 42001))
        logger.info("Connected")
        print("Connected")

    def send(self, cmd):
        logger.info(cmd)
        print(cmd)
        head = struct.pack(">I", len(cmd))
        self.socket.send(head + cmd.encode("utf-8"))

    def broadcast(self, message):
        self.send("broadcast %s" % message)


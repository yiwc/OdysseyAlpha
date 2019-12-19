# References
# ----------
# https://wiki.python.org/moin/UdpCommunication

import socket

UDP_IP = "172.31.1.147"
## UDP_IP = "172.16.127.128"
# UDP_IP = "127.0.0.1"

# Yuanrui's port
# UDP_PORT = 12358
# Legal port
UDP_PORT = 30009

MESSAGE = b'Hello, World!'

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
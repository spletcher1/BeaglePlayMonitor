#!/usr/bin/env python
import socket
import sys
import struct
import time

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
print("Here")
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Here2")
sock.bind(('', 9999))
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
print("Here3")
mreq = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, "ff02::1"), (chr(0) * 16).encode('utf-8'))
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
print("Here4")
while True:
  data, sender = sock.recvfrom(1024)
  print (str(sender) + '  ' + repr(data))
#!/usr/bin/env python3

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

class server:
    def __init__(self):
        self.database = {
            "name": "Alizhan",
            "age": "21",
            "city": "Barcelona"
        }

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print("accepted connection from", addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)


    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                data.outb = recv_data
                
            else:
                print("closing connection to", data.addr)
                sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                
                print("For request", repr(data.outb),"sending", self.message_parser(data.outb.decode("utf-8")), "to", data.addr)
                data.outb = self.message_parser(data.outb.decode("utf-8")).encode("utf-8")
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
    
    def message_parser(self, byte_message):
        output = []
        test_str = ""
        dumm_mes = str(byte_message)
        comm_list = dumm_mes.split("-->")
        for message in comm_list:
            if message.startswith("GET"):
                try:
                    command, key = message.split(" ")
                    output.append(self.database[key])
                except ValueError:
                    return "your message does not make sense"
            elif message.startswith("PUT"):
                command, key, value = message.split(" ")
                self.database[key] = value
                output.append("'{}: {}' has been added to dictionary".format(key, value))   
            elif message.startswith("LIST"):
                output.append("{}".format(self.database))
        return "{}".format(output)

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

ser = server()

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                ser.accept_wrapper(key.fileobj)
            else:
                ser.service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
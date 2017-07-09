#!/usr/bin/python3

import os
import socket
from threading import Thread, Timer

##----IMPORTANT GLOBAL VARIABLES--##

server = None        # server socket to listen for connections
bind_ip = '0.0.0.0'
bind_port = 2718     # port to listen on (should be user editable)
live_users = []      # array to hold live (connected) users: each user = [client, addr]
max_conns = 5        # maximum number of users to accept connections from
file_locked = False  # if a live_user is accessing the file

##----DEFINE HELPER FUNCTIONS-----##


def setup ():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.listen(max_conns)
        return 1
    except Exception e:
        return 0

def recv_data (conn):
    received = ""
    while True:
        data = conn.recv(4096)
        received += data.decode("utf-8")
        if len(data) <= 4096:
            break

    return received


def accept_user (server):
    user, addr = server.accept()
    live_users.append([user, addr])
    print("[**] Accepted connection from %s:%d \n" % (addr[0], addr[1]))


##----MAIN PROGRAM STARTS HERE----##


def main ():
    ready = setup()
    if ready:
        print("[**] Listening on %s:%d \n" % (bind_ip, bind_port))
    else:
        print("[!!] Failed to start server. Exiting...\n")
        os.exit()
        quit()


if __name__ == "__main__":
    main()


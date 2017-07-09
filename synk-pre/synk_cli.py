import os, socket, hashlib, math, threading
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


"""
GENERAL PLAN:
1. User opens file and script starts
2. Obtain filename being currently edited.
3. Open a socket connection with the server (must be configured)
4. Pull changes and detect who else is editing it
5. Add shadow cursors of who else is editing
6. Detect a change in the file and send changes to server.
7. Server must decide how to integrate changes and notify client of edits (see below)
NOTE 1: A cached file is probably best for this (like Github)
NOTE 2: It is probably best to have parallel uplink and downlink connections to avoid latency
        (Pulling writes to file, pushing only reads it)

How to control changes:
RULE 1: always take commits serially. The first commit to appear will be applied first.
1. Always pull changes from server as they appear
2. Compare pulled file to local file.
3. If different, cache the local file.
4. Apply pulled changes, commit the cached file and push to server.
"""


##----VARIABLE DECLARATIONS----##

VERSION = 0.1
UPORT = 5498    # port to send to
DPORT = 4589    # port to listen on
PROJECTDIR = "/home/conrad/Github/f4l1ing/"    # Directory of the project
                                               # NOTE: This should be generated in a sublime plugin
filename = "test.py"                           # Should generate with sublime plugin

##----HELPER FUNCTION DECLARATIONS----##


def gen_hash(file, mode="file") -> "sha256sum":
    checksum = hashlib.sha256()
    if mode == "file":
        checksum.update(file.encode("utf-8"))
    elif mode == "data":
        for line in file:
            checksum.update(line.encode("utf-8"))

    return checksum.hexdigest()


def recv_data(conn):
    received = ""
    while True:
        data = conn.recv(4096)
        received += data.decode("utf-8")
        if len(data) <= 4096:
            break

    return received


def send_data(conn, data) -> None:
    conn.send(data.encode("utf-8"))


def write_file(fname, data):
    with open(fname, 'w') as f:
        for line in data:
            f.write(line + '\n')


def read_file(fname):
    content = ""
    with open(fname, 'r') as f:
        content = f.read()

    return content


def downlink(server, port, attempts=5):
    for a in range(attempts):
        downsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            downsock.connect((server, port))
            break
        except:
            continue
    while True:
        received = recv_data(downsock)
        print(received)

        received = received.split('\n')
        downfile = received[0]

        if not downfile == filename:
            break

        if gen_hash(filename) != gen_hash(received[1:], mode="data"):
            cached_file = "/tmp/" + filename.split('/')[-1]
            write_file(cached_file, read_file(filename))
            write_file(filename, received[1:])


def uplink(server, port, attempts=5):
    for a in range(attempts):
        upsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            upsock.connect((server, port))
            break
        except:
            continue
    while True:



##----MAIN PROGRAM STARTS HERE----##


def main():



if __name__ == "__main__":
    main()


print(gen_hash(PROJECTDIR + "/synk/test.py"))

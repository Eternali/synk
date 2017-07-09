"""

"""

import difflib
import hashlib
import math
import os
import socket
import time

# global variables

settings_filename = "/home/fa11en/.config/synk/synk-settings.conf"
server_ip_field = "server_ip"
server_port_field = "server_port"
local_project_loc_field = "local_project_location"
server_project_loc_field = "server_project_location"
delay_field = "delay"  # in seconds

cached_project_location = "/tmp/synkProjects/"

# server connection class


class Server_conn(pbject):

    def __init__(self, settings, attempts):
        # get the relevent settings
        self.server_ip = settings[server_ip_field]
        self.server_port = settings[server_port_field]
        self.local_project_location = settings[local_project_loc_field]
        self.server_project_location = settings[server_project_loc_field]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # cache the current project to the current directory
        os.system("cp -r %s %s" %
                  (self.local_project_location, cached_project_location))
        for attempt in range(attempts):
            try:
                self.sock.connect((self.server_ip, self.server_port))
                return
            except Exception:
                continue
        print(
            "[!!] An error occured while connecting to the server, please check your settings.")

    def recv_data(self):
        received = ""
        while True:
            data = self.sock.recv(4096)
            received += data.decode("utf-8")
            if len(data) <= 4096:
                break

        return received

    def send_data(self, data):
        self.sock.send(data.encode("utf-8"))

    def push_changes(self, files):
        for file in files:
            self.indices = self.diffs = []
            self.get_local_changes(file, cached_project_location +
                                   file.replace(self.local_project_location, ""))
            self.send_data(self.encode_data(locations, diffs))

    def pull_changes(self):

    def file_changed(self):
        files_changed = []
        # check for changes between the current file mtime and cached mtime and
        # locate the changes
        for subdir, dirs, files in os.walk(self.local_project_location):
            for file in files:
                curmtime = os.path.getmtime(os.path.join(subdir, file))
                pastmtime = os.path.getmtime(
                    cached_project_location + os.path.join(subdir, file).replace(self.local_project_location, ""))
                if curmtime > pastmtime:
                    files_changed.append(os.path.join(subdir, file))

        return files_changed

    def get_local_changes(self, file, cached_file):
        # it is assumed there is a difference between the file and the
        # cached_file
        with open(file, 'r') as nf:
            nlines = nf.readlines()
        with open(cached_file, 'r') as cf:
            clines = cf.readlines()

        self.calc_diffs(list(clines), list(nlines))

    def calc_diffs(self, old, new):
        ls = largest_substring(''.join(old), ''.join(new))
        if len(ls):
            start, end = ''.join(new).index(
                ls), ''.join(new).index(ls) + len(ls)
            self.indices.append([start, end])
            self.diffs.append(
                [''.join(old).index(ls), ''.join(old).index(ls) + len(ls)])
            new[start:end] = [None for n in range(end - start)]
            calc_diffs(old, new)
        else:
            i = 0
            while i < len(new):
                if new[i] is not None:
                    if i == len(new) - 1:
                        lastNone = new[i + 1:].index(None) + i + 1
                        self.indices.append(''.join(new[i:lastNone]))
                        self.diffs.append(i)
                        i = lastNone
                i += 1
            self.indices.append(''.join(new.strip(None)))
            self.diffs.append([])
            for i in self.indices[-1]:
                self.diffs[-1].append(new.index(i))

    # parameter location is of form [file, row, column] (start of changes) and difference is of form [old, new]
    # e.g. ["synk/test.py", 1,5], ["", "this"] for appending "this" to line 2 which was originally just 5 characters long
    # everything is still 0 indexed :)
    # this will encode it into a string to be sent over the socket
    def encode_data(self, locations, differences):
        encoded = ""
        for l in range(len(locations)):
            encoded += ':'.join(locations[l]) + \
                ';' + ':'.join(differences[l]) + ' '

        return encoded


def largest_substring(strings):
    substr = ""
    if len(strings) > 1 and len(strings[0]):
        for i in range(len(strings[0])):
            for j in range(len(strings[0]) - i + 1):
                if j > len(substr) and all(strings[0][i:i + j] in s for s in strings):
                    substr = strings[0][i:i + j]

    return substr


# file input/output functions
def file_read(filename):
    file_contents = []
    with open(filename, 'r') as rfile:
        for line in rfile:
            file_contents.append(line)

    return file_contents


def file_write(filename, data):
    with open(filename, 'w') as wfile:
        for line in data:
            wfile.write(line + '\n')


# run on startup to read the settings from a file
def startup():
    sets = {}
    settings_tmp = [x.split(':') for x in file_read(settings_filename)]
    for i in range(len(settings_tmp)):
        sets[settings_tmp[i][0].strip()] = settings_tmp[i][-1].strip()
    os.system("mkdir %s" % cached_project_location)
    return sets


# main program
def main():
    # get the settings
    settings = startup()
    conns = [new Server_conn(settings, 5)]
    # while True:
    #     for conn in conns:
    #         if len(conn.file_changed()):
    #             conn.push_changes()
    #         conn.pull_changes()

    #     time.sleep(settings[delay_field])


if __name__ == '__main__':
    main()

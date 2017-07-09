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


class Server_conn(object):

    def __init__(self, settings, attempts):dsa
        # get the relevent settings
        self.server_ip = settings[server_ip_field]

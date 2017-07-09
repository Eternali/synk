'''
Synk - Sublime Text Plugin

'''

import os
import socket
import sublime
import sublime_plugin
from threading import Thread, Timer

# variables for storing user defined settings
settings_filename = "synk_pre.sublime-settings"

enabled_field = "enabled"
server_ips_field = "project_server_ips"     # NOTE: add feature to have more than one server later
uplink_ports_field = "uplink_ports"
downlink_ports_field = "downlink_ports"
all_files_field = "synk_all_files"
current_file_field = "synk_current_file"
delay_field = "delay_in_seconds"


# Object for connecting to the server
class ServerConnection(object):
    def __init__(self, attempts=5):
        self.settings = sublime.load_settings(settings_filename)
        self.delay = self.settings.get(delay_field)
        self.server = self.settings.get(server_ips_field)
        self.up_port = self.settings.get(uplink_ports_field)
        self.down_port = self.settings.get(downlink_ports_field)
        self.current_file = self.settings.get(current_file_field)
        self.upsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.downsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.file_locked = False
        for a in range(attempts):
            try:
                self.upsock.connect((self.server, self.up_port))
                self.downsock.connect((self.server, self.down_port))
                return
            except:
                continue
        sublime.status_message("An error occured while attempting to connect to the server.")

    def recv_data(conn):
        received = ""
        while True:
            data = conn.recv(4096)
            received += data.decode("utf-8")
            if len(data) <= 4096:
                break

        return received

    def write_file(fname, data, mode="w"):
        with open(fname, mode) as f:
            for line in data:
                f.write(line + '\n')

    def push_changes(self, filename=self.current_file, attempts=30):
        for a in attempts:
            if not self.file_locked:
                self.file_locked = True
                data = self.current_file + '\n' + view.substr(sublime.Region(0, view.size()))
                self.upsock.send(data.encode("utf-8"))
                self.file_locked = False
                break

    def get_changes(self):
        #change_thread = Thread(target=self.get_changes_thread)
        #change_thread.start()
        Timer(self.delay, self.get_changes_thread).start()

    def get_changes_thread(self):
        while True:
            self.recved_data = self.recv_data(self.downsock)
            if len(self.recv_data) and not self.file_locked and not view.is_loading():
                self.file_locked = True
                self.write_file(self.current_file, self.recved_data)
                self.file_locked = False


class SynkPreListener(sublime_plugin.EventListener):
    save_queue = []

    @staticmethod
    def generate_backup_filename(filename):
        dirname, basename = [os.path.dirname(filename), os.path.basename(filename).split('.')]
        if len(basename) > 1:
            basename.insert(-1, 'bak')
        else:
            basename.append('bak')

        return dirname + '/' + '.'.join(basename)

    def on_modified(self, view):
        settings = sublime.load_settings(settings_filename)
        if not (view.file_name() and view.is_dirty()):
            return

        delay = settings.get(delay_field)
        all_files = settings.get(all_files_field)
        current_file = settings.get(current_file_field)

        if not all_files and current_file != view.file_name():
            return

    def callback():
        settings = sublime.load_settings(settings_filename)
        current_file = settings.get(current_file_field)
        if view.is_dirty() and not view.is_loading():
            view.run_command("save")
            serv_conn.push_changes(filename=current_file)
        else:
            content = view.substr(sublime.Region(0, view.size()))
            try:
                with open(SynkPreListener.generate_backup_filename(view.filename()), 'w', encoding="utf-8") as f:
                    f.write(content)
            except Exception as e:
                sublime.status_message(str(e))
                raise e


class SynkPreCommand(sublime_plugin.TextCommand):
    def run(self, **kwargs):
        enable = kwargs.get("enable", None)
        all_files = kwargs.get("all_files", False)

        settings = sublime.load_settings(settings_filename)
        if enable is None:
            enable = not settings.get(enabled_field)

        if not enable:
            message = "Autosynk is turned off."
            filename = settings.get(current_file_field)

        settings.set(enabled_field, enable)
        settings.set(all_files_field, all_files)
        filename = sublime.Window.active_view(sublime.active_window()).file_name()
        settings.set(current_file_field, filename)

        if enable:
            message = "Autosynk is turned on."
            if not all_files:
                message += " for: " + os.path.basename(filename)
                serv_conn = ServerConnection()
                global serv_conn
                serv_conn.get_changes()

        sublime.status_message(message)



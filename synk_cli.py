import socket, os, time, multiprocessing

proto = "https"
git_server = "github.com/Eternali/synk.git"
usernm = "Eternali"
passwd = ""


def setup():
    os.system("git remote remove origin")
    os.system("git remote add origin " + proto + "://%s:%s@%s" % (usernm, passwd, git_server))


def upload_changes():
    os.system("git add -f . && git commit -am 'autocommit' && git push origin master")


def get_changes():
    os.system("git pull origin master")
    os.system(" ")


while True:
    os.system("git add -f . && git commit -am 'autocommit'")



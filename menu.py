from pyfiglet import Figlet
import os
from consolemenu import *
from consolemenu.items import *


def main_menu():
    f = Figlet(font='slant')
    menu = ConsoleMenu(f.renderText('OneBroadband'),)
    menu.show()


def dictionary_attack():
    dict_path = input('Enter the dictionary filepath: ')

    if os.path.isfile(dict_path):
        pass

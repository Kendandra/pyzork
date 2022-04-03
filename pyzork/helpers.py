# Shameless stolen from https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console

import os

def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')



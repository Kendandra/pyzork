# Shameless stolen from https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console

import os

# Apparently this is cross platform.
# I'm guessing 'nt' is windows, in which case the answer you're fucked.
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

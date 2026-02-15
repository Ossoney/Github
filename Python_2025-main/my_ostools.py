import os
'''
Sistema operativo
'''

def clear_screen():
    if os.name in ('nt', 'dos'):  # Sistemas Windows - MS-DOS
        command = 'cls'
    elif os.name in ('posix'):  # Sistemas *NIX
        command = 'clear'

    os.system(command)

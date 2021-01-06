# This is a sample Python script.

# not tested!!!

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import editor.amidict
import example_package.subpackage1.moduleX
import tests.test_editor

print('main.py', '__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('run main')
    tests.test_editor()
    example_package.subpackage1.moduleX

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

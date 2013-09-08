import sys
from django.conf import settings
from eso.imports import load_simple
from eso.rotation import rotate_guess
from eso.imports import card_dump

def take_commands():
    while 1:
        main_menu()
    exit()

def main_menu():
    print 'What do you want to do?'
    print '1) Test'
    print '2) Load simple'
    print '3) Rotation check'
    print '4) Find dump'
    print 'x) Exit'
    user_response = sys.stdin.readline()
    menu_response = user_response[0]
    if menu_response == '1':
        test()
    if menu_response == '2':
        load_simple.main()
    if menu_response == '3':
        rotate_guess.main()
    if menu_response == '4':
        card_dump.main()
    if menu_response == 'x':
        exit()

def test():
    print settings.ROB_TEST 
    print "Successful"


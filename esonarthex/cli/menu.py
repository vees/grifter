import sys
from django.conf import settings 

def take_commands():
	while 1:
		main_menu()
	exit()

def main_menu():
	print 'What do you want to do?'
	print '1) Test'
	print 'x) Exit'
	user_response = sys.stdin.readline()
	menu_response = user_response[0]
	if menu_response == '1':
		test()
	if menu_response == 'x':
		exit()

def test():
	print settings.ROB_TEST 
	print "Successful"


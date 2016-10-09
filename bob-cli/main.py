import sys
sys.path.append('.') #this is the path relative to bob_init.sh
from common.sender import sender

if __name__ == '__main__':
	cursor = '>> '
	command = ''
	exit = False
	print 'OBM BOB Command line interface: insert a command or write quit to exit'
	while not exit:
		command = raw_input(cursor)
		if command == 'quit':
			exit = True
		else:
			print sender.sendMessage(command)
	
import socket

server_add = './bob_system_socket'
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
	sock.connect(server_add)
except socket.error:
	print 'Socket not available.'

def sendMessage(message):
	data = None
	sock.send(message)
	data = sock.recv(1024)
	return data

if __name__ == '__main__':
	print sendMessage('get name')
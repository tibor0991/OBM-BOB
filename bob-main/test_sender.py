import socket
import sys
import time

server_add = './bob_system_socket'

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
message = sys.argv[1]+" "+sys.argv[2]
if sys.argv[1] == 'set':
	message+= " "+sys.argv[3]
else:
	message+= " null"
try:
	sock.connect(server_add)
except socket.error, msg:
	print >>sys.stderr, msg
	sys.exit(1)
	
sock.send(message)
data = sock.recv(1024)
if data: print 'reply from server:', data
time.sleep(1)
sock.close()


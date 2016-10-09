import socket
import select
import Queue
from abc import ABCMeta, abstractmethod
import os

class CommandInterface:
	def run(self):
		serv_addr = './bob_system_socket'
		try:
			os.unlink(serv_addr)
		except OSError:
			if os.path.exists(serv_addr):
				raise
		
		self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.socket.bind(serv_addr)
		self.socket.listen(2)
	
		inputReqs = [ self.socket ]
		outputReqs = []
		message_queues = {}
		
		while inputReqs:
			readable, writable, exceptional = select.select(inputReqs, outputReqs, [])
			#handle incoming requests===============================
			for client in readable:
				if client is self.socket:
					conn, addr = self.socket.accept()
					conn.setblocking(False)
					inputReqs.append(conn)
					message_queues[conn] = Queue.Queue()
				else:
					data = client.recv(1024)
					if data:
						message_queues[client].put(data)
						#add output channel to reply to the request
						if client not in outputReqs:
							outputReqs.append(client)
					else:
						if client in outputReqs:
							outputReqs.remove(client)
						inputReqs.remove(client)
						client.close()
						del message_queues[client]
			
			#handle outgoing requests=========================
			for client in writable:
				try:
					next_msg = message_queues[client].get_nowait()
				except Queue.Empty:
					#no messages left, client has disconnected
					outputReqs.remove(client)
				else:
					#here I should process the command requests
					client.send(self.processCommand(next_msg))
			#Handle exceptions==================================		
			for client in exceptional:
				#remove a faulty client from the list
				inputReqs.remove(client)
				if client in outputReqs:
					outputReqs.remove(client)
				client.close()
				del message_queues[client]
				
	@abstractmethod
	def processCommand(self, cmd):
		pass
		
		
		
if __name__ == '__main__':
	print 'CommandInterface test'
	comm = CommandInterface()
	comm.run()
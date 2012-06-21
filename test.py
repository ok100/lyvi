import socket
import time

data_old = ''
s = socket.socket( socket.AF_UNIX )
s.connect( '/home/ok/.shell-fm/socket' )
while 1:
	s.send( 'info %a%t (%f)%I%l\n' )
	time.sleep( 1 )
	data = s.recv( 1024 ).strip()
	if data and data_old != data:
	    data_old = data
	print data
	time.sleep( 2 )
	s.send( 'skip' )
	time.sleep( 1 )
	data = s.recv( 1024 ).strip()
	if data and data_old != data:
	    data_old = data
	print data
	time.sleep( 2 )

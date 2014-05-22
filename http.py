import socket,threading,time
from os import stat,pipe


def accept_request(sock):

	cgi = False
	buf = get_line(sock)
	numchars = len(buf)

	method,url,proto = buf.split(' ')
	method = method.upper()
	if method != 'GET' and method != 'POST':
		unimplemented(sock)
		return 

	if method == 'POST':
		cgi = True

	if method == 'GET':
		query_string = url
		if '?' in query_string:
			cgi = True
			_,query_string = url.split('?')

	path = 'htdocs'+url
	if url == '/':
		path += 'index.html'
	try:
		stat(path)
	except:
		while numchars >0 and buf != '\n':
			buf = get_line(sock)
			numchars = len(buf)
		not_found(sock)
	else:
		if not cgi:
			serve_file(sock,path)
		else:
			execute_cgi(sock,path)
	finally:
		sock.close()




def bad_request(sock):
	pass

def cat(sock,resourse):
	for line in resourse:
		line = bytes(line,encoding='utf-8')
		sock.send(line)
	sock.send(b'\r\n\r\n')

def cannot_execute(sock):
	pass

def error_die():
	pass

def execute_cgi(sock,path,method,query_string):
	if method == 'GET':
		buf = ''
		while buf != '\n':
			buf = get_line(sock)
	else:
		content_length = -1
		buf = get_line(sock)
		while buf != '\n':
			if 'Content-Type' in buf:
				_,content_length = buf.split(':')
				content_length = int(conten_length)
		if conten_length == -1:
			bad_request(sock)
			return 
	buf = b'HTTP/1.0 200 OK\r\n'
	sock.send(buf)

	cgi_output = os.pipe()
	cgi_input = os.pipe()

		



def get_line(sock):
	buf = []
	i = 0
	c = '\0'
	while c!= '\n':
		c = sock.recv(1)
		c = c.decode()
		if c == '\r':
			c = sock.recv(1,socket.MSG_PEEK)
			c = c.decode()
			if c == '\n':
				c = sock.recv(1)
				c = c.decode()
			else:
				c = '\n'
		buf.append(c)
	return ''.join(buf)


def headers(sock,path):
	buf = b'HTTP/1.0 200 OK\r\n'
	sock.send(buf)
	buf = b'Server: jdbhttpd/0.1.0\r\n'
	sock.send(buf)
	buf = b'Content-Type: text/html; charset=utf-8\r\n'
	sock.send(buf)
	buf = b'\r\n'
	sock.send(buf)

def not_found(sock):
	buf = b'HTTP/1.0 400 NOT FOUND\r\n'
	sock.send(buf)
	buf = b'Content-Type: text/html\r\n'
	sock.send(buf)
	buf = b'\r\n'
	sock.send(buf)
	buf = b'<HTML><TITLE>Not Found</TITLE>\r\n'
	sock.send(buf)
	buf = b'<BODY><P>The server could not fulfill\r\n'
	sock.send(buf)
	buf = b'your request because the resource specified\r\n'
	sock.send(buf)
	buf = b'is unavailable or nonexistent.\r\n'
	sock.send(buf)
	buf = b'</BODY></HTML>\r\n\r\n'
	sock.send(buf)

def serve_file(sock,path):
	buf = ''
	while buf != '\n':
		buf = get_line(sock)
	try:
		resourse = open(path,encoding = 'utf-8')
	except:
		not_found(sock)
	else:
		headers(sock,path)
		cat(sock,resourse)
	finally:
		resourse.close()

def startup(port):
	sk = socket.socket()
	sk.bind(('127.0.0.1',port))
	sk.listen(5)
	print(sk)
	return sk

def unimplemented():
	pass

if __name__ == '__main__':
	port = 80
	serv_sock = startup(port)
	print(serv_sock.getsockname())
	print('httpd running on port %d\n'%port)

	while 1:
		client_sock,client_addr = serv_sock.accept()
		if client_sock == None:
			error_die('accept')
		th = threading.Thread(target = accept_request,args = (client_sock,))
		th.start()

	serv_sock.close()
	exit(0)

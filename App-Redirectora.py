#!/usr/bin/python

import socket
import random
# Create a TCP objet socket and bind it to a port
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind(('localhost', 1234))

# Queue a maximum of 5 TCP connection requests
mySocket.listen(5)
# Accept connections, read incoming data, and call
try:
    while True:
        print 'Waiting for connections'
        (recvSocket, address) = mySocket.accept()
        print 'HTTP request received'
        request = recvSocket.recv(1024)
        numero = random.randint(0, 999999)
        url = "http://localhost:1234/" + str(numero)
        print 'Answering back...'
        recvSocket.send("HTTP/1.1 308 Permanent Redirect \r\n" +
                        "Location: " + url + "\r\n" +
                        "<html><body><h1> Your being redirected again!</h1>" +
                        "</body></html>" + "\r\n")

        recvSocket.close()

except KeyboardInterrupt:
    print "Closing binding socket"
    mySocket.close()

#test_proxy.
# https://www.geeksforgeeks.org/creating-a-proxy-webserver-in-python-set-1/
import re
import sys, socket
from socket import *


error_page = "http://zebroid.ida.liu.se/error1.html"

server_port = 12345
#my_socket = socket(AF_INET, SOCK_DGRAM) # UDP socket
server_socket = socket(AF_INET, SOCK_STREAM)

server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #Re-use the socket (Jag vet inte vad detta gör)
server_socket.bind(('127.0.0.1', server_port))
server_socket.listen(10)

while True:
    print("test")
    client_socket, client_address = server_socket.accept() # Accepterar en ny tcp connection?
    #print("client_socket: {}\n client_address: {}".format(
    #    client_socket, client_address))

    request = client_socket.recv(3000) # request:en som clienten vill skicka.
    print(request)
    match = re.search('://(([\w.]+)/[\w./]*)', request.decode())
    webserver = match.group(2)
    print(webserver)

    # Ta reda på om hemsidan har en legal url.
    legal_url = True
    url = match.group(1).lower()
    illegal_content = ["norrkoping", "spongebob",
                       "britney_spears", "britneyspears",
                       "paris_hilton", "parishilton"]
    for illegal_item in illegal_content:
        if re.search(illegal_item, url):
            legal_url = False
            print("found illegal url")
            break

    print('This is legal checking: ', legal_url)
    # om illegal url
    if not legal_url:
        print("Gonna redirect...")
        bad_url_redirect = "http://zebroid.ida.liu.se/error1.html"
        webserver = "zebroid.ida.liu.se"

        #request = b'GET HTTP/1.1 302
        error_page = "http://zebroid.ida.liu.se/error1.html"

        #print(request)

        error_message = "HTTP/1.1 302 Found\r\nLocation: " + error_page + "\r\nHost: " + "zebroid.ida.liu.se" + "\r\nConnection: close\r\n\r\n"
        print("SEEEE HRÄÄRÄTÄRRÄ:  ", error_message.encode('ASCII'))
        client_socket.send(error_message.encode('ASCII'))
        client_socket.close()
        #sys.exit(1)

    else:

        # Om hemsidan är appropriate -> skicka vidare till extern server.
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(10)
        s.connect((webserver, 80))
        print("starting s.sendall")
        s.send(request)



        # Ta emot paket och skicka vidare till webbläsaren.
        while True:
            # receive data from web server
            print("1")
            data = s.recv(3000)
            print("2")

            if (len(data) > 0):
                client_socket.send(data) # send to browser/client
            else:
                break  # Bryter när hela "Http innehållet är inläst"

            # inappropriate hemsida -> skicka någon annan rolig request.
        s.close()
        client_socket.close()

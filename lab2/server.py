import socket
import sys

#Function that returns a bool whether the URL(OR content) contains any "bad words"
def find_bad_word(text_to_check):
    bad_words = ["SpongeBob", "Britney Spears"
    , "Paris Hilton", "norrkoping"]
    for i in bad_words:
        if i in text_to_check:
            print("Returning true")
            return True
    print("Returning False")
    return False


#Function that makes it so we dont have a limit on the size of HTTP data
def receive(socket):
    received_data = bytes('', encoding = 'ISO-8859-1')
    while 1:
        data = socket.recv(4096)
        if data:
            received_data += data
        else:
            break
    print("\nReceive function finished\n")
    return received_data


#Formats url in order for it to be used with the rest of the program
def format_url(url):
    http_pos = url.find("://")
    temp = url[(http_pos+3):]
    webserver_pos = temp.find("/")
    if webserver_pos == -1:
        webserver_pos = len(temp)
    print (temp[:webserver_pos],"\n")
    webpage = temp[:webserver_pos]
    return webpage


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind(("127.0.0.1", int(sys.argv[1])))
    print("Creating client_socket with port number:", sys.argv[1])
    client_socket.listen(1)
    print("Socket successfully created")

    while 1:
        conn, client_addr = client_socket.accept()
        request = conn.recv(4096)
        # request = receive(conn)
        if request:
            print("\nHere is the request: \n", request.decode('ISO-8859-1'))
            proxy(request, conn, client_addr)
        else:
            print("\nEmpty Request\n")

    client_socket.close()

#Function that handles everything.
def proxy(request, conn, client_addr):
    request_decoded = request.decode('ISO-8859-1')
    head_line = request_decoded.split('\n')[0]
    url = head_line.split(' ')[1]
    if find_bad_word(url):
        print("\nBad URL, redirecting...")
        webpage = format_url("http://zebroid.ida.liu.se/error1.html")
        request = b'HTTP/1.1 302 Found\r\nLocation: http://zebroid.ida.liu.se/error1.html\r\nHost: zebroid.ida.liu.se\r\nConnection: keep-alive\r\n\r\n'
        conn.sendall(request)
        print("Sending data")
        print("Success! Closing socket\n")
        conn.close()
    else:
        bad_content = False
        webpage = format_url(url)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((webpage, 80))
        server_socket.send(request)
        data = receive(server_socket)
        print("\n\n\n\nDATA!!: ", data, "\n\n\n\n")
        if "text/" in request.decode('ISO-8859-1'):
            if find_bad_word(data.decode('ISO-8859-1')):
                bad_content = True

        if bad_content:
            print("\nBad Content, redirecting..")
            server_socket.close()
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            webpage = format_url("http://zebroid.ida.liu.se/error2.html")
            request = b'GET http://zebroid.ida.liu.se/error2.html HTTP/1.1\r\nHost: zebroid.ida.liu.se\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\n\r\n'
            server_socket.connect((webpage, 80))
            server_socket.send(request)
            data = receive(server_socket)
            conn.sendall(data)
        else:
            conn.sendall(data)
            print("\nSending data")
        print("Success! Closing socket\n")
        server_socket.close()
        conn.close()

main()

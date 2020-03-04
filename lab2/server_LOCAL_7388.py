import socket
# next create a socket object

bad_words = ["SpongeBob", "Britney Spears"
, "Paris Hilton", "Norrkoping"]

def find_bad_word(bad_words_list, text_to_check):
    for i in bad_words_list:
        if i in text_to_check:
            return True
        else:
            return False

def format_url(url):
    http_pos = url.find("://")
    temp = url[(http_pos+3):]
    webserver_pos = temp.find("/")
    if webserver_pos == -1:
        webserver_pos = len(temp)
    print (temp[:webserver_pos],"\n")
    webpage = temp[:webserver_pos]
    return webpage


def make_request(url):
    error_message = "HTTP/1.1 302 Found\r\nLocation: " + url + "\r\nHost: " + "zebroid.ida.liu.se" + "\r\nConnection: keep-alive\r\n\r\n"
    request = error_message.encode('ASCII')
    return request
    # print("New Request: ", request,"\n")
    # http_pos = error_page.find("://")
    # temp = error_page[(http_pos+3):]
    # webserver_pos = temp.find("/")
    # print (temp[:webserver_pos],"\n")


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind(("127.0.0.1", 12345))
    client_socket.listen(1)
    print("Socket successfully created")

    while 1:
        conn, client_addr = client_socket.accept()
        request = conn.recv(4096)
        # print("Det här är requesten: ", request)
        if request:
            proxy(request, conn, client_addr)
        else:
            # print("Detta är en tom request: ", request)
            break
    client_socket.close()

def proxy(request, conn, client_addr):
    # print("REQUESTEN ÄR HÄR;;; ", request)
    request_decoded = request.decode('ISO-8859-1')
    # print("Detta är en decodad request: ", request_decoded)
    head_line = request_decoded.split('\n')[0]
    url = head_line.split(' ')[1]
    if find_bad_word(bad_words, url):
        webpage = format_url("http://zebroid.ida.liu.se/error1.html")
        request = make_request("http://zebroid.ida.liu.se/error1.html")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((webpage, 80))
        server_socket.send(request)
        conn.send(request)
        server_socket.close()
        conn.close()
    else:
        data_to_send = ""
        bad_content = False
        webpage = format_url(url)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((webpage, 80))
        server_socket.send(request)
        while 1:
            # print(" \njeglrkjelgkaejlkg \n")
            data = server_socket.recv(4096)
            # print("här är content i datan: \n", data.decode('ISO-8859-1'))
            # print("Här slutar datan \n")
            if find_bad_word(bad_words, data.decode('ISO-8859-1')):
                # print ("\nAKSFDJFLAKMALKDM\n")
                bad_content = True
                break
            if not data:
                # print("HMMMMMMMMMMMMM")
                break
            else:
                data_to_send += data.decode('ISO-8859-1')
        if bad_content:
            server_socket.close()
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            webpage = format_url("http://zebroid.ida.liu.se/error2.html")
            # print("OLD REQUEST:  ", request, "\n")
            # request = make_request("http://zebroid.ida.liu.se/error2.html")
            request = b'GET http://zebroid.ida.liu.se/error2.html HTTP/1.1\r\nHost: zebroid.ida.liu.se\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\n\r\n'
            server_socket.connect((webpage, 80))
            server_socket.send(request)
            while 1:
                data = server_socket.recv(4096)
                # print("Data från server: ", str(data),"\n")
                if data:
                    conn.send(data)
                    print("Det funkade! \n")
                else:
                    print("Tjenahopp")
                    break
        else:
            conn.send(data_to_send.encode('ASCII'))
            print("Det Funkade! \n")

        server_socket.close()
        conn.close()

main()

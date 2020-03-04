import socket
import sys

bad_words = ["SpongeBob", "Britney Spears"
, "Paris Hilton", "Norrkoping"]
<<<<<<< HEAD
=======

#Function that returns a bool whether the URL(OR content) contains any "bad words"
def find_bad_word(bad_words_list, text_to_check):
>>>>>>> 83cf7a0a900bd5b2dfe339806ef86b979b768504

def find_bad_word(bad_words_list, text_to_check):
    for i in bad_words_list:
        if i in text_to_check:
            return True
        else:
            return False

def receive(socket):
    received_data = ""
    while 1:
        data = socket.recv(4096)
        if data:
            received_data += data.decode('ISO-8859-1')
        else:
            break
    print("\nReceive function finished\n")
    return received_data.encode('ASCII')


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

<<<<<<< HEAD

def make_request(url):
    error_message = "HTTP/1.1 302 Found\r\nLocation: " + url + "\r\nHost: " + "zebroid.ida.liu.se" + "\r\nConnection: keep-alive\r\n\r\n"
    request = error_message.encode('ASCII')
    return request
    # print("New Request: ", request,"\n")
    # http_pos = error_page.find("://")
    # temp = error_page[(http_pos+3):]
    # webserver_pos = temp.find("/")
    # print (temp[:webserver_pos],"\n")


=======
>>>>>>> 83cf7a0a900bd5b2dfe339806ef86b979b768504
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind(("127.0.0.1", int(sys.argv[1])))
    print("Create client_socket with port number:", sys.argv[1])
    client_socket.listen(1)
    print("Socket successfully created")

    while 1:
        conn, client_addr = client_socket.accept()
        request = conn.recv(4096)
        # request = receive(conn)
        if request:
            print("Det här är requesten: ", request.decode('ISO-8859-1'))
            proxy(request, conn, client_addr)
        else:
            print("Detta är en tom request: ", request)
            #break
    client_socket.close()

#Function that handles everything.
def proxy(request, conn, client_addr):
    # print("REQUESTEN ÄR HÄR;;; ", request)
    request_decoded = request.decode('ISO-8859-1')
    # print("Detta är en decodad request: ", request_decoded)
    head_line = request_decoded.split('\n')[0]
    url = head_line.split(' ')[1]
    # if find_compressed(compressed_words, url)
    # if "text/" in request.decode('ISO-8859-1'):
    #     print("HMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
    if find_bad_word(bad_words, url):
        webpage = format_url("http://zebroid.ida.liu.se/error1.html")
        request = b'HTTP/1.1 302 Found\r\nLocation: http://zebroid.ida.liu.se/error1.html\r\nHost: zebroid.ida.liu.se\r\nConnection: keep-alive\r\n\r\n'
        # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server_socket.connect((webpage, 80))
        # server_socket.send(request)
        conn.sendall(request)
        # server_socket.close()
        conn.close()
        # else:
        #     data_to_send = ""
        #     bad_content = False
        #     webpage = format_url(url)
        #     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     server_socket.connect((webpage, 80))
        #     server_socket.send(request)
        #     while 1:
        #         # print(" \njeglrkjelgkaejlkg \n")
        #         data = server_socket.recv(4096)
        #         # print("här är content i datan: \n", data.decode('ISO-8859-1'))
        #         # print("Här slutar datan \n")
        #         if find_bad_word(bad_words, data.decode('ISO-8859-1')):
        #             # print ("\nAKSFDJFLAKMALKDM\n")
        #             bad_content = True
        #             break
        #         if not data:
        #             # print("HMMMMMMMMMMMMM")
        #             break
        #         else:
        #             data_to_send += data.decode('ISO-8859-1')
    else:
        data_to_send = ""
        bad_content = False
        webpage = format_url(url)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((webpage, 80))
        server_socket.send(request)
        data = receive(server_socket)
        print("\n\n\n\nDATA!!: ", data, "\n\n\n\n")
        if "text/" in request.decode('ISO-8859-1'):
            if find_bad_word(bad_words, data.decode('ISO-8859-1')):
                bad_content = True
        # while 1:
        #     # print(" \njeglrkjelgkaejlkg \n")
        #     data = server_socket.recv(16)
        #
        #     if "text/" in data.decode('ISO-8859-1'):
        #         print("HMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
            # print("här är content i datan: \n", data.decode('ISO-8859-1'))
            # print("Här slutar datan \n")
                # if find_bad_word(bad_words, data.decode('ISO-8859-1')):
                #     # print ("\nAKSFDJFLAKMALKDM\n")
                #     bad_content = True
                #     break
        #     if not data:
        #         # print("HMMMMMMMMMMMMM")
        #         break
        #     else:
        #         data_to_send += data.decode('ISO-8859-1')
        if bad_content:
            server_socket.close()
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            webpage = format_url("http://zebroid.ida.liu.se/error2.html")
            # print("OLD REQUEST:  ", request, "\n")
            # request = make_request("http://zebroid.ida.liu.se/error2.html")
            request = b'GET http://zebroid.ida.liu.se/error2.html HTTP/1.1\r\nHost: zebroid.ida.liu.se\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\n\r\n'
            server_socket.connect((webpage, 80))
            server_socket.send(request)
            data = receive(server_socket)
            conn.sendall(data)
            # while 1:
            #     data = server_socket.recv(400096)
            #     # print("Data från server: ", str(data),"\n")
            #     if data:
            #         conn.sendall(data)
            #         print("Det funkade! \n")
            #     else:
            #         print("Tjenahopp")
            #         break
        else:
            conn.sendall(data)
            print("Det Funkade! \n")
        print("\n\n\n\nlajglkadjglkadjg\n\n\n\n")
        server_socket.close()
        conn.close()

main()

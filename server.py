#Farhan Sadiq
#1001859500


#Importing the os, threading and socket module for networking interfaces, multi threading support and OS related functionality.
import os
import socket
import threading

#Defining the host ip address.
HOST = 'localhost'

#Defining the portnumber that the server intends to listen.
PORT = 6789

#Defining the directory that has all the files.
MY_DIR = "all_files"

#Function c_r handles the client requests.
def c_r(c_s):

    #Receiving data from the client socket.
    data = c_s.recv(1024)

    #Parsing the request by calling the p_r() function.
    fp = p_r(data)

    #print(fp)           #Debugging purpose

    #Generating the response for the request by calling the g_r() function.
    output_data = g_r(fp)

    #Sending the response to the client.    
    c_s.sendall(output_data)

    #Closing the client socket.
    c_s.close()


#Function p_r() is responsible for parsing the client request.
def p_r(data):

    #Spliting data into lines.
    lines = data.decode().split('\r\n')

    #First line contains method and path.
    l1 = lines[0]

    #Splitting line into components.
    s_c = l1.split(' ')

    #Get the requested file path
    fp = s_c[1]

    #print(fp)           #Debugging purpose
    
    #Serving the requested file.
    return os.path.join(MY_DIR, fp.lstrip('/'))


#Function that generates response for the file that is requested.
def g_r(fp):

    #Checks if file does not exist.
    if not os.path.exists(fp):
        #Shows error 404.
        fp = os.path.join(MY_DIR, '404.html')

        #Setting the status code for 404 error.
        status_code = '404 Not Found'
    
    #Checks if the fp is referring to page1.
    elif(fp == '/page1.html'):
        #Sets the status code
        status_code = '301 Moved permanently'

        #Joins page2.html
        fp = os.path.join(MY_DIR, 'page2.html')

    else:
        #Setting status code for correct response.
        status_code = '200 OK'

    #Open file to read contents of the file.
    with open(fp, 'rb') as file:
        content = file.read()

    #Http response headers, content type headers and content length headers.
    headers = f"HTTP/1.1 {status_code}\r\n"
    headers = headers + "Content-Type: text/html\r\n"
    headers = headers + f"Content-Length: {len(content)}\r\n\r\n"

    #Returning the content and encoded headers.
    return headers.encode() + content

#Function that starts the server.
def start_server():
    #Creating the TCP socket.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Binding the socket to HOST and PORT.
    server_socket.bind((HOST, PORT))

    #Listening for connections
    server_socket.listen(5)

    #The print statement indicates that the server is actively listening.
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        #Accepts client connections and creates new thread to handle clent.
        client_socket, _ = server_socket.accept()
        client_thread = threading.Thread(target = c_r, args = (client_socket,))
        client_thread.start()

if __name__ == "__main__":

    #Calls the function to start server.
    start_server()

import socket
import thread
import select

serverPort = 12035
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind(('',serverPort))
serverSocket.listen(5)
print 'The server is ready to receive'

list_name = ['user1', 'user2','user3']
list_pwd = ['0000', '0001','0010']
online = ['0','0','0']
listonline = []
ex_socket = ['0','0','0']

off_msg = {}
off_msg['user1'] = ''
off_msg['user2'] = ''
off_msg['user3'] = ''

connect_soc = []

log_in_suc = 0

def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != serverSocket and socket != sock :
            try :
                socket.send(message)
            except :
                socket.close()
                CONNECTION_LIST.remove(socket)

def log_in():
    #check username & password
    name = connectionSocket.recv(1024)
    for i in range(len(list_name)):
        if name == list_name[i]:
            no_find = 0
            print 'right user'
            connectionSocket.send('01')
            #password
            passwd = connectionSocket.recv(1024)
            print passwd
            if passwd == list_pwd[i]:
                print 'right password'
                log_in_suc = 1
                online[i] = 1
                ex_socket[i] = connectionSocket
                connectionSocket.send('02')
                listonline.append(list_name[i])

                if off_msg[list_name[i]] != '':
                    print off_msg[list_name[i]]
                    connectionSocket.send(off_msg[list_name[i]])
            else:
                print 'error passwd'

    if no_find == 1:
        print 'error user'

def acceptThread(connSock):
    print 'client is accepted'
    while 1:
        #command mode
        command_rec = connSock.recv(1024)   
        print command_rec
        
        #chat mode
        CONNECTION_LIST = [connSock]
        if command_rec == '1':
            r_sockets, w_sockets, e_sockets = select.select(CONNECTION_LIST,[],CONNECTION_LIST)
            if (e_sockets):
                return
            
            chat_user = connSock.recv(1024) #get username
            chat_user = chat_user[0:5]
            print chat_user

            for sock in r_sockets:
                if chat_user in list_name:
                    print 'user exist'
                    
                    data = sock.recv(1024)
                    if data == 'quit\n':
                        break
                    if data[0:4] == 'send':
                        for i in range(len(list_name)):
                            if list_name[i] == data[5:10]:
                                ex_socket[i].send(data[10:len(data)])
                else:
                    print 'user not online'
                    data = sock.recv(1024)
                    print data
                    off_msg[data[5:10]] = data[10:len(data)]

        #list
        elif command_rec == '2':
            print 'listonline'
            print listonline
            connSock.send(str(listonline))
        #broadcastst
        elif command_rec == '3':
            message = connSock.recv(1024)
            print message
            for i in range(len(list_name)):
                if (ex_socket[i] != '0') and (ex_socket[i] != connSock):
                    ex_socket[i].send(message)
                    #broadcast_data (connSock,  message)
        elif command_rec == '4':
            name = connSock.recv(1024)
            listonline.remove(name)
    connSock.close()


while 1:
    connectionSocket, addr = serverSocket.accept()
    print 'accepted'

    no_find = 1
    log_in()
    
    thread.start_new_thread(acceptThread, (connectionSocket,))
    
connectionSocket.close()

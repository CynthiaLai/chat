import socket
import select
import thread
import time
import sys
import getpass

serverName = socket.gethostname()
serverPort = 12035
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
clientSocket.connect((serverName,serverPort))
logout_flag = 0

def broadThread(connSock):
    while logout_flag == 0:
        data = connSock.recv(1024)
	print '\r' + data

def commmdThread(cmndSock):
    print '(1)chatting mode\n(2)list all user\n(3)broadcast\n(4)log out'
    while 1:
        command_rec = raw_input('>')
        if command_rec == '1':
            global msg_list
            chat_mode = 1 
            command_rec = '1'		
            cmndSock.send(command_rec)
            chat_user = raw_input('\nchoose user: (quit to exit chat mode)\n')

            while chat_user != 'quit':
                cmndSock.send(chat_user)
                msg = raw_input('msg : ')
                if msg == 'quit':
                    break
                msg = 'send' + ' ' + chat_user + ' ' + msg
                clientSocket.send(msg)
        elif command_rec == '2':	
            cmndSock.send(command_rec)
            print 'list user'
        elif command_rec == '3':
            cmndSock.send(command_rec)
            broad_msg = raw_input('broadcast msg: ')
            cmndSock.send(broad_msg)                           
        elif command_rec == '4':
            global logout_flag
            cmndSock.send(command_rec)
            cmndSock.send(name)
            print name + ' logout'
            logout_flag = 1
            break
    
print 'log in '
#receive username & password
name = raw_input('username : ')
clientSocket.send(name)

passkey = clientSocket.recv(1024)
if (passkey == '01'):
    passwd = getpass.getpass('password : ')
    clientSocket.send(passwd)
    passkey = clientSocket.recv(1024)
    if (passkey == '02'):
        print 'user login success!'
        
        thread.start_new_thread(broadThread, (clientSocket,))
        print 'command mode: '
        thread.start_new_thread(commmdThread, (clientSocket,))
    else:
        print 'error password'
else:
    print 'error user'


while logout_flag == 0:
    time.sleep(1)
clientSocket.close()

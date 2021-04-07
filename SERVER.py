import socket
from _thread import *
import sys

server = socket.gethostname()
port = 55555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def read(str):
    str = str.split(",")
    return (int(str[0]), int(str[1]))
def read1(str,b):
    str = str.split(",")
    if b == 0:    
        a  =  1530 - int(str[0])    
        return (a,int(str[1])) 
    else:
        return (int(str[0]),int(str[1])) 

def make(tup):
    return str(tup[0]) + "," + str(tup[1])
def make1(tup):
    return '1' + str(tup[0]) + "," + str(tup[1])  
pos = [(335,475),(335,480)]
pos1 = [(765,405),(765,405)]
def threaded_client(conn, player):
    conn.sendall(str.encode(make(pos[player])))
    reply = ""
    reply1 = ""
    while True:
        try:
            data = conn.recv(2048).decode()
     
 
            if data[0] == 'B':
                
                data = read1(data[2:],player)
              
                pos1[player] = data 

                if player == 1:
                    reply1= pos1[0]
                    
                    conn.sendall(str.encode(make1(reply1)))
                else:
                    conn.sendall(str.encode("HELLO"))  
            else:
                data = read(data[2:])
                pos[player] = data
          
    
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]


                conn.sendall(str.encode(make(reply)))
        except:
            break

    print("Lost connection")
    conn.close()

cp = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, cp))
    cp += 1 

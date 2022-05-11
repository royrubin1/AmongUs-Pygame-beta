import random
import socket
import threading
import pickle
import time

ServerSocket = socket.socket()
host = '0.0.0.0'
port = 1233
ThreadCount = 0
Lock =  threading.Lock()
IMPOSTERS_NUMBER = 1

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

ServerSocket.settimeout(0.1)

#print('Waiting for a Connection..')
#ServerSocket.listen(10)

data_list = []
thread_list = []
socket_list = []

def threaded_client(connection, ThreadNum):
    global data_list, Lock

    connection.settimeout(0.1)
    while True:
        try:
            # getting the client data
            data = connection.recv(2048)
            data = pickle.loads(data)
            Lock.acquire()
            data_list[ThreadNum] = data
            Lock.release()
            # sending a reply message to the client
            connection.send(pickle.dumps(data_list))
        except socket.timeout as e:
            if Lock.locked():
                Lock.release
    connection.close()

while True:
    ServerSocket.listen(5)
    try:
        Client, address = ServerSocket.accept()
        socket_list.append(Client)
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        data_list.append([''])
        t = threading.Thread(target = threaded_client, args = (Client, ThreadCount))
        ThreadCount += 1
        thread_list.append(t)
        t.start()
    except socket.timeout as e:
        pass
    except Exception as e:
        print(str(e))
    
    if ThreadCount >= 4: #7 
        break
ServerSocket.close()


def send_all(shuffled_list, limit, message1, message2):
    for i in range(len(thread_list)):
        if i in l[:limit]:
            socket_list[i].send(message1.encode())
        else:
            socket_list[i].send(message2.encode()) # CREW

# Fase 2 - The actual game
start_time = time.time()
time.sleep(0.1)
l = list(range(ThreadCount))
random.shuffle(l)

send_all(l,IMPOSTERS_NUMBER, "I", "C")

while time.time() - start_time < 5*60:
    pass

send_all(l,0, "", "DONE")

"""
if pickle is valid -> game message
if pickle is invalid -> irregular message, i.e. game_start / game_end / someone_killed / etc.
"""

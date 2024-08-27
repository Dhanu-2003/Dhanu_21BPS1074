import socket
import threading
import random

data = {}
pos = {}
grid = {}
chat = {}
moves = {}
turn = {}

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"Connection closed by {client_address}")
                break
            if message[0]=="1":
                name = message.split("-")[1]
                while True:
                    try:
                        code = str(random.randint(12345,99999))
                        data[code] = [[client_socket,name+" [A]"],[]]
                        pos[code] = [[],[]]
                        data[code][0][0].send(code.encode('utf-8'))
                        moves[code] = []
                        grid[code] = []
                        chat[code] = []
                        turn[code] = [1,0]
                        break
                    except:
                        continue
            elif message[0]=="2":
                temp = message.split("-")
                code = temp[1]
                name = temp[2]
                try:
                    data[code][1].append(client_socket)
                    data[code][1].append(name+" [B]")
                    data[code][1][0].send("1".encode('utf-8'))
                except Exception as e:
                    print(e)
                    client_socket.send("0".encode('utf-8'))
            elif message[0]=="a":
                temp = message.split("-")[1::]
                k = temp[0:5]
                if temp[-2]==data[temp[-1]][0][1]:
                    for i in range(5):
                        if k[i]=="1":
                            k[i]="A:P"
                        elif k[i]=="2":
                            k[i]="A:H1"
                        elif k[i]=="3":
                            k[i]="A:H2"
                    print(k)
                    pos[temp[-1]][0].extend(k)
                    print(pos)
                    data[temp[-1]][0][0].send("1".encode("utf-8"))
                else:
                    for i in range(5):
                        if k[i]=="1":
                            k[i]="B:P"
                        elif k[i]=="2":
                            k[i]="B:H1"
                        elif k[i]=="3":
                            k[i]="B:H2"
                    print(k)
                    pos[temp[-1]][1].extend(k)
                    print(pos)
                    data[temp[-1]][1][0].send("1".encode("utf-8"))
            elif message[0]=="3":
                temp = message.split("-")[1::]
                print(temp)
                if data[temp[1]][0][1]==temp[0]:
                    if pos[temp[-1]][1]!=[]:
                        toSend = data[temp[-1]][0][1]+"-"+data[temp[-1]][1][1]+"-"+temp[-1]
                        temp_code = temp[1]
                        
                        grid[temp_code] = [pos[temp_code][0]]
                        grid[temp_code].extend([["" for _ in range(5)] for _ in range(3)]+[pos[temp_code][1]])
                        print(toSend)
                        print("--------------------------")
                        client_socket.send(toSend.encode("utf-8"))
                    else:
                        client_socket.send("0".encode("utf-8"))
                else:
                    if pos[temp[-1]][0]!=[]:
                        toSend = data[temp[-1]][1][1]+"-"+data[temp[-1]][0][1]+"-"+temp[-1]
                        temp_code = temp[-1]
                        
                        grid[temp_code] = [pos[temp_code][0]]
                        grid[temp_code].extend([["" for _ in range(5)] for _ in range(3)]+[pos[temp_code][1]])
                        print(toSend)
                        print("--------------------------")
                        client_socket.send(toSend.encode("utf-8"))
                    else:
                        client_socket.send("0".encode("utf-8"))
            
            elif message[0]=="A":
                temp = message.split("-")
                temp_code = temp[1]
                temp_name = temp[2]
                temp_grid = grid[temp_code]
                if data[temp_code][0][1]==temp_name:
                    temp_turn = turn[temp_code][0]
                else:
                    temp_turn = turn[temp_code][1]
                toSend = str([temp_turn,temp_grid,moves[temp_code],chat[temp_code]])
                client_socket.send(toSend.encode("utf-8"))
                        
                    

                


        except ConnectionResetError:
            print(f"Connection reset by {client_address}")
            break

    client_socket.close()

def start_server(host='0.0.0.0', port=1074):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server()

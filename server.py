import socket
import threading
import random

data = {}
pos = {}
grid = {}
chat = {}
moves = {}
turn = {}

cap = {}

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
                        data[code] = [[client_socket,name,"A"],[]]
                        pos[code] = [[],[]]
                        data[code][0][0].send(code.encode('utf-8'))
                        moves[code] = []
                        grid[code] = []
                        chat[code] = []
                        turn[code] = [1,0]
                        cap[code] = [[],[]]
                        break
                    except:
                        continue
            elif message[0]=="2":
                temp = message.split("-")
                code = temp[1]
                name = temp[2]
                try:
                    data[code][1].append(client_socket)
                    data[code][1].append(name)
                    data[code][1].append("B")
                    data[code][1][0].send("1".encode('utf-8'))
                except Exception as e:
                    print(e)
                    client_socket.send("0".encode('utf-8'))
            elif message[0]=="a":
                temp = message.split("-")[1::]
                coin = {"P":0,"H1":0,"H2":0}
                k = temp[0:5]
                if temp[-2]==data[temp[-1]][0][1]:
                    for i in range(5):
                        if k[i]=="1":
                            coin["P"]+=1
                            k[i]="A:P"+str(coin["P"])
                        elif k[i]=="2":
                            coin["H1"]+=1
                            k[i]="A:H1"+str(coin["H1"])
                        elif k[i]=="3":
                            coin["H2"]+=1
                            k[i]="A:H2"+str(coin["H2"])
                    
                    pos[temp[-1]][0] = k
                    data[temp[-1]][0][0].send("1".encode("utf-8"))
                else:
                    for i in range(5):
                        if k[i]=="1":
                            coin["P"]+=1
                            k[i]="B:P"+str(coin["P"])
                        elif k[i]=="2":
                            coin["H1"]+=1
                            k[i]="B:H1"+str(coin["H1"])
                        elif k[i]=="3":
                            k[i]="B:H2"+str(coin["H2"])
                    
                    pos[temp[-1]][1] = k
                    data[temp[-1]][1][0].send("1".encode("utf-8"))
            elif message[0]=="3":
                temp = message.split("-")[1::]
                print(temp)
                if data[temp[1]][0][1]==temp[0]:
                    if pos[temp[-1]][1]!=[]:
                        toSend = data[temp[-1]][0][1]+" ["+data[temp[-1]][0][2]+"]"+"-"+data[temp[-1]][1][1]+" ["+data[temp[-1]][1][2]+"]"+"-"+temp[-1]
                        temp_code = temp[1]
                        grid[temp_code] = [pos[temp_code][0]]
                        grid[temp_code].extend([["" for _ in range(5)] for _ in range(3)]+[pos[temp_code][1]])
                        print(grid[temp_code])
                        client_socket.send(toSend.encode("utf-8"))
                    else:
                        client_socket.send("0".encode("utf-8"))
                else:
                    if pos[temp[-1]][0]!=[]:
                        toSend = data[temp[-1]][1][1]+" ["+data[temp[-1]][1][2]+"]"+"-"+data[temp[-1]][0][1]+" ["+data[temp[-1]][0][2]+"]"+"-"+temp[-1]
                        temp_code = temp[-1]
                        grid[temp_code] = [pos[temp_code][0]]
                        grid[temp_code].extend([["" for _ in range(5)] for _ in range(3)]+[pos[temp_code][1]])
                        print(grid[temp_code])
                        client_socket.send(toSend.encode("utf-8"))
                    else:
                        client_socket.send("0".encode("utf-8"))
            
            elif message[0]=="A":
                temp = message.split("-")
                temp_code = temp[1]
                temp_name = temp[2].split()[0]
                temp_grid = grid[temp_code]
                if data[temp_code][0][1]==temp_name:
                    temp_turn = turn[temp_code][0]
                else:
                    temp_turn = turn[temp_code][1]
                print(turn,temp_turn)
                toSend = str([temp_turn,temp_grid,moves[temp_code],chat[temp_code]])
                client_socket.send(toSend.encode("utf-8"))
            elif message[0]=="B":
                temp = message.split("-")[1::]
                
                temp_n = temp[0].split()
                if data[temp[1]][0][1] in temp_n[0]:
                    temp_g = grid[code]
                    se = int(temp[-1])
                    row = se//5
                    col = se%5
                    ele = temp_grid[row][col]
                    pos_mov = []
                    print(data[temp[1]][0][2])
                   
                    if "P" in ele:
                        try:
                            print(temp_g[row+1][col])
                            if(temp_g[row+1][col]==""):
                                
                                pos_mov.append("F")
                        except:
                            pass
                        try:
                            if row!=0:
                                if(temp_g[row-1][col]==""):
                                    pos_mov.append("B")
                        except:
                            pass
                        try:
                            if col!=0:
                                print(temp_g[row][col-1],row,col)
                                if(temp_g[row][col-1]==""):
                                    print(True,data[temp[1]][0][2])
                                    pos_mov.append("L")
                        except:
                            pass
                        try:
                            if(temp_g[row][col+1]==""):
                                pos_mov.append("R")
                        except:
                            pass
                    elif "H1" in ele:
                        print(row,col)
                        try:
                            if(data[temp[1]][0][2] not in temp_g[row+1][col] and data[temp[1]][0][2] not in temp_g[row+2][col]):
                                pos_mov.append("F")
                        except:
                            pass
                        try:
                            if row>1:
                                if(data[temp[1]][0][2] not in temp_g[row-2][col] and data[temp[1]][0][2] not in temp_g[row-1][col]):
                                    pos_mov.append("B")
                        except:
                            pass
                        try:
                            if col>1:
                                if(data[temp[1]][0][2] not in temp_g[row][col-1] and data[temp[1]][0][2] not in temp_g[row][col-2]):
                                    pos_mov.append("L")
                        except:
                            pass
                        try:
                            if(data[temp[1]][0][2] not in temp_g[row][col+1] and data[temp[1]][0][2] not in temp_g[row][col+2]):
                                pos_mov.append("R")
                        except:
                            pass
                        
                    elif "H2" in ele:
                        try:
                            if(data[temp[1]][0][2] not in temp_g[row+1][col+1] and data[temp[1]][0][2] not in temp_g[row+2][col+2]):
                                pos_mov.append("FR")
                        except:
                            pass
                        try:
                            if col>1 and row>1:
                                if(data[temp[1]][0][2] not in temp_g[row-1][col-1] and data[temp[1]][0][2] not in temp_g[row-2][col-2]):
                                    pos_mov.append("BL")
                        except:
                            pass
                        try:
                            if col>1:
                                if(data[temp[1]][0][2] not in temp_g[row+1][col-1] and data[temp[1]][0][2] not in temp_g[row+2][col-2]):
                                    pos_mov.append("FL")
                        except:
                            pass
                        try:
                            if row>1:
                                if(data[temp[1]][0][2] not in temp_g[row-1][col+1] and data[temp[1]][0][2] not in temp_g[row-2][col+2]):
                                    pos_mov.append("BL")
                        except:
                            pass
                else:
                    
                    temp_g = grid[code]
                    se = int(temp[-1])
                    row = se//5
                    col = se%5
                    ele = temp_grid[row][col]
                    print(ele)
                    pos_mov = []
                    if "P" in ele:
                        try:
                            if(data[temp[1]][1][2] not in temp_g[row+1][col] ):
                                pos_mov.append("B")
                        except:
                            pass
                        try:
                            if row!=0:
                                if(data[temp[1]][1][2] not in temp_g[row-1][col]):
                                    
                                    pos_mov.append("F")
                        except:
                            pass
                        try:
                            if col!=0:
                                print(temp_g[row][col-1],row,col)
                                if(data[temp[1]][1][2] not in temp_g[row][col-1]):
                                    print(True,data[temp[1]][1][2])
                                    pos_mov.append("L")
                        except:
                            pass
                        try:
                            if(data[temp[1]][1][2] not in temp_g[row][col+1]):
                                pos_mov.append("R")
                        except:
                            pass
                    elif "H1" in ele:
                        try:
                            if(data[temp[1]][1][2] not in temp_g[row+1][col] and data[temp[1]][1][2] not in temp_g[row+2][col]):
                                pos_mov.append("B")
                        except:
                            pass
                        try:
                            if row>1:
                                if(data[temp[1]][1][2] not in temp_g[row-2][col] and data[temp[1]][1][2] not in temp_g[row-1][col]):
                                    pos_mov.append("F")
                        except:
                            pass
                        try:
                            if col>1:
                                if(data[temp[1]][1][2] not in temp_g[row][col-1] and data[temp[1]][1][2] not in temp_g[row][col-2]):
                                    pos_mov.append("L")
                        except:
                            pass
                        try:
                        
                            if(data[temp[1]][1][2] not in temp_g[row][col+1] and data[temp[1]][1][2] not in temp_g[row][col+2]):
                                pos_mov.append("R")
                        except:
                            pass
                        
                    elif "H2" in ele:
                        try:
                            if(data[temp[1]][1][2] not in temp_g[row+1][col+1] and data[temp[1]][1][2] not in temp_g[row+2][col+2]):
                                pos_mov.append("BR")
                        except:
                            pass
                        try:
                            if row>1 and col>1:
                                if(data[temp[1]][1][2] not in temp_g[row-1][col-1] and data[temp[1]][1][2] not in temp_g[row-2][col-2]):
                                    pos_mov.append("FL")
                        except:
                            pass
                        try:
                            if col>1:
                                if(data[temp[1]][1][2] not in temp_g[row+1][col-1] and data[temp[1]][1][2] not in temp_g[row+2][col-2]):
                                    pos_mov.append("BL")
                        except:
                            pass
                        try:
                            if row>1:
                                if(data[temp[1]][1][2] not in temp_g[row-1][col+1] and data[temp[1]][1][2] not in temp_g[row-2][col+2]):
                                    pos_mov.append("FL")
                        except:
                            pass
                client_socket.send(str(pos_mov).encode("utf-8"))
            elif message[0]=="C":
                temp = message.split("-")[1::]
                t_m = temp[0]
                t_e = temp[1]
                t_c = temp[2]
                row = int(t_e)//5
                col = int(t_e)%5
                tele = grid[t_c][row][col]
                if "B" in tele:
                    if t_m=="F":
                        t_m="B"
                    elif t_m=="B":
                        t_m="F"
                    elif t_m=="L":
                        t_m="R"
                    elif t_m=="R":
                        t_m="L"
                    elif t_m=="FR":
                        t_m="BR"
                    elif t_m=="FL":
                        t_m="BL"
                    elif t_m=="BR":
                        t_m="FR"
                    elif t_m=="BL":
                        t_m="FL"
                moves[t_c].append(tele+"-"+t_m)
                print(moves)
                if turn[t_c][0]==1:
                    turn[t_c][0]=0
                    turn[t_c][1]=1
                else:
                    turn[t_c][1]=0
                    turn[t_c][0]=1
                print(turn[t_c])
                if t_m=="F":
                    
                    if "P" in tele:
                        grid[t_c][row][col],grid[t_c][row+1][col] = grid[t_c][row+1][col],grid[t_c][row][col]
                    elif "H1" in tele:
                        
                        if grid[t_c][row+1][col]!="":
                            if tele[0]=="A":
                                cap[t_c][0].append(grid[t_c][row+1][col])
                            else:
                                cap[t_c][1].append(grid[t_c][row+1][col])
                        if grid[t_c][row+2][col]!="":
                            if tele[0]=="A":
                                cap[t_c][0].append(grid[t_c][row+2][col])
                            else:
                                cap[t_c][1].append(grid[t_c][row+2][col])
                        
                        grid[t_c][row+2][col],grid[t_c][row][col] = grid[t_c][row][col],""
                elif t_m=="L":
                    
                    if "P" in tele:
                        grid[t_c][row][col],grid[t_c][row][col-1] = grid[t_c][row][col-1],grid[t_c][row][col]
                    elif "H1" in tele:
                        
                        if grid[t_c][row][col-1]!="":
                            if tele[0]=="A":
                                cap[t_c][0].append(grid[t_c][row][col-1])
                            else:
                                cap[t_c][1].append(grid[t_c][row][col-1])
                        if grid[t_c][row][col-2]!="":
                            if tele[0]=="A":
                                cap[t_c][0].append(grid[t_c][row][col-2])
                            else:
                                cap[t_c][1].append(grid[t_c][row][col-2])
                        
                        grid[t_c][row][col-2],grid[t_c][row][col] = grid[t_c][row][col],""
                elif t_m=="R":
                    
                    if "P" in tele:
                        grid[t_c][row][col],grid[t_c][row][col+1] = grid[t_c][row][col+1],grid[t_c][row][col]
                    elif "H1" in tele:
                        
                        if grid[t_c][row][col+1]!="":
                            if tele[0]=="A":
                                cap[t_c][0].append(grid[t_c][row][col+1])
                            else:
                                cap[t_c][1].append(grid[t_c][row][col+1])
                        if grid[t_c][row][col+2]!="":
                            if tele[0]=="A":
                                cap[t_c][0].append(grid[t_c][row][col+2])
                            else:
                                cap[t_c][1].append(grid[t_c][row][col+2])
                        
                        grid[t_c][row+2][col],grid[t_c][row][col] = grid[t_c][row][col],""
                elif t_m=="B":
                    
                    if "P" in tele:
                        grid[t_c][row][col],grid[t_c][row-1][col] = grid[t_c][row-1][col],grid[t_c][row][col]
                    elif "H1" in tele:
                        if grid[t_c][row-1][col]!="":
                            if tele[0]=="A":
                                cap[t_c][0].append(grid[t_c][row-1][col])
                            else:
                                cap[t_c][1].append(grid[t_c][row-1][col])
                        if grid[t_c][row-2][col]!="":
                            if tele[0]=="A":
                                cap[t_c][0].append(grid[t_c][row-2][col])
                            else:
                                cap[t_c][1].append(grid[t_c][row-2][col])
                        
                        grid[t_c][row-2][col],grid[t_c][row][col] = grid[t_c][row][col],""
                
                elif t_m=="FL":
                    print("inside")
                    if grid[t_c][row+1][col-1]!="":
                        if tele[0]=="A":
                            cap[t_c][0].append(grid[t_c][row+1][col-1])
                        else:
                            cap[t_c][1].append(grid[t_c][row+1][col-1])
                    if grid[t_c][row+2][col-2]!="":
                        if tele[0]=="A":
                            cap[t_c][0].append(grid[t_c][row+2][col-2])
                        else:
                            cap[t_c][1].append(grid[t_c][row+2][col-2])
                    
                    grid[t_c][row+2][col-2],grid[t_c][row][col] = grid[t_c][row][col],""
                elif t_m=="FR":
                    if grid[t_c][row+1][col+1]!="":
                        if tele[0]=="A":
                            cap[t_c][0].append(grid[t_c][row+1][col+1])
                        else:
                            cap[t_c][1].append(grid[t_c][row+1][col+1])
                    if grid[t_c][row+2][col+2]!="":
                        if tele[0]=="A":
                            cap[t_c][0].append(grid[t_c][row+2][col+2])
                        else:
                            cap[t_c][1].append(grid[t_c][row+2][col+2])
                    
                    grid[t_c][row+2][col+2],grid[t_c][row][col] = grid[t_c][row][col],""
                
                elif t_m=="BL":
                    if grid[t_c][row-1][col-1]!="":
                        if tele[0]=="A":
                            cap[t_c][0].append(grid[t_c][row-1][col-1])
                        else:
                            cap[t_c][1].append(grid[t_c][row-1][col-1])
                    if grid[t_c][row-2][col-2]!="":
                        if tele[0]=="A":
                            cap[t_c][0].append(grid[t_c][row-2][col-2])
                        else:
                            cap[t_c][1].append(grid[t_c][row-2][col-2])
                    
                    grid[t_c][row-2][col-2],grid[t_c][row][col] = grid[t_c][row][col],""
                
                elif t_m=="BR":
                    if grid[t_c][row-1][col+1]!="":
                        if tele[0]=="A":
                            cap[t_c][0].append(grid[t_c][row-1][col+1])
                        else:
                            cap[t_c][1].append(grid[t_c][row-1][col+1])
                    if grid[t_c][row-2][col+2]!="":
                        if tele[0]=="A":
                            cap[t_c][0].append(grid[t_c][row-2][col+2])
                        else:
                            cap[t_c][1].append(grid[t_c][row-2][col+2])
                    
                    grid[t_c][row-2][col+2],grid[t_c][row][col] = grid[t_c][row][col],""
                
                print(tele)

                if "A" in tele:
                    
                    toSend = str(turn[t_c][0])+"-"+str(grid[t_c])+"-"+str(chat[t_c])+"-"+str(moves[t_c])
                else:
                    toSend = str(turn[t_c][1])+"-"+str(grid[t_c])+"-"+str(chat[t_c])+"-"+str(moves[t_c])
                client_socket.send(toSend.encode("utf-8"))

            elif message[0]=="H":
                temp = message.split("-")[1::]
                print(turn[temp[1]][0],turn[temp[1]][1],turn,temp[1])
                if temp[0]=="A":
                    toSend = "9-"+str(turn[temp[1]][0])+"-"+str(grid[temp[1]])+"-"+str(chat[temp[1]])+"-"+str(moves[temp[1]])
                else:
                    toSend = "9-"+str(turn[temp[1]][1])+"-"+str(grid[temp[1]])+"-"+str(chat[temp[1]])+"-"+str(moves[temp[1]])
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

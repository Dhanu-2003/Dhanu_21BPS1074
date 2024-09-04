from flask import Flask, render_template, redirect, url_for
import socket
import threading
import time

app = Flask(__name__)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 1074))

code = ""
player_name = ""
opo = "Waiting"

cap = []

grid = []
chat = []
moves = []
turn = 0

selected_p = ""

pos_mov=[]
    
def send(message):
        client.send(message.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        return response

def listen():
    global turn,grid,chat,moves,selected_p,pos_mov
    selected_p = ""
    mes = client.recv(1024).decode('utf-8')    
    temp = mes.split("-")
    turn = eval(temp[0])
    grid = eval(temp[1])
    chat = eval(temp[2])
    moves = eval(temp[3])
    print(moves)
    selected_p = ""
    pos_mov = []
    return redirect(url_for("begin"))
     
@app.route("/")
def first():
     return render_template("index.html")


@app.route("/start/<name>", methods=["GET"])
def start(name):
     global player_name,code
     code = send("1-"+name)
     player_name = name
     return redirect(url_for("inputs"))
@app.route("/join/<name>/<code1>",methods=["GET"])
def join(name,code1):
     global player_name, code
     temp = send("2-"+code1+"-"+name)
     player_name = name
     print(temp)
     if temp=="1":
          code = code1
          return redirect(url_for("inputs"))
     else:
          return "Invalid"

@app.route("/inputs")
def inputs():
     global player_name,opo,code
     return render_template("start_page.html", data = [player_name,opo,code])
@app.route("/letsplay/<a>/<b>/<c>/<d>/<e>",methods=["GET"])
def letsplay(a,b,c,d,e):
     global player_name,code,opo,grid,chat,moves,turn

    

     check = "0"
     pos = "a-"+a+"-"+b+"-"+c+"-"+d+"-"+e+"-"+player_name+"-"+code
     send(pos)
     while check=="0":
          print("inside")
          check = send("3-"+player_name+"-"+code)
          print(check)
          time.sleep(1)

     temp = check.split("-")
     print(temp)
     opo = temp[1]
     player_name = temp[0]
     code = temp[2]

     temp_d = eval(send("A-"+code+"-"+player_name))
     turn = temp_d[0]
     grid = temp_d[1]
     moves = temp_d[2]
     chat = temp_d[3]
     print(temp_d)
     
     return redirect(url_for("begin"))
@app.route("/begin")
def begin():
     global player_name,code,opo,turn,grid,chat,moves,selected_p,pos_mov
     temp=""
     
     for i in pos_mov:
          if len(i)==1:
               temp+=(i+" ")
          else:
               temp+=i
     t_moves = []
     
     return render_template("game.html",data = [player_name,opo,code,turn,grid,chat,moves,player_name[-2],selected_p,temp,cap])
          
     
@app.route("/select/<num>",methods = ["GET"])
def select(num):
     global selected_p,pos_mov
     selected_p = num
     mes = eval(send("B-"+player_name+"-"+code+"-"+selected_p))
     pos_mov = mes
     print(mes)
     return redirect(url_for("begin"))

@app.route("/mm/<f>/<selec>",methods=["GET"])
def mm(f,selec):
     global turn, grid, chat,moves,selected_p,pos_mov,cap
     data = send("C-"+str(f)+"-"+str(selec)+"-"+code).split("-")
     print(data)
     print("===========")
     turn = eval(data[0])
     grid = eval(data[1])
     chat = eval(data[2])
     moves = eval(data[3])
     cap = eval(data[4])
     print("------------")
     print(moves) 
     print("------------------------")
     selected_p = ""
     pos_mov=""
     if int(data[5])==5:
          return "Win"
     return redirect(url_for("begin"))

@app.route("/oponent")
def oponent():
    global turn,grid,chat,moves,selected_p,pos_mov,cap

    selected_p = ""
    while True:
        mes = send("H-"+str(player_name[-2])+"-"+code)
        print(mes)
        if mes[0]=="9":
            temp = mes.split("-")[1::]
            turn = eval(temp[0])
            grid = eval(temp[1])
            chat = eval(temp[2])
            moves = eval(temp[3])
            cap = eval(temp[4])
            selected_p = ""
            time.sleep(1)
            pos_mov = []
            if int(temp[5])==5:
                 return "Loose"
            break
        time.sleep(5)
    print(moves)

    return redirect(url_for("begin"))

if __name__ == "__main__":

    app.run(host='0.0.0.0',debug=True,port=5100)

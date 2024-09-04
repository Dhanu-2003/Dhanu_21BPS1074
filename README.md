**ADVANCED CHESS Game**

   Rules : 
   
      PAWM - Move 1 step in LEFT, RIGHT, BACKWARD, FORWARD
      Hero1 - MOVE 2 step in LEFT, RIGHT, BACKWARD, FORWARD
      Hero2 - MOVE 2 step in DIAGONAL BACKWARD LEFT, BACKWARD RIGHT, FORWARD LEFT, FORWARD RIGHT
  Power : 
  
    According to the given question,
        Pawn does not have power to cut a coin. Other two have power to eliminate coin in the moving direction

**How to configure**
     make sure you have installed the requirement.txt file.
     You have three files in server.py, client1.py, client2.py

     step 1 - To experience the connected system locally, First connect all your device in same wifi network
     step 2 - run your server in any one system. Let's say system A
     step 3 - run client1.py and client2.py in two different system call it as system B and system C
     step 4 - In system B use challenge your friend option to create a room code
     step 5 -  In system C use the room code in Accept challenge senction and join
     step 6 - Now you both are connected in a single room.
     step 7 - Now you both have to select all 5 component to continue
     step 8 - Once you done the previos task, now you both can enjoy the game.
     step 9 - In right side coner you will see all the history of movements and the coins you captured
              and you are only allowed to select your coin in your turn. Once you select a coin you will 
              be shown the possible moves. Only those moves can be made to avoid errors.
    step 10: Once you captured all coins of oponent you will be informed that you WIN else you will be informed that you LOST.


 **CODE FLOW**
 
     - You have a common server. Each player is considered as a client. Here I used different port.
     - It is advaicable to use same port. The reason I used different port is to show that you can 
       connect with differnt mobile at different time and enjoy the experience. 
     - When ever you interact with the front end a code encrypted data will be sent to backend which 
       will be processed and the result will be shown in frontend

**Future works**

   It was decided to integrate it with AI which recommend the next best move to win the game.
   Further I was thinking to add a dedicated AI chat bot which will help and assist on player quereys.


Other Approach:
   I made the process using if else conditions. You can approach like 
      Creting a dictionary 
            d = {P:[F1,B1,L1,R1],H1:[F2,B2,L2,R2],H2:[FL2,FR2,BL2,BR2]}
      Creating a function validate(move,posx,posy,grid) for validation
            move can be taken from d[coin]. The last element tells the number of moves and first element tell the direction.
                  you can write like
                     tempr = posx
                     tempc = posy
                     m =  int(move[-1])
                     for i in move[0;len(move)-1]:
                        if i=="F":
                           tempr+=m
                        elif i=="B":
                           tempr-=m
                        elif i=="L":
                           tempc-=m
                        elif i=="R":
                           tempc+=m
                     if grid[tempr][tempc] is empty or grid[tempr][tempc] is oponent:
                           return True
                     return False
      Creating a function makemove(move,posx,posy,grid) for movements
                     tempr = posx
                     tempc = posy
                     m =  int(move[-1])
                     for i in move[0;len(move)-1]:
                        if i=="F":
                           tempr+=m
                        elif i=="B":
                           tempr-=m
                        elif i=="L":
                           tempc-=m
                        elif i=="R":
                           tempc+=m
                     grid[posx][posy],grid[tempx][tempy]=grid[posx][posy],grid[tempx][tempy]
               
**Note :  Spectator option is yet to add to front end. I already completed the backend process. It is yet to shown in front end.**

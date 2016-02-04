from random import randint
from time import sleep
import re
import os
def createGrid(size,grid):
    for y in range(0,size):
        grid.append([])
        for x in range(0,size):
            grid[y].append(0)
def cls(title=""):
    if os.name == "nt":
        clearCommand = "cls"
    elif os.name == "posix":
        clearCommand = "clear"
    else:
        return "failed"
    os.system(clearCommand)
    print("Battleship!")
    if(len(title.strip())>0):
        print(title)
def attackCell(attackX,attackY,player):
    if(player==1):
        gridOffense=offenseGrid1
        gridDefense=defenseGrid2
    elif(player==2):
        gridOffense=offenseGrid2
        gridDefense=defenseGrid1
    else:
        return("invalid player")
    if(gridDefense[attackX][attackY]==empty):
        gridDefense[attackX][attackY]=miss
        return("miss")
    elif(gridDefense[attackX][attackY]==ship):
        gridDefense[attackX][attackY]=hit
        return("hit")
    else:
        return("has been attacked")
def gridCount(gridVar,value):
    count=0
    for x in range(0, len(gridVar)):
        for y in range(0, len(gridVar[x])):
            if(gridVar[x][y]==value):
                count+=1
    return count
def printGrid(gridVar):
    for y in range(0, len(gridVar[0])):
        for x in range(0, len(gridVar)):
            print(cell[gridVar[x][y]]," ",end="")
        print()
def addShip(shipX,shipY,direction,length,gridVar,bot=False):
    beforeCount = gridCount(gridVar, ship)
    if(direction=="u"):
        if(shipY-length>=-1):
            for y in range(shipY, shipY-length,-1):
                if(gridVar[shipX][y]==ship):
                    return "ship"
            if(bot):
                shipsGrid2.append([])
            else:
                shipsGrid1.append([])
            for y in range(shipY, shipY-length,-1):
                gridVar[shipX][y]=ship
                if(bot):
                    shipsGrid2[len(shipsGrid2)-1].append(str(shipX)+str(y))
                else:
                    shipsGrid1[len(shipsGrid2)-1].append(str(shipX)+str(y))
        else:
            return "out"
    else:
        uFail=True
    if(direction=="d"):
        if(shipY+length<=len(gridVar)):
            for y in range(shipY, shipY+length):
                if(gridVar[shipX][y]==ship):
                    return "ship"
            if(bot):
                shipsGrid2.append([])
            else:
                shipsGrid1.append([])
            for y in range(shipY, shipY+length):
                gridVar[shipX][y]=ship
                if(bot):
                    shipsGrid2[len(shipsGrid2)-1].append(str(shipX)+str(y))
                else:
                    shipsGrid1[len(shipsGrid2)-1].append(str(shipX)+str(y))
        else:
            return "out"
    else:
        dFail=True
    if(direction=="l"):
        if(shipX-length>=-1):
            for x in range(shipX, shipX-length,-1):
                if(gridVar[x][shipY]==ship):
                    return "ship"
            if(bot):
                shipsGrid2.append([])
            else:
                shipsGrid1.append([])
            for x in range(shipX, shipX-length,-1):
                gridVar[x][shipY]=ship
                if(bot):
                    shipsGrid2[len(shipsGrid2)-1].append(str(x)+str(shipY))
                else:
                    shipsGrid1[len(shipsGrid2)-1].append(str(x)+str(shipY))
        else:
            return "out"
    else:
        lFail=True
    if(direction=="r"):
        if(shipX+length<=len(gridVar)):
            for x in range(shipX, shipX+length):
                if(gridVar[x][shipY]==ship):
                    return "ship"
            if(bot):
                shipsGrid2.append([])
            else:
                shipsGrid1.append([])
            for x in range(shipX, shipX+length):
                gridVar[x][shipY]=ship
                if(bot):
                    shipsGrid2[len(shipsGrid2)-1].append(str(x)+str(shipY))
                else:
                    shipsGrid1[len(shipsGrid2)-1].append(str(x)+str(shipY))
        else:
            return "out"
    else:
        rFail=True
    if(gridCount(gridVar, ship) == beforeCount):
        return "direction"
    return "good"
directionDict = {0:'u',1:'d',2:'l',3:'r'}
cell = {0:'-',1:'O',2:'#',3:'X'}
empty = 0   #Constant
miss = 1    #Constant
ship = 2    #Constant
hit = 3     #Constant
gridSize = 10
activeTitle = "Starting..."
queueGrid1 = []
offenseGrid1 = []
offenseGrid2 = []
defenseGrid1 = []
defenseGrid2 = []
shipsGrid1 = []
shipsGrid2 = []
createGrid(gridSize,offenseGrid1)
createGrid(gridSize,offenseGrid2)
createGrid(gridSize,defenseGrid1)
createGrid(gridSize,defenseGrid2)
createGrid(gridSize,queueGrid1)
#0=Empty 1=Miss 2=Ship 3=Hit
cls("Placing ships... ")
while(gridCount(defenseGrid1, ship)<17):
    if(gridCount(defenseGrid1, ship)==0):
        print("Place your Patrol Boat (2 Squares Long)")
        shipLength=2;
    if(gridCount(defenseGrid1, ship)==2):
        print("Place your Cruiser (3 Squares Long)")
        shipLength=3;
    if(gridCount(defenseGrid1, ship)==5):
        print("Place your Submarine (3 Squares Long)")
        shipLength=3
    if(gridCount(defenseGrid1, ship)==8):
        print("Place your Battleship (4 Squares Long)")
        shipLength=4
    if(gridCount(defenseGrid1, ship)==12):
        print("Place your Aircraft Carrier (5 Squares Long")
        shipLength=5
    inputX = input("X coordinate from 1-"+str(gridSize)+"\n")
    inputY = input("Y coordinate from 1-"+str(gridSize)+"\n")
    shipX = re.sub(r"\D","",inputX)
    shipY = re.sub(r"\D","",inputY)
    print(shipX)
    print(shipY)
    shipDirection = input("Is it facing up, down, left, or right?\n").lower()[0:1]
    errormessage = addShip(int(shipX)-1, int(shipY)-1, shipDirection, shipLength, defenseGrid1)
    cls("Placing ships... ")
    if(errormessage=="good"):
        print("Ship placed. ")
    else:
        if(errormessage=="ship"):
            print("There is already a ship in that Square. ")
        if(errormessage=="out"):
            print("That's out of bounds. ")
        if(errormessage=="direction"):
            print("Invalid direction. ")
        print("Failed to place ship. ")
    printGrid(defenseGrid1)
cls("Your ships:")
printGrid(defenseGrid1)
sleep(3)
print("The bot is chosing ship locations. ")
while(gridCount(defenseGrid2, ship)<17):
    if(gridCount(defenseGrid2, ship)==0):
        shipLength=2;
    if(gridCount(defenseGrid2, ship)==2):
        shipLength=3;
    if(gridCount(defenseGrid2, ship)==5):
        shipLength=3
    if(gridCount(defenseGrid2, ship)==8):
        shipLength=4
    if(gridCount(defenseGrid2, ship)==12):
        shipLength=5
    shipX=randint(0,9)
    shipY=randint(0,9)
    direction=directionDict[randint(0,3)]
    addShip(shipX, shipY, direction, shipLength, defenseGrid2, bot)
print("The bot has placed it's ships. ")
sleep(2)
game=True
turnCount=1
while(game):
    if(turnCount%2>0):
        if(gridCount(offenseGrid1, empty)<gridSize^2):
            print("Your hits and misses: ")
        printGrid(offenseGrid1)
        print("It is your turn! Choose the cell to attack! ")
        attackX=eval(input("X coordinate from 1-",str(gridSize),"\n"))-1
        attackY=eval(input("Y coordinate from 1-",str(gridSize),"\n"))-1
        errormessage=attackCell(attackX, attackY)
        if(errormessage=="miss"):
            print("You didn't hit a ship! ")
            turnCount+=1
        if(errormessage=="hit"):
            print("You hit a ship! ")
            XY=str(attackX)+str(attackY)
            if(gridCount(shipsGrid2, XY)>0):
                queueBreak=False
                for X in range(0,len(shipsGrid2)):
                    if(queueBreak):
                        break
                    for Y in range(0,len(shipsGrid2[X])):
                        if(shipsGrid2[X][Y]==XY):
                            shipsGrid2[X].pop(Y)
                            if(len(shipsGrid2[X])==0):
                                if(X==0):
                                    print("You sunk a patrol boat!")
                                if(X==1):
                                    print("You sunk a cruiser!")
                                if(X==2):
                                    print("You sunk a submarine!")
                                if(X==3):
                                    print("Bot: You sunk my battleship!")
                                if(X==4):
                                    print("You sunk an aircraft carrier!")
                                sleep(2)
                            queueBreak=True
                            break
            if(gridCount(defenseGrid2, ship)==gridCount(offenseGrid1, hit)):
                print("You won congratulations! ")
                game=False
            turnCount+=1
        if(errormessage=="retry"):
            print("You have already attacked that spot. Chooose a different cell. ")
        if(errormessage=="out"):
            print("Out of bounds. Choose a different cell. ")
    else:
        attackX=randint(0,gridSize-1)
        attackY=randint(0,gridSize-1)
        queueBreak=False
        for x in range(0,gridSize):
            if(queueBreak):
                break
            for y in range(0,gridSize):
                if(queueGrid1[x][y]==1):
                    attackX=x
                    attackY=y
                    queueBreak=True
                    break
        errormessage=attackCell(attackX, attackY, bot)
        attackX+=1
        attackY+=1
        if(errormessage != "retry"):
            print("Your ships and shots the bot has fired: ")
            printGrid(defenseGrid1)
            print("Bot:",attackX,attackY)
            attackX-=1
            attackY-=1
            queueGrid1[attackX][attackY]=0
        if(errormessage=="hit"):
            print("The bot hit you! ")
            XY=str(attackX)+str(attackY)
            if(gridCount(shipsGrid1, XY)>0):
                queueBreak=False
                for X in range(0,len(shipsGrid1)):
                    if(queueBreak):
                        break
                    for Y in range(0,len(shipsGrid1[X])):
                        if(shipsGrid1[X][Y]==XY):
                            shipsGrid1[X].pop(Y)
                            if(len(shipsGrid1[X])==0):
                                if(X==0):
                                    print("Your patrol boat has sunk!")
                                if(X==1):
                                    print("Your cruiser has sunk!")
                                if(X==2):
                                    print("Your submarine has sunk!")
                                if(X==3):
                                    print("Player: You sunk my battleship!")
                                if(X==4):
                                    print("Your aircraft carrier has sunk!")
                            queueBreak=True
                            break
            if(gridCount(defenseGrid1, ship)==0):
                print("The bot won. Better luck next time!")
                game=False
            turnCount+=1
            if(attackX-1>=0 and defenseGrid1[attackX-1][attackY] != 2 and defenseGrid1[attackX-1][attackY] != 3):
                queueGrid1[attackX-1][attackY]=1
            if(attackY-1>=0 and defenseGrid1[attackX][attackY-1] != 2 and defenseGrid1[attackX][attackY-1] != 3):
                queueGrid1[attackX][attackY-1]=1
            if(attackX+1<10 and defenseGrid1[attackX+1][attackY] != 2 and defenseGrid1[attackX+1][attackY] != 3):
                queueGrid1[attackX+1][attackY]=1
            if(attackY+1<10 and defenseGrid1[attackX][attackY+1] != 2 and defenseGrid1[attackX][attackY+1] != 3):
                queueGrid1[attackX][attackY+1]=1
        if(errormessage=="miss"):
            print("The bot missed! ")
            turnCount+=1

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
        gridOffense = offenseGrid2
        gridDefense = defenseGrid1
    if(gridOffense[attackX][attackY]%2==0 and gridDefense[attackX][attackY]%2==0):
        gridOffense[attackX][attackY]+=1
        gridDefense[attackX][attackY]+=1
    else:
        return("retry")
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
def addShip(shipX,shipY,direction,length,player):
    if(player==1):
        defenseGrid=defenseGrid1
        shipsGrid=shipsGrid1
    elif(player==2):
        defenseGrid=defenseGrid2
        shipsGrid=shipsGrid2
    bot = hotfixDict[player]
    beforeCount = gridCount(defenseGrid, ship)
    if(direction=="u"):
        if(shipY-length>=-1):
            for y in range(shipY, shipY-length,-1):
                if(defenseGrid[shipX][y]==ship):
                    return "ship"
            shipsGrid.append([])
            for y in range(shipY, shipY-length,-1):
                defenseGrid[shipX][y]=ship
                shipsGrid[len(shipsGrid)-1].append(str(shipX)+str(y))
        else:
            return "out"
    elif(direction=="d"):
        if(shipY+length<=len(defenseGrid)):
            for y in range(shipY, shipY+length):
                if(defenseGrid[shipX][y]==ship):
                    return "ship"
            shipsGrid.append([])
            for y in range(shipY, shipY+length):
                defenseGrid[shipX][y]=ship
                shipsGrid[len(shipsGrid)-1].append(str(shipX)+str(y))
        else:
            return "out"
    elif(direction=="l"):
        if(shipX-length>=-1):
            for x in range(shipX, shipX-length,-1):
                if(defenseGrid[x][shipY]==ship):
                    return "ship"
            shipsGrid.append([])
            for x in range(shipX, shipX-length,-1):
                defenseGrid[x][shipY]=ship
                shipsGrid[len(shipsGrid)-1].append(str(x)+str(shipY))
        else:
            return "out"
    elif(direction=="r"):
        if(shipX+length<=len(defenseGrid)):
            for x in range(shipX, shipX+length):
                if(defenseGrid[x][shipY]==ship):
                    return "ship"
            shipsGrid.append([])
            for x in range(shipX, shipX+length):
                defenseGrid[x][shipY]=ship
                shipsGrid[len(shipsGrid)-1].append(str(x)+str(shipY))
        else:
            return "out"
    else:
        return "direction"
    if(gridCount(defenseGrid, ship) < beforeCount + length):
        raise CustomError("Not enough ship tiles placed.")
    return "good"
class CustomError(Exception):
    def __init__(self, errorName):
        self.errorName = errorName
    def __str__(self):
        return repr(self.errorName)
directionDict = {0:'u',1:'d',2:'l',3:'r'}
cell = {0:'-',1:'O',2:'#',3:'X'}
shipDict = {0:"patrol boat",1:"cruiser",2:"submarine",3:"battleship",4:"aircraft carrier"}
hotfixDict = {1:False,2:True}
empty = 0       #Constant
miss = 1        #Constant
ship = 2        #Constant
hit = 3         #Constant
gridSize = 10   #Configuarable constant
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
    shipCount=gridCount(defenseGrid1, ship)
    if(shipCount==0):
        shipLength=2;
        print("Place your Patrol Boat (2 Squares Long)")
    elif(shipCount==2):
        shipLength=3;
        print("Place your Cruiser (3 Squares Long)")
    elif(shipCount==5):
        shipLength=3
        print("Place your Submarine (3 Squares Long)")
    elif(shipCount==8):
        shipLength=4
        print("Place your Battleship (4 Squares Long)")
    elif(shipCount==12):
        shipLength=5
        print("Place your Aircraft Carrier (5 Squares Long")
    else:
        raise customError("ShipError")
    inputX = input("X coordinate from 1-"+repr(gridSize)+"\n")
    inputY = input("Y coordinate from 1-"+repr(gridSize)+"\n")
    shipX = re.sub(r"\D","",inputX)
    shipY = re.sub(r"\D","",inputY)
    print(shipX)
    print(shipY)
    shipDirection = input("Is it facing up, down, left, or right?\n").lower()[0:1]
    errormessage = addShip(int(shipX)-1, int(shipY)-1, shipDirection, shipLength, 1)
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
    addShip(shipX, shipY, direction, shipLength, 2)
print("The bot has placed it's ships. ")
sleep(2)
game=True
turnCount=0
while(game):
    if(turnCount%2==0):
        if(gridCount(offenseGrid1, empty)<gridSize^2):
            print("Your hits and misses: ")
            printGrid(offenseGrid1)
        print("It is your turn! Choose the cell to attack! ")
        attackX=eval(input("X coordinate from 1-"+repr(gridSize)+"\n"))-1
        attackY=eval(input("Y coordinate from 1-"+repr(gridSize)+"\n"))-1
        errormessage=attackCell(attackX, attackY, 1)
        if(errormessage!="retry"):
            if(offenseGrid1[attackX][attackY]%2==1 and defenseGrid2[attackX][attackY]%2==1):
                print("You didn't hit a ship. ")
            elif(offenseGrid1[attackX][attackY]%2==3 and defenseGrid2[attackX][attackY]%2==3):
                print("You hit a ship! ")
                XY=str(attackX)+str(attackY)
                if(gridCount(shipsGrid2, XY)>0):
                    breakNext=False
                    for X in range(0,len(shipsGrid2)):
                        if(breakNext):
                            break
                        for Y in range(0,len(shipsGrid2[X])):
                            if(shipsGrid2[X][Y]==XY):
                                shipsGrid2[X].pop(Y)
                                if(len(shipsGrid2[X])==0):
                                    if(X==3):
                                        print("Enemy: You sank my "+repr(shipDict[X])+"!")
                                    else:
                                        print("You sunk the enemy's "+repr(shipDict[X])+", nice shot!")
                                    sleep(2)
                                breakNext=True
                                break
                else:
                    raise CustomError("Ship not found")
                if(gridCount(defenseGrid2, ship)==gridCount(offenseGrid1, hit)):
                    print("Congratulations, you won!! ")
                    game=False
            turnCount+=1
        else:
            print("You have already attacked that spot. Chooose a different cell. ")
    else:
        attackX=randint(0,gridSize-1)
        attackY=randint(0,gridSize-1)
        breakNext=False
        for x in range(0,gridSize):
            if(breakNext):
                break
            for y in range(0,gridSize):
                if(queueGrid1[x][y]==1):
                    attackX=x
                    attackY=y
                    breakNext=True
                    break
        errormessage=attackCell(attackX, attackY, 2)
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
                breakNext=False
                for X in range(0,len(shipsGrid1)):
                    if(breakNext):
                        break
                    for Y in range(0,len(shipsGrid1[X])):
                        if(shipsGrid1[X][Y]==XY):
                            shipsGrid1[X].pop(Y)
                            if(len(shipsGrid1[X])==0):
                                if(X==3):
                                    print("Player: You sank my "+repr(shipDict[X])+"!")
                                else:
                                    print("Your "+repr(shipDict[X])+", has sunk.")
                            breakNext=True
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

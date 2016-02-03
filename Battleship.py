from random import randint
from time import sleep
import re
import os
botGrid = []
botGridQueue = []
playerGridOffence = []
playerGridDefence = []
playerShips = []
botShips = []
directionDict={0:'u',1:'d',2:'l',3:'r'}
bot = True #Used to make code easier to read. Do not edit
def cls(title=""):
    os.system('cls')
    print("Battleship!")
    if(len(title.strip())>0):
        print(title)
def attackCell(attackX,attackY,bot=False):
    if(attackX in range(0,10) and attackY in range(0,10)):
        if(bot):
            if(playerGridDefence[attackX][attackY]=='X'):
                return("retry")
            if(playerGridDefence[attackX][attackY]=='#'):
                playerGridDefence[attackX][attackY]='X'
                return("hit")
            if(playerGridDefence[attackX][attackY]=='-'):
                playerGridDefence[attackX][attackY]='O'
                return("miss")
            if(playerGridDefence[attackX][attackY]=='O'):
                return("retry")
        else:
            if(playerGridOffence[attackX][attackY]=='X'):
                return("retry")
            if(botGrid[attackX][attackY]==1):
                playerGridOffence[attackX][attackY]='X'
                return("hit")
            if(playerGridOffence[attackX][attackY] == '-'):
                playerGridOffence[attackX][attackY]='O'
                return("miss")
            if(playerGridOffence[attackX][attackY]=='O'):
                return("retry")
    else:
        return("out")
def searchGrid(gridVar,value):
    count=0
    for x in range(0, len(gridVar)):
        for y in range(0, len(gridVar[x])):
            if(gridVar[x][y]==value):
                count+=1
    return count
def printGrid(gridVar):
    for y in range(0, len(gridVar[0])):
        for x in range(0, len(gridVar)):
            print(gridVar[x][y]," ", end="")
        print()
def addShip(shipX,shipY,direction,length,gridVar,bot=False):
    if(bot):
        filler=1
    else:
        filler='#'
    beforeCount = searchGrid(gridVar, filler)
    if(direction=="u"):
        if(shipY-length>=-1):
            for y in range(shipY, shipY-length,-1):
                if(gridVar[shipX][y]==filler):
                    return "ship"
            if(bot):
                botShips.append([])
            else:
                playerShips.append([])
            for y in range(shipY, shipY-length,-1):
                gridVar[shipX][y]=filler
                if(bot):
                    botShips[len(botShips)-1].append(str(shipX)+str(y))
                else:
                    playerShips[len(botShips)-1].append(str(shipX)+str(y))
        else:
            return "out"
    else:
        uFail=True
    if(direction=="d"):
        if(shipY+length<=len(gridVar)):
            for y in range(shipY, shipY+length):
                if(gridVar[shipX][y]==filler):
                    return "ship"
            if(bot):
                botShips.append([])
            else:
                playerShips.append([])
            for y in range(shipY, shipY+length):
                gridVar[shipX][y]=filler
                if(bot):
                    botShips[len(botShips)-1].append(str(shipX)+str(y))
                else:
                    playerShips[len(botShips)-1].append(str(shipX)+str(y))
        else:
            return "out"
    else:
        dFail=True
    if(direction=="l"):
        if(shipX-length>=-1):
            for x in range(shipX, shipX-length,-1):
                if(gridVar[x][shipY]==filler):
                    return "ship"
            if(bot):
                botShips.append([])
            else:
                playerShips.append([])
            for x in range(shipX, shipX-length,-1):
                gridVar[x][shipY]=filler
                if(bot):
                    botShips[len(botShips)-1].append(str(x)+str(shipY))
                else:
                    playerShips[len(botShips)-1].append(str(x)+str(shipY))
        else:
            return "out"
    else:
        lFail=True
    if(direction=="r"):
        if(shipX+length<=len(gridVar)):
            for x in range(shipX, shipX+length):
                if(gridVar[x][shipY]==filler):
                    return "ship"
            if(bot):
                botShips.append([])
            else:
                playerShips.append([])
            for x in range(shipX, shipX+length):
                gridVar[x][shipY]=filler
                if(bot):
                    botShips[len(botShips)-1].append(str(x)+str(shipY))
                else:
                    playerShips[len(botShips)-1].append(str(x)+str(shipY))
        else:
            return "out"
    else:
        rFail=True
    if(searchGrid(gridVar, filler) == beforeCount):
        return "direction"
    return "good"
#'-'=Empty '#'=Ship 'X'=Hit 'O'=Miss
cls("Starting... ")
for i in range(0,10):
    playerGridOffence.append(['-','-','-','-','-','-','-','-','-','-'])
    playerGridDefence.append(['-','-','-','-','-','-','-','-','-','-'])
    botGrid.append([0,0,0,0,0,0,0,0,0,0])
    botGridQueue.append([0,0,0,0,0,0,0,0,0,0])
cls("Placing ships... ")
while(searchGrid(playerGridDefence, '#')<17):
    if(searchGrid(playerGridDefence, '#')==0):
        print("Place your Patrol Boat (2 Squares Long)")
        shipLength=2;
    if(searchGrid(playerGridDefence, '#')==2):
        print("Place your Cruiser (3 Squares Long)")
        shipLength=3;
    if(searchGrid(playerGridDefence, '#')==5):
        print("Place your Submarine (3 Squares Long)")
        shipLength=3
    if(searchGrid(playerGridDefence, '#')==8):
        print("Place your Battleship (4 Squares Long)")
        shipLength=4
    if(searchGrid(playerGridDefence, '#')==12):
        print("Place your Aircraft Carrier (5 Squares Long")
        shipLength=5
    inputX = input("X coordinate from 1-10\n")
    inputY = input("Y coordinate from 1-10\n")
    shipX = re.sub(r"\D","",inputX)
    shipY = re.sub(r"\D","",inputY)
    print(shipX)
    print(shipY)
    shipDirection = input("Is it facing up, down, left, or right?\n").lower()[0:1]
    errormessage = addShip(int(shipX)-1, int(shipY)-1, shipDirection, shipLength, playerGridDefence)
    cls("Placeing ships... ")
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
    printGrid(playerGridDefence)
cls("Your ships:")
printGrid(playerGridDefence)
sleep(3)
print("The bot is chosing ship locations. ")
while(searchGrid(botGrid, 1)<17):
    if(searchGrid(botGrid, 1)==0):
        shipLength=2;
    if(searchGrid(botGrid, 1)==2):
        shipLength=3;
    if(searchGrid(botGrid, 1)==5):
        shipLength=3
    if(searchGrid(botGrid, 1)==8):
        shipLength=4
    if(searchGrid(botGrid, 1)==12):
        shipLength=5
    shipX=randint(0,9)
    shipY=randint(0,9)
    direction=directionDict[randint(0,3)]
    addShip(shipX, shipY, direction, shipLength, botGrid, bot)
print("The bot has placed it's ships. ")
sleep(2)
game=True
turnCount=1
while(game):
    if(turnCount%2>0):
        if(searchGrid(playerGridOffence, '-')<100):
            print("Your hits and misses: ")
        printGrid(playerGridOffence)
        print("It is your turn! Choose the cell to attack! ")
        attackX=eval(input("X coordinate from 1-10\n"))-1
        attackY=eval(input("Y coordinate from 1-10\n"))-1
        errormessage=attackCell(attackX, attackY)
        if(errormessage=="miss"):
            print("You didn't hit a ship! ")
            turnCount+=1
        if(errormessage=="hit"):
            print("You hit a ship! ")
            XY=str(attackX)+str(attackY)
            if(searchGrid(botShips, XY)>0):
                queueBreak=False
                for X in range(0,len(botShips)):
                    if(queueBreak):
                        break
                    for Y in range(0,len(botShips[X])):
                        if(botShips[X][Y]==XY):
                            botShips[X].pop(Y)
                            if(len(botShips[X])==0):
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
            if(searchGrid(botGrid, 1)==searchGrid(playerGridOffence, 'X')):
                print("You won congratulations! ")
                game=False
            turnCount+=1
        if(errormessage=="retry"):
            print("You have already attacked that spot. Chooose a different cell. ")
        if(errormessage=="out"):
            print("Out of bounds. Choose a different cell. ")
    else:
        attackX=randint(0,9)
        attackY=randint(0,9)
        queueBreak=False
        for x in range(0,10):
            if(queueBreak):
                break
            for y in range(0,10):
                if(botGridQueue[x][y]==1):
                    attackX=x
                    attackY=y
                    queueBreak=True
                    break
        errormessage=attackCell(attackX, attackY, bot)
        attackX+=1
        attackY+=1
        if(errormessage!="retry"):
            print("Your ships and shots the bot has fired: ")
            printGrid(playerGridDefence)
            print("Bot:",attackX,attackY)
            attackX-=1
            attackY-=1
            botGridQueue[attackX][attackY]=0
        if(errormessage=="hit"):
            print("The bot hit you! ")
            XY=str(attackX)+str(attackY)
            if(searchGrid(playerShips, XY)>0):
                queueBreak=False
                for X in range(0,len(playerShips)):
                    if(queueBreak):
                        break
                    for Y in range(0,len(playerShips[X])):
                        if(playerShips[X][Y]==XY):
                            playerShips[X].pop(Y)
                            if(len(playerShips[X])==0):
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
            if(searchGrid(playerGridDefence, '#')==0):
                print("The bot won. Better luck next time!")
                game=False
            turnCount+=1
            if(attackX-1>=0 and playerGridDefence[attackX-1][attackY] != 'X' and playerGridDefence[attackX-1][attackY] != 'O'):
                botGridQueue[attackX-1][attackY]=1
            if(attackY-1>=0 and playerGridDefence[attackX][attackY-1] != 'X' and playerGridDefence[attackX][attackY-1] != 'O'):
                botGridQueue[attackX][attackY-1]=1
            if(attackX+1<10 and playerGridDefence[attackX+1][attackY] != 'X' and playerGridDefence[attackX+1][attackY] != 'O'):
                botGridQueue[attackX+1][attackY]=1
            if(attackY+1<10 and playerGridDefence[attackX][attackY+1] != 'X' and playerGridDefence[attackX][attackY+1] != 'O'):
                botGridQueue[attackX][attackY+1]=1
        if(errormessage=="miss"):
            print("The bot missed! ")
            turnCount+=1
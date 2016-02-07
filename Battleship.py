from random import randint
from time import sleep
from itertools import accumulate
import os, re
def createGrid(size,grid):
	for y in range(0,size):
		grid.append([])
		for x in range(0,size):
			grid[y].append(0)
def cls(title=""):
	if(os.name == "nt"):
		clearCommand = "cls"
	elif(os.name == "posix"):
		clearCommand = "clear"
	else:
		return("failed")
	os.system(clearCommand)
	print("Battleship!")
	if(len(title.strip())>0):
		print(title)
def attackCell(attackX,attackY,player):
	if(player==0):
		gridDefense = defenseGrid2
	elif(player==1):
		gridDefense = defenseGrid1
	try:
		if(gridDefense[attackX][attackY]%2>0):
			return("retry")
	except IndexError:
		return("out")
	else:
		gridDefense[attackX][attackY]+=1
def listCount(array,value,func=lambda a, b: a.count(b),maximum=0):
	num=func(array,value)
	for i in array:
		if(num<maximum or not maximum):
			if(str(type(i))[-6:-2]=='list'):
				num+=listCount(i,value,func)
		else:
			return maximum
	return num
def printGrid(grid,team="defense"):
	for y in range(0, len(grid[0])):
		for x in range(0, len(grid)):
			if(grid[x][y]==ship and team=="offense"):
				print(cell[empty]," ",end="")
			else:
				print(cell[grid[x][y]]," ",end="")
		print()
def addShip(shipX,shipY,direction,length,player):
	if(player==0):
		defenseGrid=defenseGrid1
		shipsGrid=shipsGrid1
	elif(player==1):
		defenseGrid=defenseGrid2
		shipsGrid=shipsGrid2
	beforeCount=listCount(defenseGrid, ship)
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
	if(listCount(defenseGrid, ship) < beforeCount + length):
		raise GameError("Not enough ship tiles placed.")
	return "good"
class GameError(Exception):
	def __init__(self, errorName="Unknown"):
		self.errorName = errorName
	def __str__(self):
		return repr(self.errorName)
inGrid = lambda ig1, ig2: listCount(ig1,ig2,lambda ig3, ig4: ig4 in ig3,1)==1#Returns boolean
printLoc = lambda text, x, y:print('\033['+str(y)+';'+str(x)+'H'+text)
global directionDict,cell,ships,shipLength,empty,miss,ship,hit,player1,player2,queueGrid1,queueGrid2,shipsGrid1,shipsGrid2,defenseGrid1,defenseGrid2,cyan,whiteBright,white,whiteDim,red,reset,green
cyan = '\033[36m'    #cyan for grid letters and numbers
whiteBright  = '\033[1;37m'  #bold white for misses and maybe titles
white = '\033[37m' #Normal white
whiteDim  = '\033[2;37m'  #dim white for grid cells
red  = '\033[1;31m'  #bold red for hits
reset = '\033[0m'     #end color formatting and return to normal
green = '\033[32m'    #green for user prompts
empty,miss,ship,hit = 0,1,2,3#Constants
directionDict = {0:'u',1:'d',2:'l',3:'r'}
cell = {empty:cyan+'~'+reset,miss:whiteBright+'O'+reset,ship:white+'#'+reset,hit:red+'X'+reset}
ships = ("patrol boat","cruiser","submarine","battleship","aircraft carrier")
shipLength = [2,3,3,4,5]#Constant
player1,player2 = 0,1#Constants
gridSize = 10#Constant
attackCellAlreadyAttacked = False#Constant
queueGrid1,queueGrid2,defenseGrid1,defenseGrid2,shipsGrid1,shipsGrid2 = [],[],[],[],[],[]
createGrid(gridSize,defenseGrid1)
createGrid(gridSize,defenseGrid2)
createGrid(gridSize,queueGrid2)
cls("Place your ships")
while(listCount(defenseGrid1, ship)<sum(shipLength)):
	shipID=len(shipLength)
	for shipCount in reversed(list(accumulate(shipLength))):
		if(shipCount==listCount(defenseGrid1, ship)):
			break
		shipID-=1
	print("Place your "+ str(ships[shipID]) + " (" + repr(shipLength[shipID]) + " cells long)")
	inputX = input("X coordinate from 1-"+repr(gridSize)+"\n")
	inputY = input("Y coordinate from 1-"+repr(gridSize)+"\n")
	shipX = re.sub(r"\D","",inputX).strip()
	shipY = re.sub(r"\D","",inputY).strip()
	shipDirection = input("Is it facing up, down, left, or right?\n").lower()[0:1]
	shipMessage = addShip(int(shipX)-1, int(shipY)-1, shipDirection, shipLength[shipID], player1)
	cls("Place your ships")
	if(shipMessage=="good"):
		print("Ship placed.")
	else:
		if(shipMessage=="ship"):
			print("There is already a ship in that Square.")
		if(shipMessage=="out"):
			print("That's out of bounds.")
		if(shipMessage=="direction"):
			print("Invalid direction.")
		print("Failed to place ship.")
	printGrid(defenseGrid1)
cls("Your ships:")
printGrid(defenseGrid1)
sleep(2)
cls("Your enemy is placing ships.")
while(listCount(defenseGrid2, ship)<sum(shipLength)):
	shipID=len(shipLength)
	for shipCount in reversed(list(accumulate(shipLength))):
		if(shipCount==listCount(defenseGrid2, ship)):
			break
		shipID-=1
	shipX=randint(0,gridSize-1)
	shipY=randint(0,gridSize-1)
	direction=directionDict[randint(0,3)]
	addShip(shipX, shipY, direction, shipLength[shipID], player2)
game=True
turnCount=0
while(game):
	if(turnCount%2==0):
		if(turnCount>0):
			cls("Your attacks:")
		else:
			cls("Attack a cell:")
		printGrid(defenseGrid2,"offense")
		print("It is your turn! Choose the cell to attack!")
		attackX=int(input("X coordinate from 1-"+repr(gridSize)+"\n"))-1
		attackY=int(input("Y coordinate from 1-"+repr(gridSize)+"\n"))-1
		attackMessage=attackCell(attackX, attackY, player1)
		if(attackMessage=="retry" and attackCellAlreadyAttacked==False):
			print("You have already attacked that spot. Choose a different cell.")
			sleep(1)
		else:
			cls("Your attacks:")
			printGrid(defenseGrid2,"offense")
			if(defenseGrid2[attackX][attackY]==miss):
				print("You didn't hit a ship.")
			elif(defenseGrid2[attackX][attackY]==hit):
				print("You hit a ship!")
				XY=str(attackX)+str(attackY)
				if(inGrid(shipsGrid2,XY)):
					breakNext=False
					for X in range(0,len(shipsGrid2)):
						if(breakNext):
							break
						for Y in range(0,len(shipsGrid2[X])):
							if(shipsGrid2[X][Y]==XY):
								shipsGrid2[X].pop(Y)
								if(len(shipsGrid2[X])==0):
									print("You sunk the enemy's "+str(ships[X])+", nice shot!")
								breakNext=True
								break
				elif(attackCellAlreadyAttacked):
					print("You have already attacked that spot, you lose your turn.")
				else:
					raise GameError("Hit location not found in shipsGrid2")
				if(not(inGrid(defenseGrid1,ship))):
					print("Congratulations, you won in "+str(turnCount+1)+" turns!")
					game=False
			sleep(1)
			turnCount+=1
	else:
		attackX=randint(0,gridSize-1)
		attackY=randint(0,gridSize-1)
		breakNext=False
		for y in range(0,gridSize):
			if(breakNext):
				break
			for x in range(0,gridSize):
				if(queueGrid2[x][y]==1):
					attackX=x
					attackY=y
					breakNext=True
					break
		atackMessage=attackCell(attackX, attackY, player2)
		if(attackMessage!="retry"):
			cls("Your fleet:")
			printGrid(defenseGrid1)
			print("Enemy:",repr(attackX+1),repr(attackY+1))
			queueGrid2[attackX][attackY]=0
			if(defenseGrid1[attackX][attackY]==miss):
				print("You weren't hit.")
			elif(defenseGrid1[attackX][attackY]==hit):
				print("Your enemy hit you! ")
				XY=str(attackX)+str(attackY)
				if(inGrid(shipsGrid1,XY)):
					breakNext=False
					for X in range(0,len(shipsGrid1)):
						if(breakNext):
							break
						for Y in range(0,len(shipsGrid1[X])):
							if(shipsGrid1[X][Y]==XY):
								shipsGrid1[X].pop(Y)
								if(len(shipsGrid1[X])==0):
									print("Your "+repr(ships[X])+", has sunk.")
								breakNext=True
								break
				else:
					raise GameError("Hit location not found in shipsGrid1")
				if(not(inGrid(defenseGrid1,ship))):
					print("Your enemy won in "+str(turnCount+1)+" turns. Better luck next time!")
					game=False
				if(attackX>0 and defenseGrid1[attackX-1][attackY]%2==0):
					queueGrid2[attackX-1][attackY] = 1
				if(attackY>0 and defenseGrid1[attackX][attackY-1]%2==0):
					queueGrid2[attackX][attackY-1]=1
				if(attackX+1<gridSize and defenseGrid1[attackX+1][attackY]%2==0):
					queueGrid2[attackX+1][attackY]=1
				if(attackY+1<gridSize and defenseGrid1[attackX][attackY+1]%2==0):
					queueGrid2[attackX][attackY+1]=1
			sleep(3)
			turnCount+=1

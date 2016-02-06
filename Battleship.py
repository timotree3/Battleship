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
def gridCount(grid,value):
	count=0
	for x in range(0, len(grid)):
		for y in range(0, len(grid[x])):
			if(grid[x][y]==value):
				count+=1
	return count
def printGrid(grid,team="defense"):
	for y in range(0, len(grid[0])):
		for x in range(0, len(grid)):
			if(team=="defense"):
				print(cellDefense[grid[x][y]]," ",end="")
			elif(team=="offense"):
				print(cellOffense[grid[x][y]]," ",end="")
		print()
def addShip(shipX,shipY,direction,length,player):
	if(player==0):
		defenseGrid=defenseGrid1
		shipsGrid=shipsGrid1
	elif(player==1):
		defenseGrid=defenseGrid2
		shipsGrid=shipsGrid2
	beforeCount=gridCount(defenseGrid, ship)
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
		raise GameError("Not enough ship tiles placed.")
	return "good"
class GameError(Exception):
	def __init__(self, errorName="Unknown"):
		self.errorName = errorName
	def __str__(self):
		return repr(self.errorName)
global directionDict,cell,ships,shipLength,empty,miss,ship,hit,player1,player2,queueGrid1,queueGrid2,shipsGrid1,shipsGrid2
directionDict = {0:'u',1:'d',2:'l',3:'r'}
cellDefense = {0:'-',1:'O',2:'#',3:'X'}
cellOffense = {0:'-',1:'O',2:'-',3:'X'}
ships = ["patrol boat","cruiser","submarine","battleship","aircraft carrier"]
shipLength = [2,3,3,4,5]#Constant
empty = 0#Constant
miss = 1#Constant
ship = 2#Constant
hit = 3#Constant
player1 = 0#Constant
player2 = 1#Constant
gridSize = 10#Constant
attackCellAlreadyAttacked = False#Constant
queueGrid2 = []
defenseGrid1 = []
defenseGrid2 = []
shipsGrid1 = []
shipsGrid2 = []
createGrid(gridSize,defenseGrid1)
createGrid(gridSize,defenseGrid2)
createGrid(gridSize,queueGrid2)
#0=Empty 1=Miss 2=Ship 3=Hit
cls("Place your ships")
while(gridCount(defenseGrid1, ship)<sum(shipLength)):
	shipID=len(shipLength)
	for shipCount in reversed(list(accumulate(shipLength))):
		if(shipCount==gridCount(defenseGrid1, ship)):
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
while(gridCount(defenseGrid2, ship)<sum(shipLength)):
	shipID=len(shipLength)
	for shipCount in reversed(list(accumulate(shipLength))):
		if(shipCount==gridCount(defenseGrid2, ship)):
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
		attackX=eval(input("X coordinate from 1-"+repr(gridSize)+"\n"))-1
		attackY=eval(input("Y coordinate from 1-"+repr(gridSize)+"\n"))-1
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
										print("Enemy: You sank my "+repr(ships[X])+"!")
									else:
										print("You sunk the enemy's "+repr(ships[X])+", nice shot!")
								breakNext=True
								break
				elif(attackCellAlreadyAttacked):
					print("You have already attacked that spot, you lose your turn.")
				else:
					raise GameError("Hit location not found in shipsGrid2")
				if(gridCount(defenseGrid2, ship)==0):
					print("Congratulations, you won!")
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
										print("Player: You sank my "+repr(ships[X])+"!")
									else:
										print("Your "+repr(ships[X])+", has sunk.")
								breakNext=True
								break
				else:
					raise GameError("Hit location not found in shipsGrid1")
				if(gridCount(defenseGrid1, ship)==0):
					print("Your enemy won. Better luck next time!")
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

from random import randint
from time import sleep
from itertools import accumulate
import os, re
def parseInput(text,findDir):
	parsed1 = seperator.split(text)
	x=None
	y=None
	direction=None
	for element in parsed1:
		if(regexDir.fullmatch(element) and direction==-1 and findDir):
			direction=element[0:1].lower()
		elif(regexX.fullmatch(element[0:1]) and x==-1):
			x=element[0:1]
		elif(regexY.fullmatch(element[0:1]) and y==-1):
			y=element[0:1].lower()
	if(findDir):
		if(x and y and direction):
			return list(x,y,direction)
		else:
			return False
	else:
		if(x and y):
			return list(x,y)
		else:
			return False
def createGrid(size,grid):
	for team in [player1,player2]:
		for x in range(0,size):
			grid[team].append([])
			for y in range(0,size):
				grid[team][x].append(0)
def cls(title=""):
	print("\033[2J")
	os.system('cls' if os.name == 'nt' else 'clear')
def attackCell(attackX,attackY,player):
	gridDefense = defenseGrid[player]
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
def setupScreen():
	cls()
	printLoc(white+title,centerAlign(title),2)
	printLoc(white+offenseTitle,leftAlign(offenseTitle),4)
	printLoc(white+defenseTitle,rightAlign(defenseTitle),4)
	printLoc(whiteDim+topRuler,leftAlign(topRuler),6)
	printLoc(whiteDim+legendTitle,centerAlign(legendTitle),7)
	printLoc(legendEmpty,centerAlign(legendEmpty)+4,8)
	printLoc(legendMiss,centerAlign(legendMiss)+3,9)
	printLoc(legendShip,centerAlign(legendShip)+2,10)
	printLoc(legendHit,centerAlign(legendHit)+3,11)
	printLoc(whiteDim+legendTitle,centerAlign(legendTitle),7)
	printLoc(whiteDim+legendTitle,centerAlign(legendTitle),7)
	printLoc(whiteDim+legendTitle,centerAlign(legendTitle),7)
	printLoc(whiteDim+topRuler,rightAlign(topRuler),6)
	for y in range(0,gridSize):
		printLoc(whiteDim+str(y),9,7+y)
		printLoc(whiteDim+str(y),49,7+y)
		for x in range(0,gridSize):
			printLoc(cyan+"~",11+x*2,7+y)
			printLoc(cyan+"~",51+x*2,7+y)
	printLoc(green+"Setting screen...",0,18)
def getInput(prompt,example=None,hiddenLength=0,encodings='\033[32m'):
	printLoc('\033[2K'+str(encodings)+str(prompt),0,18)
	if(example):
		printLoc('\033[2K'+examples[example][0]+' examples: ('+examples[example][1]+')',0,19)
	else:
		printLoc('\033[2K'+"No example found.",0,19)
	answer=input(reset+"\033[18;"+str(len(prompt)+2-hiddenLength)+"H"+reset)
	return answer.strip()
def addShip(shipX,shipY,direction,length,player):
	defenseGrid=defenseGrid[player]
	shipsGrid=shipsGrid[player]
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
global inGrid,printLoc,leftAlign,centerAlign,rightAlign
inGrid = lambda ig1, ig2: listCount(ig1,ig2,lambda ig3, ig4: ig4 in ig3,1)==1#Returns boolean
printLoc = lambda text, x, y:print('\033['+str(y)+';'+str(x)+'H'+text+reset)
leftAlign = lambda text:(80//4)-len(text)//2
centerAlign = lambda text:(80//2)-len(text)//2
rightAlign = lambda text:(80*3)//4-len(text)//2
global cyan,whiteBright,white,whiteDim,red,reset,green,yellow
cyan = '\033[0;36m'#cyan for grid letters and numbers
whiteBright  = '\033[1;37m'#bold white for misses and maybe titles
white = '\033[37m'#Normal white
whiteDim  = '\033[0;37m'#dim white for grid cells
red  = '\033[1;31m'#bold red for hits
reset = '\033[0m'#end color formatting and return to normal
green = '\033[32m'#green for user prompts
yellow = '\033[33m'#yellow for ship
global empty,miss,ship,hit
empty,miss,ship,hit = 0,1,2,3#CONST
global cell,cellNoformat
cell = {empty:cyan+'~',miss:whiteBright+'O',ship:yellow+'#',hit:red+'X'}#CONST
cellNoformat = {empty:'~',miss:'O',ship:'#',hit:'X'}#CONST
global shipName,shipLength
shipName = ("patrol boat","cruiser","submarine","battleship","aircraft carrier")#CONST
shipLength = (2,3,3,4,5)#CONST
global up,right,down,left
up,right,down,left = 0,1,2,3#CONST
global player1,player2
player1,player2 = 0,1#CONST
gridSize = 10#CONST
attackCellAlreadyAttacked = False#CONST
global seperator,regexX,regexY,regexDir
seperator = re.compile(r'[, |.;-]+')
regexX = re.compile(r'[A-J]',re.I)
regexY = re.compile(r'[0-9]')
regexDir = re.compile(r'(?:[urdl]|up|rightAlign|down|leftAlign)',re.I)
global title,offenseTitle,defenseTitle,topRuler,legendTitle,legendEmpty,legendMiss,legendShip,legendHit,examples
title="===TimoTree Battleship==="
offenseTitle,defenseTitle="Map of Enemy Fleet","Map of YOUR Fleet"
topRuler="A B C D E F G H I J"
legendTitle="Symbol Key:"
legendEmpty=cell[empty]+" - Empty"
legendMiss=cell[miss]+" - Miss"
legendShip=cell[ship]+" - Ship"
legendHit=cell[hit]+" - Hit"
examples = {'ship':("Ship location",'A 0 Down | A,0,D | a,0 DoWN'),'attack':("Coordinate",'A,0 | 0,a | a 0')}
setupScreen()
global queueGrid,defenseGrid,shipsGrid
queueGrid,defenseGrid,shipsGrid = [[],[]],[[],[]],[[],[]]
createGrid(gridSize,defenseGrid)
createGrid(gridSize,defenseGrid)
createGrid(gridSize,queueGrid)
while(listCount(defenseGrid[player1], ship)<sum(shipLength)):
	shipID=len(shipLength)
	for shipCount in reversed(list(accumulate(shipLength))):
		if(shipCount==listCount(defenseGrid[player1], ship)):
			break
		shipID-=1
	result = parseInput(getInput("Place your "+str(shipName[shipID])+yellow+(' '+cellNoformat[ship])*shipLength[shipID],'ship',5),True)
	getInput(str(result))
	if(result):
		shipMessage = addShip(result[0],result[1],result[2],shipLength[shipID],player1)
	# shipMessage = addShip(int(shipX)-1, int(shipY)-1, shipDirection, shipLength[shipID], player1)
	# if(shipMessage=="good"):
	# 	print("Ship placed.")
	else:
		# if(shipMessage=="ship"):
		# 	print("There is already a ship in that Square.")
		# if(shipMessage=="out"):
		# 	print("That's out of bounds.")
		# if(shipMessage=="direction"):
		# 	print("Invalid direction.")
		# print("Failed to place ship.")
		addHistory("Placement failed")
	printGrid(defenseGrid[player1])
printGrid(defenseGrid[player1])
sleep(2)
while(listCount(defenseGrid[player2], ship)<sum(shipLength)):
	shipID=len(shipLength)
	for shipCount in reversed(list(accumulate(shipLength))):
		if(shipCount==listCount(defenseGrid[player2], ship)):
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
		printGrid(defenseGrid[player2],"offense")
		print("It is your turn! Choose the cell to attack!")
		attackX=int(input("X coordinate from 1-"+repr(gridSize)+"\n"))-1
		attackY=int(input("Y coordinate from 1-"+repr(gridSize)+"\n"))-1
		attackMessage=attackCell(attackX, attackY, player1)
		if(attackMessage=="retry" and attackCellAlreadyAttacked==False):
			print("You have already attacked that spot. Choose a different cell.")
			sleep(1)
		else:
			printGrid(defenseGrid[player2],"offense")
			if(defenseGrid[player2][attackX][attackY]==miss):
				print("You didn't hit a ship.")
			elif(defenseGrid[player2][attackX][attackY]==hit):
				print("You hit a ship!")
				XY=str(attackX)+str(attackY)
				if(inGrid(shipsGrid[player2],XY)):
					breakNext=False
					for X in range(0,len(shipsGrid[player2])):
						if(breakNext):
							break
						for Y in range(0,len(shipsGrid[player2][X])):
							if(shipsGrid[player2][X][Y]==XY):
								shipsGrid[player2][X].pop(Y)
								if(len(shipsGrid[player2][X])==0):
									print("You sunk the enemy's "+str(shipName[X])+", nice shot!")
								breakNext=True
								break
				elif(attackCellAlreadyAttacked):
					print("You have already attacked that spot, you lose your turn.")
				else:
					raise GameError("Hit location not found in shipsGrid")
				if(not(inGrid(defenseGrid[player1],ship))):
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
			printGrid(defenseGrid[player1])
			print("Enemy:",repr(attackX+1),repr(attackY+1))
			queueGrid[player2][attackX][attackY]=0
			if(defenseGrid[player1][attackX][attackY]==miss):
				print("You weren't hit.")
			elif(defenseGrid[player1][attackX][attackY]==hit):
				print("Your enemy hit you! ")
				XY=str(attackX)+str(attackY)
				if(inGrid(shipsGrid[player1],XY)):
					breakNext=False
					for X in range(0,len(shipsGrid[player1])):
						if(breakNext):
							break
						for Y in range(0,len(shipsGrid[player1][X])):
							if(shipsGrid[player1][X][Y]==XY):
								shipsGrid[player1][X].pop(Y)
								if(len(shipsGrid[player1][X])==0):
									print("Your "+repr(shipName[X])+", has sunk.")
								breakNext=True
								break
				else:
					raise GameError("Hit location not found in shipsGrid")
				if(not(inGrid(defenseGrid[player1],ship))):
					print("Your enemy won in "+str(turnCount+1)+" turns. Better luck next time!")
					game=False
				if(attackX>0 and defenseGrid[player1][attackX-1][attackY]%2==0):
					queueGrid[player2][attackX-1][attackY] = 1
				if(attackY>0 and defenseGrid[player1][attackX][attackY-1]%2==0):
					queueGrid[player2][attackX][attackY-1]=1
				if(attackX+1<gridSize and defenseGrid[player1][attackX+1][attackY]%2==0):
					queueGrid[player2][attackX+1][attackY]=1
				if(attackY+1<gridSize and defenseGrid[player1][attackX][attackY+1]%2==0):
					queueGrid[player2][attackX][attackY+1]=1
			sleep(3)
			turnCount+=1

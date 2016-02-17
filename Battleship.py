from random import randint
from time import sleep
from itertools import accumulate
import os
import re
global cyan,whiteBright,white,whiteDim,red,reset,green,yellow
cyan = '\033[0;36m'#cyan for ocean
whiteBright  = '\033[1;37m'#bold white for misses and maybe titles
white = '\033[37m'#Normal white
whiteDim  = '\033[0;37m'#dim white for grid cells
red  = '\033[1;31m'#bold red for hits
reset = '\033[0m'#end color formatting and return to normal
green = '\033[32m'#green for user prompts
yellow = '\033[0;33m'#yellow for ship
global regex
regex = (re.compile(r'[, |.;-]+'),re.compile(r'[A-J]',re.I),re.compile(r'[0-9]'),re.compile(r'(?:[urdl]|up|right|down|left)',re.I))#CONST
global examples
examples = {'ship':("Ship location",'A 0 Down | A,0,D | a,0 DoWN'),'attack':("Coordinate",'A,0 | 0,a | a 0')}
global history,oldScreen
history = ["game started"]
oldScreen = []
refreshCount=0
global shipName,shipLength
shipName = ("patrol boat","cruiser","submarine","battleship","aircraft carrier")#CONST
shipLength = (2,3,3,4,5)#CONST
global cell,cellPlain,empty,miss,ship,hit
empty,miss,ship,hit = 0,1,2,3#CONST
cell = {empty:cyan+'~',miss:whiteBright+'O',ship:yellow+'#',hit:red+'X'}#CONST
cellPlain = {empty:'~',miss:'O',ship:'#',hit:'X'}#CONST
global up,right,down,left
up,right,down,left = 0,1,2,3#CONST
global player1,player2
player1,player2 = 0,1#CONST
global gridSize
gridSize = 10#CONST
attackCellAlreadyAttacked = False#CONST
global queueGrid,defenseGrid,shipsGrid
defenseGrid,queueGrid = [[*[[[0]*10]*10]*2]]*2
shipsGrid = [[],[]]
def addHistory(*args):
	centerAlign = lambda text:(80//2)-len(text)//2
	from shutil import get_terminal_size
	for arg in args:
		history.append(arg)
	y=20
	maxLength = (get_terminal_size()[1]-1)-y
	printLoc(green+"History:",centerAlign("History:"),y)
	for element in reversed(history[-maxLength:]):
		y+=1
		printLoc(green+element.title()+'.',centerAlign(element+'.'),y)
def parseInput(text,findDir,default=[None,None,None]):
	parsed1 = regex[0].split(text)
	x,y,direction = default
	for element in parsed1:
		if(regex[1].fullmatch(element[0:1]) and x==None):
			x=element[0:1]
		elif(regex[2].fullmatch(element[0:1]) and y==None):
			y=element[0:1]
		elif(regex[3].fullmatch(element) and direction==None and findDir):
			direction=element[0:1]
	if(findDir):
		if(x and y and direction):
			return [int(ord(x.upper())-65),int(y),direction.upper(),x]
		else:
			return False
	else:
		if(x and y):
			return [int(ord(x.upper())-65),int(y),x]
		else:
			return False
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
def recurseList(array,value,func=lambda a, b: a.count(b),func2=lambda a, b, c, d, e, f:a+recurseList(b,c,d,e,f),maximum=None):
	result=func(array,value)
	for element in array:
		if(not(maximum) or result<maximum):
			if(type(element)==list):
				result=func2(result,element,value,func,func2,maximum)
		else:
			return maximum
	return result
def updateScreen(screen=[defenseGrid[player2],defenseGrid[player1],"Map of Enemy Fleet","Map of YOUR Fleet"]):
	global refreshCount
	leftGrid,rightGrid,leftTitle,rightTitle = screen[0],screen[1],screen[2],screen[3]
	title="===TimoTree Battleship==="
	ruler="A B C D E F G H I J"
	legendTitle,legendEmpty,legendMiss,legendShip,legendHit="Symbol Key:",cell[empty]+" - Empty",cell[miss]+" - Miss",cell[ship]+" - Ship",cell[hit]+" - Hit"
	leftAlign = lambda text,hidden=0:(80//4)-(len(text)-hidden)//2
	centerAlign = lambda text,hidden=0:(80//2)-(len(text)-hidden)//2
	rightAlign = lambda text,hidden=0:(80*3)//4-(len(text)-hidden)//2
	if(refreshCount == 0):
		cls()
		printLoc(white+title,centerAlign(title),2)
		printLoc(white+leftTitle,leftAlign(leftTitle),4)
		printLoc(white+rightTitle,rightAlign(rightTitle),4)
		printLoc(whiteDim+ruler,leftAlign(ruler),6)
		printLoc(whiteDim+ruler,rightAlign(ruler),6)
		printLoc(whiteDim+legendTitle,centerAlign(legendTitle),7)
		printLoc(legendEmpty,centerAlign(legendEmpty,7),8)
		printLoc(legendMiss,centerAlign(legendMiss,7),9)
		printLoc(legendShip,centerAlign(legendShip,7),10)
		printLoc(legendHit,centerAlign(legendHit,7),11)
	for y in range(0,gridSize):
		printLoc(whiteDim+str(y),9,7+y)
		printLoc(whiteDim+str(y),49,7+y)
		for x in range(0,gridSize):
			if(leftGrid[x][y]==ship):
				printLoc(cell[empty],11+x*2,7+y)
			else:
				printLoc(cell[leftGrid[x][y]],11+x*2,7+y)
			printLoc(cell[rightGrid[x][y]],51+x*2,7+y)
	oldScreen = []
	refreshCount += 1
def getInput(prompt,example=None,hidden=0):
	printLoc('\033[2K'+str('\033[32m')+str(prompt),0,18)
	if(example):
		printLoc('\033[2K'+examples[example][0]+' examples: ('+examples[example][1]+')',0,19)
	else:
		printLoc('\033[2K'+"No example found.",0,19)
	answer=input(reset+"\033[18;"+str(len(prompt)+2-hidden)+"H"+reset)
	printLoc('\033[2K',0,18)
	printLoc('\033[2K',0,19)
	return answer.strip()
def addShip(x,y,direction,length,player):
	placementQueue = []
	beforeCount=recurseList(defenseGrid[player], ship)
	if(type(direction)==str):
		direction = {'U':up,'R':right,'D':down,'L':left}[direction]
	step, direction = {up:(-1,1),right:(1,0),down:(1,1),left:(-1,0)}[direction]
	xLength,yLength,xStep,yStep = [1,step*length,1,step] if(direction) else [step*length,1,step,1]
	for xIter in range(x,x+xLength,xStep):
		for yIter in range(y,y+yLength,yStep):
			try:
				if(defenseGrid[player][xIter][yIter]==empty):
					placementQueue.append(str(xIter)+str(yIter))
				else:
					return 'occupied'
			except IndexError:
				return 'out'
	shipsGrid[player].append([])
	for shipLoc in placementQueue:
		xIter,yIter = int(shipLoc[0]),int(shipLoc[1])
		defenseGrid[player][xIter][yIter]=ship
		shipsGrid[player][-1].append(str(xIter)+str(yIter))
	if(recurseList(defenseGrid[player], ship) < beforeCount + length):
		raise GameError("Not enough ship tiles placed.")
	return "good"
class GameError(Exception):
	def __init__(self, errorName="Unknown"):
		self.errorName = errorName
	def __str__(self):
		return repr(self.errorName)
global inGrid,printLoc
inGrid = lambda array, value: recurseList(array,value,lambda array2, value2: value2 in array2,maximum=1)>0#Returns boolean
printLoc = lambda text, x, y:print('\033['+str(y)+';'+str(x)+'H'+text+reset)
updateScreen()
addHistory()
while(recurseList(defenseGrid[player1], ship)<sum(shipLength)):
	shipID=len(shipLength)
	for shipCount in reversed(list(accumulate(shipLength))):
		if(shipCount==recurseList(defenseGrid[player1], ship)):
			break
		shipID-=1
	result = parseInput(getInput("Place your "+str(shipName[shipID])+yellow+(' '+cellPlain[ship])*shipLength[shipID],'ship',5),True)
	if(result):
		shipMessage = addShip(result[0],result[1],result[2],shipLength[shipID],player1)
		addHistory("placed at "+result[3]+str(result[1]))
	else:
		# 	print("There is already a ship in that Square.")
		# 	print("That's out of bounds.")
		# 	print("Invalid direction.")
		addHistory("placement failed")
	updateScreen()
while(recurseList(defenseGrid[player2], ship)<sum(shipLength)):
	shipID=len(shipLength)
	for shipCount in reversed(list(accumulate(shipLength))):
		if(shipCount==recurseList(defenseGrid[player2], ship)):
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
		updateScreen()
		# print("Attack a cell")
		result = parseInput(getInput("Attack a cell",'attack'),False)
		if(result):
			attackX=result[0]
			attackY=result[1]
			attackMessage = attackCell(attackX,attackY,player2)
			if(attackMessage=="retry" and attackCellAlreadyAttacked==False):
				print("You have already attacked that spot. Choose a different cell.")
			else:
				updateScreen()
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
				turnCount+=1
		else:
			addHistory("attack failed")
	else:
		attackX=randint(0,gridSize-1)
		attackY=randint(0,gridSize-1)
		breakNext=False
		for y in range(0,gridSize):
			if(breakNext):
				break
			for x in range(0,gridSize):
				if(queueGrid[player2][x][y]==1):
					attackX=x
					attackY=y
					breakNext=True
					break
		atackMessage=attackCell(attackX, attackY, player2)
		if(attackMessage!="retry"):
			updateScreen()
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
			turnCount+=1

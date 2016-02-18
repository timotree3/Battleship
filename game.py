from random import randint
from time import sleep
from itertools import accumulate
import os
import re
global inGrid,printLoc
inGrid = lambda array, value: recurseList(array,value,lambda array2, value2: value2 in array2,maximum=1)>0#Returns boolean
printLoc = lambda text, x, y:print('\033['+str(y)+';'+str(x)+'H'+text+reset)
global cyan,whiteBright,white,whiteDim,red,reset,green,yellow
cyan = '\033[0;36m'#cyan for ocean
whiteBright  = '\033[1;37m'#bold white for misses and maybe titles
white = '\033[37m'#Normal white
whiteDim  = '\033[0;37m'#dim white for grid cells
red  = '\033[1;31m'#bold red for hits
reset = '\033[0m'#end color formatting and return to normal
green = '\033[32m'#green for user prompts
yellow = '\033[0;33m'#yellow for ship
seperator = lambda txt:re.split(r'[, |.;/+\\-]+',txt)
xFilter = lambda txt:re.fullmatch(r'[A-J]',txt,re.I)
yFilter = lambda txt:re.fullmatch(r'[0-9]',txt)
dirFilter = lambda txt:re.fullmatch(r'(?:[urdl]|up|right|down|left)',txt,re.I)
global examples
examples = {'ship':'A 0 Down | A,0,D | a,0 DoWN','attack':'A,0 | 0,a | a 0',None:'No example found'}
global history,oldScreen
history = ["game started"]
oldScreen = []
refreshCount=0
global shipName,shipLength,ships
shipName = ("patrol boat",'cruiser',"submarine",'battleship',"aircraft carrier")#CONST
shipLength = (2,3,3,4,5)#CONST
ships = tuple(zip(
shipName,
shipLength,
[0]+list(accumulate(shipLength))))
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
defenseGrid,queueGrid = [[[[0 for y in range(gridSize)] for x in range(gridSize)] for team in range(2)] for i in range(2)]
shipsGrid = [[],[]]
def addHistory(*args):
	from shutil import get_terminal_size
	centerAlign = lambda text:(80//2)-len(text)//2
	for arg in args:
		history.append(arg)
	y=20
	maxLength = (get_terminal_size()[1]-1)-y
	printLoc('\033[2K'+green+"History:",centerAlign('History:'),y)
	for element in reversed(history[-maxLength:]):
		y+=1
		printLoc('\033[2K'+green+element.title()+'.',centerAlign(element+'.'),y)
def parseInput(text,preparation,*filters):
	from itertools import permutations
	prepared = preparation(text)
	found = False
	for inputLength in range(len(filters),len(prepared)+1):
		for combo in permutations(prepared[:inputLength]):
			match = [None for i in range(len(filters))]
			for i, Filter in enumerate(filters):
				# if(Filter.fullmatch(combo[i])):
				if(Filter(combo[i])):
					match[i] = combo[i]
			if(None not in match):
				found = True
				break
		if(found):
			return match
	return False
	# return [int(ord(x.upper()[:1])-65),int(y),direction.upper()[:1],x]
def cls(title=""):
	print('\033[s\033[2J\033[u')
	os.system('cls' if os.name == 'nt' else 'clear')
def attackCell(attackX,attackY,player):
	try:
		if(defenseGrid[player][attackX][attackY]%2>0):
			return('retry')
	except IndexError:
		return('out')
	else:
		defenseGrid[player][attackX][attackY]+=1
def recurseList(array,value,func=lambda a, b: a.count(b),func2=lambda a, b, c, d, e, f:a+recurseList(b,c,d,e,f),maximum=None):
	result=func(array,value)
	for element in array:
		if(not(maximum) or result<maximum):
			if(type(element)==list):
				result=func2(result,element,value,func,func2,maximum)
		else:
			return maximum
	return result
def updateScreen(screen=None):
	if(not(screen)):
		screen=[defenseGrid[player2],defenseGrid[player1],"Map of Enemy Fleet","Map of YOUR Fleet"]
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
	for y in range(gridSize):
		printLoc(whiteDim+str(y),9,7+y)
		printLoc(whiteDim+str(y),49,7+y)
		for x in range(gridSize):
			if(leftGrid[x][y]==ship):
				printLoc(cell[empty],11+x*2,7+y)
			else:
				printLoc(cell[leftGrid[x][y]],11+x*2,7+y)
			printLoc(cell[rightGrid[x][y]],51+x*2,7+y)
	refreshCount += 1
def getInput(prompt,example=None,hidden=0):
	printLoc('\033[2K'+green+str(prompt),0,18)
	printLoc('\033[2K'+green+'Example(s): ('+examples[example]+')',0,19)
	answer=input("\033[18;"+str(len(prompt)+2-hidden)+"H"+reset)
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
					placementQueue.append((str(xIter),str(yIter)))
				else:
					return 'occupied'
			except IndexError:
				return 'out'
	shipsGrid[player].append([])
	for shipLoc in placementQueue:
		x,y = int(shipLoc[0]),int(shipLoc[1])
		defenseGrid[player][x][y]=ship
		shipsGrid[player][-1].append((str(x),str(y)))
	if(recurseList(defenseGrid[player], ship) < beforeCount + length):
		raise GameError("Not enough ship tiles placed.")
	return 'good'
class GameError(Exception):
	def __init__(self, errorName='unknown'):
		self.errorName = errorName
		updateScreen()
	def __str__(self):
		return str(self.errorName[:1].upper()+self.errorName[1:])
updateScreen()
addHistory()
while(recurseList(defenseGrid[player1], ship)<sum(shipLength)):
	for shipInfo in ships:
		if(shipInfo[2]==recurseList(defenseGrid[player1], ship)):
			break
	result = parseInput(getInput("Place your "+str(shipInfo[0])+yellow+(' '+cellPlain[ship])*shipInfo[1],'ship',7),seperator,xFilter,yFilter,dirFilter)
	if(result):
		shipX,shipY,shipDir,prettyX = int(ord(result[0].upper())-65),int(result[1]),result[2].upper()[:1],result[0]
		shipMessage = addShip(shipX,shipY,shipDir,shipInfo[1],player1)
		if(shipMessage=='good'):
			addHistory("placed at "+prettyX+str(shipY))
		elif(shipMessage=='occupied'):
			addHistory("location already filled")
		elif(shipMessage=='out'):
			addHistory("location out of bounds")
	else:
		addHistory("invalid ship location")
	updateScreen()
while(recurseList(defenseGrid[player2], ship)<sum(shipLength)):
	for shipInfo in ships:
		if(shipInfo[2]==recurseList(defenseGrid[player2], ship)):
			break
	shipX=randint(0,gridSize-1)
	shipY=randint(0,gridSize-1)
	direction=randint(up,left)
	addShip(shipX, shipY, direction, shipInfo[1], player2)
game=True
turnCount=0
while(game):
	updateScreen()
	if(turnCount%2==0):
		result = parseInput(getInput("Attack a cell",'attack'),seperator,xFilter,yFilter)
		if(result):
			attackX,attackY,prettyX = int(ord(result[0].upper())-65),int(result[1]),result[0]
			attackMessage = attackCell(attackX,attackY,player2)
			if(attackMessage=='retry' and attackCellAlreadyAttacked==False):
				addHistory("cell already attacked")
			elif(attackCellAlreadyAttacked):
				addHistory("attack wasted")
			else:
				if(defenseGrid[player2][attackX][attackY]==miss):
					addHistory(str(prettyX)+str(attackY)+" miss")
				elif(defenseGrid[player2][attackX][attackY]==hit):
					addHistory(str(prettyX)+str(attackY)+" hit")
					XY=(str(attackX),str(attackY))
					if(inGrid(shipsGrid[player1],XY)):
						queuedBreak = False
						for i, shipCells in enumerate(shipsGrid[player2]):
							if queuedBreak: break
							for location in shipCells:
								if(location==XY):
									shipCells.remove(location)
									if(len(shipCells)==0):
										addHistory("sunk enemy's "+str(shipName[i]))
									queuedBreak = True
									break
					else:
						raise GameError("Hit location not found in shipsGrid")
					if(not(inGrid(defenseGrid[player1],ship))):
						printLoc('\033[J',0,17)
						printLoc("You won in "+str(turnCount)+" turns!",(80-len("You won in "+str(turnCount)+" turns!"))//2,18)
						game=False
				turnCount+=1
		else:
			addHistory("invalid attack location")
	else:
		attackX=randint(0,gridSize-1)
		attackY=randint(0,gridSize-1)
		breakNext=False
		for y in range(gridSize):
			if(breakNext):
				break
			for x in range(gridSize):
				if(queueGrid[player2][x][y]==1):
					attackX=x
					attackY=y
					breakNext=True
					break
		atackMessage=attackCell(attackX, attackY, player1)
		if(attackMessage!='retry'):
			queueGrid[player2][attackX][attackY]=0
			if(defenseGrid[player1][attackX][attackY]==miss):
				addHistory(str(chr(attackX+65))+str(attackY)+" miss")
			elif(defenseGrid[player1][attackX][attackY]==hit):
				addHistory(str(chr(attackX+65))+str(attackY)+" hit")
				XY=(str(attackX),str(attackY))
				if(inGrid(shipsGrid[player1],XY)):
					queuedBreak = False
					for i, shipCells in enumerate(shipsGrid[player1]):
						if queuedBreak: break
						for location in shipCells:
							if(location==XY):
								shipCells.remove(location)
								if(len(shipCells)==0):
									addHistory("sunk your "+str(shipName[i]))
								queuedBreak = True
								break
				else:
					raise GameError("Hit location not found in shipsGrid")
				if(not(inGrid(defenseGrid[player1],ship))):
					printLoc('\033[J',0,17)
					printLoc("You lost in "+str(turnCount+1)+" turns!",(80-len("You lost in "+str(turnCount+1)+" turns!"))//2,18)
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

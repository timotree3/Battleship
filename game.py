from random import randint
from time import sleep
from itertools import accumulate
from shutil import get_terminal_size
import re
global cyan, whiteBright, white, whiteDim, red, reset, green, yellow
cyan = '\033[0;36m'#cyan for ocean
whiteBright = '\033[1;37m'#bold white for misses and maybe titles
white = '\033[37m'#Normal white
whiteDim = '\033[0;37m'#dim white for grid cells
red = '\033[1;31m'#bold red for hits
reset = '\033[0m'#end color formatting and return to normal
green = '\033[32m'#green for user prompts
yellow = '\033[0;33m'#yellow for ship
seperator = lambda txt:re.split(r'[, |.;/+\\\t-]+', txt)
xFilter = lambda txt:re.fullmatch(r'[A-J]', txt, re.I)
yFilter = lambda txt:re.fullmatch(r'[0-9]', txt)
dirFilter = lambda txt:re.fullmatch(r'(?:[urdl]|up|right|down|left)', txt, re.I)
screenWidth, screenHeight = get_terminal_size()
screenWidth = (screenWidth//8)*8
examples = {'ship':'A 0 Down | A, 0, D | a, 0 DoWN', 'attack':'A, 0 | 0, a | a 0', None:'No example found'}
history = ["game started"]
refresh = True
global shipName, shipLength, ships
shipName = ("patrol boat", 'cruiser', "submarine", 'battleship', "aircraft carrier")#CONST
shipLength = (2, 3, 3, 4, 5)#CONST
ships = tuple(zip(shipName, shipLength, [0]+list(accumulate(shipLength))))
global empty, miss, ship, hit, cell
empty, miss, ship, hit = 0, 1, 2, 3#CONST
cell = {empty:cyan+'~', miss:whiteBright+'O', ship:yellow+'#', hit:red+'X'}#CONST
global up, right, down, left
up, right, down, left = 0, 1, 2, 3#CONST
global player1, player2
player1, player2 = 0, 1#CONST
global gridSize, grid
gridSize = 10#CONST
grid = range(gridSize)
attackSameCell = False#CONST
global queueGrid, defenseGrid, shipsGrid
defenseGrid = [[[0 for y in grid] for x in grid] for team in range(2)]
shipsGrid, queueGrid = [[], []], [[], []]
global inGrid, printLoc
inGrid = lambda array, value: recurseList(array, value, lambda array2, value2: value2 in array2, maximum = 1)>0#Returns boolean
printLoc = lambda text, x, y:print('\033['+str(y)+';'+str(x)+'H'+text+reset)
def parseInput(text, preparation, *filters):
	from itertools import permutations
	prepared = preparation(text)
	found = False
	for inputLength in range(len(filters), len(prepared)+1):
		for combo in permutations(prepared[:inputLength]):
			match = [None for i in range(len(filters))]
			for i, Filter in enumerate(filters):
				if(Filter(combo[i])):
					match[i] = combo[i]
			if(None not in match):
				found = True
				break
		if(found):
			return match
	return False
def cls(title = ""):
	from os import name, system
	print('\033[s\033[2J')
	system('cls' if name == 'nt' else 'clear')
	print('\033[u')
def attackCell(attackX, attackY, player):
	if(attackX in grid and attackY in grid):
		if(defenseGrid[player][attackX][attackY]%2>0):
			return('retry')
		else:
			defenseGrid[player][attackX][attackY]+=1
			return('success')
	else:
		return('out')
def recurseList(array, value, func = lambda a, b: a.count(b), func2 = lambda a, b, c, d, e, f:a+recurseList(b, c, d, e, f), maximum = None):
	result = func(array, value)
	for element in array:
		if(not(maximum) or result<maximum):
			if(type(element) == list):
				result = func2(result, element, value, func, func2, maximum)
		else:
			return maximum
	return result
def popShip(x, y, player):
	for shipCells in shipsGrid[player]:
		if((x, y) in shipCells):
			shipCells.remove((x, y))
			if(not(shipCells)):
				return ships[shipsGrid[player].index(shipCells)]
			return True
	return None
def updateScreen():
	leftGrid, rightGrid, leftTitle, rightTitle = defenseGrid[player2], defenseGrid[player1], "Enemy Fleet", "YOUR Fleet"
	title = "=== TimoTree Battleship ==="
	ruler = "A B C D E F G H I J"
	legendTitle, legendEmpty, legendMiss, legendShip, legendHit = "Symbol Key:", cell[empty]+" - Empty", cell[miss]+" - Miss", cell[ship]+" - Ship", cell[hit]+" - Hit"
	histName = "History:"
	global screenWidth, screenHeight, history, refresh
	b4Width, b4Height, screenWidth, screenHeight = screenWidth, screenHeight, *get_terminal_size()
	if(screenWidth<72 or screenHeight<24 or b4Width != screenWidth or b4Height != screenHeight):
		if(screenWidth<72 or screenHeight<24):
			printLoc("Please enlarge your screen", 0, 0)
		refresh = True
		while(screenWidth<72 or screenHeight<24 or b4Width != screenWidth or b4Height != screenHeight):
			b4Width, b4Height, screenWidth, screenHeight = screenWidth, screenHeight, *get_terminal_size()
			sleep(0.1)
	leftAlign = lambda text, hidden = 0:screenWidth//4-(len(text)-hidden)//2
	centerAlign = lambda text, hidden = 0:screenWidth//2-(len(text)-hidden)//2
	rightAlign = lambda text, hidden = 0:screenWidth*3//4-(len(text)-hidden)//2
	leftX, rightX = screenWidth//4-11, screenWidth*3//4-11
	if(refresh):
		cls()
		printLoc(white+title, centerAlign(title), 2)
		printLoc(white+leftTitle, leftAlign(leftTitle), 4)
		printLoc(white+rightTitle, rightAlign(rightTitle), 4)
		printLoc(whiteDim+ruler, leftX+2, 6)
		printLoc(whiteDim+ruler, rightX+2, 6)
		printLoc(whiteDim+legendTitle, centerAlign(legendTitle), 7)
		printLoc(legendEmpty, centerAlign(legendEmpty, 7), 8)
		printLoc(legendMiss, centerAlign(legendMiss, 7), 9)
		printLoc(legendShip, centerAlign(legendShip, 7), 10)
		printLoc(legendHit, centerAlign(legendHit, 7)-1, 11)
	for y in grid:
		printLoc(whiteDim+str(y), leftX, 7+y)
		printLoc(whiteDim+str(y), rightX, 7+y)
		for x in grid:
			printLoc(cell[{ship:empty}.get(leftGrid[x][y], leftGrid[x][y])], leftX+(x+1)*2, 7+y)
			printLoc(cell[rightGrid[x][y]], rightX+(x+1)*2, 7+y)
	printLoc('\033[2K'+green+histName, centerAlign(histName), 20)
	for y, action in zip(range(21, screenHeight), reversed(history[-(screenHeight):])):
		printLoc('\033[2K'+green+action.title()+'.', centerAlign(action+'.'), y)
	refresh = False
def getInput(prompt, example = None, hidden = 0):
	global examples
	printLoc('\033[2K'+green+str(prompt), 0, 18)
	printLoc('\033[2K'+green+'Example(s): ('+examples[example]+')', 0, 19)
	answer = input("\033[18;"+str(len(prompt)+2-hidden)+"H"+reset)
	printLoc('\033[2K', 0, 18)
	printLoc('\033[2K', 0, 19)
	return answer.strip()
def addShip(x, y, direction, length, player):
	placementQueue = []
	beforeCount = recurseList(defenseGrid[player], ship)
	if(type(direction) == str):
		direction = {'U':up, 'R':right, 'D':down, 'L':left}[direction]
	step, direction = {up:(-1, 1), right:(1, 0), down:(1, 1), left:(-1, 0)}[direction]
	xLength, yLength, xStep, yStep = [1, step*length, 1, step] if(direction) else [step*length, 1, step, 1]
	for xIter in range(x, x+xLength, xStep):
		for yIter in range(y, y+yLength, yStep):
			if(xIter in grid and yIter in grid):
				if(defenseGrid[player][xIter][yIter] == empty):
					placementQueue.append((str(xIter), str(yIter)))
				else:
					return 'occupied'
			else:
				return 'out'
	shipsGrid[player].append([])
	for shipLoc in placementQueue:
		x, y = int(shipLoc[0]), int(shipLoc[1])
		defenseGrid[player][x][y] = ship
		shipsGrid[player][-1].append((x, y))
	if(recurseList(defenseGrid[player], ship) < beforeCount + length):
		raise GameError("Not enough ship tiles placed.")
	return 'success'
class GameError(Exception):
	def __init__(self, errorName = 'unknown'):
		self.errorName = errorName
		updateScreen()
	def __str__(self):
		return str(self.errorName[:1].upper()+self.errorName[1:])
while(recurseList(defenseGrid[player1], ship)<sum(shipLength)):
	updateScreen()
	sleep(0.75)
	for shipInfo in ships:
		if(shipInfo[2] == recurseList(defenseGrid[player1], ship)):
			break
	result = getInput("Place your "+str(shipInfo[0])+(' '+cell[ship])*shipInfo[1], 'ship', 7*shipInfo[1])
	if(result == 'dev' and ships.index(shipInfo) == 0):
		for i, x in enumerate(range(0, gridSize, 2)):
			addShip(x, 0, down, shipLength[i], player1)
		break
	else:
		result = parseInput(result, seperator, xFilter, yFilter, dirFilter)
	if(result):
		shipX, shipY, shipDir, prettyX = int(ord(result[0].upper())-65), int(result[1]), result[2].upper()[:1], result[0]
		shipMessage = addShip(shipX, shipY, shipDir, shipInfo[1], player1)
		if(shipMessage == 'success'):
			history.append("placed at "+prettyX+str(shipY))
		elif(shipMessage == 'occupied'):
			history.append("location already filled")
		elif(shipMessage == 'out'):
			history.append("location out of bounds")
	else:
		history.append("invalid ship location")
while(recurseList(defenseGrid[player2], ship)<sum(shipLength)):
	for shipInfo in ships:
		if(shipInfo[2] == recurseList(defenseGrid[player2], ship)):
			break
	shipX = randint(0, gridSize-1)
	shipY = randint(0, gridSize-1)
	direction = randint(up, left)
	addShip(shipX, shipY, direction, shipInfo[1], player2)
game = True
turnCount = 0
while(game):
	updateScreen()
	sleep(0.75)
	if(turnCount%2 == 0):
		result = parseInput(getInput("Attack a cell", 'attack'), seperator, xFilter, yFilter)
		if(result):
			attackX, attackY, prettyX = int(ord(result[0].upper())-65), int(result[1]), result[0]
			attackMessage = attackCell(attackX, attackY, player2)
			if(attackMessage == 'retry'):
				if(attackSameCell):
					history.append("attack wasted")
				else:
					history.append("cell already attacked")
			else:
				if(defenseGrid[player2][attackX][attackY] == miss):
					history.append(str(prettyX)+str(attackY)+" miss")
				elif(defenseGrid[player2][attackX][attackY] == hit):
					history.append(str(prettyX)+str(attackY)+" hit")
					poppedShip = popShip(attackX, attackY, player2)
					if(type(poppedShip) == tuple):
						history.append("sunk enemy "+str(poppedShip[0]))
					elif(poppedShip == False):
						raise GameError('Ship not found in shipsGrid')
					if(not(inGrid(defenseGrid[player2], ship))):
						printLoc('\033[J', 0, 17)
						printLoc("You won in "+str(turnCount)+" turns!", (screenWidth-len("You won in "+str(turnCount)+" turns!"))//2, 18)
						game = False
				turnCount+=1
		else:
			history.append("invalid attack location")
	else:
		if(queueGrid[player2]):
			attackX, attackY = queueGrid[player2][randint(0, len(queueGrid[player2])-1)]
		else:
			attackX = randint(0, gridSize-1)
			attackY = randint(0, gridSize-1)
		attackMessage = attackCell(attackX, attackY, player1)
		while(inGrid(queueGrid[player2], (attackX, attackY))):
			queueGrid[player2].remove((attackX, attackY))
		if(attackMessage == 'success'):
			if(defenseGrid[player1][attackX][attackY] == miss):
				history.append(str(chr(attackX+65))+str(attackY)+" miss")
			elif(defenseGrid[player1][attackX][attackY] == hit):
				addQueue = True
				history.append(str(chr(attackX+65))+str(attackY)+" hit")
				poppedShip = popShip(attackX, attackY, player1)
				if(type(poppedShip) == tuple):
					history.append("sunk your "+str(poppedShip[0]))
					addQueue = False
				elif(poppedShip == False):
					raise GameError('Ship not found in shipsGrid')
				if(not(inGrid(defenseGrid[player1], ship))):
					printLoc('\033[J', 0, 17)
					printLoc("You lost in "+str(turnCount+1)+" turns!", (screenWidth-len("You lost in "+str(turnCount+1)+" turns!"))//2, 18)
					game = False
				for x in [attackX-1, attackX+1]:
					for y in [attackY-1, attackY+1]:
						if(x in grid and y in grid and (x, y) in queueGrid[player2]):
							queueGrid[player2].remove((x, y))
				if(addQueue):
					for direction in [attackX, attackY]:
						for coord in [direction-1, direction+1]:
							x, y = (coord, attackY) if direction == attackX else (attackX, coord)
							if(x in grid and y in grid and defenseGrid[player1][x][y]%2 == 0):
								queueGrid[player2].append((x, y))
			turnCount+=1

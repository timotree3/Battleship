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
xFilter = lambda txt:re.fullmatch(r'[A-Z]', txt, re.I)
yFilter = lambda txt:re.fullmatch(r'[0-9]', txt)
dirFilter = lambda txt:re.fullmatch(r'(?:[urdl]|up|right|down|left)', txt, re.I)
screenWidth, screenHeight = get_terminal_size()
screenWidth = (screenWidth//8)*8
examples = {'ship':'A 0 Down | A, 0, D | a, 0 DoWN', 'attack':'A, 0 | 0, a | a 0', None:'No example found'}
history = []
refresh = True
global shipName, shipLength, ships
shipName = ("patrol boat", 'cruiser', "submarine", 'battleship', "aircraft carrier")
shipLength = (2, 3, 3, 4, 5)
ships = tuple(zip(shipName, shipLength, [0]+list(accumulate(shipLength))))
global empty, miss, ship, hit, cell
empty, miss, ship, hit = 0, 1, 2, 3
cell = {empty:cyan+'~', miss:whiteBright+'O', ship:yellow+'#', hit:red+'X'}
global up, right, down, left
up, right, down, left = 0, 1, 2, 3
global player1, player2
player1, player2 = 0, 1
global gridSize, grid
gridSize = 10
grid = range(gridSize)
attackSameCell = False
global queueGrid, defenseGrid, shipsGrid
defenseGrid = [[[0 for y in grid] for x in grid] for team in range(2)]
shipsGrid, queueGrid = [[], []], [[], []]
global inGrid, printLoc
inGrid = lambda array, value: recurseList(array, value, lambda array2, value2: value2 in array2, maximum = 1)>0#Returns boolean
printLoc = lambda text, x, y:print('\033[{y};{x}H{text}'.format(y = y, x = x,text = text)+reset)
def updateScreen():
	leftGrid, rightGrid, leftTitle, rightTitle = defenseGrid[player2], defenseGrid[player1], "Enemy Fleet", "YOUR Fleet"
	title = "=== TimoTree Battleship ==="
	ruler = "A B C D E F G H I J"
	legendTitle, legendEmpty, legendMiss, legendShip, legendHit = "Legend:", cell[empty]+" - Empty", cell[miss]+" - Miss", cell[ship]+" - Ship", cell[hit]+" - Hit"
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
		from os import name, system
		print('\033[s\033[2J')
		system('cls' if name == 'nt' else 'clear')
		print('\033[u')
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
	printLoc('\033[2K{color}{title}'.format(color = green, title = histName), centerAlign(histName), 21)
	for y, action in zip(range(22, screenHeight), reversed(history[-(screenHeight):])):
		printLoc('\033[2K{color}{action}.'.format(color = green, action = action.title()), centerAlign(action+'.'), y)
	refresh = False
def getInput(prompt, example = None, hidden = 0):
	global examples, inputMessage
	printLoc('\033[2K{color}{message}.'.format(color = green, message = inputMessage[0].upper()+inputMessage[1:]), 0, 18)
	printLoc('\033[2K{color}{prompt}{color}:'.format(color = green, prompt = prompt), 0, 19)
	printLoc('\033[2K{color}Example(s): ({examples})'.format(color = green, examples = examples[example]), 0, 20)
	answer = input("\033[19;{x}H".format(x = len(prompt)+3-hidden)+reset)
	printLoc('\033[2K\n'*3, 0, 18)
	return answer.strip()
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
def offensiveTurn(x,y,player,queue=False,random=False):
	enemy = abs(player-1)
	while(random or queue):
		if(queue and len(queueGrid[player]) > 0):
			x, y = queueGrid[player][randint(0, len(queueGrid[player])-1)]
		elif(random):
			x, y = randint(min(grid),max(grid)),randint(min(grid),max(grid))
		else:
			break
		if(inGrid(queueGrid[player], (x, y))):
			queueGrid[player].remove((x, y))
		if(defenseGrid[enemy][x][y]%2 == 0):
			break
	if(x in grid and y in grid):
		try:
			defenseGrid[enemy][x][y] = {empty:miss,ship:hit}[defenseGrid[enemy][x][y]]
		except KeyError:
			return(('occupied', x, y))
	else:
		return(('out', x, y))
	if(defenseGrid[enemy][x][y] == miss):
		return(('miss', x, y))
	elif(defenseGrid[enemy][x][y] == hit):
		sunk = None
		for i, shipCells in enumerate(shipsGrid[enemy]):
			if((x, y) in shipCells):
				shipCells.remove((x, y))
				if(len(shipCells) == 0):
					sunk = i
				break
		else:
			raise GameError('ship not found in shipsGrid')
		for queueX in (x-1, x+1):
			for queueY in (y-1, y+1):
				if(queueX in grid and queueY in grid and (queueX, queueY) in queueGrid[player]):
					queueGrid[player].remove((queueX, queueY))
		if(sunk):
			return((sunk,x,y))
		for direction in (x, y):
			for coord in (direction-1, direction+1):
				queueX, queueY = (coord, y) if direction == x else (x, coord)
				if(defenseGrid[enemy][queueX][queueY]%2 == 0 and queueX in grid and queueY in grid):
					queueGrid[player].append((queueX, queueY))
		return(('hit', x, y))
def recurseList(array, value, func = lambda a, b: a.count(b), maximum = None):
	result = func(array, value)
	for element in array:
		if(not(maximum) or result<maximum):
			if(type(element) == list):
				result += recurseList(element, value, func, maximum)
		else:
			return maximum
	return result
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
		return(str(self.errorName[0].upper()+self.errorName[1:]))
inputMessage = "game started"
while(recurseList(defenseGrid[player1], ship)<sum(shipLength)):
	updateScreen()
	for shipInfo in ships:
		if(shipInfo[2] == recurseList(defenseGrid[player1], ship)):
			break
	result = getInput("Place your {name}{preview}".format(name = shipInfo[0], preview = (' '+cell[ship])*shipInfo[1]), 'ship', 7*shipInfo[1])
	inputMessage = "setting up board"
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
			inputMessage = "location already filled"
		elif(shipMessage == 'out'):
			inputMessage = "location out of bounds"
	else:
		inputMessage = "invalid ship location"
while(recurseList(defenseGrid[player2], ship)<sum(shipLength)):
	for shipInfo in ships:
		if(shipInfo[2] == recurseList(defenseGrid[player2], ship)):
			break
	shipX = randint(0, gridSize-1)
	shipY = randint(0, gridSize-1)
	direction = randint(up, left)
	addShip(shipX, shipY, direction, shipInfo[1], player2)
turnCount = 0
inputMessage = "you are now attacking"
while(True):
	updateScreen()
	if(turnCount%2 == 0):
		result = parseInput(getInput("Attack a cell", 'attack'), seperator, xFilter, yFilter)
		inputMessage = "it is your turn"
		if(result):
			attackX, attackY, prettyX = int(ord(result[0].upper())-65), int(result[1]), result[0]
			turnMessage = offensiveTurn(attackX, attackY, player1)[0]
			status, player = 'won', player1
		else:
			inputMessage = "invalid input"
			continue
	else:
		sleep(0.75)
		turnMessage, attackX, attackY = offensiveTurn(0, 0, player2, queue = True, random = True)
		prettyX = chr(attackX+65)
		status, player = 'lost', player2
	if(turnMessage == 'out'):
		raise GameError("location out of bounds")
	elif(not(turnMessage == 'occupied' and attackSameCell == False)):
		turnCount += 1
		if(turnMessage == 'occupied' and attackSameCell):
			inputMessage = "turn wasted on already attacked cell"
			turnMessage = 'wasted'
		if(type(turnMessage) == int):
			history.append("{x}{y} sunk {name}".format(x = prettyX, y = attackY, name = ships[turnMessage][0]))
			if(not(inGrid(defenseGrid[player], ship))):
				printLoc('\033[J', 0, 17)
				printLoc("You {status} in {turns} turns!".format(status = status, turns = turnCount//2), (screenWidth-len("You {status} in {turns} turns!".format(status = status, turns = turnCount//2)))//2, 18)
				break
		else:
			history.append("{x}{y} {action}".format(x = prettyX, y = attackY, action = turnMessage))

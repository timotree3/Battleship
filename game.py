from random import randint
from time import sleep
from itertools import chain
from shutil import get_terminal_size
import re
global white, reset, green, yellow
red = '\033[1;31m'
green = '\033[32m'#UI elements
yellow = '\033[33m'#Ships and History
white = '\033[37m'#UI elements and Misses
reset = '\033[m'#End coloring
global empty, miss, ship, hit, cell
empty, miss, ship, hit = 0, 1, 2, 3
cell = {empty:'\033[36m' + '~', miss:white + 'O', ship:yellow + '#', hit:red + 'X'}
global up, right, down, left
up, right, down, left = 0, 1, 2, 3
global player1, player2
player1, player2 = 0, 1
global gridSize, grid
gridSize = 10
grid = range(gridSize)
attackSameCell = False
global shipName, shipLength, ships
shipName = ("patrol boat", 'cruiser', 'submarine', 'battleship', "aircraft carrier")
shipLength = (2, 3, 3, 4, 5)
ships = tuple(zip(shipName, shipLength))
seperator = lambda txt:re.split(r'[, |.;/+\\\t]+', txt)
xFilter = (lambda txt:re.fullmatch(r'[A-Z]+', txt, re.I), lambda txt: txt.upper())
yFilter = (lambda txt:re.fullmatch(r'[0-9]+', txt), lambda txt: int(txt))
dirFilter = (lambda txt:re.fullmatch(r'(?:[urdl]|up|right|down|left)', txt, re.I), lambda txt: txt.upper()[0])
screenWidth, screenHeight = get_terminal_size()
examples = {'ship':("A 0 Down", "A, 0, D", "a, 0 DoWN"), 'attack':("A, 0", "0, a", "a 0")}
refresh = True
global queueGrid, defenseGrid, shipsGrid
defenseGrid = [[[0 for y in grid] for x in grid] for team in range(2)]
shipsGrid, queueGrid = [[], []], [[], []]
history = [('War', 'Declared', green)]
global printLoc
printLoc = lambda text, x, y:print('\033[{y};{x}H{text}'.format(y = y, x = x,text = text)+reset)
practicalX = lambda coord: sum([(([chr(i + 65) for i in range(26)].index(val.upper()) + 1) * 26 ** i) for i, val in enumerate(reversed(coord))])-1
def round(num: float):
	adder = 0
	for digit in reversed(str(num)[str(num).index('.') + 1:]):
		adder = int(int(digit) + adder >= 5)
	return(int(str(num)[:str(num).index('.')]) + adder)
def updateScreen():
	leftGrid, rightGrid, leftTitle, rightTitle = defenseGrid[player2], defenseGrid[player1], "Enemy Fleet", "Your Fleet"
	title = "=== TimoTree Battleship ==="
	ruler = "A B C D E F G H I J"
	legend = {'title':'Legend:', empty:'Empty', miss:'Miss', ship:'Ship', hit:'Hit'}
	histName = 'History'
	global screenWidth, screenHeight, history, refresh
	b4Width, b4Height, screenWidth, screenHeight = screenWidth, screenHeight, *get_terminal_size()
	if(screenWidth<72 or screenHeight<24 or b4Width != screenWidth or b4Height != screenHeight):
		if(screenWidth<72 or screenHeight<24):
			printLoc("Please enlarge your terminal", 0, 0)
		refresh = True
		while(screenWidth<72 or screenHeight<24 or b4Width != screenWidth or b4Height != screenHeight):
			b4Width, b4Height, screenWidth, screenHeight = screenWidth, screenHeight, *get_terminal_size()
			sleep(0.1)
	align = lambda text, alignment, hidden = 0:round(hidden + {'l':screenWidth / 4, 'm':screenWidth / 2, 'r':screenWidth * 3 / 4}[alignment] - (len(text) / 2))
	leftX, legendX, rightX = screenWidth // 4 - 11, align(legend['title'], 'm') - 1, screenWidth * 3 // 4 - 11
	if(refresh):
		from os import name, system
		print('\033[s\033[2J')
		system('cls' if name == 'nt' else 'clear')
		print('\033[u')
		printLoc(white+title, align(title, 'm'), 2)
		printLoc(white+leftTitle, align(leftTitle, 'l') - 1, 4)
		printLoc(white+rightTitle, align(rightTitle, 'r'), 4)
		printLoc(white+ruler, leftX+2, 6)
		printLoc(white+ruler, rightX+2, 6)
		printLoc(white+legend['title'], legendX + 1, 7)
		for i, cellType in enumerate(cell):
			printLoc(cell[cellType] + " - " + legend[cellType], legendX, i + 8)
	for y in grid:
		printLoc(white+str(y), leftX, 7+y)
		printLoc(white+str(y), rightX, 7+y)
		for x in grid:
			printLoc(cell[{ship:empty}.get(leftGrid[x][y], leftGrid[x][y])], leftX+(x+1) * 2, 7+y)
			printLoc(cell[rightGrid[x][y]], rightX+(x+1) * 2, 7+y)
	printLoc('\033[J' + green + histName, align(histName, 'm'), 21)
	for place, action, color, y in zip(*zip(*reversed(history)), range(22, screenHeight)):
		message = '{}: {}'.format(place, action)
		printLoc(color + message, align(message, 'm'), y)
	refresh = False
def getInput(prompt, example = None, queue = None, hidden = 0):
	global examples, inputMessage
	printLoc(inputMessage[1] + '{}.'.format(inputMessage[0].capitalize()), 0, 18)
	printLoc(green + '{}{}:'.format(prompt, reset), 0, 19)
	if(example in examples):
		printLoc(green + 'Example input{1}: ({0})'.format(' | '.join(examples[example]), 's'[:len(example) - 1]), 0, 20)
	if(queue):
		printLoc('\033[2K' + green + 'Suggested move{1}: {0}'.format(', '.join(['{} {}'.format(chr(x + 65), y) for x, y in queue[-3:]]), 's'[:len(queue)]), 0, 20)
	answer = input('\033[19;{}H'.format(len(prompt + ':  ') - hidden) + reset)
	printLoc('\033[2K\n' * 3, 0, 18)
	return answer.strip()
def parseInput(text, preparation, *filters):
	from itertools import permutations
	prepared = preparation(text)
	for inputLength in range(len(filters), len(prepared)+1):
		for combo in permutations(prepared[:inputLength]):
			match = []
			for element, Filter in zip(combo, filters):
				match.append(Filter[1](element) if(Filter[0](element)) else None)
			if(None not in match):
				return match
	return False
def offensiveTurn(x,y,player,queue = False,random = False):
	enemy = abs(player - 1)
	while(random or queue):
		if(queue and len(queueGrid[player]) > 0):
			x, y = queueGrid[player][randint(0, len(queueGrid[player]) - 1)]
		elif(random):
			x, y = randint(min(grid),max(grid)),randint(min(grid),max(grid))
		else:
			break
		while((x, y) in queueGrid[player]):
			queueGrid[player].remove((x, y))
		if(defenseGrid[enemy][x][y] % 2 == 0):
			break
	if(x not in grid or y not in grid):
		return ('out', x, y)
	try:
		defenseGrid[enemy][x][y] = {empty:miss,ship:hit}[defenseGrid[enemy][x][y]]
	except KeyError:
		return ('occupied', x, y)
	if(defenseGrid[enemy][x][y] == miss):
		return ('miss', x, y)
	elif(defenseGrid[enemy][x][y] == hit):
		sunk = None
		for i, shipCells in enumerate(shipsGrid[enemy]):
			if((x, y) in shipCells):
				shipCells.remove((x, y))
				if(len(shipCells) == 0):
					sunk = i
				break
		for queueX in (x - 1, x+1):
			for queueY in (y - 1, y+1):
				if(queueX in grid and queueY in grid and (queueX, queueY) in queueGrid[player]):
					queueGrid[player].remove((queueX, queueY))
		if(sunk != None):
			return (sunk, x, y)
		for queueX, queueY in ((x - 1, y), (x+1, y), (x, y - 1), (x, y+1)):
			if(queueX in grid and queueY in grid and defenseGrid[enemy][queueX][queueY] % 2 == 0):
				queueGrid[player].append((queueX, queueY))
		return ('hit', x, y)
def count(array, value, boolean = False):
	result = array.count(value)
	if(result > 0 and boolean):
		return(True)
	for element in array:
		if(type(element) == list):
			result += count(element, value, maximum)
	return result
def addShip(x, y, direction, length, player):
	placementQueue = []
	if(type(direction) == str):
		direction = {'U':up, 'R':right, 'D':down, 'L':left}[direction]
	step, direction = {up:( - 1, 1), right:(1, 0), down:(1, 1), left:( - 1, 0)}[direction]
	xLength, yLength, xStep, yStep = [1, step * length, 1, step] if(direction) else [step * length, 1, step, 1]
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
		shipsGrid[player][ - 1].append((x, y))
	return 'success'
class GameError(Exception):
	def __init__(self, errorName = 'unknown'):
		self.errorName = errorName
		updateScreen()
	def __str__(self):
		return(str(self.errorName[0].upper()+self.errorName[1:]))
inputMessage = ("game started", green)
while(len(shipsGrid[player1]) < len(ships)):
	updateScreen()
	shipInfo = ships[len(shipsGrid[player1])]
	result = getInput("Place your {}{preview}".format(shipInfo[0], preview = (' '+cell[ship]) * shipInfo[1]), 'ship', hidden = 5 * shipInfo[1])
	inputMessage = ("filling board", green)
	if(result == 'dev' and len(shipsGrid[player1]) == 0):
		for i, x in enumerate(range(0, gridSize, 2)):
			addShip(x, 0, down, shipLength[i], player1)
	else:
		result = parseInput(result, seperator, xFilter, yFilter, dirFilter)
		if(result):
			prettyX, shipY, shipDir = result
			shipX = practicalX(prettyX)
			shipMessage = addShip(shipX, shipY, shipDir, shipInfo[1], player1)
			if(shipMessage == 'success'):
				history.append((prettyX + str(shipY), 'Ship Placed', yellow))
			elif(shipMessage == 'occupied'):
				inputMessage = ("location already filled", red)
			elif(shipMessage == 'out'):
				inputMessage = ("location out of bounds", red)
		else:
			inputMessage = ("invalid ship location", red)
while(len(shipsGrid[player2]) < len(shipLength)):
	shipInfo = ships[len(shipsGrid[player2])]
	shipX, shipY = randint(min(grid), max(grid)), randint(min(grid), max(grid))
	direction = randint(0, 3)
	addShip(shipX, shipY, direction, shipInfo[1], player2)
turnCount = 0
inputMessage = ("you are now attacking", green)
history = [("Ships", 'Placed', yellow)]
while(True):
	updateScreen()
	if(turnCount % 2 == 0):
		status, player, enemy = 'won', player1, player2
		result = parseInput(getInput("Attack a cell", 'attack', queueGrid[player]), seperator, xFilter, yFilter)
		inputMessage = ("it is your turn", green)
		if(result):
			prettyX, attackY = result
			attackX = practicalX(prettyX)
			turnMessage = offensiveTurn(attackX, attackY, player1)[0]
		else:
			inputMessage = ("invalid input", red)
			continue
	else:
		sleep(0.75)
		status, player, enemy = 'lost', player2, player1
		turnMessage, attackX, attackY = offensiveTurn(0, 0, player2, queue = True, random = True)
		prettyX = chr(attackX+65)
	if(turnMessage == 'out'):
		inputMessage = ("location out of bounds", red)
	elif(not(turnMessage == 'occupied' and attackSameCell == False)):
		turnCount += 1
		if(turnMessage == 'occupied' and attackSameCell):
			inputMessage = ("turn wasted on already attacked cell", red)
			turnMessage = 'wasted'
		if(type(turnMessage) == int):
			updateScreen()
			history.append((prettyX + str(attackY), "Sunk '{}'".format(ships[turnMessage][0].title()), yellow))
			if(len(list(chain.from_iterable(shipsGrid[enemy]))) == 0):
				printLoc('\033[J\n' + green + "You {} in {turns} turns!".format(status, turns = turnCount // 2).center(screenWidth - 1) + reset, 0, 17)
				break
		else:
			history.append((prettyX + str(attackY), turnMessage.capitalize(), {'miss': white, 'hit': red}.get(turnMessage, yellow)))
input()

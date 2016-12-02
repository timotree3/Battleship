#!/bin/env python3
from time import sleep as delay
from itertools import chain as combine
from shutil import get_terminal_size
from json import load
from random import choice
EMPTY, MISS, SHIP, HIT = 0, 1, 2, 3
USER, BOT = 0, 1
RESET = '\033[0m'
def refresh():
    from os import system, name
    ruler = ' '.join([chr(i + 65) for i in range(gridSize)])
    legend = ('Empty', 'Miss', 'Ship', 'Hit', 'Legend:')
    legendX = int(width / 2 - len(legend[-1]) / 2) - 1
    leftX, rightX = width // 4 - (gridSize + 1), width * 3 // 4 - (gridSize + 1)
    print('\033[s\033[2J')
    system('cls' if name == 'nt' else 'clear')
    print('\033[u')
    printLoc(colors['interface'] + "=== TimoTree Battleship ===", int((width-len("=== TimoTree Battleship ===")) / 2), 2)
    printLoc(colors['interface'] + "Enemy Fleet", int(width / 4 - len("Enemy Fleet") / 2) - 1, 4)
    printLoc(colors['interface'] + "Your Fleet", int(width * 3 / 4 - len("Your Fleet") / 2), 4)
    printLoc(colors['interface'] + ruler, leftX + 2, 6)
    printLoc(colors['interface'] + ruler, rightX + 2, 6)
    printLoc(colors['interface'] + legend[-1], legendX + 1, 7)
    for i in range(len(cell)):
        printLoc(cell[i] + " - " + legend[i], legendX, i + 8)
def update():
    leftGrid, rightGrid = defenseGrid[BOT], defenseGrid[USER]
    global width, height, history
    widthBefore, heightBefore = width, height
    width, height = get_terminal_size()
    changed = (width != widthBefore or width < 72
               or height != heightBefore or height < 24)
    while width < 72 or height < 24:
        printLoc("Please enlarge your terminal", 0, 0)
        delay(0.4)
        width, height = get_terminal_size()
    if changed:
        refresh()
    leftX, rightX = width // 4 - (gridSize + 1), width * 3 // 4 - (gridSize + 1)
    for y in grid:
        printLoc(colors['interface'] + str(y), leftX, 7+y)
        printLoc(colors['interface'] + str(y), rightX, 7+y)
        for x in grid:
            printLoc(cell[{SHIP:EMPTY}.get(leftGrid[x][y], leftGrid[x][y])], leftX+(x+1) * 2, 7+y)
            printLoc(cell[rightGrid[x][y]], rightX+(x+1) * 2, 7+y)
    printLoc('\033[J' + colors['prompt'] + 'History', int((width-len('History')) / 2), gridSize + 11)
    for subject, change, color, y in zip(*zip(*reversed(history)), range(gridSize + 12, height)):
        entry = subject + ': ' + change
        printLoc(color + entry, int((width-len(entry)) / 2), y)
def getInput(prompt, example=None, queue=None):
    global examples, feedback
    printLoc(feedback[1] + '{}.'.format(feedback[0].capitalize()), 0, gridSize + 8)
    if example in examples:
        printLoc(colors['prompt'] + 'Example input{1}: ({0})'.format(' | '.join(examples[example]), 's'[:len(example) - 1]), 0, gridSize + 10)
    if queue:
        printLoc('\033[2K' + colors['prompt'] + 'Suggested move{1}: {0}'.format(', '.join(['{} {}'.format(chr(x + 65), y) for x, y in queue[-3:]]), 's'[:len(queue)]), 0, gridSize + 10)
    answer = input(colors['prompt'] + '\033[{y};0H{}{}: '.format(prompt, RESET, y=gridSize + 9))
    printLoc('\033[2K\n' * 3, 0, gridSize + 8)
    return answer.strip()
def getLocation(text, *extras):
    from itertools import permutations
    from re import split, fullmatch, IGNORECASE
    tests = [(r'[A-Z]+', str.upper), (r'\d+', int)] + list(extras)
    values = split(r',? +', text)
    for length in range(len(tests), len(values)+1):
        for combo in permutations(values[:length]):
            match = []
            for value, test in zip(combo, tests):
                if not fullmatch(test[0], value, IGNORECASE):
                    break
                match.append(test[1](value))
            else:#runs only if loop ended without a encountering a 'break' statement
                return match
    return False
def offensiveTurn(player, x=0, y=0):
    from random import randrange
    enemy = int(not player)
    if player == BOT:
        if queueGrid[player]:
            x, y = queueGrid[player].pop(randrange(len(queueGrid[player])))
        else:
            global bot
            while bot:
                queue, invalids = [], []
                for y in grid:
                    for x in grid:
                        if defenseGrid[enemy][x][y] % 2 == 0:
                            queue.append((x, y))
                        else:
                            invalids.append((x, y))
                for x, y in {'perfect':invalids, 'valid':queue}[bot]:
                    for offset in range(1, min([shipLength[i] for i, shipList in enumerate(shipsGrid[enemy]) if len(shipList) > 0])):
                        if bot == 'perfect':
                            for checkX, checkY in ((x - offset, y), (x + offset, y), (x, y - offset), (x, y + offset)):
                                if (checkX, checkY) in queue:
                                    queue.remove((checkX, checkY))
                        elif bot == 'valid':
                            for checkX, checkY in ((x - offset, y), (x + offset, y), (x, y - offset), (x, y + offset)):
                                if checkX in grid and checkY in grid and defenseGrid[enemy][checkX][checkY] != MISS:
                                    break
                            else:
                                if (x, y) in queue:
                                    queue.remove((x, y))
                if queue:
                    x, y = choice(queue)
                    break
                else:
                    bot = ('perfect', 'valid', None)[('perfect', 'valid', None).index(bot) + 1]
            while not bot:
                x, y = choice(grid), choice(grid)
                if defenseGrid[enemy][x][y] % 2 == 0:
                    break
    elif (x, y) in queueGrid[player]:
        queueGrid[player].remove((x, y))
    if x not in grid or y not in grid:
        return ('out', x, y)
    try:
        defenseGrid[enemy][x][y] = {EMPTY:MISS, SHIP:HIT}[defenseGrid[enemy][x][y]]
    except KeyError:
        return ('wasted', x, y)
    if defenseGrid[enemy][x][y] == HIT:
        sunk = None
        for i, shipCells in enumerate(shipsGrid[enemy]):
            if (x, y) in shipCells:
                shipCells.remove((x, y))
                if len(shipCells) == 0:
                    sunk = i
                break
        for x2 in (x - 1, x + 1):
            for y2 in (y - 1, y + 1):
                if x2 in grid and y2 in grid and (x2, y2) in queueGrid[player]:
                    queueGrid[player].remove((x2, y2))
        if sunk != None:
            return (sunk, x, y)
        firstHit, secondHit = [], []
        for x2, y2 in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if x2 in grid and y2 in grid:
                if defenseGrid[enemy][x2][y2] % 2 == 0 and (x2, y2) not in queueGrid[player]:
                    firstHit.append((x2, y2))
                if defenseGrid[enemy][x2][y2] == HIT and (x + (x - x2), y + (y - y2)) not in queueGrid[player]:
                    secondHit.append((x + (x - x2), y + (y - y2)))
        queueGrid[player] += secondHit if secondHit else firstHit
    return (('empty', 'miss', 'ship', 'hit')[defenseGrid[enemy][x][y]], x, y)
def addShip(x, y, direction, length, player):
    placementQueue = []
    step, axis = {'L': (-1, 'X'), 'U': (-1, 'Y'), 'R': (1, 'X'), 'D': (1, 'Y')}[direction]
    xLength, yLength, xStep, yStep = [1, step * length, 1, step] if axis == 'Y' else [step * length, 1, step, 1]
    for xIter in range(x, x+xLength, xStep):
        for yIter in range(y, y+yLength, yStep):
            if xIter in grid and yIter in grid:
                if defenseGrid[player][xIter][yIter] == EMPTY:
                    placementQueue.append((str(xIter), str(yIter)))
                else:
                    return 'occupied'
            else:
                return 'out'
    shipsGrid[player].append([])
    for shipLoc in placementQueue:
        x, y = int(shipLoc[0]), int(shipLoc[1])
        defenseGrid[player][x][y] = SHIP
        shipsGrid[player][-1].append((x, y))
    return 'success'
def checkConfig():
    class ConfigError(Exception):
        def __init__(self, error, fix):
            self.error = error
            self.fix = fix if fix else "using the default config file"
        def __str__(self):
            print("config: {}\n(try {})".format(self.error, self.fix))
    if not isinstance(wasteTurns, bool):
        raise ConfigError("wasteTurns is not type bool",
                          "making it either 'true' or 'false'")
    if not isinstance(gridSize, int):
        raise ConfigError("gridSize is not an integer",
                          "setting it to a whole number")
    if gridSize < 1:
        raise ConfigError("gridSize is less than 1",
                          "setting it to be more than 1")
    if len(shipLength) < 1:
        raise ConfigError("shipLength is empty",
                          "adding a length to it")
    if min(shipLength) < 1:
        raise ConfigError("there is a ship with a length of less than 1",
                          "making them all 1 or more")
    if max(shipLength) > gridSize:
        raise ConfigError("there is a ship too long to fit on the grid",
                          "making it shorter")
    if sum(shipLength) > gridSize*gridSize:
        raise ConfigError("not all the ships can fit",
                          "making them all shorter")
    if not isinstance(colors, dict):
        raise ConfigError("colors is not an object",
                          "adding curly braces")
width, height = get_terminal_size()
examples = {'ship':("A 0 Down", "A, 0, D", "a, 0 DoWN"), 'attack':("A, 0", "0, a", "a 0")}
bot = 'perfect'
with open("config.json") as config:
    configured = load(config)
if not isinstance(configured, dict):
    raise Exception("file is not an object")
wasteTurns = configured["wasteTurns"]
gridSize = configured["gridSize"]
shipLength, shipName = configured["shipLength"], configured["shipName"]
colors = configured["colors"]
checkConfig()
for element in colors:
    colors[element] = "\033[3{}m".format(('black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white').index(colors[element]))
grid = range(gridSize)
ships = tuple(zip(shipName, shipLength))
cell = (colors['empty'] + '~', colors['miss'] + 'O', colors['ship'] + '#', colors['hit'] + 'X')
defenseGrid = [[[0 for y in grid] for x in grid] for team in range(2)]
shipsGrid, queueGrid = [[], []], [[], []]
history = [('War', 'Declared', colors['success'])]
moveCursor = lambda x, y: '\033[{};{}H'.format(y, x)
printLoc = lambda text, x, y: print(moveCursor(x, y) + text + RESET)
practicalX = lambda coord: sum([(([chr(i + 65) for i in range(26)].index(val.upper()) + 1) * 26 ** i) for i, val in enumerate(reversed(coord))])-1
feedback = ("game started", colors['success'])
refresh()
while len(shipsGrid[USER]) < len(ships):
    update()
    shipInfo = ships[len(shipsGrid[USER])]
    result = getInput("Place your " + shipInfo[0] + (' ' + cell[SHIP]) * shipInfo[1], 'ship')
    feedback = ("filling board", colors['success'])
    if result == 'dev' and len(shipsGrid[USER]) == 0:
        for i, y in enumerate(range(0, gridSize, 2)):
            addShip(0, y, 'R', shipLength[i], USER)
    else:
        result = getLocation(result, (r'l(?:eft)?|u(?:p)?|r(?:ight)?|d(?:own)?', str.upper))
        if result:
            prettyX, shipY, shipDir = result
            shipX = practicalX(prettyX)
            output = addShip(shipX, shipY, shipDir[0], shipInfo[1], USER)
            if output == 'success':
                history.append((prettyX + str(shipY), 'Ship Placed', colors['ship']))
            elif output == 'occupied':
                feedback = ("location already filled", colors['fail'])
            elif output == 'out':
                feedback = ("location out of bounds", colors['fail'])
        else:
            feedback = ("invalid ship location", colors['fail'])
while len(shipsGrid[BOT]) < len(ships):
    addShip(choice(grid), choice(grid), choice(('L', 'U', 'R', 'D')), ships[len(shipsGrid[BOT])][1], BOT)
turnCount = 0
feedback = ("you are now attacking", colors['success'])
history = [("Ships", "Placed", colors['ship'])]
while True:
    update()
    if turnCount % 2 == 0:
        status, player, enemy = 'won', USER, BOT
        result = getLocation(getInput("Attack a cell", 'attack', queueGrid[player]))
        feedback = ("it is your turn", colors['success'])
        if result:
            prettyX, attackY = result
            attackX = practicalX(prettyX)
            output = offensiveTurn(USER, attackX, attackY)[0]
        else:
            feedback = ("invalid input", colors['fail'])
            continue
    else:
        delay(0.75)
        status, player, enemy = 'lost', BOT, USER
        output, attackX, attackY = offensiveTurn(BOT)
        prettyX = chr(attackX+65)
    if output == 'wasted':
        feedback = ("cell already attacked", colors['fail'])
    if output == 'out':
        feedback = ("location out of bounds", colors['fail'])
    elif not(output == 'wasted') or wasteTurns:
        turnCount += 1
        if isinstance(output, int):
            update()
            history.append((prettyX + str(attackY), "Sunk " + shipName[output].title(), colors['ship']))
            if len(list(combine.from_iterable(shipsGrid[enemy]))) == 0:
                input("\033[{y};0H\033[J\n{color}You {} in {} turns!{}\n".format(status, turnCount // 2, RESET, color=colors['interface'], y=gridSize + 7))
                break
        else:
            history.append((prettyX + str(attackY), output.capitalize(), colors['empty'] if output == 'wasted' else colors[output]))

from shutil import get_terminal_size
from time import sleep
from os import system
gridSize = 10
cyan = '\033[0;36m'    #cyan for grid letters and numbers
whiteBright  = '\033[1;37m'  #bold white for misses and maybe titles
white = '\033[37m' #Normal white
whiteDim  = '\033[0;37m'  #dim white for grid cells
red  = '\033[1;31m'  #bold red for hits
reset = '\033[0m'     #end color formatting and return to normal
green = '\033[32m'    #green for user prompts
yellow = '\033[33m'    #yellow for user prompts
empty,miss,ship,hit = 0,1,2,3#Constants
cell = {empty:cyan+'~',miss:whiteBright+'O',ship:yellow+'#',hit:red+'X'}
printLoc = lambda text, x, y:print('\033['+str(y)+';'+str(x)+'H'+text+reset)
left = lambda text:(80//4)-len(text)//2
center = lambda text:(80//2)-len(text)//2
right = lambda text:(80*3)//4-len(text)//2
# print('\033[1;37m This is normal')
# print("")
# for attr in range(0,8):
# 	for fg in range(30,38):
# 		print('')
# 		print('\033[1;37m default	',end="")
# 		for bg in range(40,48):
# 			print('\033['+ str(attr) +';'+ str(bg) +';'+ str(fg) +'m ' \
# 			+str(attr)+';'+str(fg)+';'+str(bg)+'\033[m ',end="")
# print("")
# print('\033[1;37m This is back to normal')
system('cls')
string="X - Hit"
title="===TimoTree Battleship==="
offenseTitle="Map of Enemy Fleet"
defenseTitle="Map of YOUR Fleet"
topRuler="A B C D E F G H I J"
legendTitle="Symbol Key:"
legendEmpty=cell[empty]+" - Empty"
legendMiss=cell[miss]+" - Miss"
legendShip=cell[ship]+" - Ship"
legendHit=cell[hit]+" - Hit"
# printLoc(str(left(string)),left(str(left(string))),1)
# printLoc(str(center(string)),center(str(center(string))),1)
# printLoc(str(right(string)),right(str(right(string))),1)
printLoc(white+title,center(title),2)
printLoc(white+offenseTitle,left(offenseTitle),4)
printLoc(white+defenseTitle,right(defenseTitle),4)
printLoc(whiteDim+topRuler,left(topRuler),6)
printLoc(whiteDim+legendTitle,center(legendTitle),7)
printLoc(legendEmpty,center(legendEmpty)+4,8)
printLoc(legendMiss,center(legendMiss)+3,9)
printLoc(legendShip,center(legendShip)+2,10)
printLoc(legendHit,center(legendHit)+3,11)
printLoc(whiteDim+legendTitle,center(legendTitle),7)
printLoc(whiteDim+legendTitle,center(legendTitle),7)
printLoc(whiteDim+legendTitle,center(legendTitle),7)
printLoc(whiteDim+topRuler,right(topRuler),6)
for y in range(0,gridSize):
	printLoc(whiteDim+str(y),9,7+y)
	printLoc(whiteDim+str(y),49,7+y)
	for x in range(0,gridSize):
		printLoc(cyan+"~",11+x*2,7+y)
		printLoc(cyan+"~",51+x*2,7+y)

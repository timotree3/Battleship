[![Stories in Ready](https://badge.waffle.io/timotree3/battleship.png?label=ready&title=Ready)](https://waffle.io/timotree3/battleship)
# ==TimoTree Battleship==
==My first battleship game. Written in Python.==

A text-based battleship game. Everything works great including:
### Signicant Features:
* Configuration file to change colors, grid size, and other things
* Open source game
* Good AI that is still being improved
* Great color coded UI with visual grid representation and history
***
### Description:
The game starts with placing ships. You an place them anywhere on the grid and you want to put them in a place the enemy won't expect.   
After the ships are placed you attack the enemies area and try to guess where there ships are.   
The game ends after all of one players ships have sunk.
```
Example window:
                          ===TimoTree Battleship===

     Map of Computer's Fleet                        Map of YOUR Fleet

   A  B  C  D  E  F  G  H  I  J                 A  B  C  D  E  F  G  H  I  J
0  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~    Legend:   0  #  ~  ~  ~  ~  ~  ~  ~  ~  #
1  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~   ~ - Empty  1  #  ~  ~  ~  ~  ~  ~  ~  ~  #
2  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~   O - Miss   2  ~  ~  ~  #  #  #  #  ~  ~  #
3  ~  ~  X  X  ~  ~  ~  ~  ~  ~   # - Ship   3  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~
4  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~   X - Hit    4  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~
5  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~              5  ~  ~  ~  ~  ~  O  ~  ~  ~  ~
6  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~              6  O  ~  ~  ~  ~  ~  ~  ~  ~  ~
7  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~              7  ~  ~  ~  ~  ~  ~  ~  ~  ~  #
8  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~              8  ~  ~  ~  #  #  #  #  #  ~  #
9  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~              9  ~  ~  ~  ~  ~  ~  ~  ~  ~  #

Attack a cell: _

Your Attacks:                         Computer's Attacks:
 C3 - Hit! Sunk Patrol Boat            F5 - Miss!
 D3 - Hit!                             A6 - Miss!
```
###### Come play with us!
***
#### Requires Python version 3.*
##### Windows versions before Windows 10 do not interpret color and mouse movement codes correctly and might require a future patch.

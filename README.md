[![Tasks in Ready](https://badge.waffle.io/timotree3/battleship.png?label=ready&title=Ready)](https://waffle.io/timotree3/battleship)

# TimoTree's Battleship

A text-based free software battleship game. (Mostly for my own learning)

## Description

The game is a Python3 script that reads the `config.json` file for configuration options. It uses ANSI escape codes for coloring text and moving the cursor which are not supported by many old terminals.

You play against a computer controlled bot.

## Gameplay

* The game starts by letting you place your ships.
* After all ships are placed you take turns blindly attacking eachother's sides.
* If you guess a spot correctly that spot on the enemy ship becomes hit.
* If every spot on a ship has been hit the ship sinks.
* The game ends when a player's last ship sinks.

### Example screen

```
                         === TimoTree Battleship ===

            Enemy Fleet                               Your Fleet

          A B C D E F G H I J                     A B C D E F G H I J
        0 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~      Legend:      0 # ~ ~ ~ ~ ~ ~ ~ ~ #
        1 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~     ~ - Empty     1 # ~ ~ ~ ~ ~ ~ ~ ~ #
        2 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~     O - Miss      2 ~ ~ ~ # # # # ~ ~ #
        3 ~ ~ X X ~ ~ ~ ~ ~ ~     # - Ship      3 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        4 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~     X - Hit       4 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        5 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~                   5 ~ ~ ~ ~ ~ O ~ ~ ~ ~
        6 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~                   6 O ~ ~ ~ ~ ~ ~ ~ ~ ~
        7 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~                   7 ~ ~ ~ ~ ~ ~ ~ ~ ~ #
        8 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~                   8 ~ ~ ~ # # # # # ~ #
        9 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~                   9 ~ ~ ~ ~ ~ ~ ~ ~ ~ #

It is your turn.
Attack a cell: _
Example inputs: (A, 0,| 0, a | a 0)
                                   History:
                                   F5: Miss
                                   D3: Hit
                                   A6: Miss
```

#### *Come play with us!*


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

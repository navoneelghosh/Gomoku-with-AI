# Gomoku-with-AI
 
Gomoku with AI is an simple terminal based implmentation of an AI for the game of Gomoku.
Gomoku is basically a bigger version of tic-tac-toe with modified rules.

The AI uses the concept of *minimax with alpha-beta pruning* to calculate the next move based on the player's last move.

To achieve this, the threat level of 16 scenarios were considered and scored based on their likeliness to win.

The following are the scenarios considered and the weightage given to each –
* "11111": 150000,
* "011110": 15000,
* "011100": 3000,
* "001110": 3000,
* "011010": 3000,
* "010110": 3000,
* "11110": 3000,
* "01111": 3000,
* "11011": 3000,
* "10111": 3000,
* "11101": 3000,
* "001100": 200,
* "001010": 200,
* "010100": 200,
* "000100": 20,
* "001000": 20
Here, each 1 in the string represents a cell filled with the same checker (either X or O) in board. For example, **“11111”** represents a **fiveInARow** and effectively indicates a winning scenario. **“011110”** represents a **twoWayOpenFourInARow** and indicates the highest to be won threat level. Similarly, the others are also weighted according to their threat level.

The way the AI is designed is that it will prioritize **“Attacking”** till it finds a 3000-level threat, at which point, it will switch to **“Defense”** and will block the opponent from winning.

**Execution Instructions -** 
To run the program, run pa2_process.py
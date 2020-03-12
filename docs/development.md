# Developing AIs for xi

AIs in xi are python classes with some minimum requirements:

* The AI name must be used in the file (e.g. headless.py)
* The class name in that file must be `ai`
* Class must contain a move function. 
  * Accepts a board parameter (2D array containing the piece names)
  * Returns a tuple or a list containing the coordinates of the piece to move and the coordinates to which that piece will be moved, or coordinates to spawn a san in 
* The class should have name, author and comment variables

### Tools

The skeleton.py file contains the basic structure of a xi AI.

There are some tools available in the lib directory, which can be used importing those modules in the IA module.

* Analysis
  * checkgame(board) -> Returns 1 if black has won, -1 if white has won and 0 if the game is ongoing
  * possible_moves(board, colour) -> list with tuples containing coordinates to which that piece can move
  * getpiece(board, coordinates) -> content of the board in coordinates
  * checklegal(board, move, colour) -> Checks if a move is legal for a given player
  * getpieces(board, colour) -> Returns a list of coordinates for all the pieces of the player
  * homerow(board, colour) -> Returns the home row of a player

* Move
  * move(board, move, colour) -> Returns the board after a move is played
  * movepiece(board, a, b) -> Returns the board after whatever is in a is moved to B
  * spawnsan(board, coords, colour) -> Spawns a san in those coordinates
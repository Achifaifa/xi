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

* Move
  * possible_moves(board, colour) -> list with tuples containing coordinates to which that piece can move
  * get_piece(board, coordinates) -> content of the board in coordinates

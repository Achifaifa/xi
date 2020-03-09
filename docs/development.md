# Developing AIs for xi

AIs in xi are python classes with some minimum requirements:

* The AI name must be used in the file (e.g. headless.py)
* The class name in that file must be `ai`
* Class must contain a move function. This must accept a board (2D array containing the piece names) and must return a tuple or a list containing the coordinates of the piece to move and the coordinates to which that piece will be moved. 

Recommended things:

* The class should have name, author and comment variables (Not mandatory)

### Tools

The skeleton.py file contains the basic structure of a xi AI.

There are some tools available in the lib directory, which can be used importing those modules in the IA module.

* Move
  * possible moves(board, colour) -> list with tuples containing coordinates to which that piece can move

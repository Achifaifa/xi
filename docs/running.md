# Running xi

The following modes are supported

### Human vs Human

Simply launch `xi`  and play using the mouse. Touchscreens may or may not be supported.

### Human vs AI

To play manually against an AI, use the -b or -w options (To select an AI for black or white). The parameter must be the name of one or the modules in the `ai` folder. 

For example, `./xi -b headless`. In this case, the AI will move first and will wait for the player after each move

### AI vs AI

Similar to human VS human, but selecting AIs for both sides (e.g. `xi -b headless -w headless`)

Some extra options are available in this mode:

* -n: number of matches (e.g. -n 100). The two AIs will play one match, swap colours, play another match and so on until all the matches have been played. At the end, a count of victories on each side will be displayed. If this is not specified it'll default to 1 and will show the moves on a board.
* -p: pause after each AI move in ms (e.g. -p 50). Makes displayed AI vs AI matches easier to see. This option is ignored if -n is 1 or if it's not specified.
* -l: limit number of moves. If the match has not been decided after this many moves, it's declared a draw.

### Other tools

* use -d to display debug information

# Running xi

## Dependencies

 * Python
 * Pygame

## Supported game modes

### Human vs Human

Launch `xi` and play using the mouse. Touchscreens may or may not be supported.

### Human vs AI

To play manually against an AI, use the -b or -w options (To select an AI for black or white). The parameter must be the name of one or the modules in the `ai` folder. 

For example, `./xi -b headless`. In this case, the AI will move first and will wait for the player after each move

### AI vs AI

Similar to human VS human, but selecting AIs for both sides (e.g. `xi -b headless -w headless`)

Some extra options are available in this mode (See 'options and parameters' below)

### Network play

To play over a network, use the `-s` option (to create a server) or the `-c <ip>` option (to connect to a server). 

The server will play as black and the client will play as white. Bots are compatible with this mode to be able to play against other bots without having to swap code, dependencies, etc. 

For example, `./xi -b headless -s` will create a server that plays automatically using the headless AI.

## Options and parameters

* use --help to display a full list

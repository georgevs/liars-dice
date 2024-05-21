# Liar's dice

https://strypes.eu/careers/liars-dice/


### Rules

THE GAME:
- the game is played by two or more players (including the user);
- each player starts the game with five dice;
- the game is played in multiple rounds;
- each round a player is declared looser and drops a dice;
- a player who looses all dice drops the game, and does not participate in the remaining rounds;
- last standing player is the game winner;
- all players may start a new game.

THE PLAYERS ORDER:
- players take turn clockwise (aka stable order) during the whole game;
- any player can be the starting player in the first round;
- if still in the game the looser starts the next round;
- if the looser drops the game the next round is started by the next in order player still in the game.

THE ROUND:
- at the beginning of the round each participating player rolls a hand and keeps it secret;
- the starting player can only place a bet;
- at their turn a player may either place a higher bet or challenge the current bet;
- the round ends when a challenge is placed, at which point all hands are revealed and the current bet is verified.
- if the bet is valid the challenger looses, otherwise the player who placed the bet looses.

THE BET:
- A bet has a claim on at least certain count of a certain die face;
- A bet is higher than another bet if the count is greater or else the face is greater;
- A bet is valid against a set of hands if the hands contain in total no less than the claimed count of the claimed die face;
- (Optional) In "wild" mode the "ones" face counts as the face of the current bid.


### High level design

THE APP:
- The number of players and "wild" mode may be confgured through the command line.

THE UI:
- A pluggable UI object implements the interface of the app with the user.

THE GAME:
- A Game object sets up the players and ensures the rules;
- At the game level the Game object keeps track of the remaining players;
- At the round level the Game object keeps track of the round history, and settles the challenge;
- Each round a new Round object is created with the remaining participating players.

THE PLAYERS:
- A Player base class represents the actions and properties of a player in the game;
- Player instances can be either the User or a Bot;
- The User Player actions consult the UI to get the user choice of actions;
- A Bot object is instantiated with a Strategy to simulate a player choice of actions;
- A Players adapter implements the order rules.

THE STRATEGY:
- Multiple strategies may be implemented for the app;
- A Strategy gains access to the associated Bot hand at the beginning of the round;
- A Strategy can consult the round history and the hand to advise the next action;
- A Strategy may have state to simulate more complicated logic through the Game.

DECISION COMPROMISES:
- For simplicity Python syntax is kept to bare minimum, no typing etc;
- Only single dumb strategy is implemented.

POSSIBLE IMPROVEMENTS:
- Implement acceptance tests via log analysis over scripted Game;
- Implement more sophisticated strategies;
- Better UI or GUI;
- Experiment with learning in strategies. Persist strategies.


### Run
PLAY:
```bash
python3 app/liars_dice.py \
  --bot-level 2 \
  --bots-count 1 \
  --show-bots-capabilities \
  --show-hands-at-settlement \
  --wild-mode
```
OBSERVE:
```bash
python3 app/liars_dice.py \
  --bot-level 2 \
  --show-hands-at-settlement \
  --wild-mode \
  --no-user
```

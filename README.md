# Board Games URAP Project :game_die:
=============================
This repository contains models of board games for an undergraduate research project started in Fall 2015, carried out under the direction and supervision of Falk Lieder and Tom Griffiths of the [Computational Cognitive Science Lab](http://cocosci.berkeley.edu/) at UC Berkeley.

## Games List
--------------
The 10 games selected for analysis based on ratings pulled from this [database](https://github.com/rasmusgreve/BoardGameGeek). The relevant files for each game are also listed.

1. Peg Solitaire (`peg_solitaire.py` `peg_markov.py`)
2. Solitaire/Patience
3. Wolfpack
4. Jasper and Zot
5. Legions of Darkness
6. B-29 Superfortress
7. Field Commander: Napoleon
8. Steel Wolves: The German Submarine Campaign Against Allied Shipping
9. Where There is Discord: War in the South Atlantic
10. Thunderbolt Apache Leader

A model of a 2x2 game of Tic-Tac-Toe is also included in this repository as a bonus. (`TicTacToe.py` `Markov.py`)

## Other Dependencies
----------------------
Besides downloading the relevant files for the game, you will also need NumPy ver1.9 or later.
It is recommended that you download it as part of the [Anaconda](https://www.continuum.io/downloads) package to ensure that further instructions work for you.

## Playing a Game
------------------
To run any file in interactive mode, use the command `python -i` followed by the name of the file.
Once you are running the main game file (the file that doesn't have "markov" in the title) in interactive mode, type in `play()` hit Enter and enjoy. Refer to code comments for further instructions on how to run learning algorithms on our models.

### URAP Apprentices
---------------------
* Fall 2015 - present: Priyam D., Jackie D., David L.



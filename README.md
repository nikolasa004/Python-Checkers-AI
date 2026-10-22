# Checkers - Python & Pygame

A small checkers game I made in Python with Pygame for a university algorithms project. Instead of building another console-only implementation, I wanted to turn what I was learning about game trees into an actual game - complete with an interface, animated pieces, and a computer opponent.

The code is definitely a little chaotic in places. A lot of the gameplay and AI logic ended up in one file, and some of the decisions I made back then were more experimental than elegant. I've kept that original character, with a few fixes to the simulation of moves and captures.

## Gameplay video

**[Watch a full gameplay showcase on YouTube](https://youtu.be/GvHHJIiKhBw)**

I should probably mention that I'm not especially good at checkers myself, as some of my moves in the video make pretty clear. But the important thing is that the AI apparently knows how to play - even if I don't. :D

## Screenshots

These are screenshots from the actual game, including the starting position, highlighted moves and captures, a promoted king, and the end-of-game screen.

| Starting board | Capture opportunity |
| :---: | :---: |
| ![Initial checkers board with red and gray pieces](docs/images/Screenshot%202026-10-22%20183532.png) | ![Mid-game board with a highlighted capture destination](docs/images/Screenshot%202026-10-22%20183601.png) |
| **Highlighted moves** | **King promotion opportunity** |
| ![Available moves highlighted in green on the board](docs/images/Screenshot%202026-10-22%20183642.png) | ![Possible king promotion squares highlighted in yellow](docs/images/Screenshot%202026-10-22%20183718.png) |
| **Possible jump** | **Victory screen** |
| ![Possible capture jumps highlighted in red](docs/images/Screenshot%202026-10-22%20184459.png) | ![Green victory screen offering to play again](docs/images/Screenshot%202026-10-22%20184606.png) |

## Features

- Play against a computer-controlled opponent on an 8×8 board.
- Choose at the start whether capturing an opponent's piece is mandatory.
- Select a piece to see available moves and capture destinations highlighted on the board.
- Capture opposing pieces, including sequences with multiple jumps.
- Promote pieces to **kings** when they reach the opposite side.
- Watch animated piece movements and use the end-of-game screen to start another match.
- Play against an AI that uses a **depth-limited Minimax search**, a hand-written heuristic, and pruning of parts of the search tree.
- Reuse some previously calculated positions through two small state-cache files, one for each capture-rule setting.

## How the AI works

The computer generates possible future positions in a game tree, evaluates them, and selects a move with the best available score. Its evaluation considers the remaining pieces, kings, board position, and possible captures. I also experimented with pruning and saving previously encountered states to avoid repeating some calculations.

The default search depth is **2 or 3**, depending on the relative number of pieces. This was a practical compromise: deeper searches take much longer, and the AI is not particularly strong even when it looks further ahead. It is an educational game AI, not a competitive checkers engine.

One issue with my original implementation was that different branches of the search tree could accidentally share mutable piece state. I later corrected the copying of logical board states and the handling of multi-capture information, without replacing the original Minimax approach or heuristic.

## How to run

The game was developed primarily for **Windows** and requires Python 3.

Clone or download the repository, open a terminal in its **root folder**, and install the dependencies:

```powershell
py -m pip install -r docs/requirements.txt
```

Then launch the game:

```powershell
py "Projekat dame/Grafika.py"
```

At the beginning of a match, choose whether captures are mandatory. Use the mouse to select one of your **gray pieces**, then click one of the highlighted destinations. The game menus and messages are in Serbian.

The dependencies are `pygame-ce` (imported in Python as `pygame`) and `tabulate` (used for console/debug output).

> **Compatibility:** The original game still uses Windows-style asset paths and some filename capitalization differs. Running it on macOS or Linux may require updating those paths to use `os.path.join()` or `pathlib` and matching the asset filenames exactly.

## Repository structure

```text
Python-Checkers-AI/
├── Projekat dame/
│   ├── Grafika.py                    # Gameplay, visuals, and AI search
│   ├── Stablo.py                     # Game-tree structures
│   ├── Konzola.py                    # Console/debug helper
│   ├── StanjaMoraJedenje.txt         # Cached positions: mandatory captures
│   ├── StanjaNeMoraJedenje.txt       # Cached positions: optional captures
│   ├── Slike/                        # Sprites and Piskel source files
│   └── Font/                         # Font used by the game
├── docs/
│   ├── images/                       # Gameplay screenshots
│   └── requirements.txt
├── .gitignore
└── README.md
```

The two `Stanja...txt` files belong beside `Grafika.py`, since the game loads saved positions from them. Depending on how you exit, the program can update these files with newly cached positions.

## Notes and credits

This is an old learning project that I wanted to preserve rather than completely rewrite. It demonstrates how I approached AI decision-making, recursion, and game-state management at the time, including some of the trade-offs and mistakes along the way.

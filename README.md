# Color Wars

Color Wars is a turn-based strategy game built with Python and Pygame.
Players place and upgrade cells, trigger chain explosions, and convert adjacent enemy cells to control the board.

The project supports both local PvP and PvE (vs AI) with multiple bot difficulties.

## Highlights

- Turn-based tactical gameplay on a 5x5 board.
- Chain-reaction explosion system.
- Territory conversion mechanics after each explosion.
- Two game modes:
  - `PVP`: human vs human (same device).
  - `PVBOT`: human (Blue) vs AI (Red).
- Three AI levels:
  - `Easy`: simple one-step evaluation.
  - `Medium`: weighted heuristic + probabilistic top-move selection.
  - `Hard`: iterative deepening + alpha-beta search.
- Responsive board rendering and fullscreen toggle.
- Explosion animation overlay for better move readability.

## Core Rules

- A move is valid only on:
  - an empty cell if the player has no owned cells yet (first entry move), or
  - one of the player's own cells afterward.
- Dot increment:
  - empty cell capture: `+3`
  - reinforce owned cell: `+1`
- Explosion threshold: `4`
  - when a cell reaches threshold, it explodes,
  - spreads dots to 4 orthogonal neighbors,
  - converts neighbors to the exploding player's color,
  - can trigger chain reactions.

## Win Condition

A player wins when they fully dominate the board, or when the opponent has been eliminated after previously entering the game.

## Project Structure

- `src/main.py`: application entry point.
- `src/game/state.py`: mutable runtime game state.
- `src/game/loop.py`: event loop, turn flow, AI turn handling, render loop.
- `src/controller.py`: move application, score calculation, winner update.
- `src/engine/rules.py`: shared game rules/constants.
- `src/engine/explosion.py`: BFS-based chain explosion resolver.
- `src/ai/ai.py`: AI difficulty dispatcher.
- `src/ai/ez_AI.py`: easy bot.
- `src/ai/med_AI.py`: medium bot.
- `src/ai/hard_AI.py`: hard bot.
- `src/view.py`: rendering, HUD, board layout, click mapping, FX overlay.
- `tests/`: unit tests for rules, explosion logic, and AI routing/validity.

## Requirements

- Python 3.10+
- See `requirements.txt` for runtime dependency installation.

## Installation

```bash
pip install -r requirements.txt
```

## Run Game

```bash
python -m src.main
```

## Controls

- Left Click: place/reinforce on a valid cell.
- `M`: toggle `PVP` / `PVBOT`.
- `R`: restart current match.
- `1` / `2` / `3`: set AI difficulty (`Easy` / `Medium` / `Hard`).
- `F11`: toggle fullscreen.

## Testing (Optional)

```bash
# On Windows PowerShell
$env:PYTHONPATH='.'; pytest -q
```

## Notes

- The runtime dependency is intentionally minimal for straightforward setup and play.
- AI and game rules share the same engine logic to keep behavior consistent.

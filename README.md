# Color Wars

Color Wars is a turn-based Pygame strategy game about placing dots, triggering chain explosions, and converting enemy territory on a 5×5 board. It supports local PvP and PvE matches with Easy, Medium, and Hard AI levels.

## Quick Start

### Requirements

- Python 3.10+
- Pygame 2.x

### Install

```bash
pip install -r requirements.txt
```

### Run

```bash
python -m src.main
```

### Test

```bash
pytest -v
```

## Controls

- Left Click: place or reinforce a valid cell
- M: toggle PvP / PvE mode
- R: restart the current match
- F11: toggle fullscreen
- Esc: go back or close overlays

## Gameplay Rules

- Empty cell capture adds 3 dots
- Reinforcing your own cell adds 1 dot
- A cell explodes at 4 dots
- Chain explosions convert adjacent cells to the exploding owner

## Project Structure

```text
asset/
  mp3/                  background music files
scripts/
  benchmark_ai.py       AI balance benchmark
src/
  main.py               application entrypoint
  controller.py         move application and win handling
  engine/               pure rules and explosion logic
  game/                 runtime state, loop, audio, analysis
  ai/                   difficulty-specific AI policies
  view/                 all Pygame rendering and UI
tests/
  ai/                   AI behavior tests
  game_logic/           rules and controller tests
  view/                 scene and HUD tests
```

## Architecture Notes

- The engine is pure and does not depend on Pygame surfaces.
- The controller owns state mutation and win detection.
- The view layer handles rendering only.
- AI reads board state and returns a move.

## AI Levels

- Easy: intentionally weak and beginner-friendly
- Medium: shallow heuristic search with light randomness
- Hard: alpha-beta search with evaluation and limited randomness

Run the AI benchmark with:

```bash
python scripts/benchmark_ai.py --games 200
```

## Screenshot

![Gameplay screenshot placeholder](docs/screenshot-placeholder.png)

## Notes

- Music, if present, is loaded from the first MP3 in `asset/mp3/`
- The game opens from the home menu first
- Tests are organized by subsystem for easier maintenance

## Testing (Optional)

```bash
# On Windows PowerShell
$env:PYTHONPATH='.'; pytest -q
```

## Additional Notes

- The runtime dependency is intentionally minimal for straightforward setup and play.
- AI and game rules share the same engine logic to keep behavior consistent.

# Leet Code Practice

This repository is my personal playground for chipping away at LeetCode concepts.
Each topic (binary search, graphs, trees, etc.) lives in its own directory, and
inside each topic there is a small language-specific workspace (right now only
Python).

## Quick start (CLI)

1. (Optional) Activate a virtual environment: `source .venv/bin/activate` or
   create your own with `python -m venv .venv`.
2. Pick a problem directory (for example `two_pointers/python`) and run a file,
   e.g. `python two-sum/python/solved/two-sum-solved.py`.
3. Update the matching markdown note in that folder with takeaways or edge cases.

## Launch the PyQt6 Learning Labs

Interactive views for the practice problems are available via PyQt6:
- From the repo root run `python launch_learning_labs.py`. The script is
  self-contained: it checks/installs PyQt6 and pyqtgraph, switches into the
  project directory, and then launches `pyqt6_learning_labs.main`.
- On macOS you can double-click or run `./launch.command`, which simply shells
  out to the same Python launcher.
- The app currently includes the Two Sum and Add Two Numbers exercises with
  helpers for visualizing inputs and outputs.

## Progress tracking

- `index.md` summarizes the status of each topic.
- Completed examples so far:
  - Add Two Numbers: `add-two-numbers/solved/add-two-nums-solved.py`
  - Two Sum: `two-sum/python/solved/two-sum-solved.py` plus practice variants

## Future improvements

- Fill in real solutions and notes for every topic.
- Add lightweight test cases per pattern for quick regression checks.
- Expand beyond Python once the core problem set is complete.

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

  <img width="1191" height="793" alt="Screenshot 2025-11-25 at 1 30 54 AM" src="https://github.com/user-attachments/assets/1eca12bc-8cc7-4e70-ba36-8d074e89e178" />
  
<img width="1191" height="793" alt="Screenshot 2025-11-25 at 1 32 02 AM" src="https://github.com/user-attachments/assets/0a0695b6-3236-4238-8951-30b25fdacad7" />

<img width="1191" height="793" alt="Screenshot 2025-11-25 at 1 32 15 AM" src="https://github.com/user-attachments/assets/7066eec9-9301-4339-93ae-28ef2d496d5e" />

<img width="1191" height="793" alt="Screenshot 2025-11-25 at 1 32 34 AM" src="https://github.com/user-attachments/assets/f09dac69-409c-4062-b91e-340c5d20318a" />

<img width="1191" height="793" alt="Screenshot 2025-11-25 at 1 32 44 AM" src="https://github.com/user-attachments/assets/1b1abe8f-484b-4beb-abce-9d0b6310cdcc" />

<img width="1191" height="793" alt="Screenshot 2025-11-25 at 1 32 56 AM" src="https://github.com/user-attachments/assets/0c0a78a6-582b-4ed7-b314-246a0f6cb3bb" />


## Progress tracking

- `index.md` summarizes the status of each topic.
- Completed examples so far:
  - Add Two Numbers: `add-two-numbers/solved/add-two-nums-solved.py`
  - Two Sum: `two-sum/python/solved/two-sum-solved.py` plus practice variants

## Future improvements

- Fill in real solutions and notes for every topic.
- Add lightweight test cases per pattern for quick regression checks.
- Expand beyond Python once the core problem set is complete.

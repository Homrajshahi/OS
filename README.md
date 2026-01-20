# Mini OS Simulator

A clean, terminal-inspired GUI application built with **Python & Tkinter** to simulate core **Operating System concepts** for educational purposes (5th Semester OS Mini Project).

> ⚠️ This is **not a real operating system** — it's an educational simulation tool.

## Features

- **CPU Scheduling**  
  Visualizes FCFS, SJF, Priority, and Round Robin algorithms  
  Gantt chart, waiting time, turnaround time, average stats

- **Disk Scheduling**  
  Implements FCFS, SSTF, SCAN, LOOK, C-SCAN  
  Head movement visualization, total/average seek time, algorithm comparison table

- Dark GitHub-inspired theme with consistent UI  
- Modular design: each module loads as an embeddable panel  
- Welcome screen with quick access cards  
- Sidebar navigation + Home button

## Technologies Used

- Python 3.x  
- Tkinter (standard GUI library)  
- No external dependencies required

## Project Structure
MiniOS/
├── main.py                # Main launcher + sidebar + welcome screen
├── theme.py               # Shared colors & fonts
├── cpu_scheduling.py      # CPU Scheduling module
├── disk_scheduling.py     # Disk Scheduling module
├── requirements.txt       # (optional - empty or comments only)
└── README.md              # This file


## How to Run

1. Clone or download the project
2. Open terminal in the project folder
3. Run the simulator

```bash
python main.py

Optional: Run individual modules standalone for testing

python cpu_scheduling.py
python disk_scheduling.py

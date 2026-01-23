```markdown
# Mini OS Simulator

A clean, terminal-inspired GUI application built with **Python & Tkinter** to simulate core **Operating System concepts** for educational purposes (5th Semester OS Mini Project).

> This is **not a real operating system** — it's an educational simulation tool.

## Features

- **CPU Scheduling**  
  Visualizes FCFS, SJF, Priority, and Round Robin algorithms  
  Gantt chart, waiting time, turnaround time, average stats

- **Memory Management**  
  Implements First Fit, Best Fit, and Worst Fit allocation  
  Memory block visualization, allocation table, fragmentation stats

- **Disk Scheduling**  
  Implements FCFS, SSTF, SCAN, LOOK, C-SCAN  
  Head movement visualization, total/average seek time, algorithm comparison

- **File Management**  
  Simulates basic file system operations: create file/directory, delete, navigate, view attributes  
  Treeview listing, path bar, disk usage percentage, terminal-style log

- Dark GitHub-inspired theme with consistent UI across all modules  
- Modular design: each module loads as an embeddable panel  
- Welcome screen with quick access cards  
- Sidebar navigation + Home button

## Technologies Used

- Python 3.8+  
- Tkinter (standard GUI library)  
- No external packages required

## Project Structure

```
MiniOS/
├── main.py                # Main launcher + sidebar + welcome screen
├── theme.py               # Shared colors & fonts
├── cpu_scheduling.py      # CPU Scheduling module
├── memory_management.py   # Memory Management module
├── disk_scheduling.py     # Disk Scheduling module
├── file_management.py     # File Management module
├── requirements.txt       # (optional - currently empty)
└── README.md              # This file
```

## How to Run the Project (Windows / Linux / macOS)

### Prerequisites (All Platforms)

- You need **Python 3.8 or higher** installed.
- Tkinter is included with Python on Windows and macOS.  
  On most Linux distributions, you may need to install it separately (very easy).

### Step 1: Download the Project

1. Go to: https://github.com/homrajshahi/OS
2. Click green **Code** button → **Download ZIP**
3. Extract the ZIP file to any folder (e.g. Desktop → MiniOS)

**Alternative (if you know Git):**

```bash
git clone https://github.com/homrajshahi/OS.git
cd OS
```

### Step 2: Install Python (if not already installed)

**Windows**  
- Download from: https://www.python.org/downloads/  
- During installation: **check** "Add Python to PATH"  
- After install, open Command Prompt and type: `python --version` (should show 3.8+)

**Linux (Ubuntu/Debian/Mint)**  
```bash
sudo apt update
sudo apt install python3 python3-tk
```

**macOS**  
- Usually already has Python (but older version)  
- Recommended: Install latest from https://www.python.org/downloads/macos/  
- Or use Homebrew:  
  ```bash
  brew install python-tk
  ```

### Step 3: Install Tkinter (only if needed on Linux)

**Ubuntu/Debian/Mint**:
```bash
sudo apt install python3-tk
```

**Fedora**:
```bash
sudo dnf install python3-tkinter
```

**Arch/Manjaro**:
```bash
sudo pacman -S tk
```

**Windows & macOS**: Tkinter is already included — no action needed.

### Step 4: Run the Project

Open a terminal / command prompt / PowerShell in the project folder (where `main.py` is located).

**Windows** (Command Prompt or PowerShell):
```cmd
python main.py
```

**Linux / macOS** (Terminal):
```bash
python3 main.py
```

**If you see error "python: command not found"**:
- Use full path or make sure Python is in PATH
- Try: `py main.py` (Windows) or `python3.11 main.py` (if you have multiple versions)

### Step 5: Using the Simulator

1. The app opens with a welcome screen and sidebar
2. Click any module name (CPU Scheduling, Memory Management, etc.)  
   or click "Open" on the cards in the welcome screen
3. Inside each module:
   - Add data (processes, blocks, requests, files) using inputs or "Random" button
   - Select algorithm (if any)
   - Click "Run Simulation" / "Allocate Memory" / etc.
   - See visualization (Gantt chart, memory blocks, disk path, file tree)
4. Click **⌂ Home** (top right) to return to welcome screen

## Troubleshooting

| Problem                              | Solution |
|--------------------------------------|------------------------------------------------|
| "No module named 'tkinter'"          | Install python3-tk (Linux) or reinstall Python with    Tkinter (Windows/macOS) |
| "python: command not found"          | Install Python or use `python3` / `py` |
| Module not loading (import error)    | Make sure all .py files are in the same folder as main.py |
| Window looks broken / colors wrong   | Make sure theme.py is present and not renamed |

## Screenshots

(Add later in `screenshots/` folder)

- Welcome Screen  
  ![Welcome](screenshots/welcome.png)

- CPU Scheduling  
  ![CPU](screenshots/cpu.png)

- Memory Management  
  ![Memory](screenshots/memory.png)

- Disk Scheduling  
  ![Disk](screenshots/disk.png)

- File Management  
  ![File](screenshots/file.png)

## License

Educational use only. Feel free to fork, modify, and learn from it!

Made with ❤️ for OS course
```

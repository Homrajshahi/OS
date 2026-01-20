# modules/cpu_scheduling.py
"""
CPU Scheduling Module – Complete basic version with FCFS
"""

import tkinter as tk
from tkinter import ttk, messagebox
from theme import Theme

class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst
        self.start_time = -1
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0


class CPUScheduler:
    @staticmethod
    def fcfs(processes):
        # Sort by arrival time, then by PID
        sorted_processes = sorted(processes, key=lambda p: (p.arrival, int(p.pid[1:])))
        time = 0
        gantt = []

        for p in sorted_processes:
            if time < p.arrival:
                gantt.append(('idle', time, p.arrival))
                time = p.arrival
            p.start_time = time
            gantt.append((p.pid, time, time + p.burst))
            time += p.burst
            p.finish_time = time
            p.turnaround_time = p.finish_time - p.arrival
            p.waiting_time = p.turnaround_time - p.burst

        return sorted_processes, gantt


class CPUSchedulingGUI:
    def __init__(self, parent):
        self.parent = parent
        self.processes = []
        self.counter = 1
        self.setup_ui()

    def setup_ui(self):
        main = tk.Frame(self.parent, bg=Theme.BG_DARK)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        tk.Label(main, text="CPU Scheduling", font=Theme.FONT_TITLE,
                 bg=Theme.BG_DARK, fg=Theme.ACCENT).pack(anchor='w', pady=(0, 10))

        tk.Label(main, text="FCFS – First Come First Serve", font=Theme.FONT,
                 bg=Theme.BG_DARK, fg=Theme.TEXT_DIM).pack(anchor='w')

        # Input section
        input_frame = tk.Frame(main, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        input_frame.pack(fill=tk.X, pady=10)

        tk.Label(input_frame, text="Arrival Time:", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT)
        self.arrival_entry = tk.Entry(input_frame, width=10, font=Theme.FONT,
                                      bg=Theme.BG_INPUT, fg=Theme.TEXT)
        self.arrival_entry.pack(side=tk.LEFT, padx=5)
        self.arrival_entry.insert(0, "0")

        tk.Label(input_frame, text="Burst Time:", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT, padx=(20, 0))
        self.burst_entry = tk.Entry(input_frame, width=10, font=Theme.FONT,
                                    bg=Theme.BG_INPUT, fg=Theme.TEXT)
        self.burst_entry.pack(side=tk.LEFT, padx=5)
        self.burst_entry.insert(0, "5")

        tk.Button(input_frame, text="+ Add Process", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.ACCENT, bd=0,
                  padx=12, pady=5, cursor='hand2',
                  command=self.add_process).pack(side=tk.LEFT, padx=10)

        # Process list
        self.process_frame = tk.Frame(main, bg=Theme.BG_DARK)
        self.process_frame.pack(fill=tk.X, pady=10)
        self.update_process_list()

        # Run button
        tk.Button(main, text="Run FCFS", font=Theme.FONT_BOLD,
                  bg=Theme.ACCENT, fg=Theme.BG_DARK, bd=0,
                  padx=20, pady=8, cursor='hand2',
                  command=self.run_fcfs).pack(pady=10)

        # Gantt placeholder
        self.gantt_label = tk.Label(main, text="Gantt chart will appear here",
                                    font=Theme.FONT, bg=Theme.BG_DARK, fg=Theme.TEXT_DIM)
        self.gantt_label.pack(pady=20)

    def add_process(self):
        try:
            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            if burst <= 0:
                raise ValueError("Burst must be > 0")

            p = Process(f"P{self.counter}", arrival, burst)
            self.processes.append(p)
            self.counter += 1
            self.update_process_list()
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.arrival_entry.insert(0, "0")
            self.burst_entry.insert(0, "5")

        except ValueError as e:
            messagebox.showerror("Error", str(e) or "Enter valid numbers")

    def update_process_list(self):
        for widget in self.process_frame.winfo_children():
            widget.destroy()

        if not self.processes:
            tk.Label(self.process_frame, text="No processes added yet",
                     font=Theme.FONT_SMALL, bg=Theme.BG_DARK, fg=Theme.TEXT_DIM).pack()
            return

        for p in self.processes:
            tk.Label(self.process_frame,
                     text=f"{p.pid}  Arrival: {p.arrival}  Burst: {p.burst}",
                     font=Theme.FONT, bg=Theme.BG_DARK, fg=Theme.TEXT).pack(anchor='w')

    def run_fcfs(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Add at least one process first")
            return

        _, gantt = CPUScheduler.fcfs(self.processes)

        # Simple text Gantt for now
        gantt_text = "Gantt: "
        for item in gantt:
            pid, start, end = item
            gantt_text += f"{pid}({start}-{end}) → "

        self.gantt_label.config(text=gantt_text.rstrip(" → "))


def open_cpu(parent_frame):
    CPUSchedulingGUI(parent_frame)


# Standalone test
if __name__ == "__main__":
    root = tk.Tk()
    root.title("CPU Scheduling – Standalone")
    root.geometry("1000x700")
    root.configure(bg=Theme.BG_DARK)
    CPUSchedulingGUI(root)
    root.mainloop()
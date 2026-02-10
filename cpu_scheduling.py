import tkinter as tk
from tkinter import ttk, messagebox
from theme import Theme
import random

class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst
        self.start_time = -1
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

class CPUScheduler:
    @staticmethod
    def fcfs(processes):
        sorted_p = sorted(processes, key=lambda p: (p.arrival, int(p.pid[1:])))
        time = 0
        gantt = []
        for p in sorted_p:
            if time < p.arrival:
                gantt.append(('idle', time, p.arrival))
                time = p.arrival
            p.start_time = time
            gantt.append((p.pid, time, time + p.burst))
            time += p.burst
            p.completion_time = time
            p.turnaround_time = p.completion_time - p.arrival
            p.waiting_time = p.turnaround_time - p.burst
        return sorted_p, gantt

    @staticmethod
    def sjf(processes):
        sorted_p = sorted(processes, key=lambda p: (p.arrival, p.burst, int(p.pid[1:])))
        time = 0
        gantt = []
        completed = 0
        while completed < len(sorted_p):
            available = [p for p in sorted_p if p.arrival <= time and p.remaining > 0]
            if not available:
                next_arr = min((p.arrival for p in sorted_p if p.remaining > 0), default=time)
                gantt.append(('idle', time, next_arr))
                time = next_arr
                continue
            current = min(available, key=lambda p: p.burst)
            if current.start_time == -1:
                current.start_time = time
            gantt.append((current.pid, time, time + current.burst))
            time += current.burst
            current.remaining = 0
            current.completion_time = time
            current.turnaround_time = current.completion_time - current.arrival
            current.waiting_time = current.turnaround_time - current.burst
            completed += 1
        return sorted_p, gantt

    @staticmethod
    def priority(processes):
        sorted_p = sorted(processes, key=lambda p: (p.arrival, p.priority, int(p.pid[1:])))
        time = 0
        gantt = []
        completed = 0
        while completed < len(sorted_p):
            available = [p for p in sorted_p if p.arrival <= time and p.remaining > 0]
            if not available:
                next_arr = min((p.arrival for p in sorted_p if p.remaining > 0), default=time)
                gantt.append(('idle', time, next_arr))
                time = next_arr
                continue
            current = min(available, key=lambda p: p.priority)
            if current.start_time == -1:
                current.start_time = time
            gantt.append((current.pid, time, time + current.burst))
            time += current.burst
            current.remaining = 0
            current.completion_time = time
            current.turnaround_time = current.completion_time - current.arrival
            current.waiting_time = current.turnaround_time - current.burst
            completed += 1
        return sorted_p, gantt

    @staticmethod
    def round_robin(processes, quantum):
        queue = []
        time = 0
        gantt = []
        completed = 0
        n = len(processes)
        sorted_p = sorted(processes, key=lambda p: p.arrival)
        idx = 0
        while completed < n:
            while idx < n and sorted_p[idx].arrival <= time:
                queue.append(sorted_p[idx])
                idx += 1
            if not queue:
                if idx < n:
                    gantt.append(('idle', time, sorted_p[idx].arrival))
                    time = sorted_p[idx].arrival
                continue
            current = queue.pop(0)
            if current.start_time == -1:
                current.start_time = time
            exec_time = min(quantum, current.remaining)
            gantt.append((current.pid, time, time + exec_time))
            time += exec_time
            current.remaining -= exec_time
            while idx < n and sorted_p[idx].arrival <= time:
                queue.append(sorted_p[idx])
                idx += 1
            if current.remaining > 0:
                queue.append(current)
            else:
                current.completion_time = time
                current.turnaround_time = current.completion_time - current.arrival
                current.waiting_time = current.turnaround_time - current.burst
                completed += 1
        return sorted_p, gantt

class CPUSchedulingGUI:
    def __init__(self, parent):
        self.parent = parent
        self.processes = []
        self.counter = 1
        self.setup_ui()

    def setup_ui(self):
        # Outer container for scrolling
        outer = tk.Frame(self.parent, bg=Theme.BG_DARK)
        outer.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable canvas (no visible scrollbar)
        self.scroll_canvas = tk.Canvas(outer, bg=Theme.BG_DARK, highlightthickness=0)
        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Main content frame inside canvas
        main = tk.Frame(self.scroll_canvas, bg=Theme.BG_DARK)
        self.scroll_canvas.create_window((0, 0), window=main, anchor="nw", tags="main_frame")
        
        # Bind mouse wheel scrolling
        def on_mousewheel(event):
            self.scroll_canvas.yview_scroll(-1 * (event.delta // 120), "units")
        def on_scroll_up(event):
            self.scroll_canvas.yview_scroll(-1, "units")
        def on_scroll_down(event):
            self.scroll_canvas.yview_scroll(1, "units")
        
        self.scroll_canvas.bind("<MouseWheel>", on_mousewheel)
        self.scroll_canvas.bind("<Button-4>", on_scroll_up)
        self.scroll_canvas.bind("<Button-5>", on_scroll_down)
        
        def bind_scroll_to_children(widget):
            widget.bind("<MouseWheel>", on_mousewheel)
            widget.bind("<Button-4>", on_scroll_up)
            widget.bind("<Button-5>", on_scroll_down)
            for child in widget.winfo_children():
                bind_scroll_to_children(child)
        
        def update_scroll_region(event=None):
            self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
            self.scroll_canvas.itemconfig("main_frame", width=self.scroll_canvas.winfo_width())
            bind_scroll_to_children(main)
        
        main.bind("<Configure>", update_scroll_region)
        self.scroll_canvas.bind("<Configure>", lambda e: self.scroll_canvas.itemconfig("main_frame", width=e.width))

        # Add padding inside main
        content = tk.Frame(main, bg=Theme.BG_DARK)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(content, text="CPU Scheduling", font=Theme.FONT_TITLE,
                 bg=Theme.BG_DARK, fg=Theme.ACCENT).pack(anchor='w', pady=(0, 10))

        input_frame = tk.Frame(content, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        input_frame.pack(fill=tk.X, pady=10)

        labels = ["Arrival Time:", "Burst Time:", "Priority:"]
        self.entries = {}
        for label in labels:
            tk.Label(input_frame, text=label, font=Theme.FONT_SMALL,
                     bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT, padx=(0, 5))
            entry = tk.Entry(input_frame, width=10, font=Theme.FONT,
                             bg=Theme.BG_INPUT, fg=Theme.TEXT,
                             insertbackground=Theme.ACCENT)
            entry.pack(side=tk.LEFT, padx=5)
            entry.insert(0, "0")
            self.entries[label] = entry

        tk.Button(input_frame, text="+ Add Process", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.ACCENT, bd=0,
                  padx=12, pady=5, cursor='hand2',
                  command=self.add_process).pack(side=tk.LEFT, padx=10)

        tk.Button(input_frame, text="Random", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.TEXT, bd=0,
                  padx=12, pady=5, cursor='hand2',
                  command=self.generate_random).pack(side=tk.LEFT, padx=5)

        tk.Button(input_frame, text="Clear All", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.ERROR, bd=0,
                  padx=12, pady=5, cursor='hand2',
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)

        self.process_frame = tk.Frame(content, bg=Theme.BG_DARK)
        self.process_frame.pack(fill=tk.X, pady=10)
        self.update_process_list()

        algo_frame = tk.Frame(content, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        algo_frame.pack(fill=tk.X, pady=10)
        self.algo_var = tk.StringVar(value="FCFS")
        algorithms = ["FCFS", "SJF", "Priority", "Round Robin"]
        for algo in algorithms:
            tk.Radiobutton(algo_frame, text=algo, variable=self.algo_var, value=algo,
                           font=Theme.FONT, bg=Theme.BG_SECONDARY, fg=Theme.TEXT,
                           selectcolor=Theme.BG_TERTIARY).pack(side=tk.LEFT, padx=15)

        tk.Label(algo_frame, text="Quantum:", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT, padx=(30, 5))
        self.quantum_entry = tk.Entry(algo_frame, width=6, font=Theme.FONT,
                                      bg=Theme.BG_INPUT, fg=Theme.TEXT)
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.pack(side=tk.LEFT)

        tk.Button(algo_frame, text="Run Simulation", font=Theme.FONT_BOLD,
                  bg=Theme.ACCENT, fg=Theme.BG_DARK, bd=0,
                  padx=20, pady=8, cursor='hand2',
                  command=self.run_simulation).pack(side=tk.RIGHT, padx=10)

        # Gantt Chart
        self.gantt_canvas = tk.Canvas(content, height=100, bg=Theme.BG_DARK,
                                      highlightthickness=0)
        self.gantt_canvas.pack(fill=tk.X, pady=10)

        results_frame = tk.Frame(content, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        results_frame.pack(fill=tk.X)
        
        # Header and averages in a fixed row
        results_header = tk.Frame(results_frame, bg=Theme.BG_SECONDARY)
        results_header.pack(fill=tk.X)
        tk.Label(results_header, text="RESULTS", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT)
        
        # Average times - always visible on the right
        self.avg_label = tk.Label(results_header, text="", font=('Consolas', 11, 'bold'),
                                  bg=Theme.BG_DARK, fg=Theme.SUCCESS, padx=15, pady=5)
        self.avg_label.pack(side=tk.RIGHT, padx=10)

        # Scrollable results table
        results_container = tk.Frame(results_frame, bg=Theme.BG_DARK)
        results_container.pack(fill=tk.X, pady=(5, 0))
        
        self.results_body = tk.Frame(results_container, bg=Theme.BG_DARK)
        self.results_body.pack(fill=tk.X)

    def add_process(self):
        try:
            arrival = int(self.entries["Arrival Time:"].get())
            burst = int(self.entries["Burst Time:"].get())
            priority = int(self.entries["Priority:"].get())
            if burst <= 0:
                raise ValueError("Burst time must be positive")
            p = Process(f"P{self.counter}", arrival, burst, priority)
            self.processes.append(p)
            self.counter += 1
            self.update_process_list()
            for entry in self.entries.values():
                entry.delete(0, tk.END)
                entry.insert(0, "0")
        except ValueError as e:
            messagebox.showerror("Error", str(e) or "Enter valid numbers")

    def generate_random(self):
        self.clear_all()
        n = random.randint(4, 7)
        for i in range(n):
            arrival = random.randint(0, 10)
            burst = random.randint(2, 12)
            priority = random.randint(1, 5)
            p = Process(f"P{i+1}", arrival, burst, priority)
            self.processes.append(p)
        self.counter = n + 1
        self.update_process_list()

    def clear_all(self):
        self.processes = []
        self.counter = 1
        self.update_process_list()
        self.gantt_canvas.delete("all")
        for widget in self.results_body.winfo_children():
            widget.destroy()
        self.avg_label.config(text="")

    def update_process_list(self):
        for widget in self.process_frame.winfo_children():
            widget.destroy()
        if not self.processes:
            tk.Label(self.process_frame, text="No processes added yet",
                     font=Theme.FONT_SMALL, bg=Theme.BG_DARK, fg=Theme.TEXT_DIM).pack()
            return
        for p in self.processes:
            tk.Label(self.process_frame,
                     text=f"{p.pid}  Arrival: {p.arrival}  Burst: {p.burst}  Priority: {p.priority}",
                     font=Theme.FONT, bg=Theme.BG_DARK, fg=Theme.TEXT).pack(anchor='w')

    def run_simulation(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Add at least one process first")
            return

        algo = self.algo_var.get()
        if algo == "Round Robin":
            try:
                quantum = int(self.quantum_entry.get())
                if quantum <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Invalid quantum (must be positive integer)")
                return
            processes, gantt = CPUScheduler.round_robin([Process(p.pid, p.arrival, p.burst, p.priority) for p in self.processes], quantum)
        elif algo == "SJF":
            processes, gantt = CPUScheduler.sjf([Process(p.pid, p.arrival, p.burst, p.priority) for p in self.processes])
        elif algo == "Priority":
            processes, gantt = CPUScheduler.priority([Process(p.pid, p.arrival, p.burst, p.priority) for p in self.processes])
        else:  # FCFS
            processes, gantt = CPUScheduler.fcfs([Process(p.pid, p.arrival, p.burst, p.priority) for p in self.processes])

        self.draw_gantt(gantt)
        self.display_results(processes)

    def draw_gantt(self, gantt):
        self.gantt_canvas.delete("all")
        if not gantt:
            return

        canvas_width = self.gantt_canvas.winfo_width() - 40 or 900
        total_time = gantt[-1][2]
        scale = canvas_width / total_time if total_time > 0 else 1
        x_start = 20
        x = x_start
        y = 20
        height = 50

        colors = ['#00d4aa', '#3fb950', '#d29922', '#f85149', '#a371f7', '#79c0ff']

        for pid, start, end in gantt:
            width = (end - start) * scale
            if pid == 'idle':
                color = Theme.BG_TERTIARY
                self.gantt_canvas.create_rectangle(x, y, x + width, y + height,
                                                   fill=color, outline=Theme.BORDER)
                # Show process ID only
                self.gantt_canvas.create_text(x + width/2, y + height/2,
                                              text="IDLE", font=Theme.FONT_SMALL, 
                                              fill=Theme.TEXT_DIM, justify='center')
            else:
                color = colors[hash(pid) % len(colors)]
                self.gantt_canvas.create_rectangle(x, y, x + width, y + height,
                                                   fill=color, outline=Theme.BORDER)
                # Show process ID only
                self.gantt_canvas.create_text(x + width/2, y + height/2,
                                              text=pid, font=Theme.FONT_BOLD, 
                                              fill=Theme.BG_DARK, justify='center')
            x += width

        # Draw timeline ruler below the Gantt chart
        ruler_y = y + height + 5
        # Draw horizontal line
        self.gantt_canvas.create_line(x_start, ruler_y, x_start + canvas_width, ruler_y,
                                      fill=Theme.TEXT_DIM, width=1)
        
        # Calculate tick interval (show every 1, 2, or 5 units based on total time)
        if total_time <= 20:
            tick_interval = 1
        elif total_time <= 50:
            tick_interval = 2
        else:
            tick_interval = 5
        
        # Draw ticks and labels
        for t in range(0, total_time + 1, tick_interval):
            tick_x = x_start + t * scale
            # Draw tick mark
            self.gantt_canvas.create_line(tick_x, ruler_y, tick_x, ruler_y + 8,
                                          fill=Theme.TEXT_DIM, width=1)
            # Draw time label
            self.gantt_canvas.create_text(tick_x, ruler_y + 12, text=str(t),
                                          font=Theme.FONT_SMALL, fill=Theme.TEXT_DIM, anchor='n')
        
        # Always draw the final time if it's not on interval
        if total_time % tick_interval != 0:
            final_x = x_start + total_time * scale
            self.gantt_canvas.create_line(final_x, ruler_y, final_x, ruler_y + 8,
                                          fill=Theme.ACCENT, width=1)
            self.gantt_canvas.create_text(final_x, ruler_y + 12, text=str(total_time),
                                          font=Theme.FONT_SMALL, fill=Theme.ACCENT, anchor='n')

    def display_results(self, processes):
        for widget in self.results_body.winfo_children():
            widget.destroy()

        total_wt = 0
        total_tat = 0
        header = ["PID", "Arrival", "Burst", "Priority", "Completion", "Waiting", "Turnaround"]
        header_frame = tk.Frame(self.results_body, bg=Theme.BG_TERTIARY)
        header_frame.pack(fill=tk.X)
        for h in header:
            tk.Label(header_frame, text=h, font=Theme.FONT_BOLD,
                     bg=Theme.BG_TERTIARY, fg=Theme.ACCENT, width=12).pack(side=tk.LEFT)

        for p in processes:
            row = tk.Frame(self.results_body, bg=Theme.BG_DARK)
            row.pack(fill=tk.X)
            values = [p.pid, p.arrival, p.burst, p.priority, p.completion_time,
                      p.waiting_time, p.turnaround_time]
            for v in values:
                tk.Label(row, text=str(v), font=Theme.FONT,
                         bg=Theme.BG_DARK, fg=Theme.TEXT, width=12).pack(side=tk.LEFT)

            total_wt += p.waiting_time
            total_tat += p.turnaround_time

        n = len(processes)
        avg_wt = total_wt / n if n else 0
        avg_tat = total_tat / n if n else 0
        self.avg_label.config(text=f"Avg Waiting Time: {avg_wt:.2f} | Avg Turnaround Time: {avg_tat:.2f}")

def open_cpu(parent_frame):
    CPUSchedulingGUI(parent_frame)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CPU Scheduling – Standalone")
    root.geometry("1000x750")
    root.configure(bg=Theme.BG_DARK)
    CPUSchedulingGUI(root)
    root.mainloop()
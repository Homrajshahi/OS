"""
Disk Scheduling Module
Terminal-Inspired Minimal UI
Implements FCFS, SSTF, SCAN, LOOK, and C-SCAN algorithms
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random
from theme import Theme  # ← Import shared theme

class DiskScheduler:
    @staticmethod
    def fcfs(requests, head, disk_size=200):
        sequence = [head]
        total_seek = 0
        current = head
        for req in requests:
            total_seek += abs(req - current)
            current = req
            sequence.append(req)
        return sequence, total_seek

    @staticmethod
    def sstf(requests, head, disk_size=200):
        requests = requests.copy()
        sequence = [head]
        total_seek = 0
        current = head
        while requests:
            closest = min(requests, key=lambda x: abs(x - current))
            total_seek += abs(closest - current)
            current = closest
            sequence.append(closest)
            requests.remove(closest)
        return sequence, total_seek

    @staticmethod
    def scan(requests, head, disk_size=200, direction="right"):
        requests = sorted(requests)
        sequence = [head]
        total_seek = 0
        current = head
        left = [r for r in requests if r < head]
        right = [r for r in requests if r >= head]
        if direction == "right":
            for r in right:
                total_seek += abs(r - current)
                current = r
                sequence.append(r)
            if right and left:
                total_seek += abs(disk_size - 1 - current)
                current = disk_size - 1
                sequence.append(current)
            for r in reversed(left):
                total_seek += abs(r - current)
                current = r
                sequence.append(r)
        else:
            for r in reversed(left):
                total_seek += abs(r - current)
                current = r
                sequence.append(r)
            if left and right:
                total_seek += current
                current = 0
                sequence.append(current)
            for r in right:
                total_seek += abs(r - current)
                current = r
                sequence.append(r)
        return sequence, total_seek

    @staticmethod
    def look(requests, head, disk_size=200, direction="right"):
        requests = sorted(requests)
        sequence = [head]
        total_seek = 0
        current = head
        left = [r for r in requests if r < head]
        right = [r for r in requests if r >= head]
        if direction == "right":
            for r in right:
                total_seek += abs(r - current)
                current = r
                sequence.append(r)
            for r in reversed(left):
                total_seek += abs(r - current)
                current = r
                sequence.append(r)
        else:
            for r in reversed(left):
                total_seek += abs(r - current)
                current = r
                sequence.append(r)
            for r in right:
                total_seek += abs(r - current)
                current = r
                sequence.append(r)
        return sequence, total_seek

    @staticmethod
    def c_scan(requests, head, disk_size=200, direction="right"):
        requests = sorted(requests)
        sequence = [head]
        total_seek = 0
        current = head
        left = [r for r in requests if r < head]
        right = [r for r in requests if r >= head]
        for r in right:
            total_seek += abs(r - current)
            current = r
            sequence.append(r)
        if right:
            total_seek += abs(disk_size - 1 - current)
            current = disk_size - 1
            sequence.append(current)
        if left:
            total_seek += current
            current = 0
            sequence.append(current)
        for r in left:
            total_seek += abs(r - current)
            current = r
            sequence.append(r)
        return sequence, total_seek

class DiskSchedulingGUI:
    def __init__(self, parent):
        self.parent = parent
        self.requests = []
        self.disk_size = 200
        self.setup_gui()

    def setup_gui(self):
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

        # ─────────────────────────────────────────────
        # HEADER
        # ─────────────────────────────────────────────
        header = tk.Frame(content, bg=Theme.BG_DARK)
        header.pack(fill=tk.X, pady=(0, 15))
        tk.Label(header, text="Disk Scheduling", font=Theme.FONT_TITLE,
                 bg=Theme.BG_DARK, fg=Theme.ACCENT).pack(side=tk.LEFT)
        tk.Label(header, text=" FCFS | SSTF | SCAN | LOOK | C-SCAN",
                 font=Theme.FONT, bg=Theme.BG_DARK, fg=Theme.TEXT_DIM).pack(side=tk.LEFT)

        # ─────────────────────────────────────────────
        # INPUT SECTION
        # ─────────────────────────────────────────────
        input_frame = tk.Frame(content, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        input_frame.pack(fill=tk.X, pady=(0, 12))
        tk.Label(input_frame, text="─── PARAMETERS ───", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(anchor='w')

        row1 = tk.Frame(input_frame, bg=Theme.BG_SECONDARY)
        row1.pack(fill=tk.X, pady=10)

        tk.Label(row1, text="Disk Size:", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT)
        self.disk_size_entry = tk.Entry(row1, width=8, font=Theme.FONT,
                                        bg=Theme.BG_INPUT, fg=Theme.TEXT,
                                        insertbackground=Theme.ACCENT, bd=0,
                                        highlightthickness=1,
                                        highlightbackground=Theme.BORDER)
        self.disk_size_entry.insert(0, "200")
        self.disk_size_entry.pack(side=tk.LEFT, padx=(5, 20))

        tk.Label(row1, text="Head Position:", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT)
        self.head_entry = tk.Entry(row1, width=8, font=Theme.FONT,
                                   bg=Theme.BG_INPUT, fg=Theme.TEXT,
                                   insertbackground=Theme.ACCENT, bd=0,
                                   highlightthickness=1,
                                   highlightbackground=Theme.BORDER)
        self.head_entry.insert(0, "50")
        self.head_entry.pack(side=tk.LEFT, padx=(5, 20))

        tk.Label(row1, text="Direction:", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT)
        self.dir_var = tk.StringVar(value="right")
        tk.Radiobutton(row1, text="Right", variable=self.dir_var, value="right",
                       font=Theme.FONT_SMALL, bg=Theme.BG_SECONDARY, fg=Theme.TEXT,
                       selectcolor=Theme.BG_TERTIARY).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(row1, text="Left", variable=self.dir_var, value="left",
                       font=Theme.FONT_SMALL, bg=Theme.BG_SECONDARY, fg=Theme.TEXT,
                       selectcolor=Theme.BG_TERTIARY).pack(side=tk.LEFT)

        row2 = tk.Frame(input_frame, bg=Theme.BG_SECONDARY)
        row2.pack(fill=tk.X, pady=5)
        tk.Label(row2, text="Add Request:", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT)
        self.request_entry = tk.Entry(row2, width=10, font=Theme.FONT,
                                      bg=Theme.BG_INPUT, fg=Theme.TEXT,
                                      insertbackground=Theme.ACCENT, bd=0,
                                      highlightthickness=1,
                                      highlightbackground=Theme.BORDER)
        self.request_entry.pack(side=tk.LEFT, padx=(5, 15))

        tk.Button(row2, text="+ Add", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.ACCENT, bd=0,
                  padx=10, pady=3, cursor='hand2',
                  command=self.add_request).pack(side=tk.LEFT, padx=3)
        tk.Button(row2, text="Random", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.TEXT, bd=0,
                  padx=10, pady=3, cursor='hand2',
                  command=self.generate_random).pack(side=tk.LEFT, padx=3)
        tk.Button(row2, text="Clear", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.ERROR, bd=0,
                  padx=10, pady=3, cursor='hand2',
                  command=self.clear_all).pack(side=tk.LEFT, padx=3)

        # ─────────────────────────────────────────────
        # REQUEST QUEUE
        # ─────────────────────────────────────────────
        queue_frame = tk.Frame(content, bg=Theme.BG_SECONDARY, padx=15, pady=10)
        queue_frame.pack(fill=tk.X, pady=(0, 12))
        tk.Label(queue_frame, text="─── REQUEST QUEUE ───", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(anchor='w')
        self.queue_label = tk.Label(queue_frame, text="[ Empty ]",
                                    font=('Consolas', 12),
                                    bg=Theme.BG_DARK, fg=Theme.ACCENT,
                                    padx=10, pady=8)
        self.queue_label.pack(fill=tk.X, pady=5)

        # ─────────────────────────────────────────────
        # ALGORITHM SELECTION
        # ─────────────────────────────────────────────
        algo_frame = tk.Frame(content, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        algo_frame.pack(fill=tk.X, pady=(0, 12))
        tk.Label(algo_frame, text="─── ALGORITHM ───", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(anchor='w')
        algo_row = tk.Frame(algo_frame, bg=Theme.BG_SECONDARY)
        algo_row.pack(fill=tk.X, pady=10)
        self.algo_var = tk.StringVar(value="FCFS")
        for algo in ["FCFS", "SSTF", "SCAN", "LOOK", "C-SCAN"]:
            rb = tk.Radiobutton(algo_row, text=algo, variable=self.algo_var,
                                value=algo, font=Theme.FONT, bg=Theme.BG_SECONDARY,
                                fg=Theme.TEXT, selectcolor=Theme.BG_TERTIARY,
                                cursor='hand2')
            rb.pack(side=tk.LEFT, padx=10)

        tk.Button(algo_row, text="▶ Run Simulation", font=Theme.FONT_BOLD,
                  bg=Theme.ACCENT, fg=Theme.BG_DARK, bd=0,
                  padx=20, pady=6, cursor='hand2',
                  command=self.run_simulation).pack(side=tk.RIGHT)
        tk.Button(algo_row, text="Compare All", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.TEXT, bd=0,
                  padx=15, pady=5, cursor='hand2',
                  command=self.compare_all).pack(side=tk.RIGHT, padx=10)

        # ─────────────────────────────────────────────
        # VISUALIZATION
        # ─────────────────────────────────────────────
        viz_frame = tk.Frame(content, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        viz_frame.pack(fill=tk.X, pady=(0, 12))
        
        viz_header = tk.Frame(viz_frame, bg=Theme.BG_SECONDARY)
        viz_header.pack(fill=tk.X)
        tk.Label(viz_header, text="─── HEAD MOVEMENT ───", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT)
        expand_btn = tk.Label(viz_header, text="⛶ Click graph to expand", font=Theme.FONT_SMALL,
                              bg=Theme.BG_SECONDARY, fg=Theme.ACCENT, cursor='hand2')
        expand_btn.pack(side=tk.RIGHT)
        expand_btn.bind("<Button-1>", lambda e: self.open_expanded_view())
        
        self.disk_canvas = tk.Canvas(viz_frame, height=200,
                                     bg=Theme.BG_DARK, highlightthickness=0,
                                     cursor='hand2')
        self.disk_canvas.pack(fill=tk.BOTH, expand=True, pady=10)
        self.disk_canvas.bind("<Button-1>", lambda e: self.open_expanded_view())
        
        # Store current sequence for expanded view
        self.current_sequence = None
        self.current_algo = None

        # ─────────────────────────────────────────────
        # RESULTS
        # ─────────────────────────────────────────────
        results_frame = tk.Frame(content, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        results_frame.pack(fill=tk.X)
        tk.Label(results_frame, text="─── RESULTS ───", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(anchor='w')
        self.seq_label = tk.Label(results_frame, text="Seek Sequence: -",
                                  font=Theme.FONT, bg=Theme.BG_SECONDARY,
                                  fg=Theme.TEXT, wraplength=800, anchor='w')
        self.seq_label.pack(fill=tk.X, pady=5)
        stats_row = tk.Frame(results_frame, bg=Theme.BG_SECONDARY)
        stats_row.pack(fill=tk.X, pady=5)
        self.total_label = tk.Label(stats_row, text="Total Seek: -",
                                    font=Theme.FONT_BOLD, bg=Theme.BG_DARK,
                                    fg=Theme.SUCCESS, padx=15, pady=5)
        self.total_label.pack(side=tk.LEFT, padx=(0, 10))
        self.avg_label = tk.Label(stats_row, text="Average: -",
                                  font=Theme.FONT, bg=Theme.BG_DARK,
                                  fg=Theme.TEXT, padx=15, pady=5)
        self.avg_label.pack(side=tk.LEFT)

    def add_request(self):
        try:
            req = int(self.request_entry.get())
            disk_size = int(self.disk_size_entry.get())
            if req < 0 or req >= disk_size:
                messagebox.showerror("Error", f"Request must be 0-{disk_size-1}")
                return
            if req in self.requests:
                messagebox.showwarning("Warning", "Request already exists")
                return
            self.requests.append(req)
            self.update_queue()
            self.request_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    def generate_random(self):
        self.requests = []
        try:
            disk_size = int(self.disk_size_entry.get())
        except ValueError:
            disk_size = 200
        n = random.randint(6, 10)
        self.requests = random.sample(range(disk_size), n)
        self.update_queue()

    def clear_all(self):
        self.requests = []
        self.update_queue()
        self.disk_canvas.delete("all")
        self.seq_label.config(text="Seek Sequence: -")
        self.total_label.config(text="Total Seek: -")
        self.avg_label.config(text="Average: -")

    def update_queue(self):
        if self.requests:
            text = "[ " + " → ".join(map(str, self.requests)) + " ]"
        else:
            text = "[ Empty ]"
        self.queue_label.config(text=text)

    def run_simulation(self):
        if not self.requests:
            messagebox.showerror("Error", "Please add requests first")
            return
        try:
            head = int(self.head_entry.get())
            disk_size = int(self.disk_size_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid numbers")
            return
        algo = self.algo_var.get()
        direction = self.dir_var.get()
        self.disk_size = disk_size

        if algo == "FCFS":
            seq, total = DiskScheduler.fcfs(self.requests, head, disk_size)
        elif algo == "SSTF":
            seq, total = DiskScheduler.sstf(self.requests, head, disk_size)
        elif algo == "SCAN":
            seq, total = DiskScheduler.scan(self.requests, head, disk_size, direction)
        elif algo == "LOOK":
            seq, total = DiskScheduler.look(self.requests, head, disk_size, direction)
        else:
            seq, total = DiskScheduler.c_scan(self.requests, head, disk_size, direction)

        self.current_sequence = seq
        self.current_algo = algo
        self.draw_movement(seq, algo)
        self.display_results(seq, total)

    def draw_movement(self, sequence, algo):
        self.disk_canvas.delete("all")
        canvas_width = self.disk_canvas.winfo_width() - 60
        canvas_height = self.disk_canvas.winfo_height() - 50
        if canvas_width < 100:
            canvas_width = 700
        if canvas_height < 100:
            canvas_height = 180
        scale = canvas_width / self.disk_size
        y_spacing = canvas_height / len(sequence) if len(sequence) > 1 else 30
        x_start = 40
        y_top = 30

        # Draw axis
        self.disk_canvas.create_line(x_start, y_top, x_start + canvas_width, y_top,
                                     fill=Theme.BORDER, width=2)

        # Draw ticks
        for i in range(0, self.disk_size + 1, self.disk_size // 10):
            x = x_start + i * scale
            self.disk_canvas.create_line(x, y_top - 5, x, y_top + 5,
                                         fill=Theme.TEXT_DIM)
            self.disk_canvas.create_text(x, y_top - 12, text=str(i),
                                         font=Theme.FONT_SMALL, fill=Theme.TEXT_DIM)

        colors = ['#00d4aa', '#3fb950', '#d29922', '#f85149', '#a371f7',
                  '#79c0ff', '#ff7b72', '#7ee787', '#ffa657', '#d2a8ff']
        prev_x = x_start + sequence[0] * scale
        prev_y = y_top + 15

        # Start marker
        self.disk_canvas.create_oval(prev_x - 6, prev_y - 6, prev_x + 6, prev_y + 6,
                                     fill=Theme.SUCCESS, outline='')
        self.disk_canvas.create_text(prev_x, prev_y + 15, text=f"Start:{sequence[0]}",
                                     font=Theme.FONT_SMALL, fill=Theme.TEXT_DIM)

        # Draw path
        for i in range(1, len(sequence)):
            curr_x = x_start + sequence[i] * scale
            curr_y = prev_y + y_spacing
            color = colors[(i - 1) % len(colors)]

            # Line
            self.disk_canvas.create_line(prev_x, prev_y, curr_x, curr_y,
                                         fill=color, width=2, arrow=tk.LAST)

            # Point
            is_request = sequence[i] in self.requests
            point_color = Theme.ACCENT if is_request else Theme.TEXT_DIM
            self.disk_canvas.create_oval(curr_x - 4, curr_y - 4, curr_x + 4, curr_y + 4,
                                         fill=point_color, outline='')

            # Label
            self.disk_canvas.create_text(curr_x + 20, curr_y, text=str(sequence[i]),
                                         font=Theme.FONT_SMALL, fill=Theme.TEXT_DIM)

            prev_x = curr_x
            prev_y = curr_y

        # Legend
        self.disk_canvas.create_text(x_start + canvas_width - 50, canvas_height + 20,
                                     text=f"Algorithm: {algo}",
                                     font=Theme.FONT_BOLD, fill=Theme.ACCENT)

    def display_results(self, sequence, total):
        self.seq_label.config(text="Seek Sequence: " + " → ".join(map(str, sequence)))
        self.total_label.config(text=f"Total Seek: {total} cylinders")
        avg = total / (len(sequence) - 1) if len(sequence) > 1 else 0
        self.avg_label.config(text=f"Average: {avg:.2f} cyl/request")

    def open_expanded_view(self):
        if not self.current_sequence:
            messagebox.showinfo("Info", "Run a simulation first to see expanded view")
            return
        
        # Create expanded window
        win = tk.Toplevel(self.parent)
        win.title(f"Disk Scheduling - {self.current_algo} (Expanded View)")
        win.geometry("1200x800")
        win.configure(bg=Theme.BG_DARK)
        
        # Header
        header = tk.Frame(win, bg=Theme.BG_DARK)
        header.pack(fill=tk.X, padx=20, pady=15)
        tk.Label(header, text=f"Head Movement Visualization", font=Theme.FONT_TITLE,
                 bg=Theme.BG_DARK, fg=Theme.ACCENT).pack(side=tk.LEFT)
        tk.Label(header, text=f"  Algorithm: {self.current_algo}", font=Theme.FONT,
                 bg=Theme.BG_DARK, fg=Theme.TEXT_DIM).pack(side=tk.LEFT, padx=10)
        tk.Button(header, text="✕ Close", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.ERROR, bd=0,
                  padx=15, pady=5, cursor='hand2',
                  command=win.destroy).pack(side=tk.RIGHT)
        
        # Scrollable canvas frame
        canvas_frame = tk.Frame(win, bg=Theme.BG_SECONDARY, padx=20, pady=20)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Calculate required height based on sequence length
        required_height = max(500, len(self.current_sequence) * 50 + 100)
        
        expanded_canvas = tk.Canvas(canvas_frame, bg=Theme.BG_DARK, highlightthickness=0)
        expanded_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Mouse wheel scrolling only (no visible scrollbar)
        def on_mousewheel(event):
            expanded_canvas.yview_scroll(-1 * (event.delta // 120), "units")
        expanded_canvas.bind("<MouseWheel>", on_mousewheel)
        expanded_canvas.bind("<Button-4>", lambda e: expanded_canvas.yview_scroll(-1, "units"))
        expanded_canvas.bind("<Button-5>", lambda e: expanded_canvas.yview_scroll(1, "units"))
        
        # Wait for window to render, then draw
        win.update_idletasks()
        self.draw_expanded_movement(expanded_canvas, self.current_sequence, self.current_algo, required_height)
        
        # Set scroll region
        expanded_canvas.configure(scrollregion=(0, 0, 1100, required_height))
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            expanded_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        expanded_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        expanded_canvas.bind_all("<Button-4>", lambda e: expanded_canvas.yview_scroll(-1, "units"))
        expanded_canvas.bind_all("<Button-5>", lambda e: expanded_canvas.yview_scroll(1, "units"))
        
        # Results summary at bottom
        results = tk.Frame(win, bg=Theme.BG_SECONDARY, padx=20, pady=15)
        results.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        total_seek = sum(abs(self.current_sequence[i] - self.current_sequence[i-1]) 
                        for i in range(1, len(self.current_sequence)))
        avg = total_seek / (len(self.current_sequence) - 1) if len(self.current_sequence) > 1 else 0
        
        tk.Label(results, text=f"Seek Sequence: {' → '.join(map(str, self.current_sequence))}",
                 font=Theme.FONT, bg=Theme.BG_SECONDARY, fg=Theme.TEXT,
                 wraplength=1100, anchor='w').pack(fill=tk.X, pady=5)
        
        stats = tk.Frame(results, bg=Theme.BG_SECONDARY)
        stats.pack(fill=tk.X, pady=5)
        tk.Label(stats, text=f"Total Seek: {total_seek} cylinders",
                 font=Theme.FONT_BOLD, bg=Theme.BG_DARK, fg=Theme.SUCCESS,
                 padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(stats, text=f"Average: {avg:.2f} cyl/request",
                 font=Theme.FONT, bg=Theme.BG_DARK, fg=Theme.TEXT,
                 padx=15, pady=8).pack(side=tk.LEFT)

    def draw_expanded_movement(self, canvas, sequence, algo, total_height=500):
        """Draw movement on the expanded canvas with larger dimensions"""
        canvas.delete("all")
        canvas_width = canvas.winfo_width() - 80
        if canvas_width < 100:
            canvas_width = 1050
        
        scale = canvas_width / self.disk_size
        y_spacing = 45  # Fixed spacing between each step
        x_start = 60
        y_top = 50

        # Draw axis with thicker line
        canvas.create_line(x_start, y_top, x_start + canvas_width, y_top,
                           fill=Theme.BORDER, width=3)

        # Draw ticks with larger font
        for i in range(0, self.disk_size + 1, self.disk_size // 10):
            x = x_start + i * scale
            canvas.create_line(x, y_top - 8, x, y_top + 8, fill=Theme.TEXT_DIM, width=2)
            canvas.create_text(x, y_top - 20, text=str(i),
                               font=('Consolas', 11), fill=Theme.TEXT_DIM)

        colors = ['#00d4aa', '#3fb950', '#d29922', '#f85149', '#a371f7',
                  '#79c0ff', '#ff7b72', '#7ee787', '#ffa657', '#d2a8ff']
        prev_x = x_start + sequence[0] * scale
        prev_y = y_top + 25

        # Start marker (larger)
        canvas.create_oval(prev_x - 10, prev_y - 10, prev_x + 10, prev_y + 10,
                           fill=Theme.SUCCESS, outline='')
        canvas.create_text(prev_x, prev_y + 25, text=f"Start: {sequence[0]}",
                           font=('Consolas', 11, 'bold'), fill=Theme.SUCCESS)

        # Draw path with thicker lines
        for i in range(1, len(sequence)):
            curr_x = x_start + sequence[i] * scale
            curr_y = prev_y + y_spacing
            color = colors[(i - 1) % len(colors)]

            # Line (thicker)
            canvas.create_line(prev_x, prev_y, curr_x, curr_y,
                               fill=color, width=3, arrow=tk.LAST, arrowshape=(12, 15, 6))

            # Point (larger)
            is_request = sequence[i] in self.requests
            point_color = Theme.ACCENT if is_request else Theme.TEXT_DIM
            point_size = 8 if is_request else 6
            canvas.create_oval(curr_x - point_size, curr_y - point_size,
                               curr_x + point_size, curr_y + point_size,
                               fill=point_color, outline='')

            # Label (larger font)
            canvas.create_text(curr_x + 30, curr_y, text=str(sequence[i]),
                               font=('Consolas', 11), fill=Theme.TEXT)

            prev_x = curr_x
            prev_y = curr_y

        # Legend (at bottom of drawing, after last point)
        canvas.create_text(x_start + canvas_width - 80, prev_y + 40,
                           text=f"Algorithm: {algo}",
                           font=('Consolas', 14, 'bold'), fill=Theme.ACCENT)

    def compare_all(self):
        if not self.requests:
            messagebox.showerror("Error", "Please add requests first")
            return
        try:
            head = int(self.head_entry.get())
            disk_size = int(self.disk_size_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid numbers")
            return
        direction = self.dir_var.get()
        results = []
        _, fcfs = DiskScheduler.fcfs(self.requests, head, disk_size)
        results.append(("FCFS", fcfs))
        _, sstf = DiskScheduler.sstf(self.requests, head, disk_size)
        results.append(("SSTF", sstf))
        _, scan = DiskScheduler.scan(self.requests, head, disk_size, direction)
        results.append(("SCAN", scan))
        _, look = DiskScheduler.look(self.requests, head, disk_size, direction)
        results.append(("LOOK", look))
        _, cscan = DiskScheduler.c_scan(self.requests, head, disk_size, direction)
        results.append(("C-SCAN", cscan))
        results.sort(key=lambda x: x[1])

        # Create comparison window
        win = tk.Toplevel(self.parent)
        win.title("Algorithm Comparison")
        win.geometry("450x400")
        win.configure(bg=Theme.BG_DARK)
        tk.Label(win, text="Algorithm Comparison", font=Theme.FONT_TITLE,
                 bg=Theme.BG_DARK, fg=Theme.ACCENT).pack(pady=15)

        # Table
        table = tk.Frame(win, bg=Theme.BG_SECONDARY, padx=20, pady=15)
        table.pack(fill=tk.BOTH, expand=True, padx=20)

        # Header
        header = tk.Frame(table, bg=Theme.BG_TERTIARY)
        header.pack(fill=tk.X)
        for h in ["Rank", "Algorithm", "Total Seek"]:
            tk.Label(header, text=h, font=Theme.FONT_BOLD,
                     bg=Theme.BG_TERTIARY, fg=Theme.ACCENT, width=12).pack(side=tk.LEFT)

        # Rows
        for i, (algo, seek) in enumerate(results):
            row = tk.Frame(table, bg=Theme.BG_DARK)
            row.pack(fill=tk.X)
            color = Theme.SUCCESS if i == 0 else Theme.TEXT
            tk.Label(row, text=f"#{i+1}", font=Theme.FONT,
                     bg=Theme.BG_DARK, fg=color, width=12).pack(side=tk.LEFT)
            tk.Label(row, text=algo, font=Theme.FONT,
                     bg=Theme.BG_DARK, fg=color, width=12).pack(side=tk.LEFT)
            tk.Label(row, text=str(seek), font=Theme.FONT,
                     bg=Theme.BG_DARK, fg=color, width=12).pack(side=tk.LEFT)

        # Winner
        best = results[0]
        tk.Label(win, text=f"★ Best: {best[0]} ({best[1]} cylinders)",
                 font=Theme.FONT_BOLD, bg=Theme.BG_DARK, fg=Theme.SUCCESS).pack(pady=15)

def create_disk_scheduling_window():
    window = tk.Toplevel()
    window.title("Disk Scheduling")
    window.geometry("1000x750")
    window.configure(bg=Theme.BG_DARK)
    DiskSchedulingGUI(window)
    return window

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Disk Scheduling")
    root.geometry("1000x750")
    root.configure(bg=Theme.BG_DARK)
    DiskSchedulingGUI(root)
    root.mainloop()
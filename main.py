"""
Mini OS Simulator - Main Application
Clean Minimal UI
"""
import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import shared Theme from separate file
from theme import Theme

class MiniOSSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mini OS Simulator")
        self.root.geometry("1100x700")
        self.root.configure(bg=Theme.BG_DARK)
        self.root.minsize(900, 600)
        self.current_module = None
        self.setup_gui()

    def setup_gui(self):
        main = tk.Frame(self.root, bg=Theme.BG_DARK)
        main.pack(fill=tk.BOTH, expand=True)

        # ═══════════════════════════════════════════════════════════════
        # TOP HEADER
        # ═══════════════════════════════════════════════════════════════
        header = tk.Frame(main, bg=Theme.BG_SECONDARY, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        header_content = tk.Frame(header, bg=Theme.BG_SECONDARY)
        header_content.pack(fill=tk.BOTH, expand=True, padx=25, pady=12)

        # Simple title
        title_frame = tk.Frame(header_content, bg=Theme.BG_SECONDARY)
        title_frame.pack(side=tk.LEFT)
        tk.Label(title_frame, text="●", font=('Consolas', 16),
                 bg=Theme.BG_SECONDARY, fg=Theme.ACCENT).pack(side=tk.LEFT)
        tk.Label(title_frame, text=" Mini OS Simulator", font=Theme.FONT_HEADER,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT).pack(side=tk.LEFT)

        # Home button
        self.home_btn = tk.Button(header_content, text="⌂ Home", font=Theme.FONT,
                                  bg=Theme.BG_TERTIARY, fg=Theme.TEXT, bd=0,
                                  padx=12, pady=4, cursor='hand2',
                                  command=self.show_welcome)
        self.home_btn.pack(side=tk.RIGHT)

        tk.Frame(main, bg=Theme.BORDER, height=1).pack(fill=tk.X)

        # ═══════════════════════════════════════════════════════════════
        # CONTENT AREA (SIDEBAR + MAIN)
        # ═══════════════════════════════════════════════════════════════
        content = tk.Frame(main, bg=Theme.BG_DARK)
        content.pack(fill=tk.BOTH, expand=True)

        # LEFT SIDEBAR
        self.sidebar = tk.Frame(content, bg=Theme.BG_SECONDARY, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        sidebar_header = tk.Frame(self.sidebar, bg=Theme.BG_SECONDARY)
        sidebar_header.pack(fill=tk.X, padx=15, pady=15)
        tk.Label(sidebar_header, text="MODULES",
                 font=Theme.FONT_BOLD, bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_DIM).pack()

        # Navigation buttons (Memory and File buttons kept in UI, but no functionality)
        nav_items = [
            ("CPU Scheduling", self.open_cpu),
            ("Memory Management", self.placeholder),      # ← button kept, no real function
            ("Disk Scheduling", self.open_disk),
            ("File Management", self.placeholder),        # ← button kept, no real function
        ]

        for text, command in nav_items:
            btn = tk.Button(self.sidebar, text=f" {text}", command=command,
                            font=Theme.FONT, bg=Theme.BG_SECONDARY,
                            fg=Theme.TEXT, bd=0, anchor='w',
                            activebackground=Theme.BG_TERTIARY,
                            activeforeground=Theme.ACCENT,
                            padx=15, pady=10, cursor='hand2')
            btn.pack(fill=tk.X)
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=Theme.BG_TERTIARY, fg=Theme.ACCENT))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg=Theme.BG_SECONDARY, fg=Theme.TEXT))

        # Sidebar footer
        tk.Frame(self.sidebar, bg=Theme.BG_SECONDARY).pack(fill=tk.BOTH, expand=True)
        footer_frame = tk.Frame(self.sidebar, bg=Theme.BG_SECONDARY)
        footer_frame.pack(fill=tk.X, padx=15, pady=20)
        tk.Label(footer_frame, text="─────────────",
                 font=Theme.FONT_SMALL, bg=Theme.BG_SECONDARY,
                 fg=Theme.BORDER).pack()
        tk.Label(footer_frame, text="5th Semester",
                 font=Theme.FONT_SMALL, bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_DIM).pack()
        tk.Label(footer_frame, text="OS Mini Project",
                 font=Theme.FONT_SMALL, bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_DIM).pack()

        tk.Frame(content, bg=Theme.BORDER, width=1).pack(side=tk.LEFT, fill=tk.Y)

        # MAIN CONTENT AREA
        self.main_area = tk.Frame(content, bg=Theme.BG_DARK)
        self.main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.show_welcome()

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def placeholder(self):
        """Placeholder for removed modules"""
        self.clear_main_area()
        tk.Label(self.main_area,
                 text="This module is currently under development / removed",
                 font=Theme.FONT_TITLE, bg=Theme.BG_DARK, fg=Theme.TEXT_DIM).pack(expand=True)

    def show_welcome(self):
        self.clear_main_area()
        welcome = tk.Frame(self.main_area, bg=Theme.BG_DARK)
        welcome.place(relx=0.5, rely=0.45, anchor='center')

        # Simple clean logo
        logo_frame = tk.Frame(welcome, bg=Theme.BG_TERTIARY, padx=30, pady=20)
        logo_frame.pack()
        tk.Label(logo_frame, text="Mini OS", font=('Consolas', 28, 'bold'),
                 bg=Theme.BG_TERTIARY, fg=Theme.ACCENT).pack()
        tk.Label(logo_frame, text="SIMULATOR", font=('Consolas', 12),
                 bg=Theme.BG_TERTIARY, fg=Theme.TEXT_DIM).pack()

        tk.Label(welcome, text="Operating System Algorithm Visualization",
                 font=Theme.FONT_TITLE, bg=Theme.BG_DARK,
                 fg=Theme.TEXT).pack(pady=(25, 8))
        tk.Label(welcome, text="Select a module from the sidebar to begin",
                 font=Theme.FONT, bg=Theme.BG_DARK,
                 fg=Theme.TEXT_DIM).pack()

        # Quick access grid (Memory and File cards kept in UI, but lead to placeholder)
        grid_frame = tk.Frame(welcome, bg=Theme.BG_DARK)
        grid_frame.pack(pady=40)
        modules = [
            ("CPU Scheduling", "FCFS, SJF, Priority, RR", self.open_cpu),
            ("Memory Mgmt", "First/Best/Worst Fit", self.placeholder),
            ("Disk Scheduling", "FCFS, SSTF, SCAN, LOOK", self.open_disk),
            ("File Management", "Create, Delete, View", self.placeholder),
        ]
        for i, (title, desc, cmd) in enumerate(modules):
            card = tk.Frame(grid_frame, bg=Theme.BG_TERTIARY, padx=18, pady=14)
            card.grid(row=0, column=i, padx=6, pady=6)
            tk.Label(card, text=title, font=Theme.FONT_BOLD,
                     bg=Theme.BG_TERTIARY, fg=Theme.ACCENT,
                     justify=tk.CENTER).pack()
            tk.Label(card, text=desc, font=Theme.FONT_SMALL,
                     bg=Theme.BG_TERTIARY, fg=Theme.TEXT_DIM,
                     justify=tk.CENTER).pack(pady=(4, 10))
            btn = tk.Button(card, text="Open", command=cmd,
                            font=Theme.FONT_SMALL, bg=Theme.BG_SECONDARY,
                            fg=Theme.ACCENT, bd=0, padx=12, pady=3,
                            cursor='hand2', activebackground=Theme.ACCENT,
                            activeforeground=Theme.BG_DARK)
            btn.pack()

    def open_cpu(self):
        self.clear_main_area()
        from cpu_scheduling import CPUSchedulingGUI
        CPUSchedulingGUI(self.main_area)

    def open_disk(self):
        self.clear_main_area()
        from disk_scheduling import DiskSchedulingGUI
        DiskSchedulingGUI(self.main_area)

    def run(self):
        self.root.mainloop()

def main():
    app = MiniOSSimulator()
    app.run()

if __name__ == "__main__":
    main()
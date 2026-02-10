import tkinter as tk
from tkinter import messagebox
from theme import Theme
import random

class MemoryBlock:
    def __init__(self, size):
        self.size = size
        self.is_allocated = False
        self.process_id = None
        self.process_size = 0

class MemoryAllocator:
    @staticmethod
    def first_fit(blocks, process_size, process_id):
        """Allocate to FIRST block that fits, split remaining space"""
        for i, block in enumerate(blocks):
            if not block.is_allocated and block.size >= process_size:
                remaining = block.size - process_size
                block.size = process_size
                block.is_allocated = True
                block.process_id = process_id
                block.process_size = process_size
                # Create new block for remaining space if any
                if remaining > 0:
                    new_block = MemoryBlock(remaining)
                    blocks.insert(i + 1, new_block)
                return True, block
        return False, None
    
    @staticmethod
    def best_fit(blocks, process_size, process_id):
        """Allocate to SMALLEST block that fits, split remaining space"""
        best = None
        best_idx = -1
        for i, block in enumerate(blocks):
            if not block.is_allocated and block.size >= process_size:
                if best is None or block.size < best.size:
                    best = block
                    best_idx = i
        if best:
            remaining = best.size - process_size
            best.size = process_size
            best.is_allocated = True
            best.process_id = process_id
            best.process_size = process_size
            # Create new block for remaining space if any
            if remaining > 0:
                new_block = MemoryBlock(remaining)
                blocks.insert(best_idx + 1, new_block)
            return True, best
        return False, None
    
    @staticmethod
    def worst_fit(blocks, process_size, process_id):
        """Allocate to LARGEST block that fits, split remaining space"""
        worst = None
        worst_idx = -1
        for i, block in enumerate(blocks):
            if not block.is_allocated and block.size >= process_size:
                if worst is None or block.size > worst.size:
                    worst = block
                    worst_idx = i
        if worst:
            remaining = worst.size - process_size
            worst.size = process_size
            worst.is_allocated = True
            worst.process_id = process_id
            worst.process_size = process_size
            # Create new block for remaining space if any
            if remaining > 0:
                new_block = MemoryBlock(remaining)
                blocks.insert(worst_idx + 1, new_block)
            return True, worst
        return False, None

class MemoryManagementGUI:
    def __init__(self, parent):
        self.parent = parent
        self.blocks = []
        self.process_counter = 1
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
        
        # Header
        tk.Label(content, text="Memory Management", font=Theme.FONT_TITLE,
                 bg=Theme.BG_DARK, fg=Theme.ACCENT).pack(anchor='w', pady=(0, 10))
        
        # Initialize Memory Section
        init_frame = tk.Frame(content, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        init_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(init_frame, text="─── MEMORY SETUP ───", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(anchor='w')
        
        row1 = tk.Frame(init_frame, bg=Theme.BG_SECONDARY)
        row1.pack(fill=tk.X, pady=10)
        
        tk.Label(row1, text="Block Size:", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT)
        self.block_entry = tk.Entry(row1, width=10, font=Theme.FONT,
                                     bg=Theme.BG_INPUT, fg=Theme.TEXT)
        self.block_entry.insert(0, "100")
        self.block_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(row1, text="+ Add Block", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.ACCENT, bd=0,
                  padx=12, pady=5, cursor='hand2',
                  command=self.add_block).pack(side=tk.LEFT, padx=10)
        
        tk.Button(row1, text="Random Blocks", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.TEXT, bd=0,
                  padx=12, pady=5, cursor='hand2',
                  command=self.random_blocks).pack(side=tk.LEFT, padx=5)
        
        tk.Button(row1, text="Clear All", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.ERROR, bd=0,
                  padx=12, pady=5, cursor='hand2',
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Memory blocks display
        self.blocks_frame = tk.Frame(content, bg=Theme.BG_DARK)
        self.blocks_frame.pack(fill=tk.X, pady=10)
        self.update_blocks_display()
        
        # Process allocation section
        alloc_frame = tk.Frame(content, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        alloc_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(alloc_frame, text="─── ALLOCATE PROCESS ───", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(anchor='w')
        
        row2 = tk.Frame(alloc_frame, bg=Theme.BG_SECONDARY)
        row2.pack(fill=tk.X, pady=10)
        
        tk.Label(row2, text="Process Size:", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT)
        self.process_entry = tk.Entry(row2, width=10, font=Theme.FONT,
                                       bg=Theme.BG_INPUT, fg=Theme.TEXT)
        self.process_entry.insert(0, "50")
        self.process_entry.pack(side=tk.LEFT, padx=5)
        
        # Algorithm selection
        tk.Label(row2, text="Algorithm:", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT, padx=(20, 5))
        self.algo_var = tk.StringVar(value="First Fit")
        for algo in ["First Fit", "Best Fit", "Worst Fit"]:
            tk.Radiobutton(row2, text=algo, variable=self.algo_var, value=algo,
                           font=Theme.FONT_SMALL, bg=Theme.BG_SECONDARY, fg=Theme.TEXT,
                           selectcolor=Theme.BG_TERTIARY).pack(side=tk.LEFT, padx=5)
        
        tk.Button(row2, text="Allocate", font=Theme.FONT_BOLD,
                  bg=Theme.ACCENT, fg=Theme.BG_DARK, bd=0,
                  padx=20, pady=6, cursor='hand2',
                  command=self.allocate_process).pack(side=tk.RIGHT)
        
        # Visualization canvas
        viz_frame = tk.Frame(content, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        viz_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(viz_frame, text="─── MEMORY MAP ───", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(anchor='w')
        
        self.canvas = tk.Canvas(viz_frame, height=300, bg=Theme.BG_DARK,
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Stats
        self.stats_label = tk.Label(viz_frame, text="", font=Theme.FONT,
                                     bg=Theme.BG_SECONDARY, fg=Theme.SUCCESS)
        self.stats_label.pack(anchor='w', pady=5)
    
    def add_block(self):
        try:
            size = int(self.block_entry.get())
            if size <= 0:
                raise ValueError("Size must be positive")
            block = MemoryBlock(size)
            self.blocks.append(block)
            self.update_blocks_display()
            self.draw_memory()
            self.block_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e) or "Enter valid number")
    
    def random_blocks(self):
        self.clear_all()
        n = random.randint(5, 8)
        for _ in range(n):
            size = random.choice([50, 75, 100, 125, 150, 200, 250])
            self.blocks.append(MemoryBlock(size))
        self.update_blocks_display()
        self.draw_memory()
    
    def clear_all(self):
        self.blocks = []
        self.process_counter = 1
        self.update_blocks_display()
        self.canvas.delete("all")
        self.stats_label.config(text="")
    
    def update_blocks_display(self):
        for widget in self.blocks_frame.winfo_children():
            widget.destroy()
        
        if not self.blocks:
            tk.Label(self.blocks_frame, text="No memory blocks created",
                     font=Theme.FONT_SMALL, bg=Theme.BG_DARK, fg=Theme.TEXT_DIM).pack()
            return
        
        # Show block sizes with allocation status
        block_texts = []
        for b in self.blocks:
            if b.is_allocated:
                block_texts.append(f"{b.size}KB ({b.process_id})")
            else:
                block_texts.append(f"{b.size}KB")
        text = "Memory Blocks: " + " | ".join(block_texts)
        tk.Label(self.blocks_frame, text=text, font=Theme.FONT,
                 bg=Theme.BG_DARK, fg=Theme.TEXT).pack(anchor='w')
    
    def allocate_process(self):
        if not self.blocks:
            messagebox.showwarning("Warning", "Create memory blocks first")
            return
        
        try:
            size = int(self.process_entry.get())
            if size <= 0:
                raise ValueError("Size must be positive")
        except ValueError as e:
            messagebox.showerror("Error", str(e) or "Enter valid number")
            return
        
        algo = self.algo_var.get()
        process_id = f"P{self.process_counter}"
        
        if algo == "First Fit":
            success, block = MemoryAllocator.first_fit(self.blocks, size, process_id)
        elif algo == "Best Fit":
            success, block = MemoryAllocator.best_fit(self.blocks, size, process_id)
        else:  # Worst Fit
            success, block = MemoryAllocator.worst_fit(self.blocks, size, process_id)
        
        if success:
            self.process_counter += 1
            self.update_blocks_display()  # Update display to show new block structure
            self.draw_memory()
            self.update_stats()
            messagebox.showinfo("Success", f"{process_id} allocated ({size}KB) using {algo}")
        else:
            messagebox.showerror("Allocation Failed", "No suitable block found")
    
    def draw_memory(self):
        self.canvas.delete("all")
        if not self.blocks:
            return
        
        x = 50
        y = 50
        max_width = 600
        
        for i, block in enumerate(self.blocks):
            width = min(block.size * 2, max_width // len(self.blocks))
            height = 80
            
            if block.is_allocated:
                color = Theme.ERROR
                text = f"{block.process_id}\n{block.process_size}KB"
            else:
                color = Theme.SUCCESS
                text = f"Free\n{block.size}KB"
            
            # Draw block
            self.canvas.create_rectangle(x, y, x + width, y + height,
                                          fill=color, outline=Theme.BORDER, width=2)
            self.canvas.create_text(x + width//2, y + height//2,
                                    text=text, font=Theme.FONT_BOLD, fill=Theme.BG_DARK)
            
            # Block label
            self.canvas.create_text(x + width//2, y + height + 15,
                                    text=f"Block {i+1}", font=Theme.FONT_SMALL,
                                    fill=Theme.TEXT_DIM)
            
            x += width + 20
    
    def update_stats(self):
        total = sum(b.size for b in self.blocks)
        allocated = sum(b.size for b in self.blocks if b.is_allocated)
        free = sum(b.size for b in self.blocks if not b.is_allocated)
        num_free_blocks = sum(1 for b in self.blocks if not b.is_allocated)
        
        self.stats_label.config(
            text=f"Total: {total}KB | Allocated: {allocated}KB | Free: {free}KB ({num_free_blocks} blocks)"
        )

def open_memory(parent_frame):
    MemoryManagementGUI(parent_frame)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Memory Management")
    root.geometry("1000x750")
    root.configure(bg=Theme.BG_DARK)
    MemoryManagementGUI(root)
    root.mainloop()

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
        """Allocate to FIRST block that fits"""
        for block in blocks:
            if not block.is_allocated and block.size >= process_size:
                block.is_allocated = True
                block.process_id = process_id
                block.process_size = process_size
                return True, block
        return False, None
    
    @staticmethod
    def best_fit(blocks, process_size, process_id):
        """Allocate to SMALLEST block that fits"""
        best = None
        for block in blocks:
            if not block.is_allocated and block.size >= process_size:
                if best is None or block.size < best.size:
                    best = block
        if best:
            best.is_allocated = True
            best.process_id = process_id
            best.process_size = process_size
            return True, best
        return False, None
    
    @staticmethod
    def worst_fit(blocks, process_size, process_id):
        """Allocate to LARGEST block that fits"""
        worst = None
        for block in blocks:
            if not block.is_allocated and block.size >= process_size:
                if worst is None or block.size > worst.size:
                    worst = block
        if worst:
            worst.is_allocated = True
            worst.process_id = process_id
            worst.process_size = process_size
            return True, worst
        return False, None

class MemoryManagementGUI:
    def __init__(self, parent):
        self.parent = parent
        self.blocks = []
        self.process_counter = 1
        self.setup_ui()
        
    def setup_ui(self):
        main = tk.Frame(self.parent, bg=Theme.BG_DARK)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        tk.Label(main, text="Memory Management", font=Theme.FONT_TITLE,
                 bg=Theme.BG_DARK, fg=Theme.ACCENT).pack(anchor='w', pady=(0, 10))
        
        # Initialize Memory Section
        init_frame = tk.Frame(main, bg=Theme.BG_SECONDARY, padx=15, pady=12)
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
        self.blocks_frame = tk.Frame(main, bg=Theme.BG_DARK)
        self.blocks_frame.pack(fill=tk.X, pady=10)
        self.update_blocks_display()
        
        # Process allocation section
        alloc_frame = tk.Frame(main, bg=Theme.BG_SECONDARY, padx=15, pady=12)
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
        viz_frame = tk.Frame(main, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        viz_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
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
        
        text = "Memory Blocks: " + " | ".join([f"{b.size}KB" for b in self.blocks])
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
        allocated = sum(b.process_size for b in self.blocks if b.is_allocated)
        free = total - allocated
        fragmentation = sum(b.size - b.process_size for b in self.blocks if b.is_allocated)
        
        self.stats_label.config(
            text=f"Total: {total}KB | Allocated: {allocated}KB | Free: {free}KB | Internal Fragmentation: {fragmentation}KB"
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

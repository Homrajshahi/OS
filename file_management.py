"""
File Management Module
Implements Contiguous, Linked, and Indexed file allocation methods with visualization
"""
import tkinter as tk
from tkinter import messagebox
from theme import Theme
import random

class FileBlock:
    def __init__(self, file_id, block_num, is_index=False):
        self.file_id = file_id
        self.block_num = block_num
        self.is_index = is_index
        self.next_block = None  # For linked allocation

class File:
    def __init__(self, file_id, name, size, allocation_type):
        self.file_id = file_id
        self.name = name
        self.size = size  # in blocks
        self.allocation_type = allocation_type
        self.start_block = None
        self.blocks = []  # List of block numbers
        self.index_block = None  # For indexed allocation

class FileAllocationSimulator:
    def __init__(self, disk_size=50):
        self.disk_size = disk_size
        self.disk = [None] * disk_size  # None = free, else File object
        self.files = []
        self.file_counter = 1

    def allocate_contiguous(self, file_obj):
        """Find contiguous free blocks"""
        size = file_obj.size
        for i in range(self.disk_size - size + 1):
            if all(self.disk[j] is None for j in range(i, i + size)):
                # Allocate
                file_obj.start_block = i
                file_obj.blocks = list(range(i, i + size))
                for j in range(i, i + size):
                    self.disk[j] = FileBlock(file_obj.file_id, j)
                return True
        return False

    def allocate_linked(self, file_obj):
        """Allocate any free blocks and link them"""
        size = file_obj.size
        free_blocks = [i for i in range(self.disk_size) if self.disk[i] is None]
        if len(free_blocks) < size:
            return False
        
        allocated = random.sample(free_blocks, size)
        allocated.sort()
        file_obj.blocks = allocated
        file_obj.start_block = allocated[0]
        
        for idx, block_num in enumerate(allocated):
            fb = FileBlock(file_obj.file_id, block_num)
            if idx < len(allocated) - 1:
                fb.next_block = allocated[idx + 1]
            self.disk[block_num] = fb
        return True

    def allocate_indexed(self, file_obj):
        """Allocate index block + data blocks"""
        size = file_obj.size
        free_blocks = [i for i in range(self.disk_size) if self.disk[i] is None]
        if len(free_blocks) < size + 1:  # +1 for index block
            return False
        
        # First free block is index block
        index = free_blocks[0]
        data_blocks = random.sample(free_blocks[1:], size)
        data_blocks.sort()
        
        file_obj.index_block = index
        file_obj.blocks = data_blocks
        file_obj.start_block = index
        
        # Allocate index block
        self.disk[index] = FileBlock(file_obj.file_id, index, is_index=True)
        
        # Allocate data blocks
        for block_num in data_blocks:
            self.disk[block_num] = FileBlock(file_obj.file_id, block_num)
        
        return True

    def add_file(self, name, size, allocation_type):
        """Add a new file with specified allocation method"""
        file_obj = File(self.file_counter, name, size, allocation_type)
        
        if allocation_type == "Contiguous":
            success = self.allocate_contiguous(file_obj)
        elif allocation_type == "Linked":
            success = self.allocate_linked(file_obj)
        else:  # Indexed
            success = self.allocate_indexed(file_obj)
        
        if success:
            self.files.append(file_obj)
            self.file_counter += 1
            return True, file_obj
        return False, None

    def delete_file(self, file_id):
        """Delete a file and free its blocks"""
        file_obj = next((f for f in self.files if f.file_id == file_id), None)
        if not file_obj:
            return False
        
        # Free all blocks including index block
        if file_obj.index_block is not None:
            self.disk[file_obj.index_block] = None
        for block in file_obj.blocks:
            self.disk[block] = None
        
        self.files.remove(file_obj)
        return True

    def get_fragmentation(self):
        """Calculate external fragmentation"""
        free_blocks = [i for i in range(self.disk_size) if self.disk[i] is None]
        if not free_blocks:
            return 0, 0
        
        # Count number of free fragments
        fragments = 1
        for i in range(len(free_blocks) - 1):
            if free_blocks[i+1] - free_blocks[i] > 1:
                fragments += 1
        
        return len(free_blocks), fragments

class FileManagementGUI:
    def __init__(self, parent):
        self.parent = parent
        self.simulator = FileAllocationSimulator(50)
        self.setup_ui()

    def setup_ui(self):
        main = tk.Frame(self.parent, bg=Theme.BG_DARK)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        tk.Label(main, text="File Management", font=Theme.FONT_TITLE,
                 bg=Theme.BG_DARK, fg=Theme.ACCENT).pack(anchor='w', pady=(0, 10))

        # Input section
        input_frame = tk.Frame(main, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        input_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(input_frame, text="─── CREATE FILE ───", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(anchor='w')

        row1 = tk.Frame(input_frame, bg=Theme.BG_SECONDARY)
        row1.pack(fill=tk.X, pady=10)

        tk.Label(row1, text="File Name:", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT)
        self.name_entry = tk.Entry(row1, width=15, font=Theme.FONT,
                                   bg=Theme.BG_INPUT, fg=Theme.TEXT,
                                   insertbackground=Theme.ACCENT)
        self.name_entry.pack(side=tk.LEFT, padx=(5, 20))

        tk.Label(row1, text="Size (blocks):", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT)
        self.size_entry = tk.Entry(row1, width=8, font=Theme.FONT,
                                   bg=Theme.BG_INPUT, fg=Theme.TEXT,
                                   insertbackground=Theme.ACCENT)
        self.size_entry.insert(0, "3")
        self.size_entry.pack(side=tk.LEFT, padx=(5, 20))

        tk.Label(row1, text="Allocation:", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(side=tk.LEFT)
        self.alloc_var = tk.StringVar(value="Contiguous")
        for method in ["Contiguous", "Linked", "Indexed"]:
            tk.Radiobutton(row1, text=method, variable=self.alloc_var, value=method,
                          font=Theme.FONT_SMALL, bg=Theme.BG_SECONDARY, fg=Theme.TEXT,
                          selectcolor=Theme.BG_TERTIARY).pack(side=tk.LEFT, padx=5)

        row2 = tk.Frame(input_frame, bg=Theme.BG_SECONDARY)
        row2.pack(fill=tk.X, pady=5)

        tk.Button(row2, text="+ Create File", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.ACCENT, bd=0,
                  padx=12, pady=5, cursor='hand2',
                  command=self.create_file).pack(side=tk.LEFT, padx=5)

        tk.Button(row2, text="Random Files", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.TEXT, bd=0,
                  padx=12, pady=5, cursor='hand2',
                  command=self.generate_random).pack(side=tk.LEFT, padx=5)

        tk.Button(row2, text="Clear All", font=Theme.FONT,
                  bg=Theme.BG_TERTIARY, fg=Theme.ERROR, bd=0,
                  padx=12, pady=5, cursor='hand2',
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)

        # File list section
        list_frame = tk.Frame(main, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        list_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(list_frame, text="─── FILES ───", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(anchor='w')

        # Scrollable file list
        list_container = tk.Frame(list_frame, bg=Theme.BG_DARK, height=120)
        list_container.pack(fill=tk.X, pady=5)
        list_container.pack_propagate(False)

        self.file_list_canvas = tk.Canvas(list_container, bg=Theme.BG_DARK,
                                          highlightthickness=0, height=120)
        scrollbar = tk.Scrollbar(list_container, orient="vertical",
                                command=self.file_list_canvas.yview)
        self.file_list_frame = tk.Frame(self.file_list_canvas, bg=Theme.BG_DARK)

        self.file_list_frame.bind("<Configure>",
            lambda e: self.file_list_canvas.configure(scrollregion=self.file_list_canvas.bbox("all")))

        self.file_list_canvas.create_window((0, 0), window=self.file_list_frame, anchor="nw")
        self.file_list_canvas.configure(yscrollcommand=scrollbar.set)

        self.file_list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.update_file_list()

        # Disk visualization
        viz_frame = tk.Frame(main, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        viz_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(viz_frame, text="─── DISK ALLOCATION MAP ───", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(anchor='w')

        self.disk_canvas = tk.Canvas(viz_frame, height=250, bg=Theme.BG_DARK,
                                     highlightthickness=0)
        self.disk_canvas.pack(fill=tk.BOTH, expand=True, pady=10)

        # Stats section
        stats_frame = tk.Frame(main, bg=Theme.BG_SECONDARY, padx=15, pady=12)
        stats_frame.pack(fill=tk.X)
        
        tk.Label(stats_frame, text="─── STATISTICS ───", font=Theme.FONT_SMALL,
                 bg=Theme.BG_SECONDARY, fg=Theme.TEXT_DIM).pack(anchor='w')

        self.stats_label = tk.Label(stats_frame, text="", font=Theme.FONT,
                                    bg=Theme.BG_SECONDARY, fg=Theme.SUCCESS)
        self.stats_label.pack(anchor='w', pady=5)

        self.draw_disk()
        self.update_stats()

    def create_file(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Enter a file name")
            return
        
        try:
            size = int(self.size_entry.get())
            if size <= 0:
                raise ValueError("Size must be positive")
        except ValueError as e:
            messagebox.showerror("Error", str(e) or "Enter valid size")
            return

        allocation = self.alloc_var.get()
        success, file_obj = self.simulator.add_file(name, size, allocation)
        
        if success:
            self.name_entry.delete(0, tk.END)
            self.update_file_list()
            self.draw_disk()
            self.update_stats()
        else:
            messagebox.showerror("Error", "Not enough contiguous/free space")

    def delete_file(self, file_id):
        if messagebox.askyesno("Confirm", "Delete this file?"):
            self.simulator.delete_file(file_id)
            self.update_file_list()
            self.draw_disk()
            self.update_stats()

    def generate_random(self):
        self.clear_all()
        methods = ["Contiguous", "Linked", "Indexed"]
        n = random.randint(4, 6)
        
        for i in range(n):
            name = f"file{i+1}.txt"
            size = random.randint(2, 5)
            method = random.choice(methods)
            self.simulator.add_file(name, size, method)
        
        self.update_file_list()
        self.draw_disk()
        self.update_stats()

    def clear_all(self):
        self.simulator = FileAllocationSimulator(50)
        self.update_file_list()
        self.draw_disk()
        self.update_stats()

    def update_file_list(self):
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()

        if not self.simulator.files:
            tk.Label(self.file_list_frame, text="No files created yet",
                     font=Theme.FONT_SMALL, bg=Theme.BG_DARK,
                     fg=Theme.TEXT_DIM).pack()
            return

        # Header
        header = tk.Frame(self.file_list_frame, bg=Theme.BG_TERTIARY)
        header.pack(fill=tk.X)
        headers = ["ID", "Name", "Size", "Type", "Location", "Action"]
        for h in headers:
            tk.Label(header, text=h, font=Theme.FONT_BOLD,
                     bg=Theme.BG_TERTIARY, fg=Theme.ACCENT,
                     width=10).pack(side=tk.LEFT, padx=2)

        # Files
        colors = ['#00d4aa', '#3fb950', '#d29922', '#f85149', '#a371f7', '#79c0ff']
        for file_obj in self.simulator.files:
            row = tk.Frame(self.file_list_frame, bg=Theme.BG_DARK)
            row.pack(fill=tk.X, pady=1)

            color = colors[(file_obj.file_id - 1) % len(colors)]
            
            # Color indicator
            tk.Label(row, text="●", font=Theme.FONT,
                     bg=Theme.BG_DARK, fg=color, width=10).pack(side=tk.LEFT, padx=2)
            
            tk.Label(row, text=file_obj.name, font=Theme.FONT,
                     bg=Theme.BG_DARK, fg=Theme.TEXT, width=10).pack(side=tk.LEFT, padx=2)
            
            tk.Label(row, text=f"{file_obj.size}B", font=Theme.FONT,
                     bg=Theme.BG_DARK, fg=Theme.TEXT, width=10).pack(side=tk.LEFT, padx=2)
            
            tk.Label(row, text=file_obj.allocation_type, font=Theme.FONT_SMALL,
                     bg=Theme.BG_DARK, fg=Theme.TEXT_DIM, width=10).pack(side=tk.LEFT, padx=2)
            
            # Location info
            if file_obj.allocation_type == "Contiguous":
                loc = f"{file_obj.start_block}-{file_obj.start_block + file_obj.size - 1}"
            elif file_obj.allocation_type == "Indexed":
                loc = f"I:{file_obj.index_block}"
            else:
                loc = f"S:{file_obj.start_block}"
            
            tk.Label(row, text=loc, font=Theme.FONT,
                     bg=Theme.BG_DARK, fg=Theme.ACCENT, width=10).pack(side=tk.LEFT, padx=2)
            
            tk.Button(row, text="Delete", font=Theme.FONT_SMALL,
                      bg=Theme.BG_TERTIARY, fg=Theme.ERROR, bd=0,
                      padx=8, pady=2, cursor='hand2',
                      command=lambda fid=file_obj.file_id: self.delete_file(fid)
                      ).pack(side=tk.LEFT, padx=2)

    def draw_disk(self):
        self.disk_canvas.delete("all")
        
        canvas_width = self.disk_canvas.winfo_width() - 40 or 900
        canvas_height = self.disk_canvas.winfo_height() - 40 or 210
        
        blocks_per_row = 10
        rows = (self.simulator.disk_size + blocks_per_row - 1) // blocks_per_row
        
        block_width = canvas_width / blocks_per_row
        block_height = canvas_height / rows
        
        colors = ['#00d4aa', '#3fb950', '#d29922', '#f85149', '#a371f7', '#79c0ff']
        
        x_offset = 20
        y_offset = 20
        
        for i in range(self.simulator.disk_size):
            row = i // blocks_per_row
            col = i % blocks_per_row
            
            x = x_offset + col * block_width
            y = y_offset + row * block_height
            
            block = self.simulator.disk[i]
            
            if block is None:
                # Free block
                fill_color = Theme.BG_TERTIARY
                text_color = Theme.TEXT_DIM
                text = str(i)
            else:
                # Occupied block
                fill_color = colors[(block.file_id - 1) % len(colors)]
                text_color = Theme.BG_DARK
                
                if block.is_index:
                    text = f"I{block.file_id}"
                else:
                    text = f"F{block.file_id}"
            
            # Draw block
            self.disk_canvas.create_rectangle(
                x, y, x + block_width - 2, y + block_height - 2,
                fill=fill_color, outline=Theme.BORDER, width=1
            )
            
            # Draw text
            self.disk_canvas.create_text(
                x + block_width/2 - 1, y + block_height/2 - 1,
                text=text, font=Theme.FONT_SMALL, fill=text_color
            )
            
            # Draw link arrows for linked allocation
            if block and block.next_block is not None:
                next_row = block.next_block // blocks_per_row
                next_col = block.next_block % blocks_per_row
                next_x = x_offset + next_col * block_width + block_width/2
                next_y = y_offset + next_row * block_height + block_height/2
                curr_x = x + block_width/2
                curr_y = y + block_height/2
                
                self.disk_canvas.create_line(
                    curr_x, curr_y, next_x, next_y,
                    arrow=tk.LAST, fill=Theme.WARNING, width=2
                )

    def update_stats(self):
        total_blocks = self.simulator.disk_size
        used_blocks = sum(1 for b in self.simulator.disk if b is not None)
        free_blocks, fragments = self.simulator.get_fragmentation()
        
        utilization = (used_blocks / total_blocks * 100) if total_blocks > 0 else 0
        
        stats_text = (f"Total Files: {len(self.simulator.files)} | "
                     f"Used Blocks: {used_blocks}/{total_blocks} | "
                     f"Free Blocks: {free_blocks} | "
                     f"Fragments: {fragments} | "
                     f"Utilization: {utilization:.1f}%")
        
        self.stats_label.config(text=stats_text)

def open_file_management(parent_frame):
    FileManagementGUI(parent_frame)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Management – Standalone")
    root.geometry("1000x750")
    root.configure(bg=Theme.BG_DARK)
    FileManagementGUI(root)
    root.mainloop()

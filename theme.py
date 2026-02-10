class Theme:
    BG_DARK       = '#0d1117'   
    BG_SECONDARY  = '#161b22'    
    BG_TERTIARY   = '#21262d'   
    BG_INPUT      = '#0d1117'
    
    ACCENT        = '#00d4aa'    
    TEXT          = '#e6edf3'
    TEXT_DIM      = '#8b949e'
    BORDER        = '#30363d'
    
    SUCCESS       = '#3fb950'
    WARNING       = '#d29922'
    ERROR         = '#f85149'

    FONT         = ('Consolas', 11)
    FONT_BOLD    = ('Consolas', 11, 'bold')
    FONT_SMALL   = ('Consolas', 10)
    FONT_TITLE   = ('Consolas', 14, 'bold')
    FONT_HEADER  = ('Consolas', 16, 'bold')
    
    @staticmethod
    def setup_scrollbar_style(root):
        """Setup custom scrollbar style matching the dark theme"""
        from tkinter import ttk
        style = ttk.Style()
        
        # Configure the scrollbar colors
        style.theme_use('clam')  # Use clam theme as base (more customizable)
        
        style.configure("Dark.Vertical.TScrollbar",
            background='#21262d',
            troughcolor='#0d1117',
            bordercolor='#30363d',
            arrowcolor='#8b949e',
            relief='flat'
        )
        style.map("Dark.Vertical.TScrollbar",
            background=[('active', '#00d4aa'), ('pressed', '#00d4aa')],
            arrowcolor=[('active', '#e6edf3')]
        )
        
        style.configure("Dark.Horizontal.TScrollbar",
            background='#21262d',
            troughcolor='#0d1117',
            bordercolor='#30363d',
            arrowcolor='#8b949e',
            relief='flat'
        )
        style.map("Dark.Horizontal.TScrollbar",
            background=[('active', '#00d4aa'), ('pressed', '#00d4aa')],
            arrowcolor=[('active', '#e6edf3')]
        )
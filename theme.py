# theme.py
"""
Shared dark terminal / GitHub-inspired theme for Mini OS Simulator
"""

class Theme:
    # ── Colors ───────────────────────────────────────────────────────
    BG_DARK       = '#0d1117'     # main background
    BG_SECONDARY  = '#161b22'     # panels, cards
    BG_TERTIARY   = '#21262d'     # headers, buttons
    BG_INPUT      = '#0d1117'
    
    ACCENT        = '#00d4aa'     # main highlight color
    TEXT          = '#e6edf3'
    TEXT_DIM      = '#8b949e'
    BORDER        = '#30363d'
    
    SUCCESS       = '#3fb950'
    WARNING       = '#d29922'
    ERROR         = '#f85149'

    # ── Fonts ────────────────────────────────────────────────────────
    FONT         = ('Consolas', 11)
    FONT_BOLD    = ('Consolas', 11, 'bold')
    FONT_SMALL   = ('Consolas', 10)
    FONT_TITLE   = ('Consolas', 14, 'bold')
    FONT_HEADER  = ('Consolas', 16, 'bold')
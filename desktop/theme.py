COLORS = {
    'background': '#03045e',
    'card': '#023e8a',
    'border': '#0077b6',
    'primary': '#00b4d8',
    'text': '#caf0f8',
    'muted': '#90e0ef',
    'success': '#06ffa5',
    'warning': '#ffd60a',
    'error': '#ff6b6b'
}

CHART_COLORS = ['#00b4d8', '#06ffa5', '#ffd60a', '#0077b6', '#90e0ef', '#48cae4', '#023e8a', '#caf0f8']

BASE_THEME = f"""
QWidget {{
    background-color: {COLORS['background']};
    color: {COLORS['text']};
    font-family: Consolas, monospace;
}}
QLabel {{
    color: {COLORS['text']};
    font-size: 13px;
}}
QLabel#title {{
    font-size: 18px;
    font-weight: bold;
    color: {COLORS['primary']};
    padding: 10px 0;
}}
QPushButton {{
    background-color: {COLORS['border']};
    color: {COLORS['text']};
    border: none;
    padding: 12px 24px;
    font-size: 13px;
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: {COLORS['primary']};
}}
QPushButton:pressed {{
    background-color: {COLORS['card']};
}}
QPushButton:disabled {{
    background-color: #555555;
    color: #888888;
}}
QGroupBox {{
    background-color: {COLORS['card']};
    border: 2px solid {COLORS['border']};
    margin-top: 20px;
    padding: 20px;
    font-size: 14px;
    font-weight: bold;
}}
QGroupBox::title {{
    color: {COLORS['primary']};
    subcontrol-origin: margin;
    left: 20px;
    padding: 0 10px;
}}
"""

UPLOAD_THEME = BASE_THEME + f"""
QLabel#filename {{
    color: {COLORS['muted']};
    padding: 8px;
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
}}
QLabel#stat-name {{
    color: {COLORS['muted']};
    font-size: 14px;
    padding: 12px 16px;
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
}}
QLabel#stat-value {{
    color: {COLORS['success']};
    font-weight: bold;
    font-size: 14px;
    padding: 12px 16px;
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    min-width: 100px;
}}
QPushButton#browse {{
    background-color: transparent;
    border: 2px solid {COLORS['border']};
    padding: 10px 20px;
}}
QPushButton#browse:hover {{
    background-color: {COLORS['card']};
    border-color: {COLORS['primary']};
}}
QFrame#stat-row {{
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
}}
"""

HISTORY_THEME = BASE_THEME + f"""
QLabel#loading {{
    color: {COLORS['primary']};
    font-size: 14px;
    padding: 20px;
}}
QLabel#error {{
    color: {COLORS['error']};
    font-size: 13px;
    padding: 8px;
}}
QPushButton#refresh {{
    background-color: transparent;
    border: 2px solid {COLORS['border']};
    padding: 8px 16px;
}}
QPushButton#refresh:hover {{
    background-color: {COLORS['card']};
    border-color: {COLORS['primary']};
}}
QTableWidget {{
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    gridline-color: {COLORS['border']};
    selection-background-color: {COLORS['border']};
    outline: none;
}}
QTableWidget::item {{
    padding: 12px;
    border-bottom: 1px solid {COLORS['border']};
}}
QTableWidget::item:selected {{
    background-color: {COLORS['border']};
    border: none;
    outline: none;
}}
QTableWidget::item:focus {{
    background-color: {COLORS['border']};
    border: none;
    outline: none;
}}
QHeaderView::section {{
    background-color: {COLORS['background']};
    color: {COLORS['muted']};
    padding: 12px;
    border: none;
    border-bottom: 2px solid {COLORS['border']};
    font-weight: bold;
    text-transform: uppercase;
}}
"""

CHARTS_THEME = BASE_THEME + f"""
QLabel#loading {{
    color: {COLORS['primary']};
    font-size: 14px;
    padding: 40px;
}}
"""

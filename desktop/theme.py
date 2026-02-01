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
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 15px;
}}
QLabel {{
    color: {COLORS['text']};
    font-size: 15px;
}}
QLabel#title {{
    font-size: 22px;
    font-weight: bold;
    color: {COLORS['primary']};
    padding: 12px 0;
}}
QPushButton {{
    background-color: {COLORS['primary']};
    color: {COLORS['background']};
    border: none;
    border-radius: 4px;
    padding: 14px 28px;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 0.5px;
}}
QPushButton:hover {{
    background-color: #0096c7;
}}
QPushButton:pressed {{
    background-color: {COLORS['card']};
}}
QPushButton:disabled {{
    background-color: #555555;
    color: #888888;
    qproperty-alignment: AlignCenter;
}}
QGroupBox {{
    background-color: {COLORS['card']};
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    margin-top: 24px;
    padding: 24px;
    font-size: 16px;
    font-weight: bold;
}}
QGroupBox::title {{
    color: {COLORS['primary']};
    subcontrol-origin: margin;
    left: 20px;
    padding: 0 12px;
}}
"""

UPLOAD_THEME = BASE_THEME + f"""
QLabel#filename {{
    color: {COLORS['muted']};
    padding: 12px;
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    font-size: 14px;
}}
QLabel#stat-name {{
    color: {COLORS['muted']};
    font-size: 15px;
    padding: 14px 18px;
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
}}
QLabel#stat-value {{
    color: {COLORS['success']};
    font-weight: bold;
    font-size: 16px;
    padding: 14px 18px;
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    min-width: 120px;
}}
QPushButton#browse {{
    background-color: transparent;
    border: 2px solid {COLORS['border']};
    color: {COLORS['text']};
    padding: 12px 24px;
}}
QPushButton#browse:hover {{
    background-color: {COLORS['card']};
    border-color: {COLORS['primary']};
}}
QFrame#stat-row {{
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
}}
"""

HISTORY_THEME = BASE_THEME + f"""
QLabel#loading {{
    color: {COLORS['primary']};
    font-size: 16px;
    padding: 24px;
}}
QLabel#error {{
    color: {COLORS['error']};
    font-size: 15px;
    padding: 12px;
}}
QPushButton#refresh {{
    background-color: transparent;
    border: 2px solid {COLORS['border']};
    color: {COLORS['text']};
    padding: 10px 20px;
}}
QPushButton#refresh:hover {{
    background-color: {COLORS['card']};
    border-color: {COLORS['primary']};
}}
QLabel#storage {{
    color: {COLORS['primary']};
    font-size: 14px;
    font-weight: bold;
    padding: 8px 16px;
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    background-color: rgba(0, 180, 216, 0.1);
    letter-spacing: 2px;
}}
QTableWidget {{
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    gridline-color: {COLORS['border']};
    selection-background-color: {COLORS['border']};
    outline: none;
    font-size: 14px;
}}
QTableWidget QPushButton {{
    background-color: {COLORS['primary']};
    color: {COLORS['background']};
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: bold;
    min-width: 100px;
}}
QTableWidget QPushButton:hover {{
    background-color: #0096c7;
}}
QTableWidget QPushButton:disabled {{
    background-color: #555555;
    color: #888888;
}}
QTableWidget::item {{
    padding: 14px;
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
    padding: 14px;
    border: none;
    border-bottom: 2px solid {COLORS['primary']};
    font-weight: bold;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}
"""

CHARTS_THEME = BASE_THEME + f"""
QLabel#loading {{
    color: {COLORS['primary']};
    font-size: 16px;
    padding: 48px;
}}
"""

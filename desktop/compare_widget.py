from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QFrame, QGridLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from theme import COLORS
from worker import HistoryWorker, CompareWorker


COMPARE_STYLE = f"""
QWidget {{
    background-color: {COLORS['background']};
    color: {COLORS['text']};
    font-family: 'JetBrains Mono', Consolas, monospace;
}}
QLabel#title {{
    font-size: 28px;
    font-weight: bold;
    color: {COLORS['primary']};
    letter-spacing: 2px;
    padding: 8px 0;
}}
QLabel#subtitle {{
    font-size: 16px;
    color: {COLORS['muted']};
    letter-spacing: 1px;
}}
QComboBox {{
    background-color: {COLORS['card']};
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    padding: 14px 20px;
    color: {COLORS['text']};
    font-size: 16px;
    min-width: 300px;
}}
QComboBox:hover {{
    border-color: {COLORS['primary']};
}}
QComboBox::drop-down {{
    border: none;
    padding-right: 12px;
}}
QComboBox QAbstractItemView {{
    background-color: {COLORS['card']};
    border: 2px solid {COLORS['border']};
    selection-background-color: {COLORS['primary']};
    selection-color: {COLORS['background']};
    padding: 4px;
}}
QLabel#vs {{
    color: {COLORS['warning']};
    font-size: 22px;
    font-weight: bold;
    padding: 0 24px;
    letter-spacing: 2px;
}}
QPushButton#compare {{
    background-color: {COLORS['primary']};
    color: {COLORS['background']};
    border: none;
    border-radius: 6px;
    padding: 16px 40px;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 1px;
}}
QPushButton#compare:hover {{
    background-color: #0096c7;
}}
QPushButton#compare:disabled {{
    background-color: #555555;
    color: #888888;
}}
QFrame#results-container {{
    background-color: {COLORS['card']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 24px;
    margin-top: 20px;
}}
QFrame#diff-card {{
    background-color: {COLORS['background']};
    border: 2px solid {COLORS['border']};
    border-radius: 10px;
    padding: 28px;
    min-width: 200px;
}}
QLabel#card-title {{
    color: {COLORS['muted']};
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 1.5px;
    padding-bottom: 10px;
}}
QLabel#card-value {{
    font-size: 42px;
    font-weight: bold;
    padding: 8px 0;
}}
QLabel#positive {{
    color: {COLORS['success']};
}}
QLabel#negative {{
    color: {COLORS['error']};
}}
QLabel#neutral {{
    color: {COLORS['warning']};
}}
QLabel#loading {{
    color: {COLORS['primary']};
    font-size: 18px;
    padding: 20px;
}}
QLabel#error {{
    color: {COLORS['error']};
    font-size: 16px;
    padding: 10px;
}}
QLabel#results-title {{
    color: {COLORS['primary']};
    font-size: 18px;
    font-weight: bold;
    letter-spacing: 1px;
    padding-bottom: 20px;
}}
QLabel#dataset-info {{
    color: {COLORS['muted']};
    font-size: 14px;
    padding-top: 12px;
}}
"""


class DiffCard(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setObjectName("diff-card")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(4)
        
        self.title_label = QLabel(title.upper())
        self.title_label.setObjectName("card-title")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        self.value_label = QLabel("--")
        self.value_label.setObjectName("card-value")
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)
        
        self.unit_label = QLabel("")
        self.unit_label.setObjectName("card-title")
        self.unit_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.unit_label)
        
    def set_value(self, value, unit=""):
        prefix = "+" if value > 0 else ""
        self.value_label.setText(f"{prefix}{value}")
        self.unit_label.setText(unit)
        
        if value > 0:
            self.value_label.setStyleSheet(f"color: {COLORS['success']}; font-size: 42px; font-weight: bold;")
        elif value < 0:
            self.value_label.setStyleSheet(f"color: {COLORS['error']}; font-size: 42px; font-weight: bold;")
        else:
            self.value_label.setStyleSheet(f"color: {COLORS['warning']}; font-size: 42px; font-weight: bold;")


class CompareWidget(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.datasets = []
        self.history_worker = None
        self.compare_worker = None
        self.setStyleSheet(COMPARE_STYLE)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(20)
        
        header = QVBoxLayout()
        title = QLabel("DATASET COMPARISON")
        title.setObjectName("title")
        header.addWidget(title)
        
        subtitle = QLabel("Compare parameter averages between two datasets")
        subtitle.setObjectName("subtitle")
        header.addWidget(subtitle)
        layout.addLayout(header)
        
        layout.addSpacing(8)
        
        selector_layout = QHBoxLayout()
        selector_layout.setSpacing(0)
        
        ds1_container = QVBoxLayout()
        ds1_container.setSpacing(6)
        ds1_label = QLabel("DATASET A")
        ds1_label.setObjectName("card-title")
        ds1_container.addWidget(ds1_label)
        self.combo1 = QComboBox()
        ds1_container.addWidget(self.combo1)
        selector_layout.addLayout(ds1_container)
        
        vs_label = QLabel("VS")
        vs_label.setObjectName("vs")
        vs_label.setAlignment(Qt.AlignCenter)
        selector_layout.addWidget(vs_label)
        
        ds2_container = QVBoxLayout()
        ds2_container.setSpacing(6)
        ds2_label = QLabel("DATASET B")
        ds2_label.setObjectName("card-title")
        ds2_container.addWidget(ds2_label)
        self.combo2 = QComboBox()
        ds2_container.addWidget(self.combo2)
        selector_layout.addLayout(ds2_container)
        
        selector_layout.addSpacing(24)
        
        btn_container = QVBoxLayout()
        btn_container.addSpacing(18)
        self.compare_btn = QPushButton("COMPARE")
        self.compare_btn.setObjectName("compare")
        self.compare_btn.clicked.connect(self.run_comparison)
        btn_container.addWidget(self.compare_btn)
        selector_layout.addLayout(btn_container)
        
        selector_layout.addStretch()
        layout.addLayout(selector_layout)
        
        self.loading_label = QLabel("Loading datasets...")
        self.loading_label.setObjectName("loading")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.hide()
        layout.addWidget(self.loading_label)
        
        self.error_label = QLabel("")
        self.error_label.setObjectName("error")
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        self.results_frame = QFrame()
        self.results_frame.setObjectName("results-container")
        self.results_frame.hide()
        results_layout = QVBoxLayout(self.results_frame)
        results_layout.setContentsMargins(24, 24, 24, 24)
        results_layout.setSpacing(20)
        
        results_title = QLabel("PARAMETER DIFFERENCES (A − B)")
        results_title.setObjectName("results-title")
        results_layout.addWidget(results_title)
        
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        self.flowrate_card = DiffCard("Flowrate")
        cards_layout.addWidget(self.flowrate_card)
        
        self.pressure_card = DiffCard("Pressure")
        cards_layout.addWidget(self.pressure_card)
        
        self.temperature_card = DiffCard("Temperature")
        cards_layout.addWidget(self.temperature_card)
        
        cards_layout.addStretch()
        results_layout.addLayout(cards_layout)
        
        self.info_label = QLabel("")
        self.info_label.setObjectName("dataset-info")
        results_layout.addWidget(self.info_label)
        
        layout.addWidget(self.results_frame)
        
        layout.addStretch()
        self.setLayout(layout)
        self.load_datasets()
        
    def load_datasets(self):
        self.combo1.clear()
        self.combo2.clear()
        self.loading_label.show()
        self.error_label.hide()
        
        self.history_worker = HistoryWorker(self.token)
        self.history_worker.success.connect(self.on_datasets_loaded)
        self.history_worker.error.connect(self.on_load_error)
        self.history_worker.start()
        
    def on_datasets_loaded(self, data):
        self.loading_label.hide()
        self.datasets = data or []
        
        for ds in self.datasets:
            label = ds.get('filename', 'Dataset')
            self.combo1.addItem(label, ds.get('id'))
            self.combo2.addItem(label, ds.get('id'))
            
        if len(self.datasets) >= 2:
            self.combo2.setCurrentIndex(1)
            
        if len(self.datasets) < 2:
            self.error_label.setText("Upload at least 2 datasets to compare.")
            self.error_label.show()
            self.compare_btn.setEnabled(False)
            
    def on_load_error(self, message):
        self.loading_label.hide()
        self.error_label.setText(f"Error: {message}")
        self.error_label.show()
        
    def run_comparison(self):
        id1 = self.combo1.currentData()
        id2 = self.combo2.currentData()
        
        if not id1 or not id2:
            self.error_label.setText("Select both datasets.")
            self.error_label.show()
            return
            
        if id1 == id2:
            self.error_label.setText("Select two different datasets.")
            self.error_label.show()
            return
            
        self.error_label.hide()
        self.results_frame.hide()
        self.compare_btn.setEnabled(False)
        self.compare_btn.setText("COMPARING...")
        
        self.compare_worker = CompareWorker(id1, id2, self.token)
        self.compare_worker.success.connect(self.on_compare_success)
        self.compare_worker.error.connect(self.on_compare_error)
        self.compare_worker.start()
        
    def on_compare_success(self, data):
        self.compare_btn.setEnabled(True)
        self.compare_btn.setText("COMPARE")
        
        comparison = data.get("comparison", {})
        ds1 = data.get("dataset1", {})
        ds2 = data.get("dataset2", {})
        
        self.flowrate_card.set_value(comparison.get("flowrate_diff", 0), "L/min")
        self.pressure_card.set_value(comparison.get("pressure_diff", 0), "bar")
        self.temperature_card.set_value(comparison.get("temperature_diff", 0), "°C")
        
        info = f"Comparing: {ds1.get('filename', 'A')} vs {ds2.get('filename', 'B')}"
        self.info_label.setText(info)
        
        self.results_frame.show()
        
    def on_compare_error(self, message):
        self.compare_btn.setEnabled(True)
        self.compare_btn.setText("COMPARE")
        self.error_label.setText(f"Comparison failed: {message}")
        self.error_label.show()
        
    def refresh(self):
        self.load_datasets()

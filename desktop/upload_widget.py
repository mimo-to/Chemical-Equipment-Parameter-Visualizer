from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFileDialog, QGroupBox, QGridLayout, QFrame
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

from logger import get_logger
from worker import UploadWorker

log = get_logger(__name__)

THEME = """
QWidget {
    background-color: #03045e;
    color: #caf0f8;
    font-family: Consolas, monospace;
}
QLabel {
    color: #caf0f8;
    font-size: 13px;
}
QLabel#title {
    font-size: 18px;
    font-weight: bold;
    color: #00b4d8;
    padding: 10px 0;
}
QLabel#filename {
    color: #90e0ef;
    padding: 8px;
    background-color: #023e8a;
    border: 1px solid #0077b6;
}
QLabel#stat-name {
    color: #90e0ef;
    font-size: 14px;
    padding: 12px 16px;
    background-color: #023e8a;
    border: 1px solid #0077b6;
}
QLabel#stat-value {
    color: #06ffa5;
    font-weight: bold;
    font-size: 14px;
    padding: 12px 16px;
    background-color: #023e8a;
    border: 1px solid #0077b6;
    min-width: 100px;
}
QPushButton {
    background-color: #0077b6;
    color: #caf0f8;
    border: none;
    padding: 12px 24px;
    font-size: 13px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #00b4d8;
}
QPushButton:pressed {
    background-color: #023e8a;
}
QPushButton:disabled {
    background-color: #555555;
    color: #888888;
}
QPushButton#browse {
    background-color: transparent;
    border: 2px solid #0077b6;
    padding: 10px 20px;
}
QPushButton#browse:hover {
    background-color: #023e8a;
    border-color: #00b4d8;
}
QGroupBox {
    background-color: #023e8a;
    border: 2px solid #0077b6;
    margin-top: 20px;
    padding: 20px;
    font-size: 14px;
    font-weight: bold;
}
QGroupBox::title {
    color: #00b4d8;
    subcontrol-origin: margin;
    left: 20px;
    padding: 0 10px;
}
QFrame#stat-row {
    background-color: #023e8a;
    border: 1px solid #0077b6;
}
"""


class UploadWidget(QWidget):
    upload_success = pyqtSignal(int)
    
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.filepath = None
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet(THEME)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Data Acquisition")
        title.setObjectName("title")
        layout.addWidget(title)
        
        # File selection row
        file_row = QHBoxLayout()
        file_row.setSpacing(16)
        
        self.browse_btn = QPushButton("Select File")
        self.browse_btn.setObjectName("browse")
        self.browse_btn.setFixedWidth(140)
        self.browse_btn.clicked.connect(self.browse_file)
        file_row.addWidget(self.browse_btn)
        
        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("filename")
        file_row.addWidget(self.file_label, 1)
        
        self.upload_btn = QPushButton("Analyze")
        self.upload_btn.setFixedWidth(140)
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        file_row.addWidget(self.upload_btn)
        
        layout.addLayout(file_row)
        
        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ff6b6b; font-size: 13px; padding: 8px;")
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        # Stats group
        self.stats_group = QGroupBox("Analysis Results")
        self.stats_group.hide()
        
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(0)
        
        self.stat_labels = {}
        stats = [
            ("Total Records", "total_count"),
            ("Avg Flowrate", "avg_flowrate"),
            ("Avg Pressure", "avg_pressure"),
            ("Avg Temperature", "avg_temperature")
        ]
        
        for display_name, key in stats:
            row = QFrame()
            row.setObjectName("stat-row")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(0)
            
            name_label = QLabel(display_name)
            name_label.setObjectName("stat-name")
            row_layout.addWidget(name_label, 1)
            
            value_label = QLabel("--")
            value_label.setObjectName("stat-value")
            value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            row_layout.addWidget(value_label)
            
            stats_layout.addWidget(row)
            self.stat_labels[key] = value_label
            
        self.stats_group.setLayout(stats_layout)
        layout.addWidget(self.stats_group)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def browse_file(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if filepath:
            self.filepath = filepath
            # Handle both / and \ path separators
            filename = filepath.replace("\\", "/").split("/")[-1]
            self.file_label.setText(filename)
            self.upload_btn.setEnabled(True)
            self.error_label.hide()
            
    def upload_file(self):
        if not self.filepath:
            return
            
        self.set_loading(True)
        self.error_label.hide()
        self.stats_group.hide()
        
        self.worker = UploadWorker(self.filepath, self.token)
        self.worker.success.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()
        
    def on_success(self, data):
        log.info(f"Upload successful: {data}")
        
        self.stat_labels["total_count"].setText(str(data.get("total_count", 0)))
        self.stat_labels["avg_flowrate"].setText(f"{data.get('avg_flowrate', 0):.2f}")
        self.stat_labels["avg_pressure"].setText(f"{data.get('avg_pressure', 0):.2f}")
        self.stat_labels["avg_temperature"].setText(f"{data.get('avg_temperature', 0):.2f}")
        
        self.stats_group.show()
        self.set_loading(False)
        
        if "id" in data:
            self.upload_success.emit(data["id"])
            
    def on_error(self, message):
        log.error(f"Upload failed: {message}")
        self.error_label.setText(f"Error: {message}")
        self.error_label.show()
        self.set_loading(False)
        
    def set_loading(self, loading):
        self.browse_btn.setEnabled(not loading)
        self.upload_btn.setEnabled(not loading and self.filepath is not None)
        self.upload_btn.setText("Processing..." if loading else "Analyze")

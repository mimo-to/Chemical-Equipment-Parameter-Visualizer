from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFileDialog, QGroupBox, QFrame
)
from PyQt5.QtCore import pyqtSignal, Qt

from theme import UPLOAD_THEME
from worker import UploadWorker


class UploadWidget(QWidget):
    upload_success = pyqtSignal(int)
    
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.filepath = None
        self.worker = None
        self.setStyleSheet(UPLOAD_THEME)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("Data Acquisition")
        title.setObjectName("title")
        layout.addWidget(title)
        
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
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ff6b6b; font-size: 13px; padding: 8px;")
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
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
        
        for name, key in stats:
            row = QFrame()
            row.setObjectName("stat-row")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(0)
            
            name_label = QLabel(name)
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
        self.stat_labels["total_count"].setText(str(data.get("total_count", 0)))
        self.stat_labels["avg_flowrate"].setText(f"{data.get('avg_flowrate', 0):.2f}")
        self.stat_labels["avg_pressure"].setText(f"{data.get('avg_pressure', 0):.2f}")
        self.stat_labels["avg_temperature"].setText(f"{data.get('avg_temperature', 0):.2f}")
        
        self.stats_group.show()
        self.set_loading(False)
        
        if "id" in data:
            self.upload_success.emit(data["id"])
            
    def on_error(self, message):
        self.error_label.setText(f"Error: {message}")
        self.error_label.show()
        self.set_loading(False)
        
    def set_loading(self, loading):
        self.browse_btn.setEnabled(not loading)
        self.upload_btn.setEnabled(not loading and self.filepath is not None)
        self.upload_btn.setText("Processing..." if loading else "Analyze")

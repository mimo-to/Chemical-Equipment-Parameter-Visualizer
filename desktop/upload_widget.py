from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFileDialog, QGroupBox, QFrame, QToolTip
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from theme import UPLOAD_THEME
from worker import UploadWorker

ERROR_TIPS = {
    'file too large': 'Try splitting your data into smaller files or removing unnecessary rows.',
    'invalid file type': 'Save your spreadsheet as CSV (comma-separated values).',
    'missing columns': 'Required: Equipment Name, Type, Flowrate, Pressure, Temperature.',
    'unexpected columns': 'Remove extra columns. Only the 5 required columns are allowed.',
    'empty': 'Add data rows below the header line. See sample_equipment_data.csv.',
    'invalid numeric': 'Ensure values are numbers (e.g., 10.5). Remove text or special characters.',
    'connection error': 'Check your internet connection and try again.',
}


class UploadWidget(QWidget):
    upload_success = pyqtSignal(int)
    
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.filepath = None
        self.worker = None
        self.setStyleSheet(UPLOAD_THEME)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(36, 36, 36, 36)
        layout.setSpacing(24)
        
        title = QLabel("DATA ACQUISITION")
        title.setObjectName("title")
        layout.addWidget(title)
        
        file_row = QHBoxLayout()
        file_row.setSpacing(16)
        
        self.browse_btn = QPushButton("SELECT FILE")
        self.browse_btn.setObjectName("browse")
        self.browse_btn.setFixedWidth(160)
        self.browse_btn.clicked.connect(self.browse_file)
        file_row.addWidget(self.browse_btn)
        
        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("filename")
        file_row.addWidget(self.file_label, 1)
        
        self.upload_btn = QPushButton("ANALYZE")
        self.upload_btn.setFixedWidth(180)
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        file_row.addWidget(self.upload_btn)
        
        layout.addLayout(file_row)
        
        self.error_frame = QFrame()
        self.error_frame.setObjectName("error-frame")
        self.error_frame.setStyleSheet("""
            QFrame#error-frame {
                background: rgba(214, 40, 40, 0.15);
                border: 1px solid #d62828;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        error_layout = QVBoxLayout(self.error_frame)
        error_layout.setContentsMargins(12, 12, 12, 12)
        error_layout.setSpacing(8)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ff6b6b; font-size: 14px; font-weight: bold;")
        self.error_label.setWordWrap(True)
        error_layout.addWidget(self.error_label)
        
        self.error_tip_label = QLabel("")
        self.error_tip_label.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        self.error_tip_label.setWordWrap(True)
        error_layout.addWidget(self.error_tip_label)
        
        self.error_frame.hide()
        layout.addWidget(self.error_frame)
        
        self.stats_group = QGroupBox("ANALYSIS RESULTS")
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
            self.file_label.setText(filepath.replace("\\", "/").split("/")[-1])
            self.upload_btn.setEnabled(True)
            self.error_frame.hide()
            
    def upload_file(self):
        if not self.filepath:
            return
            
        self.set_loading(True)
        self.error_frame.hide()
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
        tip = self._get_error_tip(message)
        self.error_tip_label.setText(f"💡 {tip}" if tip else "")
        self.error_tip_label.setVisible(bool(tip))
        self.error_frame.show()
        self.set_loading(False)
    
    def _get_error_tip(self, message):
        msg_lower = message.lower()
        for key, tip in ERROR_TIPS.items():
            if key in msg_lower:
                return tip
        return "Check your CSV format matches sample_equipment_data.csv"
        
    def set_loading(self, loading):
        self.browse_btn.setEnabled(not loading)
        self.upload_btn.setEnabled(not loading and self.filepath is not None)
        self.upload_btn.setText("PROCESSING..." if loading else "ANALYZE")

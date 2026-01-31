from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QHBoxLayout, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from logger import get_logger
from worker import HistoryWorker, DownloadWorker

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
QLabel#loading {
    color: #90e0ef;
    font-size: 14px;
    padding: 20px;
}
QLabel#empty {
    color: #90e0ef;
    font-size: 14px;
    font-style: italic;
    padding: 40px;
}
QTableWidget {
    background-color: #023e8a;
    border: 2px solid #0077b6;
    gridline-color: #0077b6;
    font-size: 13px;
}
QTableWidget::item {
    padding: 12px;
    border-bottom: 1px solid #0077b6;
}
QTableWidget::item:selected {
    background-color: #0077b6;
    border: none;
    outline: none;
}
QTableWidget::item:focus {
    background-color: #0077b6;
    border: none;
    outline: none;
}
QTableWidget {
    selection-background-color: #0077b6;
    outline: none;
}
QHeaderView::section {
    background-color: #03045e;
    color: #00b4d8;
    padding: 14px 12px;
    border: none;
    border-bottom: 3px solid #06ffa5;
    font-size: 13px;
    font-weight: bold;
}
QPushButton {
    background-color: #0077b6;
    color: #caf0f8;
    border: none;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #00b4d8;
}
QPushButton:disabled {
    background-color: #555555;
    color: #888888;
}
QPushButton#refresh {
    padding: 10px 24px;
    font-size: 13px;
}
"""


class HistoryWidget(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.worker = None
        self.download_worker = None
        self.downloading_id = None
        self.init_ui()
        self.refresh()
        
    def init_ui(self):
        self.setStyleSheet(THEME)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header row
        header = QHBoxLayout()
        
        title = QLabel("Experiment Log (Last 5)")
        title.setObjectName("title")
        header.addWidget(title)
        
        header.addStretch()
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setObjectName("refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        header.addWidget(self.refresh_btn)
        
        layout.addLayout(header)
        
        # Loading label
        self.loading_label = QLabel("Loading experiment log...")
        self.loading_label.setObjectName("loading")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.hide()
        layout.addWidget(self.loading_label)
        
        # Empty label
        self.empty_label = QLabel("No experiments recorded yet.")
        self.empty_label.setObjectName("empty")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.hide()
        layout.addWidget(self.empty_label)
        
        # History table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Filename", "Timestamp", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.horizontalHeader().resizeSection(2, 150)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
        
        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ff6b6b; font-size: 13px; padding: 8px;")
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        self.setLayout(layout)
        
    def refresh(self):
        self.loading_label.show()
        self.empty_label.hide()
        self.table.hide()
        self.error_label.hide()
        
        self.worker = HistoryWorker(self.token)
        self.worker.success.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()
        
    def on_success(self, data):
        self.loading_label.hide()
        
        if not data:
            self.empty_label.show()
            self.table.hide()
            return
            
        self.empty_label.hide()
        self.table.show()
        self.table.setRowCount(len(data))
        
        for row, item in enumerate(data):
            # Filename
            filename_item = QTableWidgetItem(item.get("filename", ""))
            filename_item.setData(Qt.UserRole, item.get("id"))
            self.table.setItem(row, 0, filename_item)
            
            # Timestamp - convert UTC to local
            from datetime import datetime, timezone
            timestamp = item.get("uploaded_at", "")
            try:
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                local_dt = dt.astimezone()  # Convert to local timezone
                formatted = local_dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted = timestamp
            self.table.setItem(row, 1, QTableWidgetItem(formatted))
            
            # Export button
            btn = QPushButton("Export PDF")
            btn.clicked.connect(lambda checked, id=item.get("id"): self.download(id))
            self.table.setCellWidget(row, 2, btn)
            
        # Adjust row heights
        self.table.resizeRowsToContents()
            
    def on_error(self, message):
        log.error(f"History load failed: {message}")
        self.loading_label.hide()
        self.error_label.setText(f"Error: {message}")
        self.error_label.show()
        
    def download(self, dataset_id):
        if self.downloading_id:
            return
        
        # Show file save dialog
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report",
            f"report_{dataset_id}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if not filepath:  # User cancelled
            return
            
        self.downloading_id = dataset_id
        self.save_filepath = filepath
        self.update_download_buttons()
        
        self.download_worker = DownloadWorker(dataset_id, self.token)
        self.download_worker.filepath = filepath  # Pass filepath to worker
        self.download_worker.success.connect(self.on_download_success)
        self.download_worker.error.connect(self.on_download_error)
        self.download_worker.start()
        
    def on_download_success(self, filepath):
        log.info(f"Report downloaded: {filepath}")
        self.downloading_id = None
        self.update_download_buttons()
        
    def on_download_error(self, message):
        log.error(f"Download failed: {message}")
        self.downloading_id = None
        self.update_download_buttons()
        self.error_label.setText(f"Download failed: {message}")
        self.error_label.show()
        
    def update_download_buttons(self):
        for row in range(self.table.rowCount()):
            btn = self.table.cellWidget(row, 2)
            item = self.table.item(row, 0)
            if btn and item:
                dataset_id = item.data(Qt.UserRole)
                if dataset_id == self.downloading_id:
                    btn.setText("Exporting...")
                    btn.setEnabled(False)
                else:
                    btn.setText("Export PDF")
                    btn.setEnabled(self.downloading_id is None)

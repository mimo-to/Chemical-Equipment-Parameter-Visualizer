from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QHBoxLayout, QFileDialog
)
from PyQt5.QtCore import Qt
from datetime import datetime
from theme import HISTORY_THEME
from worker import HistoryWorker, DownloadWorker


class HistoryWidget(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.worker = None
        self.download_worker = None
        self.downloading_id = None
        self.setStyleSheet(HISTORY_THEME)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(36, 36, 36, 36)
        layout.setSpacing(24)
        
        header = QHBoxLayout()
        title = QLabel("EXPERIMENT LOG (Last 5)")
        title.setObjectName("title")
        header.addWidget(title)
        header.addStretch()
        
        self.refresh_btn = QPushButton("REFRESH")
        self.refresh_btn.setObjectName("refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        header.addWidget(self.refresh_btn)
        layout.addLayout(header)
        
        self.loading_label = QLabel("Loading experiment log...")
        self.loading_label.setObjectName("loading")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.hide()
        layout.addWidget(self.loading_label)
        
        self.empty_label = QLabel("No experiments recorded yet.")
        self.empty_label.setObjectName("loading")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.hide()
        layout.addWidget(self.empty_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["FILENAME", "TIMESTAMP", "ACTIONS"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.horizontalHeader().resizeSection(2, 180)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setDefaultSectionSize(50)
        layout.addWidget(self.table)
        
        self.error_label = QLabel("")
        self.error_label.setObjectName("error")
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        self.setLayout(layout)
        self.refresh()
        
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
            filename_item = QTableWidgetItem(item.get("filename", ""))
            filename_item.setData(Qt.UserRole, item.get("id"))
            self.table.setItem(row, 0, filename_item)
            
            ts = item.get("uploaded_at", "")
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                formatted = dt.astimezone().strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted = ts
            self.table.setItem(row, 1, QTableWidgetItem(formatted))
            
            btn = QPushButton("EXPORT PDF")
            btn.clicked.connect(lambda _, id=item.get("id"): self.download(id))
            self.table.setCellWidget(row, 2, btn)
            
        self.table.resizeRowsToContents()
            
    def on_error(self, message):
        self.loading_label.hide()
        self.error_label.setText(f"Error: {message}")
        self.error_label.show()
        
    def download(self, dataset_id):
        if self.downloading_id:
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Report", f"report_{dataset_id}.pdf", "PDF Files (*.pdf)"
        )
        
        if not filepath:
            return
            
        self.downloading_id = dataset_id
        self.update_buttons()
        
        self.download_worker = DownloadWorker(dataset_id, self.token)
        self.download_worker.filepath = filepath
        self.download_worker.success.connect(self.on_download_success)
        self.download_worker.error.connect(self.on_download_error)
        self.download_worker.start()
        
    def on_download_success(self, filepath):
        self.downloading_id = None
        self.update_buttons()
        
    def on_download_error(self, message):
        self.downloading_id = None
        self.update_buttons()
        self.error_label.setText(f"Download failed: {message}")
        self.error_label.show()
        
    def update_buttons(self):
        for row in range(self.table.rowCount()):
            btn = self.table.cellWidget(row, 2)
            item = self.table.item(row, 0)
            if btn and item:
                dataset_id = item.data(Qt.UserRole)
                if dataset_id == self.downloading_id:
                    btn.setText("EXPORTING...")
                    btn.setEnabled(False)
                else:
                    btn.setText("EXPORT PDF")
                    btn.setEnabled(self.downloading_id is None)

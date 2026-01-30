import os
import requests
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import pyqtSignal, Qt
from worker import Worker

class UploadWidget(QWidget):
    upload_success = pyqtSignal(dict)

    def __init__(self, token):
        super().__init__()
        self.token = token
        self.file_path = None
        self.worker = None

        layout = QVBoxLayout()

        self.info_label = QLabel("Select a CSV file to analyze")
        layout.addWidget(self.info_label)

        self.select_button = QPushButton("Select CSV File")
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)

        self.selected_file_label = QLabel("No file selected")
        layout.addWidget(self.selected_file_label)

        self.upload_button = QPushButton("Upload and Analyze")
        self.upload_button.setEnabled(False)
        self.upload_button.clicked.connect(self.start_upload)
        layout.addWidget(self.upload_button)

        self.stats_label = QLabel("")
        font = self.stats_label.font()
        font.setPointSize(14)
        self.stats_label.setFont(font)
        layout.addWidget(self.stats_label)

        layout.addStretch()
        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.file_path = file_path
            self.selected_file_label.setText(f"Selected: {os.path.basename(file_path)}")
            self.upload_button.setEnabled(True)
            self.stats_label.setText("")

    def start_upload(self):
        if not self.file_path:
            return

        self.set_loading(True)
        self.worker = Worker(self.upload_task)
        self.worker.finished.connect(self.on_upload_finished)
        self.worker.error.connect(self.on_upload_error)
        self.worker.start()

    def upload_task(self):
        with open(self.file_path, 'rb') as f:
            files = {'file': f}
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.post(
                "http://127.0.0.1:8000/api/upload/",
                files=files,
                headers=headers,
                timeout=30 
            )
            return response

    def on_upload_finished(self, response):
        self.set_loading(False)
        if response.status_code == 201:
            try:
                data = response.json()
                self.show_stats(data)
                self.upload_success.emit(data)
                QMessageBox.information(self, "Success", "File uploaded successfully!")
            except ValueError:
                 QMessageBox.warning(self, "Error", "Invalid server response (not JSON).")
        else:
            error_msg = "Upload failed"
            try:
                data = response.json()
                error_msg = data.get('error', error_msg)
            except ValueError:
                pass
            
            if response.status_code == 413:
                error_msg = "File too large (Max 10MB)"
            elif response.status_code == 500:
                error_msg = "Internal server error. Please try again later."
                
            QMessageBox.warning(self, "Error", error_msg)

    def on_upload_error(self, error_msg):
        self.set_loading(False)
        QMessageBox.critical(self, "Network Error", f"Could not connect to server: {error_msg}")

    def set_loading(self, loading):
        self.select_button.setEnabled(not loading)
        self.upload_button.setEnabled(not loading)
        self.upload_button.setText("Uploading..." if loading else "Upload and Analyze")

        if loading:
            self.setCursor(Qt.WaitCursor)
        else:
            self.unsetCursor()

    def show_stats(self, data):
        stats = (
            f"Total Records: {data.get('total_count', 0)}\n"
            f"Avg Flowrate: {data.get('avg_flowrate', 0):.2f}\n"
            f"Avg Pressure: {data.get('avg_pressure', 0):.2f}\n"
            f"Avg Temperature: {data.get('avg_temperature', 0):.2f}"
        )
        self.stats_label.setText(stats)

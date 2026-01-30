import os
import requests
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import pyqtSignal, Qt
from worker import Worker

from logger import get_logger

class UploadWidget(QWidget):
    upload_success = pyqtSignal(dict)

    def __init__(self, token):
        super().__init__()
        self.logger = get_logger(__name__)
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
            self.logger.info(f"File selected: {file_path}")

    MAX_FILE_SIZE = 10 * 1024 * 1024

    def start_upload(self):
        if not self.file_path:
            return

        if not self.file_path.lower().endswith('.csv'):
            self.logger.warning(f"Invalid file extension: {self.file_path}")
            QMessageBox.warning(self, "Invalid File", "Only .csv files are allowed.")
            return

        try:
            size = os.path.getsize(self.file_path)
            if size > self.MAX_FILE_SIZE:
                self.logger.warning(f"File too large: {size} bytes")
                QMessageBox.warning(self, "File Too Large", f"File size exceeds {self.MAX_FILE_SIZE / (1024 * 1024)}MB limit.")
                return
        except OSError as e:
            self.logger.error(f"Error checking file size: {e}")
            QMessageBox.warning(self, "Error", "Could not read file size.")
            return

        self.logger.info(f"Starting upload for file: {self.file_path}")
        self.set_loading(True)
        self.worker = Worker(self.upload_task)
        self.worker.finished.connect(self.on_upload_finished)
        self.worker.error.connect(self.on_upload_error)
        self.worker.start()

    def upload_task(self):
        with open(self.file_path, 'rb') as f:
            files = {'file': f}
            headers = {'Authorization': f'Token {self.token}'}
            self.logger.debug("Sending POST request to /api/upload/")
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
                self.logger.info("Upload successful")
                QMessageBox.information(self, "Success", "File uploaded successfully!")
            except ValueError:
                 self.logger.error("Invalid JSON response from server")
                 QMessageBox.warning(self, "Error", "Invalid server response (not JSON).")
        else:
            error_msg = "Upload failed"
            try:
                data = response.json()
                error_msg = data.get('error', error_msg)
            except ValueError:
                pass
            
            self.logger.error(f"Upload failed. Status: {response.status_code}, Error: {error_msg}")
            
            if response.status_code == 413:
                error_msg = "File too large (Max 10MB)"
            elif response.status_code == 500:
                if error_msg == "Upload failed":
                     error_msg = "Internal server error. Please try again later."
                
            QMessageBox.warning(self, "Error", error_msg)

    def on_upload_error(self, error_msg):
        self.set_loading(False)
        self.logger.error(f"Network/Worker error: {error_msg}")
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

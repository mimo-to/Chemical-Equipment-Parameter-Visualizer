import os
import requests
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                             QFileDialog, QMessageBox)

class UploadWidget(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.file_path = None

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
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        self.stats_label = QLabel("")
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

    def upload_file(self):
        if not self.file_path:
            return

        self.set_loading(True)
        
        try:
            with open(self.file_path, 'rb') as f:
                files = {'file': f}
                headers = {'Authorization': f'Token {self.token}'}
                response = requests.post(
                    "http://127.0.0.1:8000/api/upload/",
                    files=files,
                    headers=headers
                )

            if response.status_code == 201:
                data = response.json()
                self.show_stats(data)
                QMessageBox.information(self, "Success", "File uploaded successfully!")
            else:
                error_msg = "Upload failed"
                try:
                    error_msg = response.json().get('error', error_msg)
                except ValueError:
                    pass
                QMessageBox.warning(self, "Error", error_msg)

        except requests.RequestException:
            QMessageBox.critical(self, "Network Error", "Could not connect to server.")
        finally:
            self.set_loading(False)

    def set_loading(self, loading):
        self.select_button.setEnabled(not loading)
        self.upload_button.setEnabled(not loading)
        self.upload_button.setText("Uploading..." if loading else "Upload and Analyze")

    def show_stats(self, data):
        stats = (
            f"Total Records: {data.get('total_count', 0)}\n"
            f"Avg Flowrate: {data.get('avg_flowrate', 0):.2f}\n"
            f"Avg Pressure: {data.get('avg_pressure', 0):.2f}\n"
            f"Avg Temperature: {data.get('avg_temperature', 0):.2f}"
        )
        self.stats_label.setText(stats)

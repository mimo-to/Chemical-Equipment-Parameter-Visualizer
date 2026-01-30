import requests
from datetime import datetime, timezone
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                             QPushButton, QHeaderView, QMessageBox, QFileDialog, QHBoxLayout)
from PyQt5.QtCore import Qt
from worker import Worker

class HistoryWidget(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.fetch_worker = None
        self.pdf_worker = None
        
        layout = QVBoxLayout()
        
        controls_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh History")
        self.refresh_btn.clicked.connect(self.fetch_history)
        controls_layout.addWidget(self.refresh_btn)
        
        self.download_btn = QPushButton("Save PDF Report")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.start_pdf_download)
        controls_layout.addWidget(self.download_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Filename", "Uploaded At"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.itemSelectionChanged.connect(self.check_selection)
        
        font = self.table.font()
        font.setPointSize(12)
        self.table.setFont(font)
        self.table.verticalHeader().setDefaultSectionSize(40)
        
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        self.fetch_history()

    def check_selection(self):
        selected = self.table.selectedItems()
        self.download_btn.setEnabled(bool(selected))

    def fetch_history(self, *args):
        self.refresh_btn.setEnabled(False)
        self.fetch_worker = Worker(self.fetch_task)
        self.fetch_worker.finished.connect(self.on_fetch_finished)
        self.fetch_worker.error.connect(self.on_fetch_error)
        self.fetch_worker.start()

    def fetch_task(self):
        headers = {'Authorization': f'Token {self.token}'}
        return requests.get("http://127.0.0.1:8000/api/history/", headers=headers)

    def on_fetch_finished(self, response):
        self.refresh_btn.setEnabled(True)
        if response.status_code == 200:
            self.populate_table(response.json())
        else:
            QMessageBox.warning(self, "Error", "Failed to fetch history.")

    def on_fetch_error(self, error_msg):
        self.refresh_btn.setEnabled(True)
        QMessageBox.warning(self, "Network Error", f"Could not fetch history: {error_msg}")

    def populate_table(self, data):
        self.table.setRowCount(0)
        for item in data[:5]:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            id_item = QTableWidgetItem(str(item['id']))
            id_item.setFlags(id_item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 0, id_item)
            
            file_item = QTableWidgetItem(str(item['filename']))
            file_item.setFlags(file_item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 1, file_item)
            
            raw_date_str = str(item.get('uploaded_at', ''))
            formatted_date = raw_date_str
            
            try:
                if 'Z' in raw_date_str:
                    clean_date = raw_date_str.replace('Z', '')
                    dt_utc = datetime.strptime(clean_date, "%Y-%m-%dT%H:%M:%S.%f")
                    dt_utc = dt_utc.replace(tzinfo=timezone.utc)
                    dt_local = dt_utc.astimezone()
                    formatted_date = dt_local.strftime("%Y-%m-%d %I:%M %p")
            except ValueError:
                pass

            date_item = QTableWidgetItem(formatted_date)
            date_item.setFlags(date_item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 2, date_item)

    def start_pdf_download(self):
        selected = self.table.selectedItems()
        if not selected:
            return
            
        row = selected[0].row()
        dataset_id = self.table.item(row, 0).text()
        default_filename = f"report_{dataset_id}.pdf"
        
        save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", default_filename, "PDF Files (*.pdf)")
        
        if save_path:
            self.download_btn.setEnabled(False)
            self.pdf_worker = Worker(self.pdf_task, dataset_id, save_path)
            self.pdf_worker.finished.connect(self.on_pdf_finished)
            self.pdf_worker.error.connect(self.on_pdf_error)
            self.pdf_worker.start()

    def pdf_task(self, dataset_id, save_path):
        headers = {'Authorization': f'Token {self.token}'}
        response = requests.get(f"http://127.0.0.1:8000/api/report/{dataset_id}/", headers=headers)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
        return response

    def on_pdf_finished(self, response):
        self.download_btn.setEnabled(True)
        if response.status_code == 200:
            QMessageBox.information(self, "Success", "PDF Report saved successfully!")
        else:
            QMessageBox.warning(self, "Error", "Failed to generate report.")

    def on_pdf_error(self, error_msg):
        self.download_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", f"Failed to save PDF: {error_msg}")

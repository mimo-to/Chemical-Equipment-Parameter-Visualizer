import requests
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                             QPushButton, QHeaderView, QMessageBox, QFileDialog, QHBoxLayout)
from PyQt5.QtCore import Qt

class HistoryWidget(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        
        layout = QVBoxLayout()
        
        controls_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh History")
        self.refresh_btn.clicked.connect(self.fetch_history)
        controls_layout.addWidget(self.refresh_btn)
        
        self.download_btn = QPushButton("Save PDF Report")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.save_pdf)
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
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        self.fetch_history()

    def check_selection(self):
        selected = self.table.selectedItems()
        self.download_btn.setEnabled(bool(selected))

    def fetch_history(self, *args):
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get("http://127.0.0.1:8000/api/history/", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.populate_table(data)
            else:
                pass
                
        except requests.RequestException:
            QMessageBox.warning(self, "Network Error", "Could not fetch history.")

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
            
            raw_date = str(item.get('uploaded_at', ''))
            formatted_date = raw_date.replace("T", " ")[:19]
            date_item = QTableWidgetItem(formatted_date)
            date_item.setFlags(date_item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 2, date_item)

    def save_pdf(self):
        selected = self.table.selectedItems()
        if not selected:
            return
            
        row = selected[0].row()
        dataset_id = self.table.item(row, 0).text()
        default_filename = f"report_{dataset_id}.pdf"
        
        save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", default_filename, "PDF Files (*.pdf)")
        
        if save_path:
            try:
                headers = {'Authorization': f'Token {self.token}'}
                response = requests.get(f"http://127.0.0.1:8000/api/report/{dataset_id}/", headers=headers)
                
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, "Success", "PDF Report saved successfully!")
                else:
                    QMessageBox.warning(self, "Error", "Failed to generate report.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

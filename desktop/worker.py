from PyQt5.QtCore import QThread, pyqtSignal
import requests
import os
import pathlib

API_BASE = os.environ.get("API_URL", "http://localhost:8000")


class ApiWorker(QThread):
    success = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, endpoint, token=None, method='GET', data=None, files=None):
        super().__init__()
        self.endpoint = endpoint
        self.token = token
        self.method = method
        self.data = data
        self.files = files
        
    def run(self):
        try:
            headers = {"Authorization": f"Token {self.token}"} if self.token else {}
            
            if self.method == 'POST' and self.files:
                response = requests.post(f"{API_BASE}{self.endpoint}", 
                                          files=self.files, headers=headers, timeout=60)
            elif self.method == 'POST':
                response = requests.post(f"{API_BASE}{self.endpoint}", 
                                          json=self.data, timeout=30)
            else:
                response = requests.get(f"{API_BASE}{self.endpoint}", 
                                         headers=headers, timeout=30)
            
            if response.status_code in (200, 201):
                self.success.emit(response.json())
            else:
                error = response.json().get("error", "Request failed")
                self.error.emit(error)
        except requests.exceptions.RequestException as e:
            self.error.emit(f"Connection error: {str(e)}")


class LoginWorker(QThread):
    success = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def run(self):
        try:
            response = requests.post(
                f"{API_BASE}/api/login/",
                json={"username": self.username, "password": self.password},
                timeout=30
            )
            if response.status_code == 200:
                self.success.emit(response.json().get("token", ""))
            else:
                self.error.emit(response.json().get("error", "Login failed"))
        except requests.exceptions.RequestException as e:
            self.error.emit(f"Connection error: {str(e)}")


class UploadWorker(QThread):
    success = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, filepath, token):
        super().__init__()
        self.filepath = filepath
        self.token = token

    def run(self):
        try:
            with open(self.filepath, "rb") as f:
                response = requests.post(
                    f"{API_BASE}/api/upload/",
                    files={"file": (os.path.basename(self.filepath), f, "text/csv")},
                    headers={"Authorization": f"Token {self.token}"},
                    timeout=60
                )
            if response.status_code in (200, 201):
                self.success.emit(response.json())
            else:
                self.error.emit(response.json().get("error", "Upload failed"))
        except requests.exceptions.RequestException as e:
            self.error.emit(f"Connection error: {str(e)}")
        except Exception as e:
            self.error.emit(str(e))


class VisualizationWorker(QThread):
    success = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, dataset_id, token):
        super().__init__()
        self.dataset_id = dataset_id
        self.token = token

    def run(self):
        try:
            response = requests.get(
                f"{API_BASE}/api/dataset/{self.dataset_id}/visualization/",
                headers={"Authorization": f"Token {self.token}"},
                timeout=30
            )
            if response.status_code == 200:
                self.success.emit(response.json())
            else:
                self.error.emit("Failed to load visualization")
        except requests.exceptions.RequestException as e:
            self.error.emit(f"Connection error: {str(e)}")


class HistoryWorker(QThread):
    success = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, token):
        super().__init__()
        self.token = token

    def run(self):
        try:
            response = requests.get(
                f"{API_BASE}/api/history/",
                headers={"Authorization": f"Token {self.token}"},
                timeout=30
            )
            if response.status_code == 200:
                self.success.emit(response.json())
            else:
                self.error.emit("Failed to load history")
        except requests.exceptions.RequestException as e:
            self.error.emit(f"Connection error: {str(e)}")


class DownloadWorker(QThread):
    success = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, dataset_id, token):
        super().__init__()
        self.dataset_id = dataset_id
        self.token = token
        self.filepath = None

    def run(self):
        try:
            response = requests.get(
                f"{API_BASE}/api/report/{self.dataset_id}/",
                headers={"Authorization": f"Token {self.token}"},
                timeout=60
            )
            if response.status_code == 200:
                path = self.filepath or str(pathlib.Path.home() / "Downloads" / f"report_{self.dataset_id}.pdf")
                with open(path, "wb") as f:
                    f.write(response.content)
                self.success.emit(path)
            else:
                self.error.emit("Failed to download report")
        except requests.exceptions.RequestException as e:
            self.error.emit(f"Connection error: {str(e)}")
        except Exception as e:
            self.error.emit(str(e))

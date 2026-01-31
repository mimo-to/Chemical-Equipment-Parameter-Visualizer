from PyQt5.QtCore import QThread, pyqtSignal
import requests
import os

API_BASE = os.environ.get("API_URL", "http://localhost:8000")


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
                data = response.json()
                self.success.emit(data.get("token", ""))
            else:
                error_msg = response.json().get("error", "Login failed")
                self.error.emit(error_msg)
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
                error_msg = response.json().get("error", "Upload failed")
                self.error.emit(error_msg)
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
                # Use provided filepath or default to Downloads
                if self.filepath:
                    filepath = self.filepath
                else:
                    import pathlib
                    downloads = pathlib.Path.home() / "Downloads"
                    filepath = str(downloads / f"report_{self.dataset_id}.pdf")
                    
                with open(filepath, "wb") as f:
                    f.write(response.content)
                self.success.emit(filepath)
            else:
                self.error.emit("Failed to download report")
        except requests.exceptions.RequestException as e:
            self.error.emit(f"Connection error: {str(e)}")
        except Exception as e:
            self.error.emit(str(e))

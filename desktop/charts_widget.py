from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from logger import get_logger
from worker import VisualizationWorker

log = get_logger(__name__)

COLORS = {
    'background': '#03045e',
    'card': '#023e8a',
    'primary': '#00b4d8',
    'success': '#06ffa5',
    'warning': '#ffd60a',
    'text': '#caf0f8',
    'muted': '#90e0ef',
    'border': '#0077b6',
}

CHART_COLORS = ['#00b4d8', '#06ffa5', '#ffd60a', '#0077b6', '#90e0ef', 
                '#48cae4', '#023e8a', '#caf0f8', '#ade8f4', '#03045e']

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
"""


class ChartsWidget(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet(THEME)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        
        # Title
        title = QLabel("Visualization")
        title.setObjectName("title")
        self.layout.addWidget(title)
        
        # Loading/placeholder label
        self.loading_label = QLabel("Upload a dataset to see visualizations")
        self.loading_label.setObjectName("loading")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.loading_label)
        
        # Charts container
        self.charts_layout = QHBoxLayout()
        self.charts_layout.setSpacing(20)
        self.layout.addLayout(self.charts_layout, 1)
        
        self.setLayout(self.layout)
        
    def load_data(self, dataset_id):
        self.loading_label.setText("Loading visualization data...")
        self.loading_label.show()
        self.clear_charts()
        
        self.worker = VisualizationWorker(dataset_id, self.token)
        self.worker.success.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()
        
    def clear_charts(self):
        while self.charts_layout.count():
            child = self.charts_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def on_success(self, data):
        log.info("Visualization data loaded")
        self.loading_label.hide()
        self.render_charts(data)
        
    def on_error(self, message):
        log.error(f"Visualization failed: {message}")
        self.loading_label.setText(f"Error: {message}")
        
    def render_charts(self, data):
        self.clear_charts()
        
        # Pie chart for type distribution
        type_dist = data.get("type_distribution", {})
        if type_dist:
            pie_fig = Figure(figsize=(6, 5), facecolor=COLORS['background'])
            pie_ax = pie_fig.add_subplot(111)
            pie_ax.set_facecolor(COLORS['background'])
            
            labels = type_dist.get("labels", [])
            values = type_dist.get("data", [])
            colors = CHART_COLORS[:len(labels)]
            
            # Create labels with count
            total = sum(values)
            labels_with_count = [f"{label}: {val}" for label, val in zip(labels, values)]
            
            wedges, texts, autotexts = pie_ax.pie(
                values, labels=labels_with_count, colors=colors,
                autopct='%1.1f%%', startangle=90,
                textprops={'color': COLORS['text'], 'fontsize': 9, 
                           'fontfamily': 'monospace'}
            )
            for autotext in autotexts:
                autotext.set_color('#ffffff')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
                
            pie_ax.set_title("Equipment Type Distribution", 
                           color=COLORS['primary'], fontsize=14,
                           fontfamily='monospace', fontweight='bold',
                           pad=20)
            
            pie_fig.tight_layout()
            pie_canvas = FigureCanvas(pie_fig)
            self.charts_layout.addWidget(pie_canvas)
            
        # Bar chart for averages
        averages = data.get("averages", {})
        if averages:
            bar_fig = Figure(figsize=(6, 5), facecolor=COLORS['background'])
            bar_ax = bar_fig.add_subplot(111)
            bar_ax.set_facecolor(COLORS['card'])
            
            labels = averages.get("labels", [])
            values = averages.get("data", [])
            colors = CHART_COLORS[:len(labels)]
            
            bars = bar_ax.bar(labels, values, color=colors, 
                             edgecolor=COLORS['border'], linewidth=2)
            
            bar_ax.set_title("Average Parameters",
                           color=COLORS['primary'], fontsize=14,
                           fontfamily='monospace', fontweight='bold',
                           pad=20)
            bar_ax.tick_params(colors=COLORS['text'], labelsize=11)
            bar_ax.spines['bottom'].set_color(COLORS['border'])
            bar_ax.spines['left'].set_color(COLORS['border'])
            bar_ax.spines['top'].set_visible(False)
            bar_ax.spines['right'].set_visible(False)
            
            for label in bar_ax.get_xticklabels():
                label.set_fontfamily('monospace')
            for label in bar_ax.get_yticklabels():
                label.set_fontfamily('monospace')
                
            bar_fig.tight_layout()
            bar_canvas = FigureCanvas(bar_fig)
            self.charts_layout.addWidget(bar_canvas)

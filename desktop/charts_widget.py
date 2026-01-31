from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from theme import COLORS, CHART_COLORS, CHARTS_THEME
from worker import VisualizationWorker


class ChartsWidget(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.worker = None
        self.setStyleSheet(CHARTS_THEME)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(36, 36, 36, 36)
        self.layout.setSpacing(24)
        
        title = QLabel("DATA VISUALIZATION")
        title.setObjectName("title")
        self.layout.addWidget(title)
        
        self.loading_label = QLabel("Upload a dataset to see visualizations")
        self.loading_label.setObjectName("loading")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.loading_label)
        
        self.charts_layout = QHBoxLayout()
        self.charts_layout.setSpacing(24)
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
        self.loading_label.hide()
        self.render_charts(data)
        
    def on_error(self, message):
        self.loading_label.setText(f"Error: {message}")
        
    def render_charts(self, data):
        self.clear_charts()
        
        type_dist = data.get("type_distribution", {})
        if type_dist:
            fig = Figure(figsize=(6, 5), facecolor=COLORS['background'])
            ax = fig.add_subplot(111)
            ax.set_facecolor(COLORS['background'])
            
            labels = type_dist.get("labels", [])
            values = type_dist.get("data", [])
            colors = CHART_COLORS[:len(labels)]
            
            pie_labels = [f"{l}: {v}" for l, v in zip(labels, values)]
            
            _, _, autotexts = ax.pie(
                values, labels=pie_labels, colors=colors,
                autopct='%1.1f%%', startangle=90,
                textprops={'color': COLORS['text'], 'fontsize': 11, 'fontfamily': 'monospace'}
            )
            for t in autotexts:
                t.set_color('#fff')
                t.set_fontweight('bold')
                t.set_fontsize(12)
                
            ax.set_title("EQUIPMENT TYPE DISTRIBUTION", 
                         color=COLORS['primary'], fontsize=16,
                         fontfamily='monospace', fontweight='bold', pad=24)
            
            fig.tight_layout()
            self.charts_layout.addWidget(FigureCanvas(fig))
            
        averages = data.get("averages", {})
        if averages:
            fig = Figure(figsize=(6, 5), facecolor=COLORS['background'])
            ax = fig.add_subplot(111)
            ax.set_facecolor(COLORS['card'])
            
            labels = averages.get("labels", [])
            values = averages.get("data", [])
            
            ax.bar(labels, values, color=CHART_COLORS[:len(labels)], 
                   edgecolor=COLORS['border'], linewidth=2)
            
            ax.set_title("AVERAGE PARAMETERS", color=COLORS['primary'], 
                         fontsize=16, fontfamily='monospace', fontweight='bold', pad=24)
            ax.tick_params(colors=COLORS['text'], labelsize=13)
            ax.spines['bottom'].set_color(COLORS['border'])
            ax.spines['left'].set_color(COLORS['border'])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontfamily('monospace')
                
            fig.tight_layout()
            self.charts_layout.addWidget(FigureCanvas(fig))

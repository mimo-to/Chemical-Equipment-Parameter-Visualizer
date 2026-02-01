from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout
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
        
        self.stats_container = QFrame()
        self.stats_container.setObjectName("statsContainer")
        self.stats_container.setStyleSheet(f"""
            QFrame#statsContainer {{
                background-color: transparent;
                border: none;
                padding: 8px;
            }}
        """)
        self.stats_layout = QHBoxLayout(self.stats_container)
        self.stats_layout.setSpacing(16)
        self.stats_container.hide()
        self.layout.addWidget(self.stats_container)
        
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
        while self.stats_layout.count():
            child = self.stats_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.stats_container.hide()
                
    def on_success(self, data):
        self.loading_label.hide()
        self.render_charts(data)
        
    def on_error(self, message):
        self.loading_label.setText(f"Error: {message}")
        
    def render_charts(self, data):
        self.clear_charts()
        
        averages = data.get("averages", {})
        if averages:
            labels = averages.get("labels", [])
            values = averages.get("data", [])
            mins = averages.get("min", [])
            maxs = averages.get("max", [])
            
            for i, label in enumerate(labels):
                card = self.create_stat_card(
                    label, 
                    values[i] if i < len(values) else 0,
                    mins[i] if i < len(mins) else None,
                    maxs[i] if i < len(maxs) else None
                )
                self.stats_layout.addWidget(card)
            self.stats_container.show()
        
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
    
    def create_stat_card(self, label, avg, min_val, max_val):
        card = QFrame()
        card.setFixedHeight(110)
        card.setMinimumWidth(220)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['card']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
            }}
            QLabel {{
                border: none;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)
        
        lbl = QLabel(label.upper())
        lbl.setStyleSheet(f"color: {COLORS['muted']}; font-size: 12px; font-weight: bold; background: transparent;")
        layout.addWidget(lbl)
        
        row = QHBoxLayout()
        row.setSpacing(20)
        
        avg_lbl = QLabel(f"{avg:.2f}")
        avg_lbl.setStyleSheet(f"color: {COLORS['success']}; font-size: 28px; font-weight: bold; background: transparent;")
        row.addWidget(avg_lbl)
        
        row.addStretch()
        
        minmax = QVBoxLayout()
        minmax.setSpacing(4)
        
        min_text = QLabel(f"MIN: {min_val:.2f}" if min_val is not None else "MIN: 0.00")
        min_text.setStyleSheet(f"color: {COLORS['text']}; font-size: 16px; background: transparent;")
        max_text = QLabel(f"MAX: {max_val:.2f}" if max_val is not None else "MAX: 0.00")
        max_text.setStyleSheet(f"color: {COLORS['text']}; font-size: 16px; background: transparent;")
        
        minmax.addWidget(min_text)
        minmax.addWidget(max_text)
        row.addLayout(minmax)
        
        layout.addLayout(row)
        layout.addStretch()
        
        return card



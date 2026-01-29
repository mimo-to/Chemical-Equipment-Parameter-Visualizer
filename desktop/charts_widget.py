from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class ChartsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        # Type Distribution Chart (Left)
        self.figure1 = Figure(figsize=(5, 4), dpi=100)
        self.canvas1 = FigureCanvas(self.figure1)
        layout.addWidget(self.canvas1)

        # Averages Chart (Right)
        self.figure2 = Figure(figsize=(5, 4), dpi=100)
        self.canvas2 = FigureCanvas(self.figure2)
        layout.addWidget(self.canvas2)

        self.setLayout(layout)

    def update_charts(self, data):
        # 1. Type Distribution Chart
        self.figure1.clear()
        ax1 = self.figure1.add_subplot(111)
        
        type_dist = data.get('type_distribution', {})
        if type_dist:
            labels = list(type_dist.keys())
            values = list(type_dist.values())
            ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            ax1.set_title("Equipment Type Distribution")
        else:
            ax1.text(0.5, 0.5, "No Data", ha='center', va='center')

        self.canvas1.draw()

        # 2. Averages Chart
        self.figure2.clear()
        ax2 = self.figure2.add_subplot(111)

        avg_flow = data.get('avg_flowrate', 0)
        avg_press = data.get('avg_pressure', 0)
        avg_temp = data.get('avg_temperature', 0)

        params = ['Flowrate', 'Pressure', 'Temp']
        values = [avg_flow, avg_press, avg_temp]
        colors = ['blue', 'green', 'red']

        ax2.bar(params, values, color=colors)
        ax2.set_title("Average Parameters")
        ax2.set_ylabel("Value")
        
        self.canvas2.draw()

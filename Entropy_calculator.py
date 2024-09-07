#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 12:05:59 2024

@author: harish
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QSlider, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class EntropyCalculator(QWidget):
    def __init__(self):
        super(EntropyCalculator, self).__init__()  # Correctly initialize the parent class
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Entropy of a Biased Coin')
        
        # Set a fixed size for the window
        self.setMinimumSize(600, 800)  # Adjust the size as needed

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Create a slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setFixedHeight(30)  # Set a fixed height for the slider
        self.slider.valueChanged.connect(self.update_plot)
        
            # Create a label for the slider
        self.slider_label = QLabel('Biasing (from 0 to 1)')
        self.slider_label.setAlignment(Qt.AlignCenter)
        self.slider_label.setFixedHeight(30)

        # Add the canvas and slider to the layout
        layout.addWidget(self.canvas)
        layout.addWidget(self.slider)
        layout.addWidget(self.slider_label)

        # Set the layout to the main window
        self.setLayout(layout)

        # Initial plot
        self.update_plot()

    def calculate_entropy(self, p):
        if p == 0 or p == 1:
            return 0
        return -p * np.log2(p) - (1 - p) * np.log2(1 - p)

    def update_plot(self):
        # Get the slider value and convert it to a probability
        slider_value = self.slider.value()
        p = slider_value / 100.0

        # Calculate the entropy for the current probability
        entropy = self.calculate_entropy(p)

        # Clear the previous plot
        self.figure.clear()

        # Create two subplots
        ax1 = self.figure.add_subplot(211)
        ax2 = self.figure.add_subplot(212)

        # Plot the probability distribution
        ax1.bar(['Heads', 'Tails'], [p, 1 - p], color=['blue', 'orange'])
        ax1.set_title('Probability Distribution', fontsize=self.get_fontsize())
        ax1.set_ylim(0, 1)
        
        # Update tick labels fontsize
        for label in ax1.get_xticklabels() + ax1.get_yticklabels():
            label.set_fontsize(self.get_fontsize())

        # Plot the entropy as a function of biasing
        ps = np.linspace(0, 1, 100)
        entropies = [self.calculate_entropy(pi) for pi in ps]
        ax2.plot(ps, entropies, lw=3, label='Entropy')
        ax2.plot([p], [entropy], "o", ms=10, color='red', fillstyle='none', mew=2)  # Current setting
        #ax2.set_title('Entropy as a Function of Biasing', fontsize=self.get_fontsize())
        ax2.set_xlabel('Probability of Heads', fontsize=self.get_fontsize())
        ax2.set_ylabel('Entropy (bits)', fontsize=self.get_fontsize())
        #ax2.legend()
        
        plt.subplots_adjust(hspace=2.5) 
    # Update tick labels fontsize
        for label in ax2.get_xticklabels() + ax2.get_yticklabels():
            label.set_fontsize(self.get_fontsize())

        # Refresh the canvas
        plt.tight_layout()
        self.canvas.draw()

    def get_fontsize(self):
        # Dynamically adjust font size based on window width
        width = self.width()
        if width < 400:
            return 10
        elif width < 800:
            return 16
        else:
            return 26

    def resizeEvent(self, event):
        super(EntropyCalculator, self).resizeEvent(event)
        self.update_plot()

def main():
    app = QApplication(sys.argv)
    ex = EntropyCalculator()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

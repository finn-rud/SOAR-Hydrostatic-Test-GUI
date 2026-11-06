import sys
import random
from collections import deque
from unicodedata import name
from PyQt6.QtWidgets import QApplication, QGridLayout, QMainWindow, QPushButton, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer
import pyqtgraph as pg

class PressurePlot(pg.PlotWidget):
    def __init__(self,name):
        super().__init__()
        self.setTitle(name)
        self.curve = self.plot()
        self.data = deque(maxlen=200)

    def add_point(self, new_point):
        self.data.append(new_point)
          # adds the new variable value to the data deque
        self.curve.setData(list(self.data))
            # first converts the deque to a list, then calls the setData method whi


# makes the class for the GUI window, and allows the plot stuff to be created within it
class TestStandGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Stand GUI")

# makes the plot widget
       
        self.plot1 = PressurePlot("P1")
        self.plot2 = PressurePlot("P2")
        self.plot3 = PressurePlot("P3")

        layout = QGridLayout()
        layout.addWidget(self.plot1, 0, 0)
        layout.addWidget(self.plot2, 0, 1)
        layout.addWidget(self.plot3, 1, 0)

        ####################buttons#####################
#makes a new button called "Arm" and makes it toggleable, so that pressing it once essentially holds it down
        self.arm_button = QPushButton("Arm")
        self.arm_button.setCheckable(True)

#when it's clicked, call the toggle_arm method
        self.arm_button.clicked.connect(self.toggle_arm)

#makes a new button called "Bleed" and makes it toggleable
        self.bleed_button = QPushButton("Bleed")
        self.bleed_button.setCheckable(True)

#when it's clicked call the toggle_bleed method
        self.bleed_button.clicked.connect(self.toggle_bleed)

#makes another layout for the buttons and adds it to the overall layout that the plots are in too
        controls_layout = QVBoxLayout()
        controls_layout.addWidget(self.arm_button)
        controls_layout.addWidget(self.bleed_button)
        controls_layout.addStretch()
        layout.addLayout(controls_layout, 0,2,2,1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        # puts the plot in the window

# makes the timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        # the .timeout means we're dealilng with the timeout signal from timer, and the .connect means that the update_plot method
        # is called at every timeout
        self.timer.start(50)
        # sets the timeout intervals to be spaced by 50 ms

# makes the method that runs the point updates
    def update_plot(self):
        # gets the data and puts it into a variable
        self.plot1.add_point(random.random())
        self.plot2.add_point(random.random())
        self.plot3.add_point(random.random())
        # first converts the deque to a list, then calls the setData method which tells the curve attribute to redraw itself with the new numbers

#toggle method for the arm button
#changes the Arm state based on whether the buttons toggled
    def toggle_arm(self):
        if self.arm_button.isChecked():
                self.arm_button.setText("Disarm")
                print("System is armed")
        else:
            self.arm_button.setText("Arm")
            print("System is disarmed")

    def toggle_bleed(self):
        if self.bleed_button.isChecked():
                self.bleed_button.setText("Stop Bleed")
                print("System is bleeding")
        else:
                self.bleed_button.setText("Bleed")
                print("System has stopped bleeding")




# runs the GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestStandGUI()
    window.show()
    sys.exit(app.exec())
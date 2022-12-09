from PyQt5.QtWidgets import *
from view import *
from writer import *
import time

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Controller(QMainWindow, Ui_MainWindow):
    """
    This function establishes class global variables to be utilized by the initialization of the Controller

    """

    def __init__(self, *args, **kwargs):
        """
        This function initializes a controller with default values

        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.preResetTotal = 0.0
        self.splitPreSetTotal = 0.0
        self.splitCounter = 0
        self.storeSplit = 0.0
        self.splits = []
        self.totalTimes = []
        self.splitTimes = []
        self.timeName = []
        self.username = ''
        self.startButton.setCheckable(True)
        self.stopButton.setCheckable(True)
        self.splitButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.resetButton.setEnabled(False)
        self.startButton.setEnabled(False)
        self.errorText.setVisible(False)
        self.submitButton.clicked.connect(lambda: self.submit())
        self.startButton.clicked.connect(lambda: self.start())
        self.stopButton.clicked.connect(lambda: self.stop())
        self.splitButton.clicked.connect(lambda: self.split())
        self.resetButton.clicked.connect(lambda: self.reset())

    def submit(self):
        try:
            name = self.nameField.text()
            if name == '':
                raise ValueError

            else:
                self.username = name
                self.startButton.setEnabled(True)
                self.errorText.setVisible(False)

        except ValueError:
            self.errorText.setVisible(True)
            self.startButton.setEnabled(False)

    def start(self):
        """
        This function will start the timer and increment by one second
        :return:
        """
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.stopButton.setChecked(False)
        self.resetButton.setEnabled(False)
        self.splitButton.setEnabled(True)
        self.submitButton.setEnabled(False)
        self.initiate = time.time()
        self.initiate_split = time.time()
        self.convert(self.initiate, self.preResetTotal, self.splitPreSetTotal)

    def stop(self):
        """
        This function will stop the timer
        :return:
        """
        self.stopButton.setEnabled(False)
        self.startButton.setChecked(False)
        self.startButton.setEnabled(True)
        self.resetButton.setEnabled(True)
        self.splitButton.setEnabled(False)

    def split(self):
        """
        This function will start the timer and increment by one second
        :return:
        """
        self.storeTotal = time.time() - self.initiate
        self.loadTotal = self.storeTimes(self.storeTotal)
        self.storeSplit = time.time() - self.initiate_split
        self.initiate_split = time.time()
        self.loadSplit = self.storeTimes(self.storeSplit)
        self.splitPreSetTotal = 0.0
        self.splitCounter = self.splitCounter + 1
        self.split_header.setText(f'Split {self.splitCounter}')
        self.splits.append(f'Split {self.splitCounter}')
        self.timeName.append(f'{self.username}')
        self.totalTimes.append(f'{self.loadTotal}')
        self.splitTimes.append(f'{self.loadSplit}')
        self.convert(self.initiate_split, self.preResetTotal, self.splitPreSetTotal)

    def reset(self):
        """
        This function will reset the time to '00:00:00'
        :return:
        """

        self.storeTotal = time.time() - self.initiate
        self.loadTotal = self.storeTimes(self.storeTotal)
        self.storeSplit = time.time() - self.initiate_split
        self.initiate_split = time.time()
        self.loadSplit = self.storeTimes(self.storeSplit)
        self.splitPreSetTotal = 0.0
        self.splitCounter = self.splitCounter + 1
        self.split_header.setText(f'Split {self.splitCounter}')
        self.splits.append(f'Split {self.splitCounter}')
        self.timeName.append(f'{self.username}')
        self.totalTimes.append(f'{self.loadTotal}')
        self.splitTimes.append(f'{self.loadSplit}')
        self.convert(self.initiate_split, self.preResetTotal, self.splitPreSetTotal)
        save_time(self.timeName, self.splits, self.splitTimes, self.totalTimes)

        self.time_display.setText('00:00:00:00')
        self.split_display.setText('00:00:00:00')
        self.split_header.setText('Split 1')
        self.splitCounter = 0
        self.preResetTotal = 0.0
        self.splitPreSetTotal = 0.0
        self.startButton.setChecked(False)
        self.stopButton.setChecked(False)
        self.splitButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.resetButton.setEnabled(False)
        self.startButton.setEnabled(False)
        self.submitButton.setEnabled(True)
        self.nameField.setText('')
        self.username = ''
        self.splits.clear()
        self.totalTimes.clear()
        self.splitTimes.clear()
        self.timeName.clear()




    def convert(self, start_time, total_time, split_time):
        while (self.startButton.isChecked() == True) and (self.stopButton.isChecked() == False):
            QtCore.QCoreApplication.processEvents()
            self.current_time = time.time()
            self.output = self.current_time - start_time + total_time
            self.output_split = self.current_time - start_time + split_time
            self.main_clock(self.output)
            self.split_clock(self.output_split)
            self.adjust(self.output)

        self.PreResetTotal = self.output
        self.splitPreSetTotal = self.output_split


    def main_clock(self, display):
        milli = display * 100
        milli = milli % 100
        secs = display % 60
        mins = display // 60
        mins = mins % 60
        hours = mins // 60
        self.time_display.setText(f'{int(hours):02}:{int(mins):02}:{int(secs):02}:{int(milli):02}')

    def split_clock(self, display_split):
        split_milli = display_split * 100
        split_milli = split_milli % 100
        split_secs = display_split % 60
        split_mins = display_split // 60
        split_mins = split_mins % 60
        split_hours = split_mins // 60
        self.split_display.setText(f'{int(split_hours):02}:{int(split_mins):02}:{int(split_secs):02}:{int(split_milli):02}')

    def storeTimes(self, splitTimes):
        split_milli = splitTimes * 100
        split_milli = split_milli % 100
        split_secs = splitTimes % 60
        split_mins = splitTimes // 60
        split_mins = split_mins % 60
        split_hours = split_mins // 60
        return f'{int(split_hours):02}:{int(split_mins):02}:{int(split_secs):02}:{int(split_milli):02}'

    def adjust(self, newTime):
        self.preResetTotal = newTime















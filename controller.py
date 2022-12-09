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
        """
        This function checks whether the user has entered anything into the 'nameField' entry box. If nothing is
        entered, the ValueError is raised to indicate the user needs to enter something into that field in order
        to access the start button and begin the program. If there is anything in the box, the startButton is enabled
        and the errorText is hidden
        :return:
        """
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
        This function will start the timer and disable the startButton upon pressing as well as the resetButton,
        submitButton and nameField while enabling and setting the stopButton to unchecked as well as enabling the
        splitButton. self.initiate is set to time.time() and self.initiate_split is established for capturing split
        times utilizing the time library. Finally, the method self.convert is called to convert self.initiate to
        readable time output.
        :return:
        """
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.stopButton.setChecked(False)
        self.resetButton.setEnabled(False)
        self.splitButton.setEnabled(True)
        self.submitButton.setEnabled(False)
        self.nameField.setEnabled(False)
        self.initiate = time.time()
        self.initiate_split = time.time() - self.splitPreSetTotal
        self.convert(self.initiate, self.preResetTotal)

    def stop(self):
        """
        This function will stop the timer and disable the startButton, stopButton, splitButton while reenabling the
        resetButton to start a new timer and to write logged splits to a CSV file.
        :return:
        """

        self.storeTotal = time.time() - self.initiate
        self.loadTotal = self.storeTimes(self.storeTotal)
        self.storeSplit = time.time() - self.initiate_split
        self.loadSplit = self.storeTimes(self.storeSplit)
        self.initiate_split = time.time()
        self.splitPreSetTotal = time.time() - self.preResetTotal
        self.splitCounter = self.splitCounter + 1
        self.split_header.setText(f'Split {self.splitCounter}')
        self.splits.append(f'Split {self.splitCounter}')
        self.timeName.append(f'{self.username}')
        self.totalTimes.append(f'{self.loadTotal}')
        self.splitTimes.append(f'{self.loadSplit}')
        self.convert(self.initiate_split, self.preResetTotal)

        self.split_clock(self.splitPreSetTotal)
        self.stopButton.setEnabled(False)
        self.startButton.setChecked(False)
        self.startButton.setEnabled(True)
        self.resetButton.setEnabled(True)
        self.splitButton.setEnabled(False)
        self.startButton.setEnabled(False)



    def split(self):
        """
        This function will split the timer to capture splits in the total time upon clicking the splitButton
        :return:
        """
        self.storeTotal = time.time() - self.initiate
        self.loadTotal = self.storeTimes(self.storeTotal)
        self.storeSplit = time.time() - self.initiate_split
        self.loadSplit = self.storeTimes(self.storeSplit)
        self.initiate_split = time.time()
        self.splitPreSetTotal = time.time() - self.preResetTotal
        self.splitCounter = self.splitCounter + 1
        self.split_header.setText(f'Split {self.splitCounter}')
        self.splits.append(f'Split {self.splitCounter}')
        self.timeName.append(f'{self.username}')
        self.totalTimes.append(f'{self.loadTotal}')
        self.splitTimes.append(f'{self.loadSplit}')
        self.convert(self.initiate_split, self.preResetTotal)

    def reset(self):
        """
        This function will reset all variables back to their default status and call the method save_times from writer
        to write the logged times held in the lists timeName, splits, splitTimes and totalTimes to a CSV file
        :return:
        """

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
        self.nameField.setEnabled(True)
        self.nameField.setText('')
        self.username = ''
        self.splits.clear()
        self.totalTimes.clear()
        self.splitTimes.clear()
        self.timeName.clear()




    def convert(self, start_time, total_time):
        """
        This method will take in parameters to establish a time for the main time clock and split time clock in
        time.time() format and then utilizes that conversion to call the methods main_clock and split_clock to display
        time to the GUI
        :param start_time: Time that the convert method was initially called by a button push
        :param total_time: Total time held in the variable preResetTotal to keep track of total time
        :return:
        """
        while (self.startButton.isChecked() == True) and (self.stopButton.isChecked() == False):
            QtCore.QCoreApplication.processEvents()
            self.current_time = time.time()
            self.output = self.current_time - start_time + total_time
            self.output_split = self.current_time - start_time
            self.main_clock(self.output)
            self.split_clock(self.output_split)
            self.adjust(self.output)
            self.adjustSplit(self.output_split)


    def main_clock(self, display):
        """
        Method converting time.time() to traditional timeclock values to be displayed to the GUI via time_display.
        Conversions are utilized to extract milliseconds, seconds, minutes and hours respectively.
        :param display: The time.time() value to be converted to display
        :return:
        """
        milli = display * 100
        milli = milli % 100
        secs = display % 60
        mins = display // 60
        mins = mins % 60
        hours = mins // 60
        self.time_display.setText(f'{int(hours):02}:{int(mins):02}:{int(secs):02}:{int(milli):02}')

    def split_clock(self, display_split):
        """
        Method converting time.time() to traditional timeclock values to be displayed to the GUI via
        split_display. Conversions are utilized to extract milliseconds, seconds, minutes and hours respectively.
        :param display: The time.time() value to be converted to display
        :return:
        """
        split_milli = display_split * 100
        split_milli = split_milli % 100
        split_secs = display_split % 60
        split_mins = display_split // 60
        split_mins = split_mins % 60
        split_hours = split_mins // 60
        self.split_display.setText(f'{int(split_hours):02}:{int(split_mins):02}:{int(split_secs):02}:{int(split_milli):02}')

    def storeTimes(self, splitTimes):
        """
        Method converting time.time() to traditional timeclock values to be stored in respective lists and written out
        to the CSV later
        :param splitTimes: the time.time() value to be converted and returned to variable to later be stored in a list
        :return: value returned to variable as readable time format for writing
        """
        split_milli = splitTimes * 100
        split_milli = split_milli % 100
        split_secs = splitTimes % 60
        split_mins = splitTimes // 60
        split_mins = split_mins % 60
        split_hours = split_mins // 60
        return f'{int(split_hours):02}:{int(split_mins):02}:{int(split_secs):02}:{int(split_milli):02}'

    def adjust(self, newTime):
        """
        Method update PreResetTotal to newTime
        :param newTime: New time Variable to load into PreResetTotal
        :return:
        """
        self.preResetTotal = newTime

    def adjustSplit(self, newSplitTime):
        """
        Method updating splitPresetTotal to newSplitTime
        :param newSplitTime: New time Variable to load into splitPreSetTotal
        :return:
        """
        self.splitPreSetTotal = newSplitTime
















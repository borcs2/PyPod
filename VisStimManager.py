import os
import subprocess
import sys
import time
from pathlib import Path
from threading import Thread, Timer

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QDir, QObject, QSize, Slot
from PySide2.QtGui import QIcon, QImage, QImageReader, QPixmap, QTransform
from PySide2.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDoubleSpinBox, QGridLayout, QGroupBox,
                               QHBoxLayout, QInputDialog, QLabel, QLineEdit,
                               QListWidget, QListWidgetItem, QMessageBox,
                               QProgressBar, QPushButton, QRadioButton,
                               QSplashScreen, QVBoxLayout, QMenuBar, QMainWindow, QMenu)

import anim_player
import settings
from lj_input import LJInput


class VisStimManager(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()

        # Create layouts
        layout = QVBoxLayout()

        saveLoadLayout = QHBoxLayout()
        GoLayout = QHBoxLayout()
        GoSubLayout = QVBoxLayout()
        NoGoLayout = QHBoxLayout()
        NoGoSubLayout = QVBoxLayout()
        TimingLayout = QVBoxLayout()

        saveLoadBox = QGroupBox("Save this parameters or Load an old one")
        GoWithRadios = QGroupBox("Go Stimulus")
        NoGoWithGoRadios = QGroupBox("NoGo Stimulus")
        paramBox = QGroupBox("Timing parameters")

        # Define variables
        # self.parametersToSave
        self.GoPic = "media\\squareVert.png"
        self.NoGoPic = "media\\squareVert.png"
        self.GoArrow = "media\\rightRedArrow.png"
        self.NoGoArrow = "media\\rightRedArrow.png"

        #CreateMenuBar
        self.menuBar = QMenuBar()
        self.toolsMenu = QMenu()
        self.menuBar.addMenu(self.toolsMenu)


        # Create widgets
        self.saveParametersButton = QPushButton("Save actual parameters")
        self.loadParametersButton = QPushButton("Load parameters")
        self.saveDialog = QInputDialog()
        self.GoList = QComboBox()
        self.NoGoList = QComboBox()
        self.GoList.addItems(
            ["0°", "45°", "90°", "135°", "180°", "225°", "270°", "315°"])
        self.NoGoList.addItems(
            ["0°", "45°", "90°", "135°", "180°", "225°", "270°", "315°"])
        self.startButton = QPushButton("Start visual discrimination task")
        self.stopButton = QPushButton("Stop task")
        self.goRadioSin = QRadioButton("Sin")
        self.noGoRadioSin = QRadioButton("Sin")
        self.goRadioSquare = QRadioButton("Square")
        self.noGoRadioSquare = QRadioButton("Square")
        self.waitBeforeAnimation = QDoubleSpinBox()
        self.firstAnimationLength = QDoubleSpinBox()
        self.waitBetweenAnimations = QDoubleSpinBox()
        self.secondAnimationLength = QDoubleSpinBox()
        self.waitAfterAnimation = QDoubleSpinBox()
        self.waitBeforeAnimationLabel = QLabel("Wait before animation")
        self.firstAnimationLengthLabel = QLabel("First animation length")
        self.waitBetweenAnimationsLabel = QLabel("Wait between animations")
        self.secondAnimationLengthLabel = QLabel("second animation length")
        self.waitAfterAnimationLabel = QLabel("Wait after second animation")
        self.goCurrentImage = QLabel()
        self.goCurrentImage.setPixmap(
            QPixmap(self.GoPic).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
        self.goArrowImage = QLabel()
        self.goArrowImage.setPixmap(QPixmap(self.GoArrow).scaled(
            50, 50, QtCore.Qt.KeepAspectRatio))
        self.noGoArrowImage = QLabel()
        self.noGoArrowImage.setPixmap(
            QPixmap(self.NoGoArrow).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
        self.noGoCurrentImage = QLabel()
        self.noGoCurrentImage.setPixmap(
            QPixmap(self.NoGoPic).scaled(50, 50, QtCore.Qt.KeepAspectRatio))

        # Widget settings
        self.goRadioSquare.setChecked(True)
        self.noGoRadioSquare.setChecked(True)

        self.waitBeforeAnimation.setSuffix(' sec')
        self.firstAnimationLength.setSuffix(' sec')
        self.waitBetweenAnimations.setSuffix(' sec')
        self.secondAnimationLength.setSuffix(' sec')
        self.waitAfterAnimation.setSuffix(' sec')

        # Add widgets to Layouts
        saveLoadLayout.addWidget(self.saveParametersButton)
        saveLoadLayout.addWidget(self.loadParametersButton)
        saveLoadBox.setLayout(saveLoadLayout)

        GoLayout.addWidget(self.GoList)
        GoLayout.addWidget(self.goRadioSquare)
        GoLayout.addWidget(self.goRadioSin)
        GoSubLayout.addWidget(self.goCurrentImage)
        GoSubLayout.addWidget(self.goArrowImage)
        GoLayout.addLayout(GoSubLayout)

        NoGoLayout.addWidget(self.NoGoList)
        NoGoLayout.addWidget(self.noGoRadioSquare)
        NoGoLayout.addWidget(self.noGoRadioSin)
        NoGoSubLayout.addWidget(self.noGoCurrentImage)
        NoGoSubLayout.addWidget(self.noGoArrowImage)
        NoGoLayout.addLayout(NoGoSubLayout)

        TimingLayout.addWidget(self.waitBeforeAnimationLabel)
        TimingLayout.addWidget(self.waitBeforeAnimation)
        TimingLayout.addWidget(self.firstAnimationLengthLabel)
        TimingLayout.addWidget(self.firstAnimationLength)
        TimingLayout.addWidget(self.waitBetweenAnimationsLabel)
        TimingLayout.addWidget(self.waitBetweenAnimations)
        TimingLayout.addWidget(self.secondAnimationLengthLabel)
        TimingLayout.addWidget(self.secondAnimationLength)
        TimingLayout.addWidget(self.waitAfterAnimationLabel)
        TimingLayout.addWidget(self.waitAfterAnimation)

        # Set dialog layout
        GoWithRadios.setLayout(GoLayout)
        NoGoWithGoRadios.setLayout(NoGoLayout)
        paramBox.setLayout(TimingLayout)
        layout.addWidget(saveLoadBox)
        layout.addWidget(GoWithRadios)
        layout.addWidget(NoGoWithGoRadios)
        layout.addWidget(paramBox)
        layout.addWidget(self.startButton)
        layout.addWidget(self.stopButton)
        self.setLayout(layout)

        # Add Signals
        self.saveParametersButton.clicked.connect(self.save)
        self.loadParametersButton.clicked.connect(self.openLoadDialog)
        self.startButton.clicked.connect(self.passdata)
        self.stopButton.clicked.connect(self.close_stim)
        self.GoList.currentTextChanged.connect(self.updateGoPic)
        self.NoGoList.currentTextChanged.connect(self.updateNoGoPic)
        self.goRadioSin.toggled.connect(self.updateGoPic)
        self.goRadioSquare.toggled.connect(self.updateGoPic)
        self.noGoRadioSin.toggled.connect(self.updateNoGoPic)
        self.noGoRadioSquare.toggled.connect(self.updateNoGoPic)

    @Slot()
    def openLoadDialog(self):
        self.loadDialog = LoadDialog()
        self.loadDialog.show()

    def save(self):
        currentParameters = list()
        listOfFiles = os.listdir(str(Path().absolute()) + "\\sessionData\\")
        text = QInputDialog.getText(self, self.tr("Save parameters"),
                                    self.tr(
                                        "Please give mouse name:"), QLineEdit.Normal,
                                    self.tr(""))
        if text[1] == True and text[0] != '' and listOfFiles.count(text[0] + ".txt") == 0:
            currentParameters.append(text[0])

            if self.goRadioSin.isChecked() == True:
                goWtype = "Sin"
            else:
                goWtype = "Square"
            currentParameters.append(goWtype)
            currentParameters.append(self.GoList.currentText())
            if self.noGoRadioSin.isChecked() == True:
                noGoWtype = "Sin"
            else:
                noGoWtype = "Square"
            currentParameters.append(noGoWtype)
            currentParameters.append(self.NoGoList.currentText())

            currentParameters.append(float(self.waitBeforeAnimation.value()))
            currentParameters.append(float(self.firstAnimationLength.value()))
            currentParameters.append(float(self.waitBetweenAnimations.value()))
            currentParameters.append(float(self.secondAnimationLength.value()))
            currentParameters.append(float(self.waitAfterAnimation.value()))

            fh = open(str(Path().absolute()) +
                      "\\sessionData\\" + text[0] + ".txt", "w")
            fh.write(str(currentParameters)[1:-1])
            fh.write("\n")
            fh.close

        elif text[1] == True and text[0] == '':
            nameNullError = QMessageBox().warning(self, self.tr(
                "Error"), self.tr("Name cannot be empty!"), QMessageBox.Cancel)
            if nameNullError == QMessageBox.Cancel:
                self.save()
        elif text[1] == True and listOfFiles.count(text[0] + ".txt") > 0:
            alreadyExistsError = QMessageBox().warning(self, self.tr(
                "Error"), self.tr("This name already exists!"), QMessageBox.Cancel)
            if alreadyExistsError == QMessageBox.Cancel:
                self.save()

    def updateGoPic(self):

        if self.goRadioSin.isChecked() == True:
            goWtype = "Sin"
        else:
            goWtype = "Square"

        if (int(self.GoList.currentText()[:-1]) == 0):
            self.GoPic = "media\\" + goWtype.lower() + "Vert.png"
            self.GoArrow = "media\\rightRedArrow.png"
        elif (int(self.GoList.currentText()[:-1]) == 45):
            self.GoPic = "media\\" + goWtype.lower() + "Diag.png"
            self.GoArrow = "media\\rightRedArrow.png"
        elif (int(self.GoList.currentText()[:-1]) == 225):
            self.GoPic = "media\\" + goWtype.lower() + "Diag.png"
            self.GoArrow = "media\\leftRedArrow.png"
        elif (int(self.GoList.currentText()[:-1]) == 135):
            self.GoPic = "media\\" + goWtype.lower() + "InvDiag.png"
            self.GoArrow = "media\\leftRedArrow.png"
        elif (int(self.GoList.currentText()[:-1]) == 180):
            self.GoPic = "media\\" + goWtype.lower() + "Vert.png"
            self.GoArrow = "media\\leftRedArrow.png"
        elif (int(self.GoList.currentText()[:-1]) == 90):
            self.GoPic = "media\\" + goWtype.lower() + "Horiz.png"
            self.GoArrow = "media\\downRedArrow.png"
        elif (int(self.GoList.currentText()[:-1]) == 270):
            self.GoPic = "media\\" + goWtype.lower() + "Horiz.png"
            self.GoArrow = "media\\upRedArrow.png"
        else:
            self.GoPic = "media\\" + goWtype.lower() + "InvDiag.png"
            self.GoArrow = "media\\rightRedArrow.png"
        self.goCurrentImage.setPixmap(
            QPixmap(self.GoPic).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
        self.goArrowImage.setPixmap(QPixmap(self.GoArrow).scaled(
            50, 50, QtCore.Qt.KeepAspectRatio))

    def updateNoGoPic(self):

        if self.noGoRadioSin.isChecked() == True:
            noGoWtype = "Sin"
        else:
            noGoWtype = "Square"

        if (int(self.NoGoList.currentText()[:-1]) == 0):
            self.NoGoPic = "media\\" + noGoWtype.lower() + "Vert.png"
            self.NoGoArrow = "media\\rightRedArrow.png"
        elif (int(self.NoGoList.currentText()[:-1]) == 45):
            self.NoGoPic = "media\\" + noGoWtype.lower() + "Diag.png"
            self.NoGoArrow = "media\\rightRedArrow.png"
        elif (int(self.NoGoList.currentText()[:-1]) == 225):
            self.NoGoPic = "media\\" + noGoWtype.lower() + "Diag.png"
            self.NoGoArrow = "media\\leftRedArrow.png"
        elif (int(self.NoGoList.currentText()[:-1]) == 135):
            self.NoGoPic = "media\\" + noGoWtype.lower() + "InvDiag.png"
            self.NoGoArrow = "media\\leftRedArrow.png"
        elif (int(self.NoGoList.currentText()[:-1]) == 180):
            self.NoGoPic = "media\\" + noGoWtype.lower() + "Vert.png"
            self.NoGoArrow = "media\\leftRedArrow.png"
        elif (int(self.NoGoList.currentText()[:-1]) == 90):
            self.NoGoPic = "media\\" + noGoWtype.lower() + "Horiz.png"
            self.NoGoArrow = "media\\downRedArrow.png"
        elif (int(self.NoGoList.currentText()[:-1]) == 270):
            self.NoGoPic = "media\\" + noGoWtype.lower() + "Horiz.png"
            self.NoGoArrow = "media\\upRedArrow.png"
        else:
            self.NoGoPic = "media\\" + noGoWtype.lower() + "InvDiag.png"
            self.NoGoArrow = "media\\rightRedArrow.png"
        self.noGoCurrentImage.setPixmap(
            QPixmap(self.NoGoPic).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
        self.noGoArrowImage.setPixmap(
            QPixmap(self.NoGoArrow).scaled(50, 50, QtCore.Qt.KeepAspectRatio))

    def close_stim(self):
        anim_player.closeByGui()

    def passdata(self):
        # Passes data set to anim_player and start the task
        # globvar: [Gostimfilename, Nogostimfilename, waitBeforeAnimation
        #          firstAnimationLength, waitBetweenAnimations, secondAnimationLength, waitAfterAnimation]

        if self.goRadioSin.isChecked() == True:
            goWtype = "Sin"
        else:
            goWtype = "Square"
        settings.globvar.append(
            goWtype + self.GoList.currentText()[:-1] + ".ani")
        if self.noGoRadioSin.isChecked() == True:
            noGoWtype = "Sin"
        else:
            noGoWtype = "Square"
        settings.globvar.append(
            noGoWtype + self.NoGoList.currentText()[:-1] + ".ani")

        settings.globvar.append(float(self.waitBeforeAnimation.value()))
        settings.globvar.append(float(self.firstAnimationLength.value()))
        settings.globvar.append(float(self.waitBetweenAnimations.value()))
        settings.globvar.append(float(self.secondAnimationLength.value()))
        settings.globvar.append(float(self.waitAfterAnimation.value()))

        if (int(self.GoList.currentText()[:-1]) == 0 or int(self.GoList.currentText()[:-1]) == 180):
            settings.globvar.append(goWtype.lower() + "Vert.png")
        elif (int(self.GoList.currentText()[:-1]) == 45 or int(self.GoList.currentText()[:-1]) == 225):
            settings.globvar.append(goWtype.lower() + "Diag.png")
        elif (int(self.GoList.currentText()[:-1]) == 90 or int(self.GoList.currentText()[:-1]) == 270):
            settings.globvar.append(goWtype.lower() + "Horiz.png")
        else:
            settings.globvar.append(goWtype.lower() + "InvDiag.png")

        if (int(self.NoGoList.currentText()[:-1]) == 0 or int(self.NoGoList.currentText()[:-1]) == 180):
            settings.globvar.append(noGoWtype.lower() + "Vert.png")
        elif (int(self.NoGoList.currentText()[:-1]) == 45 or int(self.NoGoList.currentText()[:-1]) == 225):
            settings.globvar.append(noGoWtype.lower() + "Diag.png")
        elif (int(self.NoGoList.currentText()[:-1]) == 90 or int(self.NoGoList.currentText()[:-1]) == 270):
            settings.globvar.append(noGoWtype.lower() + "Horiz.png")
        else:
            settings.globvar.append(noGoWtype.lower() + "InvDiag.png")

        # print(settings.globvar)
        anim_player.run()


class LoadDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__()

        def fillList(self):
            listOfFiles = os.listdir(
                str(Path().absolute()) + "\\sessionData\\")
            for i in range(len(listOfFiles)):
                QListWidgetItem(listOfFiles[i][:-4], self.chooseBox)

        # Create Layouts
        loadLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()

        # Create Widgets
        self.chooseBox = QListWidget()
        self.loadButton = QPushButton("Load")
        self.deleteButton = QPushButton("Delete")
        self.cancelButton = QPushButton("Cancel")

        # Configure widgets
        self.chooseBox.setSortingEnabled(True)

        # Configure Layouts
        loadLayout.addWidget(self.chooseBox)
        loadLayout.addWidget(self.loadButton)
        buttonLayout.addWidget(self.deleteButton)
        buttonLayout.addWidget(self.cancelButton)
        loadLayout.addLayout(buttonLayout)

        self.setLayout(loadLayout)
        fillList(self)

        # Sgnals
        self.cancelButton.clicked.connect(self.onClose)
        self.loadButton.clicked.connect(self.onLoad)
        self.deleteButton.clicked.connect(self.onDelete)

    @Slot()
    def onClose(self):
        self.close()

    def onDelete(self):
        deleteMsg = QMessageBox.warning(self, self.tr("Delete"), self.tr(
            "Are you sure?\n" + "This will delete the file that belongs to this mouse."), QMessageBox.Yes | QMessageBox.Cancel)

        if deleteMsg == QMessageBox.Yes:
            os.remove(str(Path().absolute()) + "\\sessionData\\" +
                      self.chooseBox.currentItem().text() + ".txt")
            self.chooseBox.takeItem(self.chooseBox.currentRow())

    def onLoad(self):

        # print(self.chooseBox.currentItem().text())
        with open(str(Path().absolute()) + "\\sessionData\\" + self.chooseBox.currentItem().text() + ".txt") as openfileobject:
            settingsLine = openfileobject.readline().split(', ')

            lineInList = list()
            lineInList.append(settingsLine[0][1:-1])
            lineInList.append(settingsLine[1][1:-1])
            lineInList.append(settingsLine[2][1:-1])
            lineInList.append(settingsLine[3][1:-1])
            lineInList.append(settingsLine[4][1:-1])
            lineInList.append(settingsLine[5])
            lineInList.append(settingsLine[6])
            lineInList.append(settingsLine[7])
            lineInList.append(settingsLine[8])
            lineInList.append(settingsLine[9])

        if (lineInList[1] == "Sin"):
            window.goRadioSin.setChecked(True)
        else:
            window.goRadioSquare.setChecked(True)

        window.GoList.setCurrentText(lineInList[2])

        if (lineInList[3] == "Sin"):
            window.noGoRadioSin.setChecked(True)
        else:
            window.noGoRadioSquare.setChecked(True)

        window.NoGoList.setCurrentText(lineInList[4])

        window.waitBeforeAnimation.setValue(float(lineInList[5]))
        window.firstAnimationLength.setValue(float(lineInList[6]))
        window.waitBetweenAnimations.setValue(float(lineInList[7]))
        window.secondAnimationLength.setValue(float(lineInList[8]))
        window.waitAfterAnimation.setValue(float(lineInList[9]))
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    splashimg = QPixmap("media\\splash.jpg")
    splash = QSplashScreen(splashimg)
    progressBar = QProgressBar(splash)
    progressBar.setMaximum(10)
    progressBar.setGeometry(0, splashimg.height() - 15, splashimg.width(), 15)
    splash.show()
    splash.showMessage("<h1><font color='black'>Femto VisStimManager</font></h1>")

    for i in range(1, 11):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()

    time.sleep(1)

    # Create the Qt Application
    settings.init()
    window = VisStimManager()
    window.setWindowIcon(QIcon("icon.ico"))

    # Create and show the form
    window.setWindowTitle("VisStimManager")
    window.resize(250, 150)
    window.show()
    splash.finish(window)

    # Run the main Qt loop
    sys.exit(app.exec_())

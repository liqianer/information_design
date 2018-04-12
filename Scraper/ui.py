import sys
import qdarkstyle

from PyQt5.QtCore import QThread
from scraper import Scraper
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QGridLayout, QPushButton,
    QFileDialog, QApplication, QProgressBar, QMessageBox, QMainWindow,
    QGroupBox, QVBoxLayout)

class MyScraper(QMainWindow):
    savedNum = 0
    suc = 0
    fail = 0

    def __init__(self):
        super().__init__()
        self.stat = self.statusBar()
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        # 基本设置
        gridGroupBox1 = QGroupBox("基本设置")
        grid1 = QGridLayout()
        grid1.setSpacing(10)

        urlLabel = QLabel('url文件：')
        self.urlPath = QLineEdit()
        selectUrlFile = QPushButton('选择文件')
        grid1.addWidget(urlLabel, 1, 0)
        grid1.addWidget(self.urlPath, 1, 1)
        grid1.addWidget(selectUrlFile, 1, 3)
        selectUrlFile.clicked.connect(self.showDialog)

        resultLabel = QLabel('结果文件夹：')
        self.resultPath = QLineEdit()
        selectResultPath = QPushButton('选择文件夹')
        grid1.addWidget(resultLabel, 2, 0)
        grid1.addWidget(self.resultPath, 2, 1)
        grid1.addWidget(selectResultPath, 2, 3)
        selectResultPath.clicked.connect(self.showDialog)

        self.sleepLabel = QLabel("延时：")
        self.sleepTime = QLineEdit("0")
        self.start = QPushButton('开始爬取')
        grid1.addWidget(self.sleepLabel, 4, 0)
        grid1.addWidget(self.sleepTime, 4, 1)
        grid1.addWidget(self.start, 4, 3)

        self.start.clicked.connect(self.startTask)

        grid1.setColumnStretch(1, 10)
        gridGroupBox1.setLayout(grid1)

        # 代理设置
        gridGroupBox2 = QGroupBox("代理设置(阿布云)")
        grid2 = QGridLayout()
        grid2.setSpacing(10)

        userLabel = QLabel("用户名：")
        self.user = QLineEdit("")
        passLabel = QLabel("密码:")
        self.password = QLineEdit("")
        grid2.addWidget(userLabel, 1, 0)
        grid2.addWidget(self.user, 1, 1)
        grid2.addWidget(passLabel, 2, 0)
        grid2.addWidget(self.password, 2, 1)

        gridGroupBox2.setLayout(grid2)

        # 进度设置
        gridGroupBox3 = QGroupBox("进度")
        grid3 = QGridLayout()
        grid3.setSpacing(10)

        self.progress = QProgressBar()
        self.successLabel = QLabel('成功数：' + str(0))
        self.errorLabel = QLabel('失败数：' + str(0))
        grid3.addWidget(self.successLabel, 1, 0)
        grid3.addWidget(self.errorLabel, 1, 1)
        grid3.addWidget(self.progress, 2, 0, 1, 3)

        gridGroupBox3.setLayout(grid3)

        # 总体布局
        mainLayout.addWidget(gridGroupBox1)
        mainLayout.addWidget(gridGroupBox2)
        mainLayout.addWidget(gridGroupBox3)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)

        self.setWindowTitle("Ethan's Scraper")
        self.setCentralWidget(mainWidget)

    def showDialog(self):
        sender = self.sender()
        if sender.text() == '选择文件':
            urlPathText = QFileDialog.getOpenFileName(self, '选择文件', '.')
            self.urlPath.setText(urlPathText[0])
        elif sender.text() == '选择文件夹':
            resultPathText = QFileDialog.getExistingDirectory(self, '选择文件夹', '.')
            self.resultPath.setText(resultPathText)

    def startTask(self):
        self.start.setEnabled(False)

        urlPathText = self.urlPath.text()
        resultPathText = self.resultPath.text()
        user = self.user.text()
        pw = self.password.text()
        sleepTime = float(self.sleepTime.text())

        if urlPathText and resultPathText:
            self.scraperThread = QThread()
            self.scraper = Scraper(urlPathText, resultPathText, sleepTime, user, pw)

            # 绑定信号与槽
            self.scraper.maxSignal.connect(self.setMax)
            self.scraper.addsSignal.connect(self.setSuc)
            self.scraper.addfSignal.connect(self.setFail)
            self.scraper.setStatSignal.connect(self.updateStat)
            self.scraper.setProSignal.connect(self.setPro)

            self.scraper.moveToThread(self.scraperThread)

            self.scraper.finishSignal.connect(self.scraperThread.quit)
            self.scraperThread.started.connect(self.scraper.task)
            self.scraperThread.finished.connect(self.finishScraper)

            # 启动线程
            self.scraperThread.start()

    def setSuc(self):
        self.suc += 1
        self.successLabel.setText('成功数：' + str(self.suc))

    def setFail(self, num):
        self.fail += 1
        self.errorLabel.setText('失败数：' + str(self.fail))

    def setPro(self):
        self.savedNum += 1
        self.progress.setValue(self.savedNum)

    def updateStat(self, s):
        self.stat.showMessage(s)

    def setMax(self, num):
        self.progress.setMaximum(num)

    def finishScraper(self):
        QMessageBox.information(self, '提示', '任务已完成', QMessageBox.Yes | QMessageBox.No)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    myScraper = MyScraper()
    myScraper.show()
    sys.exit(app.exec_())
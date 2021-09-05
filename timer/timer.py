# -*- coding: utf-8 -*-
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import sys
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.tot = SubTimer()
        self.tot.start()
        self.br = SubTimer()
        self.t = QTimer(self)
        self.t.start(1000)
        self.t.timeout.connect(self.dp)
        self.dp_option = 'total'


    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(600, 280)
        self.button_total = QPushButton(Dialog)
        self.button_total.setObjectName(u"button_total")
        self.button_total.setGeometry(QRect(20, 40, 90, 50))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(18)
        font.setBold(False)
        self.button_total.setFont(font)
        self.button_total.clicked.connect(self.tb_clicked)

        self.button_break = QPushButton(Dialog)
        self.button_break.setObjectName(u"button_break")
        self.button_break.setGeometry(QRect(20, 150, 90, 50))
        self.button_break.setFont(font)
        self.button_break.clicked.connect(self.bb_clicked)

        self.dp_total = QLCDNumber(Dialog)
        self.dp_total.setObjectName(u"dp_total")
        self.dp_total.setGeometry(QRect(130, 20, 450, 90))
        self.dp_total.setDigitCount(8)
        self.dp_break = QLCDNumber(Dialog)
        self.dp_break.setObjectName(u"dp_break")
        self.dp_break.setGeometry(QRect(130, 130, 450, 90))
        self.dp_break.setDigitCount(8)
        self.button_save = QPushButton(Dialog)
        self.button_save.setObjectName(u"save")
        self.button_save.setGeometry(QRect(500, 240, 75, 25))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(10)
        font1.setBold(False)
        self.button_save.setFont(font1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Timer", None))
        self.button_total.setText(QCoreApplication.translate("Dialog", u"Total", None))
        self.button_break.setText(QCoreApplication.translate("Dialog", u"Break", None))
        self.button_save.setText(QCoreApplication.translate("Dialog", u"Save", None))

    def converter(self, integer_time):
        m, s = divmod(integer_time, 60)
        h, m = divmod(m, 60)
        return f'{h:02}:{m:02}:{s:02}'

    def dp(self):
        if self.dp_option == 'total':
            tos = self.tot.get_elapsed()
        elif self.dp_option == 'study':
            tos = self.tot.get_elapsed() - self.br.get_elapsed()
        self.dp_total.display(self.converter(tos))
        self.dp_break.display(self.converter(self.br.get_elapsed()))

    def start_break(self):
        self.dp_break.start()

    def bb_clicked(self):
        if self.sender().text() == 'Break':
            self.br.start()
            self.sender().setText('Study')
        elif self.sender().text() == 'Study':
            self.br.stop()
            self.sender().setText('Break')

    def tb_clicked(self):
        if self.sender().text() == 'Total':
            self.dp_option = 'study'
            self.sender().setText('Study')
        elif self.sender().text() == 'Study':
            self.dp_option = 'total'
            self.sender().setText('Total')


class Timer:
    def __init__(self):
        self.epoch = int(163e7)
        self.launch = int(time.time())
        self.d_epoch, self.s_epoch = divmod((self.launch - self.epoch), 86400)
        self.elapsed = 0

    def get_launch(self):
        return self.launch

    def get_epoch_day(self):
        return self.d_epoch

    def get_epoch_second(self):
        return self.s_epoch

    def get_elapsed(self):
        self.elapsed = int(time.time()) - self.launch
        return self.elapsed
    
    def get_everything(self):
        self.get_elapsed()
        return self.__dict__


class SubTimer(Timer):
    def __init__(self):
        Timer.__init__(self)
        self.d, self.s = divmod(self.launch, 86400)
        self.temp = self.launch
        self.started = False

    def get_day(self):
        return self.d

    def get_second(self):
        return self.s
    
    def start(self):
        self.started = True
        self.temp = int(time.time())

    def stop(self):
        self.started = False
        self.elapsed += int(time.time()) - self.temp

    def get_elapsed(self):
        if not self.elapsed and self.started:
            return int(time.time()) - self.temp
        elif self.started:
            return self.elapsed + int(time.time()) - self.temp
        return self.elapsed


def main():    
    launch = Timer()
    app = QApplication()
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

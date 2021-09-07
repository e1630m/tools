# -*- coding: utf-8 -*-
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import re
import sys
import time

class Timer(QMainWindow):
    def __init__(self):
        super(Timer, self).__init__()
        self.setupUi(self)
        self.epoch = int(163e7)
        self.launch = self.temp = int(time.time())
        self.d_epoch, self.s_epoch = divmod((self.launch - self.epoch), 86400)
        self.br_elapsed = 0
        self.br_started = False

        self.qtimer = QTimer(self)
        self.qtimer.start(1000)
        self.qtimer.timeout.connect(self.display_time)

        self.autosave = QTimer(self)
        self.autosave.start(60000)
        self.autosave.timeout.connect(self.save_log)
        
        self.parent_path = ''.join('/' if c == '\\' else c for c in sys.path[0])
        self.log_name = self.parent_path + '/timer.log'

    def setupUi(self, Timer):
        if not Timer.objectName():
            Timer.setObjectName(u"Timer")
        Timer.resize(602, 343)
        self.centralwidget = QWidget(Timer)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lcd_total = QLCDNumber(self.centralwidget)
        self.lcd_total.setObjectName(u"lcd_total")
        self.lcd_total.setGeometry(QRect(130, 10, 450, 90))
        self.lcd_total.setDigitCount(8)
        self.label_total = QLabel(self.centralwidget)
        self.label_total.setObjectName(u"label_total")
        self.label_total.setGeometry(QRect(20, 30, 90, 50))
        font_label = QFont()
        font_label.setPointSize(18)
        font_label.setBold(True)
        self.label_total.setFont(font_label)
        self.label_total.setAlignment(Qt.AlignCenter)
        self.lcd_study = QLCDNumber(self.centralwidget)
        self.lcd_study.setObjectName(u"lcd_study")
        self.lcd_study.setGeometry(QRect(130, 110, 450, 90))
        self.lcd_study.setDigitCount(8)
        self.lcd_break = QLCDNumber(self.centralwidget)
        self.lcd_break.setObjectName(u"lcd_break")
        self.lcd_break.setGeometry(QRect(130, 210, 450, 90))
        self.lcd_break.setDigitCount(8)
        self.label_study = QLabel(self.centralwidget)
        self.label_study.setObjectName(u"label_study")
        self.label_study.setGeometry(QRect(20, 130, 90, 50))
        self.label_study.setFont(font_label)
        self.label_study.setAlignment(Qt.AlignCenter)
        self.label_break = QLabel(self.centralwidget)
        self.label_break.setObjectName(u"label_break")
        self.label_break.setGeometry(QRect(20, 230, 90, 50))
        self.label_break.setFont(font_label)
        self.label_break.setAlignment(Qt.AlignCenter)
        self.btn_choose = QPushButton(self.centralwidget)
        self.btn_choose.setObjectName(u"btn_choose")
        self.btn_choose.setGeometry(QRect(320, 310, 75, 25))
        font_button = QFont()
        font_button.setPointSize(13)
        font_button.setBold(False)
        self.btn_choose.setFont(font_button)
        self.btn_choose.clicked.connect(self.btn_clicked)
        self.btn_save = QPushButton(self.centralwidget)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setGeometry(QRect(410, 310, 75, 25))
        self.btn_save.clicked.connect(self.save_log)
        self.btn_save.setFont(font_button)
        self.btn_load = QPushButton(self.centralwidget)
        self.btn_load.setObjectName(u"btn_load")
        self.btn_load.setGeometry(QRect(500, 310, 75, 25))
        self.btn_load.clicked.connect(self.load_log)
        self.btn_load.setFont(font_button)
        Timer.setCentralWidget(self.centralwidget)

        Timer.setWindowTitle(QCoreApplication.translate("Timer", u"Study Timer 0.1.0", None))
        self.label_total.setText(QCoreApplication.translate("Timer", u"Total", None))
        self.label_study.setText(QCoreApplication.translate("Timer", u"Study", None))
        self.label_break.setText(QCoreApplication.translate("Timer", u"Break", None))
        self.btn_choose.setText(QCoreApplication.translate("Timer", u"Break", None))
        self.btn_save.setText(QCoreApplication.translate("Timer", u"Save", None))
        self.btn_load.setText(QCoreApplication.translate("Timer", u"Load", None))

        QMetaObject.connectSlotsByName(Timer)

    
    def start(self):
        self.br_started = True
        self.temp = int(time.time())

    def stop(self):
        self.br_started = False
        self.br_elapsed += int(time.time()) - self.temp

    def get_elapsed(self):
        if self.br_started:
           return self.br_elapsed + int(time.time()) - self.temp
        return self.br_elapsed

    def converter(self, integer_time):
        m, s = divmod(integer_time, 60)
        h, m = divmod(m, 60)
        return f'{h:02}:{m:02}:{s:02}'

    def display_time(self):
        tot = int(time.time()) - self.launch
        br = self.get_elapsed()
        st = tot - br
        self.lcd_total.display(self.converter(tot))
        self.lcd_study.display(self.converter(st))
        self.lcd_break.display(self.converter(br))

    def btn_clicked(self):
        if self.sender().text() == 'Break':
            self.start()
            self.sender().setText('Study')
        elif self.sender().text() == 'Study':
            self.stop()
            self.sender().setText('Break')
        pass

    def save_log(self):
        with open(self.log_name, 'r') as f:
            tmp = f.readlines()
            if len(tmp) < self.d_epoch:
                if not len(tmp):
                    tmp += ['\n']
                elif not tmp[-1].endswith('\n'):
                    tmp[-1] += '\n'
            tmp += ['\n'] * (self.d_epoch - len(tmp) + (len(tmp) == 0))
        
        with open(self.log_name, 'w') as f:
            tmp[self.d_epoch - 1] = (f'D+{self.d_epoch:04}: '
                + f'Total: {int(time.time()) - self.launch}, '
                + f'Study: {int(time.time()) - self.launch - self.get_elapsed()}, '
                + f'Break: {self.get_elapsed()}')
            f.writelines(tmp[:self.d_epoch])

    def load_log(self):
        with open(self.log_name, 'r') as f:
            tmp = f.readlines()
            if len(tmp) < self.d_epoch or int(tmp[self.d_epoch - 1][2:6]) != self.d_epoch:
                print('Nothing to load')
            else:
                data = tmp[self.d_epoch - 1]
                search = re.findall("[\d]+", data)
                if len(search) == 4 and all(1 for i in search if type(i) == int):
                    self.launch = int(time.time()) - int(search[1])
                    self.br_elapsed = int(search[3])


def main():
    app = QApplication()
    ui = Timer()
    ui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtWidgets
import webbrowser
from main_window import Demo
import time
from main import main_spider
import os
################################################
#######创建主窗口
################################################
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wiget = Demo()
        self.setWindowTitle('主界面')
        self.showMaximized()
        # self.setFixedSize(self.width(), self.height())
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("resource/bg.jpg")))
        self.setPalette(window_pale)

################################################
#######主界面
################################################
class logindialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('云顶之弈最新阵容排行')
        self.setWindowIcon(QIcon('resource/win_icon.jpg'))
        self.desktop = QApplication.desktop()

        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()

        self.setFixedSize(self.width*2/3, self.height*3/4)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.setStyleSheet('''QDialog{border-image: url(resource/2.jpg)}''')
        # window_pale = QtGui.QPalette()
        # window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("resource/2.jpg")))
        # self.setPalette(window_pale)

        self.vbox_g = QVBoxLayout(self)

        self.hbox = QHBoxLayout(self)
        self.vbox = QVBoxLayout(self)
        self.sub_hbox1 = QHBoxLayout(self)
        self.sub_hbox2 = QHBoxLayout(self)

        self.title = QLabel(self)
        self.frame = QFrame(self)

        self.pbar = QProgressBar(self)
        # self.vLayout = QVBoxLayout(self.frame)
        # self.hLayout = QHBoxLayout(self.frame)
        # self.hLayout2 = QHBoxLayout(self.frame)

        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.9)

        self.pushButton_enter = QPushButton(self)
        self.pushButton_enter.setText("开始查询")
        self.pushButton_enter.setGraphicsEffect(op)

        self.pushButton_enter.setStyleSheet('''
                     QPushButton
                     {text-align : center;
                     color:white;
                     border-image: url(resource/es.png);
                     font: bold;
                     border-color: gray;
                     border-width: 2px;
                     border-radius: %dpx;
                     padding: 6px;

                     border-style: outset;
                     font : %dpx "微软雅黑";}
                     QPushButton:hover
                     {text-align : center;
                     border-image: url(resource/es_d.png)}
                     QPushButton:pressed
                     {text-align : center;
                     border-image: url(resource/es.png)}
                     
                     '''%(self.width/50, self.width/60))

        self.pushButton_quit = QPushButton(self)
        self.pushButton_quit.setText("更新数据")
        self.pushButton_quit.setStyleSheet(''' 
                             QPushButton
                             {text-align : center;
                             border-image: url(resource/es2.png);
                             font: bold;
                             border-color: gray;
                             border-width: 2px;
                             border-radius: %dpx;
                             padding: 6px;
                             border-style: outset;
                             font : %dpx "微软雅黑";}
                             QPushButton:hover
                             {text-align : center;
                             border-image: url(resource/es_d2.png)}
                             QPushButton:pressed
                             {text-align : center;
                             border-image: url(resource/es2.png)}
                             '''%(self.width/50,self.width/65))
        self.pushButton_quit.setGraphicsEffect(op)
        self.pushButton_enter.setFixedSize(self.width / 6, self.height/14)
        self.pushButton_quit.setFixedSize(self.width / 7, self.height/14)
        self.LOGO = QLabel(self)
        self.LOGO.setPixmap(QPixmap('resource\\logo.png'))
        # self.LOGO.setGeometry(0, self.width*0.005, self.width*0.5, self.height*0.36)
        self.LOGO.setScaledContents(True)

        self.vbox.setSpacing(self.height / 80)

        self.vbox.addStretch(1)
        self.vbox.addWidget(self.LOGO)
        # self.pushButton_enter.setGeometry(self.height*0.2, self.width*0.27, 400, 100)
        # self.pushButton_quit.setGeometry(340, 720, 320, 80)
        self.vbox.addStretch(2)

        self.sub_hbox1.addStretch(0.6)
        self.sub_hbox1.addWidget(self.pushButton_enter)
        self.sub_hbox1.addStretch(0.6)

        self.sub_hbox2.addStretch(0.6)
        self.sub_hbox2.addWidget(self.pushButton_quit)
        self.sub_hbox2.addStretch(0.6)

        self.vbox.addLayout(self.sub_hbox1)
        self.vbox.addLayout(self.sub_hbox2)
        self.vbox.addStretch(5)

        self.hbox.addStretch(1)
        self.hbox.addLayout(self.vbox)
        self.hbox.addStretch(15)
        self.vbox_g.addLayout(self.hbox)
        self.vbox_g.addWidget(self.pbar)
        self.setLayout(self.vbox_g)

        # self.pbar.setGeometry(0,910, 1440, 16)

        self.spider_thread = MyThread(self.pbar,self)
        ###### 绑定按钮事件
        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(self.update_data)

    def update_data(self):
        self.spider_thread.start()

    def on_pushButton_enter_clicked(self):
        if not os.path.exists('res') or not os.listdir('res'):
            self.update_data()
        else:
            self.pbar.setValue(99)
            time.sleep(0.5)
            self.accept()


class MyThread(QThread):
    def __init__(self,bar,dig):
        super(MyThread,self).__init__()
        self.bar = bar
        self.dialog = dig
    def run(self):
        self.threads = main_spider(self.bar)
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
        time.sleep(0.5)
        self.dialog.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = logindialog()
    if  dialog.exec_()==QDialog.Accepted:
        demo = Demo()
        demo.showMaximized()
        demo.setWindowTitle('Results')
        demo.setWindowIcon(QIcon('resource/win_icon.jpg'))
        sys.exit(app.exec_())

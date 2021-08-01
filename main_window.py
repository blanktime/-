import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont,QIcon
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtWidgets
import os


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.wiget = QWidget(self)
        self.Path = 'res/'
        self.cost_color={'cost1':'#808080',
                         'cost2':'#11b288',
                         'cost3':'#207ac7',
                         'cost4':'#c440da',
                         'cost5':'#ffb93b'}


        team_class_list = os.listdir(self.Path)

        v_box = QVBoxLayout(self.wiget)

        for id,tc in enumerate(team_class_list):
            if id==0:
                v_box.addLayout(self.rank_team(self.wiget,tc,top_title=True))
            else:
                v_box.addLayout(self.rank_team(self.wiget, tc))
        self.wiget.setLayout(v_box)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.wiget)

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.scroll_area)

        self.setLayout(self.h_layout)

        window_pale = QtGui.QPalette()
        window_pale.setColor(window_pale.Background,QtGui.QColor(34,34,34))
        self.setPalette(window_pale)

    def rank_team(self, wiget, team_class, top_title=False):
        team_list = os.listdir(os.path.join(self.Path,team_class))
        v_box = QVBoxLayout(wiget)
        h_box = QHBoxLayout(wiget)
        # title
        if top_title:
            Title_img = QLabel(self.wiget)
            Title_img.setPixmap(QPixmap('resource/bg2.png'))
            Title_img.setFixedHeight(300)
            Title_img.setScaledContents(True)
            v_box.addWidget(Title_img)
        for i in range(len(team_list)):
            if i == 0:
                grid_layout = QGridLayout(wiget)
                rank_label = QLabel(wiget)
                rank = team_class.split('_')[0].upper()
                if rank[3]=='0':
                    rank = rank.replace('0','-')
                else:
                    rl = list(rank)
                    rl.insert(3,'-')
                    rank=''.join(rl)

                rank_label.setText('  ' + rank)
                rank_label.setAlignment(Qt.AlignVCenter)
                if rank=='TOP-1':
                    color = self.cost_color['cost5']
                elif rank=='TOP-2':
                    color = self.cost_color['cost4']
                elif rank=='TOP-3':
                    color = self.cost_color['cost3']
                elif rank=='TOP-4':
                    color = self.cost_color['cost2']
                else:
                    color = 'white'
                rank_label.setStyleSheet('''
                                             QLabel
                                             {text-align : center;
                                             color: %s;
                                             background-color: #5e5e5e;
                                             height : 35px;
                                             font: bold;
                                             font : 25px Bahnschrift Condensed;}'''%color)
                rank_label.setFixedHeight(40)
                grid_layout.addWidget(rank_label, 0, 0, 2, 6)

                chess_class = QLabel(wiget)
                chess_class.setText(team_class.split('_')[1])

                chess_class.setAlignment(Qt.AlignCenter)
                chess_class.setStyleSheet('''
                                             QLabel
                                             {text-align : center;
                                             color: white;
                                             background-color: #5e5e5e;
                                             height : 35px;
                                             font: bold;
                                             font : 25px Bahnschrift Condensed;}''')

                grid_layout.addWidget(chess_class, 0, 5, 2, 21)
                wrate = QLabel(wiget)
                wrate.setText('WinRate%')
                wrate.setAlignment(Qt.AlignCenter)
                wrate.setStyleSheet('''
                                             QLabel
                                             {text-align : center;
                                             color: white;
                                             background-color: #5e5e5e;
                                             font: bold;
                                             font : 25px Bahnschrift Condensed;}''')
                grid_layout.addWidget(wrate, 0, 27, 2, 2)

                trate = QLabel(wiget)
                trate.setText('TOP4%')
                trate.setAlignment(Qt.AlignCenter)
                trate.setStyleSheet('''
                                             QLabel
                                             {text-align : center;
                                             color: white;
                                             background-color: #5e5e5e;
                                             font: bold;
                                             font : 25px Bahnschrift Condensed;}''')
                grid_layout.addWidget(trate, 0, 29, 2, 2)

                rrate = QLabel(wiget)
                rrate.setText('avgRank')
                rrate.setAlignment(Qt.AlignCenter)
                rrate.setStyleSheet('''
                                             QLabel
                                             {text-align : center;
                                             color: white;
                                             background-color: #5e5e5e;
                                             font: bold;
                                             font : 25px Bahnschrift Condensed;}''')
                grid_layout.addWidget(rrate, 0, 31, 2, 2)
                v_box.addLayout(grid_layout)
            else:
                border_line = QLabel(wiget)
                border_line.setStyleSheet('''QLabel{background-color: #5e5e5e}''')
                border_line.setFixedHeight(2)
                v_box.addWidget(border_line)

            team = team_list[i]
            v_box.addWidget(self.rank_unit(self.wiget, team_class, team))
            # h_box.addSpacing(20)

            h_box.addLayout(v_box)

        return h_box

    def rank_unit(self, wiget, team_class, team):
        Sub_wiget = QWidget(wiget)
        grid_layout = QGridLayout(Sub_wiget)
        grid_layout.setSpacing(10)


        QToolTip.setFont(QFont('Arial', 15))

        index = 0

        ori_path = os.path.join(self.Path,team_class, team, 'traits_list')

        trait = os.listdir(ori_path)
        ori_num = len(trait)

        if ori_num<=5:
            for j in range(5):
                ori_label = QLabel(Sub_wiget)
                ori_label.setFixedSize(50, 50)
                if j<ori_num:
                    ori_label.setPixmap(QPixmap(os.path.join(ori_path, trait[j])))
                    tip = trait[j].split('.')[0].split('_')[-1]
                    ori_label.setToolTip(tip)
                grid_layout.addWidget(ori_label, 0, j, 2, 1)
        else:
            for i in range(2):
                for j in range(5):
                    ori_label = QLabel(Sub_wiget)
                    ori_label.setFixedSize(50,50)
                    if (j+i*5)>=ori_num:
                        grid_layout.addWidget(ori_label, i, j+2, 1, 1)
                    else:
                        ori_label.setPixmap(QPixmap(os.path.join(ori_path,trait[j+i*5])))
                        tip = trait[j+i*5].split('.')[0].split('_')[-1]
                        ori_label.setToolTip(tip)
                        grid_layout.addWidget(ori_label, i, j+2, 1, 1)


        hero_path = os.path.join(self.Path, team_class,team, 'units_list')
        units = os.listdir(hero_path)
        max_num = len(units)

        for c in range(10):
            che_label = QLabel(Sub_wiget)
            che_label.setFixedSize(100, 100)

            op = QtWidgets.QGraphicsOpacityEffect()
            op.setOpacity(0.0)

            equip=[]
            if c < max_num:
                bg_label = QLabel(Sub_wiget)
                bg_label.setFixedSize(104, 104)

                link_label = QLabel(Sub_wiget)
                link_label.setFixedSize(100, 100)
                link_label.setGraphicsEffect(op)


                file = os.listdir(os.path.join(hero_path,units[c]))
                for n in file:
                    if n[0:4]=='star':
                        cost = n
                    elif n[0:4]=='item':
                        equip.append(n)
                    else:
                        name = n
                che_label.setPixmap(QPixmap(os.path.join(hero_path,units[c],name)))


                cost_label = QLabel(che_label)
                cost_label.setPixmap(QPixmap(os.path.join(hero_path, units[c], cost)))
                cost_label.setScaledContents(True)
                cost_label.setGeometry(34,3,32,10)
                cost_level = cost.split('_')[1]

                bg_label.setStyleSheet(''' QLabel{border-style: outset;
                                                border-color:%s;
                                                border-width:4px;}'''%self.cost_color[cost_level])

                for eq in range(3):
                    eq_label = QLabel(che_label)
                    if eq<len(equip):
                        eq_label.setPixmap(QPixmap(os.path.join(hero_path, units[c], equip[eq])))
                        eq_label.setScaledContents(True)
                        eq_label.setGeometry(75-eq*25,75,25,25)

                che_label.setScaledContents(True)

                link_label.setText('<a href="https://lolchess.gg/champions/set3.5/%s"><img src="resource/bg2.png"></a>'%name.split('.')[0].split('_')[1])
                link_label.setOpenExternalLinks(True)
                link_label.setToolTip(name.split('.')[0].split('_')[1])

                grid_layout.addWidget(bg_label,0, 7 + c * 2, 2, 2)
                grid_layout.addWidget(che_label, 0, 7 + c * 2, 2, 2)
                grid_layout.addWidget(link_label, 0, 7 + c * 2, 2, 2)
            else:
                grid_layout.addWidget(che_label, 0, 7 + c * 2, 2, 2)
        win_rate = QLabel(Sub_wiget)
        win_rate.setFixedSize(100,100)
        win_rate_path = os.path.join(self.Path, team_class, team, 'rates','win_rate.txt')
        with open(win_rate_path, "r") as f:  # 打开文件
            data = f.read()  # 读取文件
            win_rate.setText(data)

        win_rate.setAlignment(Qt.AlignCenter)
        win_rate.setStyleSheet('''
                        QLabel
                        {text-align : center;
                        color: white;
                        font : 25px Bahnschrift Condensed;}''')
        top4_rate = QLabel(Sub_wiget)
        top4_rate.setFixedSize(100,100)
        top4_rate_path = os.path.join(self.Path, team_class, team, 'rates', 'top4_rate.txt')
        with open(top4_rate_path, "r") as f:  # 打开文件
            data = f.read()  # 读取文件
            top4_rate.setText(data)
        top4_rate.setAlignment(Qt.AlignCenter)
        top4_rate.setStyleSheet('''
                            QLabel
                            {text-align : center;
                            color: white;
                            font : 25px Bahnschrift Condensed;}''')
        rank_rate = QLabel(Sub_wiget)
        rank_rate.setFixedSize(100,100)
        rank_rate_path = os.path.join(self.Path, team_class, team, 'rates', 'avg_rate.txt')
        with open(rank_rate_path, "r") as f:  # 打开文件
            data = f.read()  # 读取文件
            rank_rate.setText(data)

        rank_rate.setAlignment(Qt.AlignCenter)
        rank_rate.setStyleSheet('''
                                    QLabel
                                    {text-align : center;
                                    color: white;
                                    font : 25px Bahnschrift Condensed;}''')
        grid_layout.addWidget(win_rate, 0, 27, 2, 2)
        grid_layout.addWidget(top4_rate, 0, 29, 2, 2)
        grid_layout.addWidget(rank_rate, 0, 31, 2, 2)
        Sub_wiget.setLayout(grid_layout)
        return Sub_wiget


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     demo = Demo()
#     demo.showMaximized()
#     demo.setWindowTitle('Results')
#     demo.setWindowIcon(QIcon('resource/win_icon.jpg'))
#     sys.exit(app.exec_())
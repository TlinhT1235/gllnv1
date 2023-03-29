import os
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtGui import QPalette, QColor
except:
    os.system("pip install pyqt5")
    os.system("clear")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QColor
try: import requests
except: 
    os.system("pip install requests")
    os.system("clear")
import requests
import time, random, os, json, re

class GomLua(object):
    def __init__(self, tk, mk):
        self.tk = tk
        self.mk = mk
        self.headers = {
            'authority': 'gomlua.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'content-type': 'application/json',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }
    def _Login(self):
        _data = {
            "email": f"{self.tk}",
            "password": f"{self.mk}"
        }
        login = requests.post("https://gomlua.com/user/loginV2?os=web", data=_data).json()
        print(login)
        if "Thành công" in str(login):
            token = login["data"]["app_token"]
            self.headers.update({"app_token":token})
            curent_paddy = int(login["data"]["curent_paddy"])
            uid = login["data"]["uid"]
            return token, curent_paddy, uid
        else: return False
    def GetInFo(self):
        _info = requests.get("https://gomlua.com/user/info?os=web", headers=self.headers).json()
        if "Thanh cong" in str(_info):
            current_paddy = _info["data"]["current_paddy"]
            real_facebook_id = _info["data"]["real_facebook_id"]
            real_facebook_name = _info["data"]["real_facebook_name"]
            return current_paddy, real_facebook_id, real_facebook_name
    def GetLikePost(self):
        _getjob = requests.get("https://gomlua.com/cpi/listCampaignFacebook?os=web&type=like_post", headers=self.headers).json()
        if "Thanh cong" in str(_getjob) and _getjob["data"]["size"] > 0:
            return _getjob["data"]["list"]
        else: return False
    def CheckLink(self, id:str):
        _check = requests.get(f"https://gomlua.com/likeToken/checkLikeToken?os=web&link_id={id}", headers=self.headers).json()
        if str(_check["code"]) == "18":
            _check = requests.get(f"https://gomlua.com/cpi/checkLinkLike?os=web&link_id={id}", headers=self.headers).json()
            if _check["status"] == 1:
                return "cpi"
            else: return False
        return "likeToken"        
    def Report(self, cpi_id):
        _report = requests.get(f"https://gomlua.com/cpi/reportBug?site=web&cpi_id={cpi_id}&type=LIKE&report_type=PADDY", headers=self.headers, timeout=30).json()
        print(_report)
    def Receive(self, type, link_id):
        try:
            if type == "cpi":
                _receive = requests.get(f"https://gomlua.com/cpi/likeSuccess?os=web&link_id={link_id}&like_old=1", headers=self.headers).json()
            else:
                _receive =requests.get(f"https://gomlua.com/likeToken/likeSuccess?os=web&link_id={link_id}&like_count=1", headers=self.headers).json()
            print(_receive)
            if int(_receive["status"]) == 1:
                return True
            elif int(_receive["code"]) == 554:
                return "continue"
            elif int(_receive["code"]) == 504:
                return "continue"
            elif int(_receive["code"]) == 2:
                return "continue"
            elif int(_receive["code"]) == 19:
                return False
            elif int(_receive["code"]) == 507:
                return False
            elif _receive["message"] == "Vui lòng đợi 1s tiếp theo để thực hiện ":
                return "continue"
            elif _receive["message"] == "Bạn chưa thực hiện LIKE chiến dịch !":
                return False
            else: return False
        except Exception as loi:
            print(loi,'                     ')
            return False

class GetData:
    def __init__(self, tk, mk, fa):
        self.tk = tk
        self.mk = mk
        self.fa = fa
    def getToken(self):
        try:
            headers = {
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 12; M2101K7BG Build/SP1A.210812.016) [FBAN/MobileAdsManagerAndroid;FBAV/303.0.0.28.104;FBBV/413414122;FBRV/0;FBLC/vi_VN;FBMF/Xiaomi;FBBD/Redmi;FBDV/M2101K7BG;FBSV/12;FBCA/arm64-v8a:armeabi-v7a:armeabi;FBDM/{density=2.75,width=1080,height=2263};FB_FW/1;]',
                'Content-Type': 'application/json'
            }
            data = {'locale':'vi_VN','format':'json','email':self.tk,'password':self.mk,'access_token':'350685531728|62f8ce9f74b12f84c123cc23437a4a32','generate_session_cookies':"True"}
            done = requests.post(url="https://graph.facebook.com/auth/login", headers=headers, data=data).json()
            if done['error']['code'] == 406:
                loginFist = done['error']['error_data']['login_first_factor']
                uid = done['error']['error_data']['uid']
                code = requests.get(f'https://2fa.live/tok/{self.fa}').json()['token']
                _data = {
                    "locale": "vi_VN",
                    "format": "json",
                    "email": self.tk,
                    "password": self.mk,
                    "credentials_type": "two_factor",
                    "userid": uid,
                    "twofactor_code": code,
                    "first_factor": loginFist,
                    "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
                    "generate_session_cookies": "true",
                    "generate_machine_id": "true"
                }
                _headers = {
                    'Content-Type': 'application/json'
                }
                done = requests.post(url="https://graph.facebook.com/auth/login", headers=_headers, data=_data).json()
                if ('access_token' and 'session_cookies') in done:
                    token = done['access_token']
                    ck = done['session_cookies']
                    cookie = "wd=485x366;m_pixel_ratio=0.47999998927116394;"
                    for i in range(len(ck)):
                        name = ck[i]['name']
                        value = ck[i]['value']
                        data = name+'='+value+';'
                        cookie += data
                    return token, cookie
                else:
                    print(done)
                    return False
            else:
                return False
        except: return False

class Facebook:
    def __init__(self, cookie: str, token, pr=None):
        self.token = token
        try:
            if pr != None:
                tach = pr.split(':')
                if tach[3]:
                    self.proxy = {
                            'http':'http://{0}:{1}@{2}:{3}'.format(tach[2],tach[3],tach[0],tach[1]),
                            'https':'http://{0}:{1}@{2}:{3}'.format(tach[2],tach[3],tach[0],tach[1]),
                    }
                else:
                    self.proxy = {
                        'http':'http://{}'.format(pr),
                        'https':'http://{}'.format(pr),
                    }
            else:
                self.proxy = None
        except:
            self.proxy = None
        self.headers = {
            'authority': 'mbasic.facebook.com',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'cookie': cookie,
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        self.user = cookie.split('c_user=')[1].split(';')[0]
    def check(self):
        a = requests.get("https://mbasic.facebook.com/", headers=self.headers, proxies=self.proxy).text
        if 'checkpoint' in a:
            return 'checkpoint'
        elif "<title>Facebook - Đăng nhập hoặc đăng ký</title>" in a:
            return 'cookie die'
        else:
            name = requests.get('https://mbasic.facebook.com/profile.php',headers=self.headers,proxies=self.proxy).text.split('title>')[1].split('</')[0]
            return name
    def GetPosID(self, link):
        try:
            pos = requests.get(link, headers=self.headers, proxies=self.proxy).text
            try:
                _pos = pos.split('"subscription_target_id":"')[1].split('"')[0]
            except:
                _pos = pos.split('"post_id":"')[1].split('"')[0]
            return _pos
        except: return False
    def reaction(self, id: str, type_reaction: str):
        try:
            host = 'https://mbasic.facebook.com'
            url = host+f'/reactions/picker/?is_permalink=1&ft_id={id}'
            a = requests.get(url, headers=self.headers, proxies=self.proxy).text
            b= re.findall('/ufi/reaction/?.*?"',a)
            if b == []: return False
            else:
                number = 0 if type_reaction == "LIKE" else 1 if type_reaction == "LOVE" else 2 if type_reaction == "CARE" else 3 if type_reaction == "HAHA" else 4 if type_reaction == "WOW" else 5 if type_reaction == "SAD" else 6
                c = b[number].replace('amp;','').replace('"','')
                url = host+c
                done = requests.get(url=url, headers=self.headers,proxies=self.proxy).text
                if "title>Facebook - Đăng nhập hoặc đăng ký</title>" in done:
                    return "cookie die"
                filet = open("test.txt","w",encoding="utf-8")
                filet.write(done)
        except: return False

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(1470, 800)
        MainWindow.setMaximumSize(1470, 800)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/gomlua.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 1171, 771))
        font = QtGui.QFont()
        font.setFamily("Sitka Banner")
        font.setPointSize(13)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget.setGeometry(QtCore.QRect(15, 31, 1141, 721))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.tableWidget.setFont(font)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.tableWidget.setLineWidth(3)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        self.groupBox_confing = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_confing.setGeometry(QtCore.QRect(1190, 0, 261, 321))
        self.groupBox_confing.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Sitka Banner")
        font.setPointSize(13)
        self.groupBox_confing.setFont(font)
        self.groupBox_confing.setFlat(False)
        self.groupBox_confing.setCheckable(False)
        self.groupBox_confing.setObjectName("groupBox_confing")
        self.label_dlmin = QtWidgets.QLabel(self.groupBox_confing)
        self.label_dlmin.setGeometry(QtCore.QRect(20, 40, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Banner")
        font.setPointSize(12)
        self.label_dlmin.setFont(font)
        self.label_dlmin.setStyleSheet("color: rgb(255, 85, 255)")
        self.label_dlmin.setObjectName("label_dlmin")
        self.label_dlmax = QtWidgets.QLabel(self.groupBox_confing)
        self.label_dlmax.setGeometry(QtCore.QRect(20, 80, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Banner")
        font.setPointSize(12)
        self.label_dlmax.setFont(font)
        self.label_dlmax.setStyleSheet("color: rgb(255, 85, 255)")
        self.label_dlmax.setObjectName("label_dlmax")
        self.spin_min = QtWidgets.QSpinBox(self.groupBox_confing)
        # self.spin_min.setGeometry(QtCore.QRect(160, 40, 42, 31))
        self.spin_min.setGeometry(QtCore.QRect(155, 40, 70, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        self.spin_min.setFont(font)
        self.spin_min.setObjectName("spin_min")
        self.spin_max = QtWidgets.QSpinBox(self.groupBox_confing)
        self.spin_max.setGeometry(QtCore.QRect(155, 80, 70, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        self.spin_max.setFont(font)
        self.spin_max.setObjectName("spin_max")
        self.pushButton_startall = QtWidgets.QPushButton(self.groupBox_confing)
        self.pushButton_startall.setGeometry(QtCore.QRect(30, 260, 93, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(10)
        self.pushButton_startall.setFont(font)
        self.pushButton_startall.setStyleSheet("color: blue;\n"
            "background-color: #87CEFA;\n"
            "border-style: dashed;\n"
            "border-width: 3px;\n"
            "border-color: #1E90FF"
        )
        self.pushButton_startall.setCheckable(False)
        self.pushButton_startall.setAutoDefault(False)
        self.pushButton_startall.setDefault(False)
        self.pushButton_startall.setFlat(False)
        self.pushButton_startall.setObjectName("pushButton_startall")
        self.pushButton_stopall = QtWidgets.QPushButton(self.groupBox_confing)
        self.pushButton_stopall.setGeometry(QtCore.QRect(140, 260, 93, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(10)
        self.pushButton_stopall.setFont(font)
        self.pushButton_stopall.setStyleSheet("color: green;\n"
            "background-color: #7FFFD4;\n"
            "border-style: dashed;\n"
            "border-width: 3px;"
        )
        self.pushButton_stopall.setObjectName("pushButton_stopall")
        self.label_dthread = QtWidgets.QLabel(self.groupBox_confing)
        self.label_dthread.setGeometry(QtCore.QRect(20, 120, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Banner")
        font.setPointSize(12)
        self.label_dthread.setFont(font)
        self.label_dthread.setStyleSheet("color: rgb(255, 85, 255)")
        self.label_dthread.setObjectName("label_dthread")
        self.spin_max_2 = QtWidgets.QSpinBox(self.groupBox_confing)
        self.spin_max_2.setGeometry(QtCore.QRect(155, 120, 70, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        self.spin_max_2.setFont(font)
        self.spin_max_2.setObjectName("spin_max_2")
        self.label = QtWidgets.QLabel(self.groupBox_confing)
        self.label.setGeometry(QtCore.QRect(20, 200, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Banner")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 85, 255)")
        self.label.setObjectName("label")
        self.lineEdit_jobmax = QtWidgets.QLineEdit(self.groupBox_confing)
        self.lineEdit_jobmax.setGeometry(QtCore.QRect(161, 200, 60, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.lineEdit_jobmax.setFont(font)
        self.lineEdit_jobmax.setObjectName("lineEdit_jobmax")
        self.label_2 = QtWidgets.QLabel(self.groupBox_confing)
        self.label_2.setGeometry(QtCore.QRect(220, 200, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Banner")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 85, 255)")
        self.label_2.setObjectName("label_2")
        self.spin_max_3 = QtWidgets.QSpinBox(self.groupBox_confing)
        self.spin_max_3.setGeometry(QtCore.QRect(155, 160, 70, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        self.spin_max_3.setFont(font)
        self.spin_max_3.setObjectName("spin_max_3")
        self.label_dthread_2 = QtWidgets.QLabel(self.groupBox_confing)
        self.label_dthread_2.setGeometry(QtCore.QRect(20, 160, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Banner")
        font.setPointSize(12)
        self.label_dthread_2.setFont(font)
        self.label_dthread_2.setStyleSheet("color: rgb(255, 85, 255)")
        self.label_dthread_2.setObjectName("label_dthread_2")
        self.groupBox_job = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_job.setGeometry(QtCore.QRect(1190, 330, 261, 169))
        font = QtGui.QFont()
        font.setFamily("Sitka Banner")
        font.setPointSize(13)
        self.groupBox_job.setFont(font)
        self.groupBox_job.setFlat(False)
        self.groupBox_job.setCheckable(False)
        self.groupBox_job.setObjectName("groupBox_job")
        self.checkBox_like = QtWidgets.QCheckBox(self.groupBox_job)
        self.checkBox_like.setGeometry(QtCore.QRect(30, 44, 190, 33))
        font = QtGui.QFont()
        font.setFamily("Sitka Banner")
        font.setPointSize(12)
        self.checkBox_like.setFont(font)
        self.checkBox_like.setTabletTracking(False)
        self.checkBox_like.setStyleSheet("")
        self.checkBox_like.setIcon(QtGui.QIcon("icon/iconlike.png"))
        self.checkBox_like.setObjectName("checkBox_like")
        self.checkBox_comment = QtWidgets.QCheckBox(self.groupBox_job)
        self.checkBox_comment.setGeometry(QtCore.QRect(30, 84, 190, 33))
        font = QtGui.QFont()
        font.setFamily("Sitka Banner")
        font.setPointSize(12)
        self.checkBox_comment.setFont(font)
        self.checkBox_comment.setIcon(QtGui.QIcon("icon/cmt2.png"))
        # self.checkBox_comment.setStyleSheet("background-color: #2979ff")
        self.checkBox_comment.setObjectName("checkBox_comment")
        self.checkBox_share = QtWidgets.QCheckBox(self.groupBox_job)
        self.checkBox_share.setGeometry(QtCore.QRect(30, 124, 190, 33))
        font = QtGui.QFont()
        font.setFamily("Sitka Banner")
        font.setPointSize(12)
        self.checkBox_share.setFont(font)
        self.checkBox_share.setIcon(QtGui.QIcon("icon/share.jpg"))
        # self.checkBox_share.setStyleSheet("background-color: #2979ff")
        self.checkBox_share.setObjectName("checkBox_share")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Auto GomLua"))
        self.groupBox.setTitle(_translate("MainWindow", "Show"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Cookie"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Token"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Proxy"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Name GL"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Pass GL"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "State"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Total"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Paddy +"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Paddy"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("MainWindow", "Trạng Thái"))
        self.groupBox_confing.setTitle(_translate("MainWindow", "Config"))
        self.label_dlmin.setText(_translate("MainWindow", "Delay Min"))
        self.label_dlmax.setText(_translate("MainWindow", "Delay Max"))
        self.pushButton_startall.setText(_translate("MainWindow", "Start"))
        self.pushButton_stopall.setText(_translate("MainWindow", "Stop"))
        self.label_dthread.setText(_translate("MainWindow", "Delay Luồng"))
        self.label.setText(_translate("MainWindow", "Kết Thúc Khi Đạt"))
        self.label_2.setText(_translate("MainWindow", "Jobs"))
        self.label_dthread_2.setText(_translate("MainWindow", "Delay Nhận Lúa"))
        self.groupBox_job.setTitle(_translate("MainWindow", "Jobs"))
        self.checkBox_like.setText(_translate("MainWindow", "Job Reaction Post"))
        self.checkBox_comment.setText(_translate("MainWindow", "Job Comment Post"))
        self.checkBox_share.setText(_translate("MainWindow", "Job Share Post"))
        self.tableWidget.setColumnWidth(0,80)
        self.tableWidget.setColumnWidth(1,70)
        self.tableWidget.setColumnWidth(2,70)
        self.tableWidget.setColumnWidth(3,70)
        self.tableWidget.setColumnWidth(4,80)
        self.tableWidget.setColumnWidth(5,80)
        self.tableWidget.setColumnWidth(6,80)
        self.tableWidget.setColumnWidth(7,70)
        self.tableWidget.setColumnWidth(8,70)
        self.tableWidget.setColumnWidth(9,85)
        self.tableWidget.setColumnWidth(10,382)

class UiGomLua(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.buttonStart = {}
        self.buttonStop = {}
        self.checkBoxHalt = {}
        self.luong = {}
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.gui.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.gui.tableWidget.customContextMenuRequested.connect(self.menu)
        if os.path.isfile("config.json"):
            fileConFig = open("config.json",encoding="utf-8")
            config = json.load(fileConFig)
            if "delaymin" in config:
                self.gui.spin_min.setValue(config["delaymin"])
            if "delaymax" in config:
                self.gui.spin_max.setValue(config["delaymax"])
            if "delaythread" in config:
                self.gui.spin_max_2.setValue(config["delaythread"])
            if "delaynhan" in config:
                self.gui.spin_max_3.setValue(config["delaynhan"])
            if "dung" in config:
                self.gui.lineEdit_jobmax.setText(str(config["dung"]))
            if "job" in config:
                job = config["job"]
                if "like" in job:
                    self.gui.checkBox_like.setChecked(True)
                if "comment" in job:
                    self.gui.checkBox_comment.setChecked(True)
                if "share" in job:
                    self.gui.checkBox_share.setChecked(True)
    def menu(self):
        menu = QtWidgets.QMenu()
        _all = menu.addAction("Chọn Tất Cả")
        _all.setIcon(QtGui.QIcon("icon\\tap.png"))
        start = menu.addAction("Bắt Đầu")
        start.setIcon(QtGui.QIcon("icon\start.png"))
        stop = menu.addAction("Kết Thúc")
        stop.setIcon(QtGui.QIcon("icon\\stop.png"))
        load = menu.addAction("Load Data")
        load.setIcon(QtGui.QIcon("icon\load.png"))
        getDuLieu = menu.addAction("Get Data")
        getDuLieu.setIcon(QtGui.QIcon("icon\\add.png"))
        remove = menu.addAction("Xoá Hàng")
        remove.setIcon(QtGui.QIcon("icon\\remove3.png"))
        changeMode = menu.addAction("Đổi Màu")
        changeMode.setIcon(QtGui.QIcon("icon\\changemode.png"))
        action = menu.exec_(QtGui.QCursor.pos())
        if action == changeMode:
            global mode
            if mode == "light":
                qdarktheme.setup_theme("dark")
                mode = "dark"
            else:
                qdarktheme.setup_theme("light")
                mode = "light"
        if action == _all:
            self.gui.tableWidget.selectAll()
        if action == getDuLieu:
            listDuLieu = []
            with open("data.txt",encoding="utf-8") as file:
                data = file.read().split('\n')
                if data == ['']:
                    self.thongBao("Error", "File Data Hiện Đang Trống")
                else:
                    for i in range(len(data)):
                        if len(data[i]) > 10 and data[i] != "":
                            chia = data[i].split('|')
                            uid,name,tk,mk,_2fa,cookie,token,proxy,tkgl,mkgl = chia[0],chia[1],chia[2],chia[3],chia[4],chia[5],chia[6],chia[7],chia[8],chia[9]
                            if token == '' or cookie == '':
                                crawl = GetData(tk,mk,_2fa)
                                crawlData = crawl.getToken()
                                if crawlData ==  False:
                                    self.thongBao("Error","Lỗi Get Token Cookie")
                                    continue
                                else:
                                    _token , _cookie = crawlData[0], crawlData[1]
                                    if uid == '' or name == '':
                                        crawl2 = requests.get(f"https://graph.facebook.com/v15.0/me?fields=id%2Cname&access_token={_token}").json()
                                        uid , name = crawl2["id"] , crawl2["name"]
                                        end = f"{uid}|{name}|{tk}|{mk}|{_2fa}|{_cookie}|{_token}|{proxy}|{tkgl}|{mkgl}"
                                        listDuLieu.append(end)
                                    else:
                                        end = f"{uid}|{name}|{tk}|{mk}|{_2fa}|{_cookie}|{_token}|{proxy}|{tkgl}|{mkgl}"
                                        listDuLieu.append(end)
                            elif uid == '' or name == '':
                                crawl3 = requests.get(f"https://graph.facebook.com/v15.0/me?fields=id%2Cname&access_token={token}").json()
                                uid , name = crawl3["id"] , crawl3["name"]
                                end = f"{uid}|{name}|{tk}|{mk}|{_2fa}|{cookie}|{token}|{proxy}|{tkgl}|{mkgl}"
                                listDuLieu.append(end)
                            else:
                                checkToken = requests.get(f"https://graph.facebook.com/v15.0/me?fields=id%2Cname&access_token={token}").json()
                                checkCookie = requests.get("https://mbasic.facebook.com", headers={"cookie":cookie}).text
                                if "<title>Facebook - Đăng nhập hoặc đăng ký</title>" in checkCookie or ("name" and "id") not in checkToken:
                                    print("Token Hoặc Cookie Die")
                                    getDatanew = GetData(tk,mk,_2fa).getToken()
                                    if getDatanew == False:
                                        fileError = open("error.txt","a",encoding="utf-8")
                                        fileError.write(f"{uid}|{name}|{tk}|{mk}|{_2fa}|{cookie}|{token}|{proxy}|{tkgl}|{mkgl}"+"\n")
                                    else:
                                        tokenNew , cookieNew = getDatanew[0] , getDatanew[1]
                                        end = f"{uid}|{name}|{tk}|{mk}|{_2fa}|{cookieNew}|{tokenNew}|{proxy}|{tkgl}|{mkgl}"
                                        listDuLieu.append(end)
                            if tkgl == '' or mkgl == '':
                                self.thongBao("Error", "Thiếu Tài Khoản Hoặc Mật Khẩu GomLua")
            time.sleep(2)
            with open("data.txt","w",encoding="utf-8") as fileNew:
                for itemNew in listDuLieu:
                    fileNew.write(itemNew+"\n")
            time.sleep(1)
            self.thongBao("Thành Công", "Lấy Dữ Liệu Thành Công")
        if action == load:
            listAcc = []
            with open("data.txt","r",encoding="utf-8") as file:
                data = file.read().split('\n')
                for item in data:
                    if len(item) > 10 and item != "":
                        listAcc.append(item)
            for i in range(len(listAcc)):
                self.checkBoxHalt[i] = QtWidgets.QCheckBox("Stop")
                self.checkBoxHalt[i].setIcon(QtGui.QIcon("icon\stop.png"))
                self.gui.tableWidget.insertRow(i)
                if len(listAcc) >= 1 and len(listAcc) < 10:
                    self.gui.tableWidget.setColumnWidth(10,359)
                _item = listAcc[i].split("|")
                uid,name,tk,mk,_2fa,cookie,token,proxy,tkgl,mkgl = _item[0],_item[1],_item[2],_item[3],_item[4],_item[5],_item[6],_item[7],_item[8],_item[9]
                self.gui.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(name))
                self.gui.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(cookie))
                self.gui.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(token))
                self.gui.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem(proxy))
                self.gui.tableWidget.setItem(i,4,QtWidgets.QTableWidgetItem(tkgl))
                self.gui.tableWidget.setItem(i,5,QtWidgets.QTableWidgetItem(mkgl))
                self.gui.tableWidget.setCellWidget(i,6,self.checkBoxHalt[i])
        if action == start:
            allRow = self.gui.tableWidget.rowCount()
            if allRow == 0:
                self.thongBao("Error","Vui Lòng Load Data Trước Khi Chạy","Error")
            else:
                dmin = self.gui.spin_min.value()
                dmax = self.gui.spin_max.value()
                dthread = self.gui.spin_max_2.value()
                dnlua = self.gui.spin_max_3.value()
                dend = self.gui.lineEdit_jobmax.text()
                job = self.getJob()
                if job == []:
                    self.thongBao("Warning","Vui Lòng Chọn Job","Warning")
                row = self.gui.tableWidget.selectionModel().selectedRows()
                if row == []:
                    self.thongBao("Warning","Vui Lòng Bôi Đen Dòng","Warning")
                else:
                    for i in range(len(row)):
                        hang = row[i].row()
                        cookie = self.gui.tableWidget.item(hang,1).text()
                        token = self.gui.tableWidget.item(hang,2).text()
                        proxy = self.gui.tableWidget.item(hang,3).text()
                        tkgl = self.gui.tableWidget.item(hang,4).text()
                        mkgl = self.gui.tableWidget.item(hang,5).text()
                        if self.checkBoxHalt[hang].isChecked() == True:
                            print("Bỏ Qua")
                            continue
                        if len(row) > 1:
                            for x in range(dthread,-1,-1):
                                self.hienThi(hang,10,f" Bắt Đầu Sau {x} Giây")
                                self.delay()
                        self.luong[i] = MainTool(hang,cookie,token,proxy,tkgl,mkgl,dmin,dmax,dnlua,job)
                        self.luong[i].start()
                        self.luong[i].callback.connect(self.hienThi)
        if action == stop:
            row = self.gui.tableWidget.currentRow()
            try:
                print("Kill")
                self.luong[row].terminate()
                self.hienThi(row, 10, f" Kết Thúc")
            except: self.hienThi(row, 10, f" Luồng Chưa Khởi Chạy")
        if action == remove:
            select = self.gui.tableWidget.selectionModel().selectedRows()
            for item in range(len(select)):
                row = select[item].row()
                self.gui.tableWidget.removeRow(row)
    def delay(self):
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(int(1000), loop.quit)
        loop.exec()
    def thongBao(self, title, text, type="a"):
        global tb
        tb = QtWidgets.QMessageBox()
        if type == "Error":
            tb.setIcon(QtWidgets.QMessageBox.Critical)
        elif type == "Warning":
            tb.setIcon(QtWidgets.QMessageBox.Warning)
        else:
            tb.setIcon(QtWidgets.QMessageBox.Information)
        tb.setWindowTitle(title)
        font = QtGui.QFont()
        font.setFamily("Sitka Banner")
        font.setPointSize(14)
        tb.setFont(font)
        tb.setText(text)
        tb.show()
    def hienThi(self,row:int ,column:int ,nd):
        self.gui.tableWidget.setItem(row,column,QtWidgets.QTableWidgetItem(nd))
    def getJob(self):
        listjob = []
        if self.gui.checkBox_like.isChecked() == True:
            listjob.append("like")
        if self.gui.checkBox_comment.isChecked() == True:
            listjob.append("comment")
        if self.gui.checkBox_share.isChecked() == True:
            listjob.append("share")
        return listjob
    
class MainTool(QtCore.QThread):
    callback = QtCore.pyqtSignal(int,int,str)
    def __init__(self, row, cookie, token, proxy, tkgl, mkgl, dmin, dmax, dnhan, listjob):
        super().__init__()
        self.row = row
        self.cookie = cookie
        self.token = token
        self.proxy = proxy
        self.tkgl = tkgl
        self.mkgl = mkgl
        self.dmin = dmin
        self.dmax = dmax
        self.dnhan = dnhan
        self.listjob = listjob
    def run(self):
        self.callback.emit(self.row, 10,f" Start")
        time.sleep(1)
        count = 0
        xuthem = 0
        if self.proxy == "":
            self.proxy = None
        gl = GomLua(self.tkgl, self.mkgl)
        fb = Facebook(self.cookie, self.token, self.proxy)
        loginGL = gl._Login()
        if loginGL == False:
            self.callback.emit(self.row, 10,f" Login GomLua Thất Bại")
            while (True): time.sleep(10000)
        else:
            self.callback.emit(self.row, 10,f" Login GomLua Thành Công")
            time.sleep(1)
            xutong = loginGL[1]
            while (True):
                jobchay = random.choice(self.listjob)
                if jobchay == "like":
                    job = gl.GetLikePost()
                    if job == False:
                        for i in range(15, -1, -1):
                            self.callback.emit(self.row, 10, f" Hết Job! Lấy Job Sau {i} Giây")
                            time.sleep(1)
                        continue
                    else:
                        for i in range(len(job)):
                            campaign_id = job[i]["campaign_id"]
                            link_id = job[i]["link_id"]
                            react_type = job[i]["react_type"]
                            link = job[i]["link"]
                            check = gl.CheckLink(link_id)
                            if check == False: continue
                            getID = fb.GetPosID(link)
                            if getID == False: continue
                            self.callback.emit(self.row, 10, f" Tiến Hành Làm Job")
                            done = fb.reaction(getID, react_type)
                            for tam in range(10, -1, -1):
                                self.callback.emit(self.row, 10, f" Nhận Lúa Sau {tam} Giây")
                                time.sleep(1)
                            for nx in range(5):
                                nhanXu = gl.Receive(check,link_id)
                                if nhanXu == False:
                                    self.callback.emit(self.row, 10, f" Nhận Lúa Thất Bại")
                                    time.sleep(1)
                                    break
                                elif nhanXu == "continue":
                                    for nl in range(5,-1,-1):
                                        self.callback.emit(self.row, 10, f" Nhận Lại Lúa Sau {nl} Giây")
                                        time.sleep(1)
                                else:
                                    self.callback.emit(self.row, 10, f" Nhận Lúa Thành Công")
                                    time.sleep(1)
                                    xutong += 40
                                    count += 1
                                    xuthem += 40
                                    self.callback.emit(self.row, 9, f" {xutong}")
                                    self.callback.emit(self.row, 8, f" {xuthem}")
                                    self.callback.emit(self.row, 7, f" {count}")
                                    break
                            for delay in range(random.randint(self.dmin,self.dmax),-1,-1):
                                self.callback.emit(self.row,10,f" Làm Job Tiếp Theo Sau {delay} Giây")
                                time.sleep(1)
if __name__ == "__main__":
    import sys
    try:
        import qdarktheme
    except:
        os.system("pip install pyqtdarktheme")
        os.system("clear")
    import qdarktheme
    mode = "light"
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    qdarktheme.setup_theme("light")
    MainWindow = UiGomLua()
    MainWindow.show()
    sys.exit(app.exec_())

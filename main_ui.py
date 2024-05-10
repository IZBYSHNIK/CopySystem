# Copyright (C) 2024 IvanDegtyarev

# This is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published
#  by the Free Software Foundation; either version 3 of the license, or (at your choice) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; even without an implicit warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. For more information, see the GNU General Public License.


# You should have received a copy of the GNU General Public License along with this program. If this is not the case, see <https://www.gnu.org/licenses />.

from PySide6 import QtCore, QtGui, QtWidgets
from core import CopyManager
from PySide6.QtCore import QRunnable, Slot, Signal, QThreadPool
from PySide6 import QtSvgWidgets

import sys, os, requests, json, platform
import traceback

VERSION = '0.4.0'
cm = CopyManager()

import webbrowser
print(webbrowser.open('https://passport.yandex.ru/auth'))

def clearLayout(layout):
    for i in reversed(range(layout.count())): 
        child = layout.itemAt(i)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())

class WorkerSignals(QtCore.QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(object)


    def setupUi(self):
        self.setObjectName("self")
        self.resize(186, 187)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.logo_lable = QtWidgets.QLabel(parent=self)
        self.logo_lable.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logo_lable.setObjectName("logo_lable")
        self.verticalLayout_2.addWidget(self.logo_lable)
        self.line = QtWidgets.QFrame(parent=self)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.textBrowser = QtWidgets.QTextBrowser(parent=self)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.line_2 = QtWidgets.QFrame(parent=self)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 25)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.logo_GPL = QtWidgets.QLabel(parent=self)
        self.logo_GPL.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logo_GPL.setObjectName("logo_GPL")
        self.horizontalLayout.addWidget(self.logo_GPL)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.License_label = QtWidgets.QLabel(parent=self)
        self.License_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.License_label.setObjectName("License_label")
        self.verticalLayout_2.addWidget(self.License_label)
        self.Copyright_lable = QtWidgets.QLabel(parent=self)
        self.Copyright_lable.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Copyright_lable.setObjectName("Copyright_lable")
        self.verticalLayout_2.addWidget(self.Copyright_lable)

        self.retranslateUi()
     

    def retranslateUi(self):
        self.setWindowTitle(self.tr("self"))
        self.logo_lable.setText(self.tr("ЛОГО"))
        self.logo_GPL.setText(self.tr("ЛОГО"))
        self.License_label.setText(self.tr("TextLabel"))
        self.Copyright_lable.setText(self.tr("Copyright (C) 2024 IvanDegtyarev"))


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

        self.signals = WorkerSignals()

        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()  # QtCore.Slot
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()


class Push(QtWidgets.QPushButton):
    def __init__(self, parent, base_weight, base_height, growth, tool_tip=None, text=None, icon_path=None):
        super().__init__()
        if icon_path:
            self.setStyleSheet('border: none;')
        self.base_height = base_height
        self.base_weight = base_weight
        self.growth = growth
        self.setIconSize(QtCore.QSize(self.base_weight, self.base_height))
        if tool_tip:
            self.setToolTip(tool_tip)
        if icon_path:
            self.setIcon(QtGui.QIcon(icon_path))
        if not icon_path and text:
            self.setText(text)

    def enterEvent(self, e):
        self.setIconSize(QtCore.QSize(self.base_weight + self.growth, self.base_height + self.growth))

    def leaveEvent(self, e):
        self.setIconSize(QtCore.QSize(self.base_weight, self.base_height))



class Base(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('CS.ico'))
        self.resize(336, 293)


class About_UI(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setObjectName("self")
        self.resize(186, 187)
        self.setModal(True)
        
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.logo_layout = QtWidgets.QHBoxLayout(self)
        self.logo_lable = QtSvgWidgets.QSvgWidget(os.path.join('assets', 'media','CS.svg'), parent=self)
        self.logo_lable.setFixedSize(QtCore.QSize(100, 100))
        self.logo_lable.setObjectName("logo_lable")
        self.logo_layout.addWidget(self.logo_lable)
        self.verticalLayout_2.addLayout(self.logo_layout)
        self.textBrowser = QtWidgets.QTextBrowser(parent=self)
        self.textBrowser.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0%)')
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setMinimumWidth(450)
        self.textBrowser.setMinimumHeight(300)
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 25)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.update_horizontalLayout = QtWidgets.QHBoxLayout()
        self.update_horizontalLayout.addWidget(QtWidgets.QLabel(f'Версия {str(VERSION)}'))
        self.update_horizontalLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # UpdateManager
        self.update_pushButton = Push(self, 35, 35, 5, self.tr('О программе'), self.tr('i'), os.path.join('assets', 'media','update_button.svg'))
        self.update_horizontalLayout.addWidget(self.update_pushButton)
        
        self.verticalLayout_2.addLayout(self.update_horizontalLayout)

        self.logo_GPL = QtSvgWidgets.QSvgWidget(os.path.join('assets', 'media','GPL.svg'), parent=self)
        self.logo_GPL.setObjectName("logo_GPL")
        self.logo_GPL.setFixedSize(QtCore.QSize(150, 100))
        self.horizontalLayout.addWidget(self.logo_GPL)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.Copyright_lable = QtWidgets.QLabel(parent=self)
        self.Copyright_lable.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Copyright_lable.setObjectName("Copyright_lable")
        self.verticalLayout_2.addWidget(self.Copyright_lable)
        self.logo_lable.mousePressEvent = self.show_gratitude
        self.logo_GPL.mousePressEvent = self.show_license
        self.update_pushButton.clicked.connect(self.click_push_botton)

        self.retranslateUi()
     

    def retranslateUi(self):
        self.setWindowTitle(self.tr("О программе"))
        # self.logo_GPL.setText(self.tr("ЛОГО"))
        self.Copyright_lable.setText(self.tr("Copyright (C) 2024 IvanDegtyarev"))
        self.textBrowser.setText(
            """
                <h1>О программе</h1>
                <p><b>CopySystem</b> - это прогармма, которая позваляет подклчится к Yandex-диску по токену и резервиврвать определеные папки (хранилища).</p>
            """
        )

    def show_license(self, e):
        self.l = QtWidgets.QTextBrowser()
        self.l.setWindowIcon(QtGui.QIcon('CS.ico'))
        self.l.setWindowTitle(self.tr('Лицензия'))
        
        try:
            with open('COPYING', 'r', encoding='UTF-8') as f:
                temp = ''
                for i in f:
                    temp += i
        except BaseException as f:
            print(f)
        else:
            self.l.setText(temp)
            self.l.show()
        del temp

    def click_push_botton(self, e):
        self.um = UpdateManager()
        self.um.show()


    def show_gratitude(self, e):
        self.g = QtWidgets.QTextBrowser()
        self.g.setWindowIcon(QtGui.QIcon('CS.ico'))
        self.g.setMinimumWidth(800)
        self.g.setWindowTitle(self.tr('Благодарность'))
        self.g.setText(
            """
                <p>
                 <pre style='white-space: pre;' align='center'>                                                                                                                                      
                                                                                                                                              
TTTTTTTTTTTTTTTTTTTTTTTHHHHHHHHH     HHHHHHHHH               AAA               NNNNNNNN        NNNNNNNNKKKKKKKKK    KKKKKKK   SSSSSSSSSSSSSSS 
T:::::::::::::::::::::TH:::::::H     H:::::::H              A:::A              N:::::::N       N::::::NK:::::::K    K:::::K SS:::::::::::::::S
T:::::::::::::::::::::TH:::::::H     H:::::::H             A:::::A             N::::::::N      N::::::NK:::::::K    K:::::KS:::::SSSSSS::::::S
T:::::TT:::::::TT:::::THH::::::H     H::::::HH            A:::::::A            N:::::::::N     N::::::NK:::::::K   K::::::KS:::::S     SSSSSSS
TTTTTT  T:::::T  TTTTTT  H:::::H     H:::::H             A:::::::::A           N::::::::::N    N::::::NKK::::::K  K:::::KKKS:::::S            
        T:::::T          H:::::H     H:::::H            A:::::A:::::A          N:::::::::::N   N::::::N  K:::::K K:::::K   S:::::S            
        T:::::T          H::::::HHHHH::::::H           A:::::A A:::::A         N:::::::N::::N  N::::::N  K::::::K:::::K     S::::SSSS         
        T:::::T          H:::::::::::::::::H          A:::::A   A:::::A        N::::::N N::::N N::::::N  K:::::::::::K       SS::::::SSSSS    
        T:::::T          H:::::::::::::::::H         A:::::A     A:::::A       N::::::N  N::::N:::::::N  K:::::::::::K         SSS::::::::SS  
        T:::::T          H::::::HHHHH::::::H        A:::::AAAAAAAAA:::::A      N::::::N   N:::::::::::N  K::::::K:::::K           SSSSSS::::S 
        T:::::T          H:::::H     H:::::H       A:::::::::::::::::::::A     N::::::N    N::::::::::N  K:::::K K:::::K               S:::::S
        T:::::T          H:::::H     H:::::H      A:::::AAAAAAAAAAAAA:::::A    N::::::N     N:::::::::NKK::::::K  K:::::KKK            S:::::S
      TT:::::::TT      HH::::::H     H::::::HH   A:::::A             A:::::A   N::::::N      N::::::::NK:::::::K   K::::::KSSSSSSS     S:::::S
      T:::::::::T      H:::::::H     H:::::::H  A:::::A               A:::::A  N::::::N       N:::::::NK:::::::K    K:::::KS::::::SSSSSS:::::S
      T:::::::::T      H:::::::H     H:::::::H A:::::A                 A:::::A N::::::N        N::::::NK:::::::K    K:::::KS:::::::::::::::SS 
      TTTTTTTTTTT      HHHHHHHHH     HHHHHHHHHAAAAAAA                   AAAAAAANNNNNNNN         NNNNNNNKKKKKKKKK    KKKKKKK SSSSSSSSSSSSSSS   
                                                                                                                                              
                                                                                                                                              
                 <pre>                                                        
                </p>
                <h1 align='center' style="color: #1f1f1f">Дорогие друзья!</h1>
<p align='center' style="font-size: 20px; color: #1f1f1f"> Выржаю огромную благодарность за неоценимую помощь в разработке данной программы. Ваши знания, опыт и энтузиазм сделали эту программу.
Именно ваша поддержка позволила преодолеть все трудности и достичь поставленной цели. Выражаю благодарность за ваше доверие и веру.</p>
<p align='center' style="font-size: 20px;">Спасибо вам огромное!</p>
                <p align='center' style="font-size: 16px; color: #1f1f1f; text-transform: uppercase; font-style: italic;">
                <hr>
                <h3>Отдельная благодарность:</h3>
                <ui>
                <li>Моей <b>маме</b>,</li>
                <li>Вдохновителю и тестирвощику - <b>Васильеву Владу Александровичу</b>,</li>
                <li></li>
                <li></li>
                </ui>
                </p>

<pre style='white-space: pre;' align='center'>                                                                                                                                      
                                                                                                                                              
         LoveLoveLov                eLoveLoveLo          
     veLoveLoveLoveLove          LoveLoveLoveLoveLo      
  veLoveLoveLoveLoveLoveL      oveLoveLoveLoveLoveLove   
 LoveLoveLoveLoveLoveLoveL    oveLoveLoveLoveLoveLoveLo  
veLoveLoveLoveLoveLoveLoveL  oveLoveLoveLoveLoveLoveLove 
LoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLove 
LoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLove 
 LoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLo  
 veLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLove  
   LoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLo    
     veLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLove      
       LoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLo        
         veLoveLoveLoveLoveLoveLoveLoveLoveLove          
           LoveLoveLoveLoveLoveLoveLoveLoveLo            
             veLoveLoveLoveLoveLoveLoveLove              
               LoveLoveLoveLoveLoveLoveLo                
                  veLoveLoveLoveLoveLo                   
                      veLoveLoveLo                       
                           ve                            
                 <pre> 
            """
        )
        self.g.show()
      

class Parametrs(QtWidgets.QDialog):
    def __init__(self, parent, is_new=False):
        super().__init__()
        self.is_new = is_new
        self.setModal(True)
        self.setWindowIcon(QtGui.QIcon('CS.ico'))
        self.parent = parent
        self.resize(366, 298)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon_lable = QtWidgets.QLabel(parent=self)
        self.icon_lable.setWordWrap(True)
        self.icon_lable.setObjectName("icon_lable")
        self.horizontalLayout.addWidget(self.icon_lable)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.logo_layout = QtWidgets.QHBoxLayout(self)
        self.logo_lable = QtSvgWidgets.QSvgWidget(os.path.join('assets', 'media','CS.svg'), parent=self)
        self.logo_lable.setFixedSize(QtCore.QSize(100, 100))
        self.logo_lable.setObjectName("logo_lable")
        self.logo_layout.addWidget(self.logo_lable)
        self.horizontalLayout.addLayout(self.logo_layout)

        self.verticalLayout_2.addLayout(self.horizontalLayout)
        # spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        # self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(parent=self)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(parent=self)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.type_label = QtWidgets.QLabel(parent=self)
        self.type_label.setObjectName("type_label")
        self.gridLayout.addWidget(self.type_label, 4, 0, 1, 1)
        self.parametrs_gridLayout = QtWidgets.QGridLayout()
        self.parametrs_gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.parametrs_gridLayout.setObjectName("gridLayout_3")
        self.gridLayout.addLayout(self.parametrs_gridLayout, 6, 0, 1, 2)
        self.location_pushButton = QtWidgets.QPushButton(parent=self)
        self.location_pushButton.setObjectName("location_pushButton")
        self.gridLayout.addWidget(self.location_pushButton, 3, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(parent=self)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 4, 1, 1, 1)
        self.folder_label = QtWidgets.QLabel(parent=self)
        self.folder_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.folder_label.setObjectName("folder_label")
        self.gridLayout.addWidget(self.folder_label, 0, 0, 1, 2)
        self.location_label = QtWidgets.QLabel(parent=self)
        self.location_label.setObjectName("location_label")
        self.gridLayout.addWidget(self.location_label, 3, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.save_pushButton = QtWidgets.QPushButton(parent=self)
        self.save_pushButton.setObjectName("save_pushButton")
        self.verticalLayout.addWidget(self.save_pushButton)
        self.error_message = QtWidgets.QLabel(parent=self)
        self.error_message.setObjectName("error_message")
        self.verticalLayout.addWidget(self.error_message)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.comboBox.currentIndexChanged.connect(self.set_type_folder)
        self.comboBox.currentIndexChanged.connect(self.set_type_folder)

        for i in cm.TYPE_CONNECT:
            self.comboBox.addItem(i)
        
        self.save_pushButton.clicked.connect(self.save_folder)
        self.location_pushButton.clicked.connect(self.set_location_path)

        self.current_path = ''

        self.retranslateUi()

        if not is_new:
            self.load_date()
        

    def retranslateUi(self):
        self.setWindowTitle(self.tr("Параметры хранилища"))
        self.icon_lable.setText(self.tr(f"<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">CopySystem<sup>{str(VERSION)}</sup> </span></p></body></html>"))
        self.folder_label.setText(self.tr(""))
        self.type_label.setText(self.tr("Тип"))
        self.label.setText(self.tr("Название"))
        self.location_label.setText(self.tr("Расположение"))
        self.location_pushButton.setText(self.tr("Путь ..."))
       
        self.save_pushButton.setText(self.tr("Сохранить")  if not self.is_new else self.tr("Прикрепить"))

    def set_type_folder(self):
        clearLayout(self.parametrs_gridLayout)
        if self.comboBox.currentText() == 'NETWORK':
            self.URLs = QtWidgets.QComboBox()
            self.URLs.addItems(cm.NETWORK_URLs)
            self.token = QtWidgets.QTextEdit()
            self.parametrs_gridLayout.addWidget(QtWidgets.QLabel(self.tr('URL')), 0, 0, 1, 1)
            self.parametrs_gridLayout.addWidget(self.URLs, 0, 1, 1, 1)
            self.parametrs_gridLayout.addWidget(QtWidgets.QLabel(self.tr('ТОКЕН')), 1, 0, 1, 1)
            self.parametrs_gridLayout.addWidget(self.token, 1, 1, 1, 1)
        
    def load_date(self):
        
        self.lineEdit.setText(cm.WORK_DIR)
        self.location_pushButton.setText(cm.CONFIG['CONNECT_FOLDERS'][cm.WORK_DIR]['ORIGINAL_LOCATION'])
        self.comboBox.setCurrentText(cm.WORK_DIR)
        self.URLs.setCurrentText(cm.CONFIG['CONNECT_FOLDERS'][cm.WORK_DIR]['PARAMETRS'].get('URL'))
        self.token.setText(cm.CONFIG['CONNECT_FOLDERS'][cm.WORK_DIR]['PARAMETRS'].get('TOKEN'))
        

      
    def save_folder(self):
        if self.comboBox.currentText() == 'NETWORK':
            try:
                if not os.path.isdir(self.location_pushButton.text()):
                    raise ValueError()

                cm.fix_folder(self.lineEdit.text(), self.current_path, self.comboBox.currentText(), 0, {
                    'URL': self.URLs.currentText(),
                    'TOKEN': self.token.toPlainText(),
                })
            except ValueError as f:
                self.parent.main_terminal.setText( self.parent.main_terminal.toPlainText() + f'ERROR {str(f)}\n')
                self.error_message.setText(self.tr('ОШИБКА введено недопустимое значение в поле'))
            else:
                cm.save_config()
                self.parent.update_list_folders()
                self.deleteLater()

    def set_location_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self)
        if path:
            self.current_path = path
            self.location_pushButton.setText(path[:50] + ('...' if len(path) >= 50 else ''))
            self.location_pushButton.setToolTip(path)
        

class Paths_UI(QtWidgets.QDialog):
    def __init__(self,):
        super().__init__()
     
        self.setWindowIcon(QtGui.QIcon('CS.ico'))
        self.resize(366, 298)
        self.setModal(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon_lable = QtWidgets.QLabel(parent=self)
        self.icon_lable.setWordWrap(True)
        self.icon_lable.setObjectName("icon_lable")
        self.horizontalLayout.addWidget(self.icon_lable)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.logo_layout = QtWidgets.QHBoxLayout(self)
        self.logo_lable = QtSvgWidgets.QSvgWidget(os.path.join('assets', 'media','CS.svg'), parent=self)
        self.logo_lable.setFixedSize(QtCore.QSize(100, 100))
        self.logo_lable.setObjectName("logo_lable")
        self.logo_layout.addWidget(self.logo_lable)
        self.horizontalLayout.addLayout(self.logo_layout)

        self.verticalLayout_2.addLayout(self.horizontalLayout)
     
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QTextBrowser(parent=self,)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(1)
        
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
        self.original_location_lable = QtWidgets.QLabel(parent=self)
        self.original_location_lable.setObjectName("original_location_lable")
        self.gridLayout.addWidget(self.original_location_lable, 1, 0, 1, 1)
      
        self.parametrs_gridLayout = QtWidgets.QGridLayout()
        self.parametrs_gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.parametrs_gridLayout.setObjectName("gridLayout_3")
        self.gridLayout.addLayout(self.parametrs_gridLayout, 6, 0, 1, 2)
        self.is_downloading_old_place = QtWidgets.QCheckBox()
        self.gridLayout.addWidget(self.is_downloading_old_place, 2, 1, 1, 1)


        self.location_pushButton = QtWidgets.QPushButton(parent=self)
        self.location_pushButton.setObjectName("location_pushButton")
        self.gridLayout.addWidget(self.location_pushButton, 3, 1, 1, 1)
        
        
        self.location_label = QtWidgets.QLabel(parent=self)
        self.location_label.setObjectName("location_label")
        self.gridLayout.addWidget(self.location_label, 3, 0, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.save_pushButton = QtWidgets.QPushButton(parent=self)
        self.save_pushButton.setObjectName("save_pushButton")
        self.verticalLayout.addWidget(self.save_pushButton)
        self.error_message = QtWidgets.QLabel(parent=self)
        self.error_message.setObjectName("error_message")
        self.verticalLayout.addWidget(self.error_message)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.new_download_path = ''


        self.save_pushButton.clicked.connect(self.save_files)
        self.location_pushButton.clicked.connect(self.set_location_path)
        self.is_downloading_old_place.stateChanged.connect(self.change_checkbox_downloading_old_place)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(self.tr("Пути сохранения"))
        self.icon_lable.setText(self.tr(f"<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">CopySystem<sup>{str(VERSION)}</sup> </span></p></body></html>"))
        self.lineEdit.setText(cm.CONFIG['CONNECT_FOLDERS'][cm.WORK_DIR]['ORIGINAL_LOCATION'])
        self.is_downloading_old_place.setText(self.tr('Сохранить в туже папку'))
        self.original_location_lable.setText(self.tr("Исходный путь"))
        self.location_label.setText(self.tr("Путь для загрузки"))
        self.location_pushButton.setText(self.tr("Путь ..."))
        self.save_pushButton.setText(self.tr("Начать"))

    def set_location_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.new_download_path = path
        self.location_pushButton.setText(path[:50] + ('...' if len(path) >= 50 else ''))
        self.location_pushButton.setToolTip(path)

    def change_checkbox_downloading_old_place(self, e):
        if e:
            self.new_download_path = cm.CONFIG['CONNECT_FOLDERS'][cm.WORK_DIR]['ORIGINAL_LOCATION']
            self.location_pushButton.setEnabled(0)
        else:
            self.location_pushButton.setEnabled(1)
    
    def save_files(self):
        if os.path.isdir(self.new_download_path):
            cm.download_files_network(new_path=self.new_download_path)
        else:
            self.error_message.setText(self.tr('Неверно указан путь сохранения файлов'))


    
class UpdateManager(QtWidgets.QDialog):
    URL_PROJECT = 'https://api.github.com/repos/IZBYSHNIK/CopySystem/releases/latest'

    def __init__(self, parent=None):
        super(UpdateManager, self).__init__(parent)
        self.setObjectName("UpdateManager")
        self.setStyleSheet('a {font-size:18px; color: black; text-decoration: none;}')

        self.setModal(True)
        self.vertical_layout = QtWidgets.QVBoxLayout(self)

        self.title = QtWidgets.QLabel()
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet('font-size:18px; text-transform: uppercase;')

        self.message = QtWidgets.QLabel()
        self.message.setStyleSheet('font-size:14px;')

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.show_link = QtWidgets.QLabel()
        self.show_link.setStyleSheet('font-size:16px')
        self.show_link.setOpenExternalLinks(True)
        self.show_link.setFixedHeight(50)

        self.show_link.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.buttons_layout.addWidget(self.show_link)
        self.load_link = QtWidgets.QLabel()
        self.load_link.setStyleSheet('font-size:16px')
        self.load_link.setOpenExternalLinks(True)
        self.load_link.setFixedHeight(50)

        self.load_link.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.buttons_layout.addWidget(self.load_link)

        self.vertical_layout.addWidget(self.title)
        self.vertical_layout.addWidget(self.message)
        self.vertical_layout.addLayout(self.buttons_layout)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(self.tr('Обновление'))

    def fill_data(self, data):
        self.title.setText(data['title'])
        self.message.setText(data['message'])
        self.show_link.setText(f'<a href="{data["show_url"]}">' + self.tr('Посмотреть') + '</a>')
        self.load_link.setText(f'<a href="{data["download_url"]}">' + self.tr('Скачать') + '</a>')

    def link_host(self):
        data = {}
        try:
            update_massage = json.loads(requests.api.get(self.URL_PROJECT,
                                                         params={'User-Agent:': str(platform.node())}).text)
        except requests.exceptions.ConnectionError as f:
            return data

        if not update_massage:
            return {}

        
        version = [int(i) if i.isnumeric() else i for i in
                update_massage.get('tag_name', '0.0.0').split('.')]

        data = {
            'version': version,
            'title': update_massage.get('name', 'Update X'),
            'message': update_massage.get('body', 'Text'),
            'show_url': update_massage.get('html_url', ''),
            'download_url': update_massage.get('assets', ({},))[0].get('browser_download_url', '') if update_massage.get('assets', ({},)) else '',
        }
       


        return data

    @staticmethod
    def check_new_version(old, new):
        # print(old, new)
        if old < new:
            return True
        return False

    def show(self):
        data = self.link_host()

        if not data:
            return
        if not self.check_new_version([int(i) if i.isnumeric() else i for i in VERSION.split('.')], data['version']):
            return

        self.fill_data(data)

        super().show()


class Main(Base):
    def __init__(self):
        super().__init__()
        self.setObjectName("Main")
        self.resize(336, 293)
        self.setWindowIcon(QtGui.QIcon('CS.ico'))
        self.setStyleSheet("""
            QToolTip {
                color: white;
                background-color: black;                    
            }
          

        """)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon_lable = QtWidgets.QLabel(parent=self)
        self.icon_lable.setWordWrap(True)
        self.icon_lable.setObjectName("icon_lable")
        self.horizontalLayout.addWidget(self.icon_lable)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.about_pushButton = Push(self, 50, 50, 5, self.tr('О программе'), self.tr('i'), os.path.join('assets', 'media','about.svg'))
        
        
        self.about_pushButton.setObjectName("about_pushButton")
        self.horizontalLayout.addWidget(self.about_pushButton)
        self.settings_pushButton = Push(self, 50, 50, 5, self.tr('Настройки'), self.tr('Настройки'), os.path.join('assets', 'media','settings.svg'))
        self.settings_pushButton.setObjectName("settings_pushButton")
        self.horizontalLayout.addWidget(self.settings_pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        # spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        # self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.folder_label = QtWidgets.QLabel(parent=self)
        self.folder_label.setObjectName("folder_label")
        self.verticalLayout_4.addWidget(self.folder_label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBox = QtWidgets.QComboBox(parent=self)
        self.comboBox.setMinimumHeight(50)
        self.comboBox.setStyleSheet('border: none; background-color: rgb(228, 228, 228); padding: 5px;')
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.fix_folder_pushButton = Push(self, 40, 40, 0, self.tr('Добавить хранилище'), self.tr('+'), os.path.join('assets', 'media','add-folder.svg'))
        self.fix_folder_pushButton.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 5%); padding: 5px')
        self.fix_folder_pushButton.setObjectName("fix_folder_pushButton")
        self.horizontalLayout_2.addWidget(self.fix_folder_pushButton)
        self.type_pushButton = Push(self, 40, 40, 0, self.tr('ТИП'), self.tr('ТИП'), os.path.join('assets', 'media', 'type','folder-2.svg'))
        self.type_pushButton.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 5%); padding: 5px')
        # self.type_pushButton.setText("ТИП")
        self.type_pushButton.setObjectName("type_pushButton")
        self.horizontalLayout_2.addWidget(self.type_pushButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.send_folder_pushButton = Push(self, 40, 40, 0, self.tr('Отправить'), self.tr('Отправить'), os.path.join('assets', 'media','up-folder.svg'))
        self.send_folder_pushButton.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 5%); padding: 5px')
        self.send_folder_pushButton.setObjectName("send_folder_pushButton")
        self.gridLayout.addWidget(self.send_folder_pushButton, 0, 0, 1, 1)
        self.download_folder_pushButton = Push(self, 40, 40, 0, self.tr('Загрузить'), self.tr('Загрузить'), os.path.join('assets', 'media','down-folder.svg'))
        self.download_folder_pushButton.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 5%); padding: 5px')
        self.download_folder_pushButton.setObjectName("download_folder_pushButton")
        self.gridLayout.addWidget(self.download_folder_pushButton, 0, 1, 1, 1)
        self.remove_folder_pushButton =  Push(self, 40, 40, 0, self.tr('Удалить'), self.tr('Удалить'), os.path.join('assets', 'media','remove-folder.svg'))
        self.remove_folder_pushButton.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 5%); padding: 5px;')
        self.remove_folder_pushButton.setObjectName("remove_folder_pushButton")
        self.gridLayout.addWidget(self.remove_folder_pushButton, 1, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.settings_folder_pushButton = Push(self, 40, 40, 0, self.tr('Параметры хранилища'), self.tr('Параметры хранилища'), os.path.join('assets', 'media','parametrs-folder.svg'))
        self.settings_folder_pushButton.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 5%); padding: 5px;')
        self.settings_folder_pushButton.setObjectName("settings_folder_pushButton")
        self.verticalLayout.addWidget(self.settings_folder_pushButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.hl1 = QtWidgets.QHBoxLayout()
        self.hl1.setObjectName("hl1")
        self.label = QtWidgets.QLabel(parent=self)
        self.label.setObjectName("label")
        self.hl1.addWidget(self.label)
        self.status_label = QtWidgets.QLabel(parent=self)
        self.status_label.setAlignment(QtGui.Qt.AlignmentFlag.AlignRight)
        self.status_label.setText('')

        self.status_label.setObjectName("status_label")
        self.hl1.addWidget(self.status_label)
        self.verticalLayout_5.addLayout(self.hl1)
        self.main_terminal = QtWidgets.QTextBrowser(parent=self)
        self.main_terminal.setObjectName("main_terminal")
        self.verticalLayout_5.addWidget(self.main_terminal)
        self.verticalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.comboBox.currentTextChanged.connect(self.active_folder)
        self.update_list_folders()
        
        self.settings_folder_pushButton.clicked.connect(self.show_parametrs)
        self.fix_folder_pushButton.clicked.connect(self.fix_folder)
        self.remove_folder_pushButton.clicked.connect(self.remove_folder)
        self.send_folder_pushButton.clicked.connect(self.send_folder)
        self.download_folder_pushButton.clicked.connect(self.download_folder)
        self.about_pushButton.clicked.connect(self.show_about)
        self.threadpool = QThreadPool()

        self.retranslateUi()
    
    def update_list_folders(self):
        self.comboBox.clear()
        for i in cm.CONFIG['CONNECT_FOLDERS']:
            self.comboBox.addItem(i)

    def retranslateUi(self):
        self.setWindowTitle(self.tr("CopySystem"))
        self.icon_lable.setText(self.tr(f"<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">CopySystem<sup>{str(VERSION)}</sup> </span></p></body></html>"))
        
        # self.settings_pushButton.setText(self.tr("Настрйоки"))
        self.folder_label.setText(self.tr(""))
        self.send_folder_pushButton.setText(self.tr("Отправить"))
        self.download_folder_pushButton.setText(self.tr("Загрузить"))
        self.remove_folder_pushButton.setText(self.tr("Удалить"))
        # self.fix_folder_pushButton.setText(self.tr("+"))
        self.settings_folder_pushButton.setText(self.tr("Параметры хранилища"))
        self.label.setText(self.tr("Ход выполнения"))

    def active_folder(self):
        if self.comboBox.currentText():
            icon_type = {
                'NETWORK': 'folder-0.svg', 
                'BETWEEN': 'folder-1.svg', 
                'LOCAL': 'folder-2.svg', 

            }
            cm.activate_folder(self.comboBox.currentText())
            self.main_terminal.setText( self.main_terminal.toPlainText() + f'АКТИВАЦИЯ: {self.comboBox.currentText()}\n')
            
            # self.type_pushButton.setText(cm.CONFIG['CONNECT_FOLDERS'][cm.WORK_DIR]['TYPE'])
            self.type_pushButton.setIcon(QtGui.QIcon(os.path.join('assets', 'media', 'type', icon_type.get(cm.CONFIG['CONNECT_FOLDERS'][cm.WORK_DIR]['TYPE']))))
    
    def remove_folder(self):
        message = QtWidgets.QMessageBox.question(self, self.tr('Открепление хранилищя'),
                                                 self.tr(
                                                     f'Вы точно хоите открепить хранилище {cm.WORK_DIR}?'),
                                                 QtWidgets.QMessageBox.StandardButton.No | QtWidgets.QMessageBox.StandardButton.Yes)
        if message.Yes == message:
            cm.remove_link_folder(cm.WORK_DIR)
            cm.save_config()
            self.main_terminal.setText( self.main_terminal.toPlainText() + f'ОТКРЕПЛЕНИЕ: {self.comboBox.currentText()}\n')
            self.update_list_folders()
        
    def show_parametrs(self):
        self.p = Parametrs(self)
        self.p.show()

    def fix_folder(self):
        self.p = Parametrs(self, is_new=True)
        self.p.show()

    def ssf(self, progress_callback, *args, **kwargs):
        progress_callback.emit(args[0])
        

    def show_send_files(self, progress_callback):
        cm.show_stream_upload_files = lambda *args, **kwargs: self.ssf(progress_callback, *args, **kwargs) 
        cm.send_folder_network()


    def send_folder(self):
        # cm.send_folder_network()
        
        self.w = Worker(self.show_send_files)

        self.w.signals.progress.connect(lambda x : self.main_terminal.setText( self.main_terminal.toPlainText() + f'ОТПРАВКА: {str(x)}\n'))
        self.w.signals.result.connect(lambda x : self.main_terminal.setText( self.main_terminal.toPlainText() + f'РЕЗУЛЬТАТ: {str(x)}\n'))
        self.w.signals.error.connect(lambda x : self.main_terminal.setText( self.main_terminal.toPlainText() + f'ОШИБКА: {str(x)}\n'))

        self.threadpool.start(self.w)
        # print('SEND')

    def download_folder(self):
        self.paths = Paths_UI()
        self.paths.show()

    
    def show_about(self):
        self.about = About_UI()
        self.about.show()
        
    





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
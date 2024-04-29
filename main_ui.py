from PySide6 import QtCore, QtGui, QtWidgets
from core import CopyManager
import sys, os

VERSION = '0.2.0'
cm = CopyManager()

def clearLayout(layout):
    for i in reversed(range(layout.count())): 
        child = layout.itemAt(i)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())

class Parametrs(QtWidgets.QWidget):
    def __init__(self, parent, is_new=False):
        super().__init__()
        self.is_new = is_new
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
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
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
        print(cm.CONFIG['CONNECT_FOLDERS'][cm.WORK_DIR]['ORIGINAL_LOCATION'])
        self.location_pushButton.setText(cm.CONFIG['CONNECT_FOLDERS'][cm.WORK_DIR]['ORIGINAL_LOCATION'])
        self.comboBox.setCurrentText(cm.WORK_DIR)
      
    def save_folder(self):
        if self.comboBox.currentText() == 'NETWORK':
            try:
                if not os.path.isdir(self.location_pushButton.text()):
                    raise ValueError()

                cm.fix_folder(self.lineEdit.text(), self.location_pushButton.text(), self.comboBox.currentText(), 0, {
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
        self.location_pushButton.setText(path)
        
        



class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Main")
        self.resize(336, 293)
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
        self.about_pushButton = QtWidgets.QPushButton(parent=self)
        self.about_pushButton.setObjectName("about_pushButton")
        self.horizontalLayout.addWidget(self.about_pushButton)
        self.settings_pushButton = QtWidgets.QPushButton(parent=self)
        self.settings_pushButton.setObjectName("settings_pushButton")
        self.horizontalLayout.addWidget(self.settings_pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
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
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.fix_folder_pushButton = QtWidgets.QPushButton(parent=self)
        self.fix_folder_pushButton.setObjectName("fix_folder_pushButton")
        self.horizontalLayout_2.addWidget(self.fix_folder_pushButton)
        self.type_pushButton = QtWidgets.QPushButton(parent=self)
        self.type_pushButton.setText("ТИП")
        self.type_pushButton.setObjectName("type_pushButton")
        self.horizontalLayout_2.addWidget(self.type_pushButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(parent=self)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(parent=self)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.settings_folder_pushButton = QtWidgets.QPushButton(parent=self)
        self.settings_folder_pushButton.setObjectName("settings_folder_pushButton")
        self.verticalLayout.addWidget(self.settings_folder_pushButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(parent=self)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.main_terminal = QtWidgets.QTextBrowser(parent=self)
        self.main_terminal.setObjectName("main_terminal")
        self.verticalLayout_5.addWidget(self.main_terminal)
        self.verticalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.comboBox.currentTextChanged.connect(self.active_folder)
        self.update_list_folders()
        

        
        self.settings_folder_pushButton.clicked.connect(self.show_parametrs)
        self.fix_folder_pushButton.clicked.connect(self.fix_folder)

        self.retranslateUi()
    
    def update_list_folders(self):
        self.comboBox.clear()
        for i in cm.CONFIG['CONNECT_FOLDERS']:
            self.comboBox.addItem(i)


     

    def retranslateUi(self):
        self.setWindowTitle(self.tr("CopySystem"))
        self.icon_lable.setText(self.tr(f"<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">CopySystem<sup>{str(VERSION)}</sup> </span></p></body></html>"))
        self.about_pushButton.setText(self.tr("О нас"))
        self.settings_pushButton.setText(self.tr("Настрйоки"))
        self.folder_label.setText(self.tr(""))
        self.pushButton_2.setText(self.tr("Отправить"))
        self.pushButton_5.setText(self.tr("Загрузить"))
        self.pushButton.setText(self.tr("Удалить"))
        self.fix_folder_pushButton.setText(self.tr("+"))
        self.settings_folder_pushButton.setText(self.tr("Параметры хранилища"))
        self.label.setText(self.tr("Ход выполнения"))

    def active_folder(self):
       
        if self.comboBox.currentText():
            cm.activate_folder(self.comboBox.currentText())
            self.main_terminal.setText( self.main_terminal.toPlainText() + f'ACTIVATE {self.comboBox.currentText()}\n')
            self.type_pushButton.setText(cm.CONFIG['CONNECT_FOLDERS'][cm.WORK_DIR]['TYPE'])
        

    def show_parametrs(self):
        self.p = Parametrs(self)
        self.p.show()
    

    def fix_folder(self):
        self.p = Parametrs(self, is_new=True)
        self.p.show()
        
    





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'desk_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class DeskUi(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(836, 664)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet("QWidget{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 255, 147, 255), stop:1 rgba(0, 255, 244, 255));\n"
"    border: 0px solid;\n"
"    border-radius: 5px;\n"
"}")
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.desk_name = QtWidgets.QLineEdit(Form)
        self.desk_name.setStyleSheet("QLineEdit{\n"
"    background-color: transparent;\n"
"    border: 0px solid;\n"
"    \n"
"}")
        self.desk_name.setObjectName("desk_name")
        self.horizontalLayout_2.addWidget(self.desk_name)
        self.delete_desk_button = QtWidgets.QPushButton(Form)
        self.delete_desk_button.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    border: 0px solid;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px 5px;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 223, 129, 255), stop:1 rgba(0, 212, 203, 255));\n"
"    border: 0px solid;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px 5px;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(135, 255, 204, 255), stop:1 rgba(126, 255, 250, 255));\n"
"    border: 0px solid;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px 5px;\n"
"}")
        self.delete_desk_button.setText("")
        self.delete_desk_button.setObjectName("delete_desk_button")
        self.horizontalLayout_2.addWidget(self.delete_desk_button)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 10, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.create_card_button = QtWidgets.QPushButton(Form)
        self.create_card_button.setMinimumSize(QtCore.QSize(355, 0))
        self.create_card_button.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    border: 0px solid;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px 5px;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 223, 129, 255), stop:1 rgba(0, 212, 203, 255));\n"
"    border: 0px solid;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px 5px;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(135, 255, 204, 255), stop:1 rgba(126, 255, 250, 255));\n"
"    border: 0px solid;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px 5px;\n"
"}")
        self.create_card_button.setObjectName("create_card_button")
        self.verticalLayout_2.addWidget(self.create_card_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.desk_name.setText(_translate("Form", "??????????"))
        self.create_card_button.setText(_translate("Form", "?????????????? ????????????????"))

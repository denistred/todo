# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wid_1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(403, 320)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.card_name = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.card_name.sizePolicy().hasHeightForWidth())
        self.card_name.setSizePolicy(sizePolicy)
        self.card_name.setMinimumSize(QtCore.QSize(310, 0))
        self.card_name.setStyleSheet("QLineEdit {\n"
"    background-color: transparent;\n"
"    border: 0px solid;\n"
"    border-radius: 3px;\n"
"    padding: 2px 5px 2px;\n"
"}\n"
"QLineEdit:hover{\n"
"    background-color:#ACACAC;\n"
"    border: 0px solid;\n"
"    border-radius: 3px;\n"
"    padding: 2px 5px 2px;\n"
"}\n"
"QLineEdit:pressed{\n"
"    background-color:#fcfafa;\n"
"    border: 0px solid;\n"
"    border-radius: 3px;\n"
"    padding: 2px 5px 2px;\n"
"}")
        self.card_name.setObjectName("card_name")
        self.horizontalLayout.addWidget(self.card_name)
        self.delete_widget_button = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_widget_button.sizePolicy().hasHeightForWidth())
        self.delete_widget_button.setSizePolicy(sizePolicy)
        self.delete_widget_button.setMinimumSize(QtCore.QSize(22, 22))
        self.delete_widget_button.setMaximumSize(QtCore.QSize(22, 22))
        self.delete_widget_button.setStyleSheet("QPushButton {\n"
"    background-color:transparent;\n"
"    border: 0px solid;\n"
"    border-radius: 3px;\n"
"    padding: 5px 10px 5px;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color:#ACACAC;\n"
"    border: 0px solid;\n"
"    border-radius: 3px;\n"
"    padding: 5px 10px 5px;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color:#fcfafa;\n"
"    border: 0px solid;\n"
"    border-radius: 3px;\n"
"    padding: 5px 10px 5px;\n"
"}")
        self.delete_widget_button.setText("")
        self.delete_widget_button.setObjectName("delete_widget_button")
        self.horizontalLayout.addWidget(self.delete_widget_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.add_task_button = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_task_button.sizePolicy().hasHeightForWidth())
        self.add_task_button.setSizePolicy(sizePolicy)
        self.add_task_button.setMinimumSize(QtCore.QSize(340, 30))
        self.add_task_button.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.add_task_button.setSizeIncrement(QtCore.QSize(0, 0))
        self.add_task_button.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setKerning(True)
        self.add_task_button.setFont(font)
        self.add_task_button.setStyleSheet("QPushButton {\n"
"    background-color:transparent;\n"
"    border: 0px solid;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px 5px;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color:#ACACAC;\n"
"    border: 0px solid;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px 5px;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color:#fcfafa;\n"
"    border: 0px solid;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px 5px;\n"
"}")
        self.add_task_button.setFlat(False)
        self.add_task_button.setObjectName("add_task_button")
        self.verticalLayout.addWidget(self.add_task_button)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.card_name.setText(_translate("Form", "Новый список"))
        self.add_task_button.setText(_translate("Form", "Добавить задачу"))

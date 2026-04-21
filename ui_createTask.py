# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createTask.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDateTimeEdit,
    QDialogButtonBox, QFormLayout, QLabel, QMainWindow,
    QMenuBar, QPlainTextEdit, QSizePolicy, QStatusBar,
    QTimeEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 626)
        self.centralwidget = QWidget(Form)
        self.centralwidget.setObjectName(u"centralwidget")
        self.formLayout = QFormLayout(self.centralwidget)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.taskNameEdit = QPlainTextEdit(self.centralwidget)
        self.taskNameEdit.setObjectName(u"taskNameEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.taskNameEdit)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.taskBucketTypeSelector = QComboBox(self.centralwidget)
        self.taskBucketTypeSelector.setObjectName(u"taskBucketTypeSelector")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.taskBucketTypeSelector)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.taskDeadlineEdit = QDateTimeEdit(self.centralwidget)
        self.taskDeadlineEdit.setObjectName(u"taskDeadlineEdit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.taskDeadlineEdit)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.estTaskTime = QTimeEdit(self.centralwidget)
        self.estTaskTime.setObjectName(u"estTaskTime")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.estTaskTime)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.taskDescriptionEdit = QPlainTextEdit(self.centralwidget)
        self.taskDescriptionEdit.setObjectName(u"taskDescriptionEdit")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.taskDescriptionEdit)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.maxSessionTimeEdit = QTimeEdit(self.centralwidget)
        self.maxSessionTimeEdit.setObjectName(u"maxSessionTimeEdit")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.maxSessionTimeEdit)

        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.buttonBox)

        Form.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Form)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        Form.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Form)
        self.statusbar.setObjectName(u"statusbar")
        Form.setStatusBar(self.statusbar)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("Form", u"Task Name", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Task Bucket Type", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Task Deadline", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Estimated Task Time", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Task Description", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Maximum Session Time", None))
    # retranslateUi


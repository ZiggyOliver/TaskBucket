# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bucketTime.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QTimeEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(518, 48)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(37, 16777215))

        self.horizontalLayout.addWidget(self.label_2)

        self.startDay = QComboBox(Form)
        self.startDay.addItem("")
        self.startDay.addItem("")
        self.startDay.addItem("")
        self.startDay.addItem("")
        self.startDay.addItem("")
        self.startDay.addItem("")
        self.startDay.addItem("")
        self.startDay.setObjectName(u"startDay")

        self.horizontalLayout.addWidget(self.startDay)

        self.startTime = QTimeEdit(Form)
        self.startTime.setObjectName(u"startTime")

        self.horizontalLayout.addWidget(self.startTime)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout.addWidget(self.label_4)

        self.finishDay = QComboBox(Form)
        self.finishDay.addItem("")
        self.finishDay.addItem("")
        self.finishDay.addItem("")
        self.finishDay.addItem("")
        self.finishDay.addItem("")
        self.finishDay.addItem("")
        self.finishDay.addItem("")
        self.finishDay.setObjectName(u"finishDay")

        self.horizontalLayout.addWidget(self.finishDay)

        self.finishTime = QTimeEdit(Form)
        self.finishTime.setObjectName(u"finishTime")

        self.horizontalLayout.addWidget(self.finishTime)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Start", None))
        self.startDay.setItemText(0, QCoreApplication.translate("Form", u"Monday", None))
        self.startDay.setItemText(1, QCoreApplication.translate("Form", u"Tuesday", None))
        self.startDay.setItemText(2, QCoreApplication.translate("Form", u"Wednesday", None))
        self.startDay.setItemText(3, QCoreApplication.translate("Form", u"Thursday", None))
        self.startDay.setItemText(4, QCoreApplication.translate("Form", u"Friday", None))
        self.startDay.setItemText(5, QCoreApplication.translate("Form", u"Saturday", None))
        self.startDay.setItemText(6, QCoreApplication.translate("Form", u"Sunday", None))

        self.label_4.setText(QCoreApplication.translate("Form", u"Finish", None))
        self.finishDay.setItemText(0, QCoreApplication.translate("Form", u"Monday", None))
        self.finishDay.setItemText(1, QCoreApplication.translate("Form", u"Tuesday", None))
        self.finishDay.setItemText(2, QCoreApplication.translate("Form", u"Wednesday", None))
        self.finishDay.setItemText(3, QCoreApplication.translate("Form", u"Thursday", None))
        self.finishDay.setItemText(4, QCoreApplication.translate("Form", u"Friday", None))
        self.finishDay.setItemText(5, QCoreApplication.translate("Form", u"Saturday", None))
        self.finishDay.setItemText(6, QCoreApplication.translate("Form", u"Sunday", None))

    # retranslateUi
class BucketTimeElement(QWidget, Ui_Form):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

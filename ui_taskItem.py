# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'taskItem.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_taskItem(object):
    def setupUi(self, taskItem):
        if not taskItem.objectName():
            taskItem.setObjectName(u"taskItem")
        taskItem.resize(245, 66)
        taskItem.setAutoFillBackground(False)
        self.verticalLayout = QVBoxLayout(taskItem)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.centralwidget = QWidget(taskItem)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setAutoFillBackground(True)
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.taskName = QLabel(self.centralwidget)
        self.taskName.setObjectName(u"taskName")

        self.verticalLayout_2.addWidget(self.taskName)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.rescheduleButton = QPushButton(self.widget)
        self.rescheduleButton.setObjectName(u"rescheduleButton")

        self.horizontalLayout.addWidget(self.rescheduleButton)


        self.verticalLayout_2.addWidget(self.widget)


        self.verticalLayout.addWidget(self.centralwidget)


        self.retranslateUi(taskItem)

        QMetaObject.connectSlotsByName(taskItem)
    # setupUi

    def retranslateUi(self, taskItem):
        taskItem.setWindowTitle(QCoreApplication.translate("taskItem", u"Form", None))
        self.taskName.setText(QCoreApplication.translate("taskItem", u"Name", None))
        self.rescheduleButton.setText(QCoreApplication.translate("taskItem", u"Reschedule", None))
    # retranslateUi


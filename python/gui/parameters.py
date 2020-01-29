from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from parameters_basic import BasicParameters
from multipliers import Multipliers
from nodes import Nodes

parameters = ['Import', 'Basic Parameters', 'Multipliers',
            'Nodes', 'Node Types', 'Elements', 'Materials']

class ParametersPage(QGroupBox):
    def __init__(self):
        super(ParametersPage, self).__init__('Parameters')
        self.parametersPageLayout = QHBoxLayout()
        self.setLayout(self.parametersPageLayout)
        self.parametersPageNav = QVBoxLayout()
        self.parametersPageNav.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.parametersPageStack = QStackedLayout()

        # Attach navigation buttons layout and layout for contents
        self.parametersPageLayout.addLayout(self.parametersPageNav)
        self.parametersPageLayout.addLayout(self.parametersPageStack)

        self.parametersPageHome = QWidget()
        self.parametersPageBasic = BasicParameters()
        self.parametersPageMult = Multipliers()
        self.parametersPageNodes = Nodes()
        self.parametersPageNodesT = QGroupBox('Node Types')
        self.parametersPageElem = QGroupBox('Elements')
        self.parametersPageMat = QGroupBox('Materials')

        self.parametersPageStack.addWidget(self.parametersPageHome)
        self.parametersPageStack.addWidget(self.parametersPageBasic)
        self.parametersPageStack.addWidget(self.parametersPageMult)
        self.parametersPageStack.addWidget(self.parametersPageNodes)
        self.parametersPageStack.addWidget(self.parametersPageNodesT)
        self.parametersPageStack.addWidget(self.parametersPageElem)
        self.parametersPageStack.addWidget(self.parametersPageMat)

        #   Add navigation buttons (widgets) to
        #       button container 'self.parametersPageStack'
        for i, parameter in enumerate(parameters):
            pbtn = QPushButton(str(parameter))
            pbtn.setGeometry(0, 0, 150, 100)

            pbtn.pressed.connect(lambda i=i:
                            self.parametersPageStack.setCurrentIndex(i)
                                )
            self.parametersPageNav.addWidget(pbtn)

        self.parametersPageNav.setContentsMargins(0, 0, 0, 0)
        self.parametersPageNav.setSpacing(20)

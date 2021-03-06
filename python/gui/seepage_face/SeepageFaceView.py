from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from enum import Enum

class SeepageFaceNodeType(Enum):
    DIRICHELT = 1
    NUEMANN = 2

class SeepageFaceView(QGroupBox):
    def __init__(self, seepageFaceModel):
        super(SeepageFaceView, self).__init__('Seepage Face ' + str(seepageFaceModel.seepageFaceID))

        self.seepageFaceModel = seepageFaceModel

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.setSpacing(20)

        nodesInputLayout = QHBoxLayout()
        nodesInputLayout.setAlignment(Qt.AlignTop)

        # column for dirichelt nodes
        self.diricheltNodesLayout = QVBoxLayout()
        #self.diricheltNodesLayout.setContentsMargins(0, 0, 20, 2)
        self.diricheltNodesLayout.setSpacing(0)
        self.diricheltNodesLayout.setAlignment(Qt.AlignTop)
        
        self.diricheltNodesHeader = QLabel('Dirichelt Node Count')
        self.diricheltNodesHeader.setFont(QFont('Arial', 13))
        #self.diricheltNodesHeader.setAlignment(Qt.AlignLeft)
        self.diricheltNodesLayout.addWidget(self.diricheltNodesHeader)

        self.diricheltNodesCount = QSpinBox()
        self.diricheltNodesCount.setAlignment(Qt.AlignCenter)
        self.diricheltNodesCount.setFixedWidth(85)
        self.diricheltNodesCount.setRange(0, 100)
        self.diricheltNodesCount.setValue(seepageFaceModel.getNumberOfDiricheltNodes())
        self.diricheltNodesCount.valueChanged.connect(self.updateNodeCount(SeepageFaceNodeType.DIRICHELT))
        self.diricheltNodesLayout.addWidget(self.diricheltNodesCount)
            
        # column for neumann nodes
        self.nuemannNodesLayout = QVBoxLayout()
        #self.nuemannNodesLayout.setContentsMargins(0, 0, 20, 2)
        self.nuemannNodesLayout.setSpacing(0)
        self.nuemannNodesLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        self.nuemannNodesHeader = QLabel('Nuemann Node Count')
        self.nuemannNodesHeader.setFont(QFont('Arial', 13))
        #self.nuemannNodesHeader.setAlignment(Qt.AlignLeft)
        self.nuemannNodesLayout.addWidget(self.nuemannNodesHeader)

        self.nuemannNodesCount = QSpinBox()
        self.nuemannNodesCount.setAlignment(Qt.AlignCenter)
        self.nuemannNodesCount.setRange(0, 100)
        self.nuemannNodesCount.setFixedWidth(85)
        self.nuemannNodesCount.setValue(seepageFaceModel.getNumberOfNuemannNodes())
        self.nuemannNodesCount.valueChanged.connect(self.updateNodeCount(SeepageFaceNodeType.NUEMANN))
        self.nuemannNodesLayout.addWidget(self.nuemannNodesCount)


        nodesInputLayout.addLayout(self.diricheltNodesLayout)
        nodesInputLayout.addLayout(self.nuemannNodesLayout)

        layout.addLayout(nodesInputLayout)
        self.setLayout(layout)

        self.updateView()


    def _clearLayout(self, layout):
        #print(layout.count())
        for i in reversed(range(layout.count())):
            # keep the label and spinner
            if i == 1:
                break

            widgetToRemove = layout.itemAt(i).widget()
            # remove it from the layout list
            layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.deleteLater()

    def _destroyView(self):
        self._clearLayout(self.diricheltNodesLayout)
        self._clearLayout(self.nuemannNodesLayout)

    def _addModelData(self, layout, viewModelEnum):
        viewModelData = None

        if viewModelEnum == SeepageFaceNodeType.NUEMANN:
            viewModelData = self.seepageFaceModel.nuemannNodes
        elif viewModelEnum == SeepageFaceNodeType.DIRICHELT:
            viewModelData = self.seepageFaceModel.diricheltNodes

        for i in range(len(viewModelData)):
            nodeEdit = QLineEdit()
            nodeEdit.setValidator(QIntValidator(0, 100))
            nodeEdit.setText(str(viewModelData[i]))
            nodeEdit.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            nodeEdit.textEdited.connect(self.updateNodeValue(viewModelEnum, i))
            nodeEdit.setFixedWidth(85)
            layout.addWidget(nodeEdit)

        
    def updateView(self):
        self._destroyView()
        self._addModelData(self.nuemannNodesLayout, SeepageFaceNodeType.NUEMANN)
        self._addModelData(self.diricheltNodesLayout, SeepageFaceNodeType.DIRICHELT)



    def updateNodeCount(self, nodeType):
        def inner(count):
            if nodeType == SeepageFaceNodeType.DIRICHELT:
                self.seepageFaceModel.setNumberOfDiricheltNodes(count)
            elif nodeType == SeepageFaceNodeType.NUEMANN:
                self.seepageFaceModel.setNumberOfNuemannNodes(count)
            self.updateView()

        return inner

    def updateNodeValue(self, nodeType, index):
        def inner(text):
            if nodeType == SeepageFaceNodeType.DIRICHELT:
                self.seepageFaceModel.setDiricheltNode(index, int(text))
            elif nodeType == SeepageFaceNodeType.NUEMANN:
                self.seepageFaceModel.setNuemannNode(index, int(text))
        return inner

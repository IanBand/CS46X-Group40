from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

nodeTableLabels = ["Node", "Boundary Type", "X-Coordinate",
            "Y-Coordinate", "Initial Pressure", "Initial Concentration"]

class Nodes(QGroupBox):
    def __init__(self):
        super(Nodes, self).__init__('Nodes')
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setLayout(self.layout)
        self.createTable(52)
        self.layout.addWidget(self.nodeTable)

    def createTable(self, numNodes):
        self.nodeTable = QTableWidget()
        self.nodeTable.setRowCount(numNodes)
        self.nodeTable.setColumnCount(len(nodeTableLabels))
        self.nodeTable.setMaximumWidth(730)
        # Set labels
        self.nodeTable.setHorizontalHeaderLabels(nodeTableLabels)
        self.nodeTable.verticalHeader().hide()
        # Set table column widths to match label size
        self.nodeTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for row in range(0, numNodes):
                nodeLabel = QLabel(str(row+1))
                nodeLabel.setAlignment(Qt.AlignCenter)
                self.nodeTable.setCellWidget(row, 0, nodeLabel)
                bComboBox = BoundaryComboBox()
                self.nodeTable.setCellWidget(row, 1, bComboBox)
                nodeX = QDoubleSpinBox()
                nodeX.setAlignment(Qt.AlignRight)
                nodeX.setRange(-9999.999, 9999.999)
                nodeX.setDecimals(3)
                nodeX.setSingleStep(0.001)
                self.nodeTable.setCellWidget(row, 2, nodeX)
                nodeY = QDoubleSpinBox()
                nodeY.setAlignment(Qt.AlignRight)
                nodeY.setRange(-9999.999, 9999.999)
                nodeY.setDecimals(3)
                nodeY.setSingleStep(0.001)
                self.nodeTable.setCellWidget(row, 3, nodeY)
                iPressure = QDoubleSpinBox()
                iPressure.setAlignment(Qt.AlignRight)
                iPressure.setRange(-9999.999, 9999.999)
                iPressure.setDecimals(3)
                iPressure.setSingleStep(0.001)
                self.nodeTable.setCellWidget(row, 4, iPressure)
                iConcentration = QDoubleSpinBox()
                iConcentration.setAlignment(Qt.AlignRight)
                iConcentration.setRange(-9999.999, 9999.999)
                iConcentration.setDecimals(3)
                iConcentration.setSingleStep(0.001)
                self.nodeTable.setCellWidget(row, 5, iConcentration)

class BoundaryComboBox(QComboBox):
    def __init__(self):
        super(BoundaryComboBox, self).__init__()
        self.addItem("Constant Head (Dirichlet)")
        self.addItem("Source/Sink")
        self.addItem("Infiltration/Evaporation (Variable Boundary)")
        self.addItem("Seepage Face")
        self.addItem("Mixed Boundary Condition")

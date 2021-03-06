from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from enum import Enum


class MaterialEnum(Enum):
    PRESSURE_HEAD = 1
    MOISTURE_CONTENT = 2
    HYDRAULIC_CONDUCTIVITY = 3

class MaterialView(QGroupBox):
    def __init__(self, materialModel):
        super(MaterialView, self).__init__("Material " + str(materialModel.materialGroup))
        self.viewModel = materialModel

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.setSpacing(20)

        self.pointCountLabel = QLabel("Number of Interpolation Points")
        self.pointCountLabel.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.pointCountLabel)

        self.pointCountSB = QSpinBox()
        self.pointCountSB.setFixedWidth(60)
        self.pointCountSB.setAlignment(Qt.AlignCenter)
        self.pointCountSB.setRange(1, 15)
        self.pointCountSB.valueChanged.connect(self.updatePointCount)
        layout.addWidget(self.pointCountSB)

        self.interpolationPointsHeader = QLabel("Interpolation Points")
        self.interpolationPointsHeader.setFont(QFont('Arial', 16))
        self.interpolationPointsHeader.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.interpolationPointsHeader)

        pointsInputLayout = QHBoxLayout()
        pointsInputLayout.setAlignment(Qt.AlignCenter)

        self.pressureHeadLayout = QVBoxLayout()
        self.pressureHeadLayout.setContentsMargins(0, 0, 20, 2)
        self.pressureHeadLayout.setSpacing(0)
        self.pressureHeadLayout.setAlignment(Qt.AlignCenter)

        self.pressureHeadLabel = QLabel("Pressure Head")
        self.pressureHeadLabel.setFont(QFont('Arial', 13))
        self.pressureHeadLabel.setAlignment(Qt.AlignLeft)
        self.pressureHeadLayout.addWidget(self.pressureHeadLabel)

        pointsInputLayout.addLayout(self.pressureHeadLayout)

        self.moistureContentLayout = QVBoxLayout()
        self.moistureContentLayout.setContentsMargins(0, 0, 20, 2)
        self.moistureContentLayout.setSpacing(0)
        self.moistureContentLayout.setAlignment(Qt.AlignCenter)

        self.moistureContentLabel = QLabel("Moisture Content")
        self.moistureContentLabel.setFont(QFont('Arial', 13))
        self.moistureContentLabel.setAlignment(Qt.AlignLeft)
        self.moistureContentLayout.addWidget(self.moistureContentLabel)

        pointsInputLayout.addLayout(self.moistureContentLayout)

        self.hydraulicConductivityLayout = QVBoxLayout()
        self.hydraulicConductivityLayout.setContentsMargins(0, 0, 20, 2)
        self.hydraulicConductivityLayout.setSpacing(0)
        self.hydraulicConductivityLayout.setAlignment(Qt.AlignCenter)

        self.hydraulicConductivityLabel = QLabel("Hydraulic Conductivity")
        self.hydraulicConductivityLabel.setFont(QFont('Arial', 13))
        self.hydraulicConductivityLabel.setAlignment(Qt.AlignLeft)
        self.hydraulicConductivityLayout.addWidget(self.hydraulicConductivityLabel)

        pointsInputLayout.addLayout(self.hydraulicConductivityLayout)

        layout.addLayout(pointsInputLayout)
        self.setLayout(layout)


        # asserts that the view has all correct data showing
        self.updateView()


    # clear layout save for labels
    def _clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            if i == 0:
                break

            widgetToRemove = layout.itemAt(i).widget()
            # remove it from the layout list
            layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.deleteLater()

    def _destroyView(self):
        self._clearLayout(self.pressureHeadLayout)
        self._clearLayout(self.moistureContentLayout)
        self._clearLayout(self.hydraulicConductivityLayout)

    def _addModelData(self, layout, viewModelEnum):

        viewModelData = None

        if viewModelEnum == MaterialEnum.HYDRAULIC_CONDUCTIVITY:
            viewModelData = self.viewModel.hydraulicConductivity
        elif viewModelEnum == MaterialEnum.MOISTURE_CONTENT:
            viewModelData = self.viewModel.moistureContent
        elif viewModelEnum == MaterialEnum.PRESSURE_HEAD:
            viewModelData = self.viewModel.pressureHead

        for i in range(len(viewModelData)):
            entryInput = QDoubleSpinBox(buttonSymbols = QDoubleSpinBox.NoButtons)
            entryInput.setDecimals(3)
            entryInput.setSingleStep(0.001)
            entryInput.setRange(-999.999, 9999.999)
            entryInput.setAlignment(Qt.AlignRight)
            entryInput.setFixedWidth(85)

            entryInput.setValue(viewModelData[i])

            # At a high level this binds the value of this UI element
            # to a value in the MaterialModel
            entryInput.valueChanged.connect(self.updatePoint(i, viewModelEnum))

            layout.addWidget(entryInput)

    def updateView(self):
        self._destroyView()

        self._addModelData(self.pressureHeadLayout, MaterialEnum.PRESSURE_HEAD)
        self._addModelData(self.moistureContentLayout, MaterialEnum.MOISTURE_CONTENT)
        self._addModelData(self.hydraulicConductivityLayout, MaterialEnum.HYDRAULIC_CONDUCTIVITY)

        self.pointCountSB.setValue(self.viewModel.getInterpolationPointCount())

    def updatePointCount(self):
        pointCount = self.pointCountSB.value()
        self.viewModel.setInterpolationPointCount(pointCount)

        # important to update the entire view here as UI
        # elements need to be added/removed when a new
        # interpolation point count is set.
        self.updateView()


    def updatePoint(self, index, viewModelEnum):
        def inner(newValue):
            if viewModelEnum == MaterialEnum.HYDRAULIC_CONDUCTIVITY:
                self.viewModel.hydraulicConductivity[index] = newValue
            elif viewModelEnum == MaterialEnum.MOISTURE_CONTENT:
                self.viewModel.moistureContent[index] = newValue
            elif viewModelEnum == MaterialEnum.PRESSURE_HEAD:
                self.viewModel.pressureHead[index] = newValue

        return inner

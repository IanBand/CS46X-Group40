import csv

from gui.simulation.SimulationModel import GS2KOD

class FileWriter:
    def __init__(self,
            materialModels,
            simulationModel,
            seepageFaceModels,
            basicParametersModel,
            elementModels,
            multipliersModel,
            elementPropertiesModels,
            nodeModels,
            nodeTypesModels):

        self.materialModels = materialModels
        self.simulationModel = simulationModel
        self.seepageFaceModels = seepageFaceModels
        self.basicParametersModel = basicParametersModel
        self.elementModels = elementModels
        self.multipliersModel = multipliersModel
        self.elementPropertiesModels = elementPropertiesModels
        self.nodeModels = nodeModels
        self.nodeTypesModels = nodeTypesModels


    def write(self, filepath):

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(
                csvfile,
                delimiter=',',
                quotechar='|', #unused, I think
                quoting=csv.QUOTE_MINIMAL #also unused
            )

            # write groups
            self._writeGroupA(writer, self.simulationModel)
            self._writeGroupB(writer, self.basicParametersModel)
            self._writeGroupC(writer, self.multipliersModel)
            self._writeGroupD(writer, self.simulationModel)
            self._writeGroupE(writer, self.nodeModels)
            self._writeGroupF(writer, self.nodeTypesModels['SSNodes'])
            self._writeGroupG(writer, self.nodeModels)
            self._writeGroupH(writer, self.nodeModels)
            self._writeGroupI(writer, self.elementModels)
            self._writeGroupJ(writer, self.elementPropertiesModels)
            self._writeGroupK(writer, self.nodeModels)
            self._writeGroupL(writer, self.nodeModels)
            self._writeGroupM(writer, self.nodeTypesModels['VariableBCNodes'])
            self._writeGroupN(writer, self.nodeTypesModels['MixedBCNodes'])
            self._writeGroupO(writer, self.seepageFaceModels)
            self._writeGroupP(writer, self.elementModels, self.nodeTypesModels['MixedBCNodes'])
            self._writeGroupQ(writer, self.materialModels)

    def _csvPad(self, cols):
        # 20 data points plus group
        maxCols = 21
        while len(cols) < maxCols:
            cols.append('')
        return cols

    def _writeGroupQ(self, csv, materials):

        # sub group Q-1
        group = "Q-1"
        csvRow = [group]
        for mat in materials:
            csvRow.append(mat.getInterpolationPointCount())

            # allows 20 values in this group
            if len(csvRow) == 21:
                csv.writerow(csvRow)
                csvRow = [group]

        # make sure the last row actually has meaningful data
        if len(csvRow) > 1:
            csv.writerow(self._csvPad(csvRow))


        groups = ["Q-2", "Q-3", "Q-4"]
        for mat in materials:
            matData = [mat.pressureHead, mat.moistureContent, mat.hydraulicConductivity]
            for i in range(3):
                csvRow = [groups[i]]
                for elem in matData[i]:
                    csvRow.append(elem)
                    # these groups contains at most 8 data points plus the group
                    if len(csvRow) == 9:
                        csv.writerow(self._csvPad(csvRow))
                        csvRow = [groups[i]]

                if len(csvRow) > 1:
                    csv.writerow(self._csvPad(csvRow))


    def _writeGroupA(self, csv, simulation):
        group = "A"
        csvRow = [group, simulation.simulationTitle]
        csv.writerow(self._csvPad(csvRow))

    def _writeGroupB(self, csv, basicParameters):
        group = "B"

        TYPE = 'BACK' if basicParameters.TYPE == "Implicit" else 'CENT'
        STATP = '1.0' if basicParameters.STATP == "Transient" else '0.0'

        if basicParameters.STAT == "Flow equation only":
            STAT = '-1.0'
        elif basicParameters.STAT == "Steady-state":
            STAT = '0.0'
        else:
            STAT = '1.0'

        # derived parameters
        # assume zeros for the time being; makes testing import do able
        NS = len(list(filter(lambda node: node.dirichelt == True, self.nodeTypesModels['VariableBCNodes'])))
        KNS = len(list(filter(lambda node: node.boundary.getData() == "Constant Concentration (Dirichlet)", self.nodeModels)))
        NF = len(list(filter(lambda node: node.boundary.getData() == "Source/Sink", self.nodeModels)))
        INC = max(map(lambda element: len(element.getIncidences()), self.elementModels))
        NSDN = len(list(filter(lambda node: node.nuemann == True, self.nodeTypesModels['VariableBCNodes'])))
        MQ4 = '0'
        KNSDN =  len(self.nodeTypesModels['MixedBCNodes'])
        COEFI = '1.0'
        NVS = '0'
        DPRDT = '0'

        csvRow = [
                group,
                basicParameters.NN.getData(),
                basicParameters.NE.getData(),
                NS,
                KNS,
                basicParameters.NB,
                basicParameters.KNB,
                NF,
                INC,
                basicParameters.NK.getData(),
                basicParameters.NSEEP.getData()
        ]

        csvRow2 = [
                group,
                NSDN,
                MQ4,
                KNSDN,
                basicParameters.PL,
                COEFI,
                basicParameters.EI,
                NVS
        ]

        csvRow3 = [
                group,
                basicParameters.DELT,
                basicParameters.CHNG,
                basicParameters.ITMAX,
                basicParameters.ITCHNG,
                basicParameters.PCHNG,
                basicParameters.BETAP,
                TYPE
        ]

        csvRow4 = [
                group,
                basicParameters.DIFUSN,
                DPRDT,
                STAT,
                STATP,
                basicParameters.CLOS1,
                basicParameters.ITER1,
                basicParameters.IGO
        ]

        csv.writerow(self._csvPad(csvRow))
        csv.writerow(self._csvPad(csvRow2))
        csv.writerow(self._csvPad(csvRow3))
        csv.writerow(self._csvPad(csvRow4))

    def _writeGroupC(self, csv, model):
        group = "C"

        csvRow1 = [
            group,
            model.AFMOBX,
            model.AFMOBY,
            model.APOR,
            model.AELONG,
            model.AETRANS,
            model.APHII,
            model.ACONCI,
            model.XFACT
        ]

        csvRow2 = [
            group,
            model.YFACT,
            model.ATETA,
            model.AAL,
            model.AKD,
            model.ALAM,
            model.ARHO
        ]

        csv.writerow(self._csvPad(csvRow1))
        csv.writerow(self._csvPad(csvRow2))

    def _writeGroupD(self, csv, simulation):
        group = "D"
        csvRow = [group]

        # order in simulation KOD array is the same as
        # whats expected by GS2

        for kod in GS2KOD:
            csvRow.append(simulation.getOutputModifier(kod))

        csv.writerow(self._csvPad(csvRow))

    def _writeGroupE(self, csv, nodes):
        group = "E"
        for node in nodes:
            csvRow = [group, node.I, node.X, node.Y]
            csv.writerow(self._csvPad(csvRow))

    def _writeGroupG(self, csv, nodes):
        group = "G-1"
        csv.writerow(self._csvPad([group, 0.0]))

        

        group = "G-2"
        csvRow = [group]
        for node in nodes:
            csvRow.append(node.I)
            csvRow.append(node.CONCI)

            if len(csvRow) == 9:
                csv.writerow(self._csvPad(csvRow))
                csvRow = [group]

        if len(csvRow) > 1:
            csv.writerow(self._csvPad(csvRow))

    def _writeGroupF(self, csv, ssModels):
        group = "F-1"
        csvRow = [group]

        for node in ssModels:
            csvRow.append(node.nodeID)
            csvRow.append(node.FQ)
            if len(csvRow) == 9:
                csv.writerow(self._csvPad(csvRow))
                csvRow = [group]

        if len(csvRow) > 1:
            csv.writerow(self._csvPad(csvRow))

        group = "F-2"
        csvRow = [group]

        for node in ssModels:
            csvRow.append(node.nodeID)
            csvRow.append(node.CFQ)
            if len(csvRow) == 9:
                csv.writerow(self._csvPad(csvRow))
                csvRow = [group]

        if len(csvRow) > 1:
            csv.writerow(self._csvPad(csvRow))

    def _writeGroupI(self, csv, elementModels):
        group = "I"
        for element in elementModels:
            csvRow = [ group, element.elementNumber ]

            for node in element.getIncidences():
                csvRow.append(node)

            csv.writerow(self._csvPad(csvRow))

    def _writeGroupJ(self, csv, elementPropertiesModels):
        materialGroups = {}
        for group in range(1, (self.basicParametersModel.NK.getData()+1)):
            materialGroups[str(group)] = []
        for element in self.elementModels:
            materialGroups[str(element.materialGroup)].append(element.elementNumber)

        for materialGroup in elementPropertiesModels:
            group = "J-1"
            csvRow = [
                group, 
                materialGroups[str(materialGroup.materialGroupId)][0],
                materialGroups[str(materialGroup.materialGroupId)][-1],
                materialGroup.materialGroupId
            ]
            csv.writerow(self._csvPad(csvRow))
            group = "J-2"
            csvRow = [
                group,
                materialGroup.FMOBX,
                materialGroup.FMOBY,
                materialGroup.ELONG,
                materialGroup.ETRANS,
                materialGroup.POR,
                materialGroup.TTA,
                materialGroup.ALPHA,
                materialGroup.KD,
            ]
            csv.writerow(self._csvPad(csvRow))
            csvRow = [
                group,
                materialGroup.LAMBDA,
                materialGroup.RHO,
            ]
            csv.writerow(self._csvPad(csvRow))

    def _writeGroupM(self, csv, variableBCNodes):

        if len(variableBCNodes) == 0:
            return

        group = "M-1"
        csvRow = [group]
        for vbcNode in variableBCNodes:
            if vbcNode.dirichlet == true:
                csvRow.append(vbcNode.nodeID)

        csv.writerow(self._csvPad(csvRow))

        group = "M-2"
        csvRow = [group]
        for vbcNode in variableBCNodes:
            if vbcNode.neumann == true:
                csvRow.append(vbcNode.nodeID)

        csv.writerow(self._csvPad(csvRow))

        group = "M-3"
        csvRow = [group]
        for vbcNode in variableBCNodes:
            csvRow.append(vbcNode.nodeID)
            csvRow.append(vbcNode.COEF)
            if len(csvRow) == 11:
                csv.writerow(self._csvPad(csvRow))
                csvRow = [group]

        if len(csvRow) > 1:
            csv.writerow(self._csvPad(csvRow))

        group = "M-4"
        csvRow = [group]
        for vbcNode in variableBCNodes:
            csvRow.append(vbcNode.nodeID)
            csvRow.append(vbcNode.VN)
            if len(csvRow) == 11:
                csv.writerow(self._csvPad(csvRow))
                csvRow = [group]

        if len(csvRow) > 1:
            csv.writerow(self._csvPad(csvRow))

    def _writeGroupN(self, csv, mixedBCNodes):
        group = "N-1"
        csvRow = [group]

        for mbcNode in mixedBCNodes:
            csvRow.append(mbcNode.nodeID)
            if len(csvRow) == 21:
                csv.writerow(self._csvPad(csvRow))
                csvRow = [group]

        if len(csvRow) > 1:
            csv.writerow(self._csvPad(csvRow))

        group = "N-2"
        csvRow = [group]
        for mbcNode in mixedBCNodes:
            csvRow.append(mbcNode.nodeID)
            csvRow.append(mbcNode.CN)
            if len(csvRow) == 11:
                csv.writerow(self._csvPad(csvRow))
                csvRow = [group]

        if len(csvRow) > 1:
            csv.writerow(self._csvPad(csvRow))

    def _writeGroupO(self, csv, seepageFaces):
        for seepageFace in seepageFaces:
            group = "O-1"
            totalNodes = seepageFace.getNumberOfDiricheltNodes() + seepageFace.getNumberOfNuemannNodes()
            csvRow = [group,  totalNodes, seepageFace.getNumberOfDiricheltNodes()]

            csv.writerow(self._csvPad(csvRow))

            groups = ["O-2", "O-3"]
            nodeLists = [seepageFace.diricheltNodes, seepageFace.nuemannNodes]

            for x in range(len(groups)):
                csvRow = [groups[x]]
                for node in nodeLists[x]:
                    csvRow.append(node)

                    # group + 20 nodes
                    if len(csvRow) == 21:
                        csv.writerow(csvRow)
                        csvRow = [groups[x]]

                if len(csvRow) > 1:
                    csv.writerow(self._csvPad(csvRow))


    def _writeGroupH(self, csv, nodeModels):
        group = "H-1"
        csvRow = [group, 0.0]

        csv.writerow(self._csvPad(csvRow))


        # we will support the other case for group H-2 later
        group = "H-2"
        csvRow = [group, 9999.0]
        csv.writerow(self._csvPad(csvRow))

        group = "H-3"
        csvRow = [group]

        for node in nodeModels:
            csvRow.append(node.I)
            csvRow.append(node.PHII)

            # gorup + 4 pairs
            if len(csvRow) == 9:
                csv.writerow(self._csvPad(csvRow))
                csvRow = [group]

        if len(csvRow) > 1:
            csv.writerow(self._csvPad(csvRow))



    def _writeGroupK(self, csv, nodeModels):
        group = "K"
        csvRow = [group]

        for node in nodeModels:
            if node.boundary.getData() == "Constant Head (Dirichlet)":
                csvRow.append(node.I)

            if len(csvRow) == 21:
                csv.writerow(self._csvPad(csvRow))
                csvRow = [group]

        if len(csvRow) > 1:
            csv.writerow(self._csvPad(csvRow))

    def _writeGroupL(self, csv, nodeModels):
        group = "L"
        csvRow = [group]

        for node in nodeModels:
            if node.boundary.getData() == "Constant Concentration (Dirichlet)":
                csvRow.append(node.I)

            if len(csvRow) == 21:
                csv.writerow(self._csvPad(csvRow))
                csvRow = [group]

        if len(csvRow) > 1:
            csv.writerow(self._csvPad(csvRow))

    # really need to specifiy the correct indices for element incidence
    def _writeGroupP(self, csv, elementModels, mixedBCModels):
        group = "P"
        csvRow = [group]

        def isMixed(incidenceIndex):
            node = list(filter(lambda n: str(n.nodeID) == str(element.incidences[incidenceIndex]), mixedBCModels))
            if not len(node):
                return False
            return True

        for element in elementModels:
            elementNum = element.elementNumber
            kf = 0

            if isMixed(0) and isMixed(1):
                kf = 1
            elif isMixed(1) and isMixed(2):
                kf = 2
            elif isMixed(2) and isMixed(3):
                kf = 3
            elif isMixed(3) and isMixed(0):
                kf = 4

            if kf != 0:
                csvRow.append(elementNum)
                csvRow.append(kf)

                if len(csvRow) == 9:
                    csv.writerow(self._csvPad(csvRow))
                    csvRow = [group]
        
        if len(csvRow) > 1:
            csv.writerow(self._csvPad(csvRow))


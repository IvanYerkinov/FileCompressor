# ARCHIVED CODE
# DO NOT USE

class Unpacker():
    def __init__(self, fileName):
        self.fileName = fileName
        self.binaryDict = {}
        self.first = 0

        self._initDict()

    def _decimalToBinary(self, n):
        return "{0:b}".format(int(n))

    def _byteToList(self, bit):
        for i in bit:
            y = self._decimalToBinary(i)
            y = list(y)
            while len(y) < 8:
                y.insert(0, '0')
            return y

    def _sectionToDict(self, byteList):
        for i in range(0, len(byteList)):
            if self.binaryDict[i][-1] == [0, 0]:
                self.binaryDict[i][-1] = [byteList[i], 1]
            elif self.binaryDict[i][-1][0] == byteList[i]:
                self.binaryDict[i][-1][1] += 1
            else:
                self.binaryDict[i].append([byteList[i], 1])

    def _initDict(self):
        for i in range(0, 8):
            self.binaryDict[i] = [[0, 0]]

    def read_binary(self):
        with open(self.fileName, "rb") as f:
            while True:
                byte = f.read(1)
                if byte == b'':
                    print(self.binaryDict)
                    return
                else:
                    y = self._byteToList(byte)

                print(y)

                self._sectionToDict(y)

    def printDict(self):
        totalamount = 0
        for i in range(0, 7):
            for y in self.binaryDict[i]:
                # print(y[0], end="")
                print(y[1], end=" ")
                totalamount += y[1]
        print(totalamount / 7)

    def writeDict(self, filename):
        with open(filename, 'w') as f:
            for i in range(0, 8):
                for y in self.binaryDict[i]:
                    test = self.compressDict(self.binaryDict[i])

                    for l in test:
                        for ll in l:
                            f.write(str(ll))
                    for l in test:
                        for ll in l:
                            print(ll, end=" ")
                    # if i == 0:
                    #     f.write(str(y[0]))
                    # f.write(str(y[1]))
    def writeDictBinary(self, filename):
        with open(filename, 'wb') as f:
            for i in range(0, 8):
                for y in self.binaryDict[i]:
                    test = self.compressDict(self.binaryDict[i])
                    print("\n")
                    for l in test:
                        for ll in l:
                            f.write(int(ll).to_bytes(2, "little"))
                    for l in test:
                        for ll in l:
                            print(ll, end=" ")

    def compressDict(self, dic):
        returnList = []
        if self.first == 0:
            x = dic.pop(0)
            a = 'a'
            if x[0] == '1':
                a = 'b'
            returnList.append([a])
            self.first = 0
        # Data structure = [i number of bits, number of loops]
        while len(dic) != 0:
            x = self._grabNext(dic)
            for i in x:
                dic.pop(0)
            if len(x) > 1 and x[0] == 1:
                x = ["i" + str(len(x))]
            # print(x, end=" ")
            returnList.append(x)
        return returnList

    def _grabNext(self, dic):
        x = dic[0]
        returnvalue = []
        returnvalue.append(x[1])
        for i in range(1, len(dic)-1):
            if x[1] == dic[i][1]:
                returnvalue.append(x[1])
            else:
                return returnvalue
        return returnvalue


un = Unpacker("test.txt")
un.read_binary()
un.printDict()
un.writeDict("test2.txt")

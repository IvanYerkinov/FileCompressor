import sys


class node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''

        pass


class Fileworker():
    def __init__(self, filename):
        self.filename = filename
        self.letterdic = {}
        self.decode = {}

    def readFile(self):
        with open(self.filename, "r") as f:
            x = f.read(1).lower()
            while x != "":
                if x == "1":
                    x = "B"
                if x == "0":
                    x = "A"
                print(x, end="")
                if x in self.letterdic:
                    self.letterdic[x] += 1
                else:
                    self.letterdic[x] = 1
                x = f.read(1).lower()
            print(self.letterdic)


            return self._split()

    def _split(self):
        temp = []
        retlistletter = []
        retlistnumber = []
        for i in self.letterdic:
            temp.append([i, self.letterdic[i]])

        for y in range(1, len(temp)):
            key = temp[y][1]
            place = temp[y]
            j = y-1

            while j >= 0 and key < temp[j][1]:
                temp[j + 1] = temp[j]
                j -= 1
            temp[j + 1] = place

        print(temp)

        for i in temp:
            retlistletter.append(i[0])
            retlistnumber.append(i[1])

        print(retlistletter)
        print(retlistnumber)
        return retlistletter, retlistnumber

    def _printNodes(self, node, val=''):
        newVal = val + str(node.huff)
        if(node.left):
            self._printNodes(node.left, newVal)
        if(node.right):
            self._printNodes(node.right, newVal)

        if(not node.left and not node.right):
            print(f"{node.symbol} -> {newVal}")

    def _makeDecode(self, node, val=''):
        newVal = val+str(node.huff)

        if(not node.left and not node.right):
            self.decode[node.symbol] = str(newVal)

        if(node.left):
            self._makeDecode(node.left, newVal)
        if(node.right):
            self._makeDecode(node.right, newVal)

    def hoffmanEncode(self, letterlist, numberlist):
        nodes = []

        for x in range(len(letterlist)):
            nodes.append(node(numberlist[x], letterlist[x]))

        while len(nodes) > 1:
            left = nodes[0]
            right = nodes[1]

            left.huff = 0
            right.huff = 1

            newNode = node(left.freq+right.freq, left.symbol+right.symbol, left, right)

            nodes.remove(left)
            nodes.remove(right)
            nodes.append(newNode)

        self._makeDecode(nodes[0])
        self._printNodes(nodes[0])
        print(self.decode)
        pass

    def prepareExport(self):
        encodedString = ""
        decodeTable = ""
        with open(self.filename, "r") as f:
            x = f.read(1).lower()
            while x != "":
                if x == "1":
                    x = "B"
                if x == "0":
                    x = "A"
                print(x, end="")
                encodedString += self.decode[x]
                x = f.read(1).lower()
        print(encodedString)
        print(len(encodedString))

        for i in self.decode.items():
            decodeTable += i[0] + i[1]
        print(decodeTable)

        return encodedString, decodeTable

        pass

    def imp(self, strin, dec):
        check = ""
        ret = ""
        for i in strin:
            check += i
            if check in dec.values():
                for y in dec.items():
                    if y[1] == check:
                        if y[0] == "B":
                            y = ("1", y[1])
                        if y[0] == "A":
                            y = ("0", y[1])
                        ret += y[0]
                check = ""
        # print(ret)
        # print(len(ret) * 8)
        return ret

    def buildDecode(self, decstring):
        codeTable = {}
        currKey = ""
        decstring = list(decstring)
        while len(decstring) > 0:
            x = decstring.pop(0)
            if x != "0" and x != "1":
                codeTable[x] = ""
                currKey = x
            else:
                codeTable[currKey] += x

        print(codeTable)
        return codeTable

    def export(self, encodedString, decodeTable):
        fileName = self.filename.split(".")
        byteStr = ""
        with open(fileName[0] + ".txt", "wb") as f:
            for i in encodedString:
                if len(byteStr) < 8:
                    byteStr += i
                if len(byteStr) == 8:
                    # print(byteStr)
                    f.write(int(byteStr, 2).to_bytes(1, "little"))
                    byteStr = ""
            while len(byteStr) > 0 and len(byteStr) < 8:
                    byteStr += "0"
            # print(byteStr)
            f.write(int(byteStr, 2).to_bytes(1, "little"))

        with open(fileName[0] + ".dec", "w") as f:
            f.write(decodeTable)

    def _decimalToBinary(self, n):
        return "{0:b}".format(int(n))

    def _byteToList(self, bit):
        for i in bit:
            y = self._decimalToBinary(i)
            y = list(y)
            while len(y) < 8:
                y.insert(0, '0')
            return y

    def loadCode(self, filename):
        binarystring = ""
        with open(filename, "rb") as f:
            b = f.read(1)
            while b != b"":
                b = self._byteToList(b)
                for i in b:
                    binarystring += i
                b = f.read(1)
        return binarystring

    def loadDec(self, filename):
        decode = ""
        with open(filename, "r") as f:
            decode = f.read()
        return self.buildDecode(decode)

    def writeDecode(self, str):
        with open(self.filename, "w") as f:
            f.write(str)

    def encodeFile(self):
        x, y = self.readFile()
        self.hoffmanEncode(x, y)
        str, dec = self.prepareExport()
        self.export(str, dec)

    def decodeFile(self):
        file = self.filename.split(".")
        a = self.loadCode(file[0] + ".txt")
        b = self.loadDec(file[0] + ".dec")
        self.writeDecode(self.imp(a, b))


if __name__ == "__main__":

    if len(sys.argv) == 3:
        un = Fileworker(sys.argv[2])
        if sys.argv[1] == "-e":
            un.encodeFile()
        elif sys.argv[1] == "-d":
            un.decodeFile()
    else:
        print("Please enter the correct amount of command line variables; -e/-d, filename")

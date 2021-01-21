import numpy as np

from dedop.model.acdc_data import NonFitParams

class UnitTestHelper():
    def __init__(self):
        pass

    # --------------------------- TESTS -------------------------------------
    #PRE: All arrays have the same size
    def testArray2D(self,result,expected,err, verbose = False) -> int:
        nFails = 0
        for i in range(0,(result.shape[0])):
            for j in range(0, (result.shape[1])):
                if (expected[i,j] == 0 and result[i,j] != expected[i,j]):
                    if verbose:
                        print(str(result[i,j])+" - "+str(expected[i,j]))
                    nFails += 1
                elif(expected[i,j] != 0 and np.abs((expected[i,j] - result[i,j])/expected[i,j]) > err):
                    if verbose:
                        print(str(result[i,j])+" - "+str(expected[i,j]))
                    nFails += 1
        return nFails

    #PRE: All arrays have the same size
    def testArray1D(self,result,expected,err, verbose = False) -> int:
        nFails = 0
        for i in range(0,(result.shape[0])):
            if (expected[i] == 0 and result[i] != expected[i]):
                if verbose:
                        print(str(result[i])+" - "+str(expected[i]))
                nFails += 1
            elif(expected[i] != 0 and np.abs((expected[i] - result[i])/expected[i]) > err):
                if verbose:
                        print(str(result[i])+" - "+str(expected[i]))
                nFails += 1
        return nFails

    def assertTestArray2D(self,result,expected,err,v = False) -> bool:
        return self.testArray2D(result,expected,err,v) == 0

    def assertTestArray1D(self,result,expected,err,v = False) -> bool:
        return self.testArray1D(result,expected,err,v) == 0

    def assertTestDouble(self,result,expected,err,v = False) -> bool:
        test = np.abs((expected - result)/expected) <= err
        if v and not test:
            print(result,"-",expected)
        return test


    # --------------------------- READS -------------------------------------
    def readArray2D(self, path, shape) -> np.array:
        file = open(path)
        array = np.empty(shape)
        i = 0
        for line in file.read().splitlines():
            line = np.array([np.double(x) for x in line.split(",")])
            array[i] = line
            i += 1
        file.close()
        return array

    def readArray1D(self, path) -> np.array:
        file = open(path)
        array = np.array([np.double(x) for x in file.readline().split(",")])
        file.close()
        return array

    def readNFP(self, path) -> NonFitParams:
        nf_p_data = open(path)
        nf_p = NonFitParams(
                Neff = np.int(nf_p_data.readline().split(" ")[1]),
                alphag_a = np.double(nf_p_data.readline().split(" ")[1]),
                alphag_r = np.double(nf_p_data.readline().split(" ")[1]),
                alphax = np.double(nf_p_data.readline().split(" ")[1]),
                alphay = np.double(nf_p_data.readline().split(" ")[1]),
                Lx = np.double(nf_p_data.readline().split(" ")[1]),
                Ly = np.double(nf_p_data.readline().split(" ")[1]),
                Lz = np.double(nf_p_data.readline().split(" ")[1]),
                h = np.double(nf_p_data.readline().split(" ")[1]),
                xp = np.double(nf_p_data.readline().split(" ")[1]),
                yp = np.double(nf_p_data.readline().split(" ")[1]),
                rou = np.double(nf_p_data.readline().split(" ")[1])
        )
        nf_p_data.close()

        return nf_p




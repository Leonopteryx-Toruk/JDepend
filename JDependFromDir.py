import os
import argparse
import subprocess
from os import listdir
from os.path import isfile, join, isdir

class JDependFromDir():

    def __init__(self):
        pass

    def correctFile(self, path):
        found = False
        toBeWritten = ""
        with open(path, mode="r") as joutput:
            for line in joutput:
                if line.startswith("Name; Class Count; Abstract Class Count; Ca; Ce; A; I; D; V"):
                    found = True
                if found:
                    toBeWritten += line
        with open(path, mode='w') as joutput:
            joutput.writelines(toBeWritten)

    def correctFiles(self, folderPath):
        onlyfiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
        for file in onlyfiles:
            pathFile = folderPath + "\\" + file
            self.correctFile(pathFile)

    def modifyFileName(self, fileName, numbers, h):
        fileNameModified = ""
        i = 0
        j = 0
        while i < len(fileName):
            digit = ""
            if str.isdigit(fileName[i]):
                j = j + 1
                while i < len(fileName) and str.isdigit(fileName[i]):
                    digit = digit + fileName[i]
                    i = i + 1
                k = 0
                lengthDigit = len(digit)
                while k < (numbers[j - 1] - lengthDigit):
                    digit = "0" + digit
                    k = k + 1
                fileNameModified += digit
                if i >= len(fileName) and j < len(numbers):
                    k = 0
                    while k < len(numbers) - j:
                        bestSeparator = sorted(h.items(), key=lambda(k,v):(v,k), reverse=True)
                        #print bestSeparator[0][0]
                        fileNameModified += bestSeparator[0][0] + "0"
                        k1 = 1
                        while k1 < numbers[k + j]:
                            fileNameModified += "0"
                            k1 += 1
                        k = k + 1
            else:
                fileNameModified += fileName[i]
                i = i + 1
        return fileNameModified

    def test(self):
        onlydirs = ["log4j-1_7", "log4j-3", "log4j-1"]
        numbers = []
        h = dict()
        for dir in onlydirs:
            i = 0
            j = 0
            while i < len(dir):
                if(str.isdigit(dir[i])):
                    j = j + 1
                    if j > len(numbers):
                        numbers.append(0)
                    digitLength = 0
                    separator = ""
                    while i < len(dir) and  str.isdigit(dir[i]):
                        digitLength += 1
                        i = i + 1
                    if i < len(dir) and str.isdigit(dir[i+1]) and not str.isalpha(dir[i]):
                        if dir[i] in h:
                            h[dir[i]] = h[dir[i]] + 1
                        else:
                            h[dir[i]] = 1
                    if numbers[j - 1] < digitLength:
                        numbers[j - 1] = digitLength
                else:
                    i = i + 1
        print numbers
        for dir in onlydirs:
            print self.modifyFileName(dir, numbers, h)

    def setClassPath(self, pathVersions, pathOutput, classpath):
        subprocess.call(["echo", "Hello word"], shell=True)
        #subprocess.call(["set", "CLASSPATH=%CLASSPATH%;C:\Program Files (x86)\jdepend-2.9.1\lib\jdepend-2.9.1.jar"], shell=True)
        #os.system("set CLASSPATH=%CLASSPATH%;C:\Program Files (x86)\jdepend-2.9.1\lib\jdepend-2.9.1.jar")
        classpath = "\"" + classpath + "\""
        onlydirs = [f for f in listdir(pathVersions) if isdir(join(pathVersions, f))]
        numbers = []
        h = dict()
        for dir in onlydirs:
            i = 0
            j = 0
            while i < len(dir):
                if(str.isdigit(dir[i])):
                    j = j + 1
                    if j > len(numbers):
                        numbers.append(0)
                    digitLength = 0
                    separator = ""
                    while i < len(dir) and  str.isdigit(dir[i]):
                        digitLength += 1
                        i = i + 1
                    if i < len(dir) and not str.isalpha(dir[i]):
                        if dir[i] in h:
                            h[dir[i]] = h[dir[i]] + 1
                        else:
                            h[dir[i]] = 1
                    if numbers[j - 1] < digitLength:
                        numbers[j - 1] = digitLength
                else:
                    i = i + 1
        for file in onlydirs:
            pathFile = "\""+pathVersions + "\\" + file+"\""
            pathV = "\""+pathOutput + "\\" + self.modifyFileName(file, numbers, h) + ".txt"+"\""
            print pathV
            print pathFile
            os.system("java -cp " + classpath + " jdepend.textui.JDepend -file " + pathV + " " + pathFile)

if __name__ == '__main__':
    #fc = JDependFromDir()
    #fc.test()
    #exit()
    print "starting..."
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="the path of the versions of the project")
    parser.add_argument("-o", "--output", help="the path of the output of jdepend")
    parser.add_argument("-cp", "--classpath", help="the path of the classpath of jdepend",
                        default="jdepend-2.9.1.jar")
    args = parser.parse_args()
    if not args.input and not args.output:
        print "insert input or output"
        exit()
    if args.output and not args.input:
        print "insert input"
        exit()
    #if args.input and args.output and not args.classpath:
    #    print "insert classpath"
    #    exit()
    f = JDependFromDir()
    print args.classpath
    if args.input:
        f.setClassPath(args.input, args.output, args.classpath)
    if args.output:
        f.correctFiles(args.output)
    print "finished"

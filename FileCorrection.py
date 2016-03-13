import os
import argparse
import subprocess
from os import listdir
from os.path import isfile, join, isdir

class FileCorrection():

    def __init__(self):
        pass

    def correctFile(self, path):
        found = False
        toBeWritten = ""
        with open(path, mode="r") as joutput:
            for line in joutput:
                if line.startswith("Name, Class Count, Abstract Class Count, Ca, Ce, A, I, D, V:"):
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

    def setClassPath(self, pathVersions, pathOutput, classpath):
        subprocess.call(["echo", "Hello word"], shell=True)
        #subprocess.call(["set", "CLASSPATH=%CLASSPATH%;C:\Program Files (x86)\jdepend-2.9.1\lib\jdepend-2.9.1.jar"], shell=True)
        #os.system("set CLASSPATH=%CLASSPATH%;C:\Program Files (x86)\jdepend-2.9.1\lib\jdepend-2.9.1.jar")
        classpath = "\"" + classpath + "\""
        onlydirs = [f for f in listdir(pathVersions) if isdir(join(pathVersions, f))]
        for file in onlydirs:
            pathFile = "\""+pathVersions + "\\" + file+"\""
            pathV = "\""+pathOutput + "\\" + file + ".txt"+"\""
            print pathV
            print pathFile
            os.system("java -cp " + classpath + " jdepend.textui.JDepend -file " + pathV + " " + pathFile)

if __name__ == '__main__':
    print "starting..."
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="the path of the versions of the project")
    parser.add_argument("-o", "--output", help="the path of the output of jdepend")
    parser.add_argument("-cp", "--classpath", help="the path of the classpath of jdepend",
                        default="C:\Program Files (x86)\jdepend-2.9.1\lib\jdepend-2.9.1.jar")
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
    f = FileCorrection()
    print args.classpath
    if args.input:
        f.setClassPath(args.input, args.output, args.classpath)
    if args.output:
        f.correctFiles(args.output)
    print "finished"

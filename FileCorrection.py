import os
import argparse

from os.path import isfile, join

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
        from os import listdir
        onlyfiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
        for file in onlyfiles:
            pathFile = folderPath + "\\" + file
            self.correctFile(pathFile)

if __name__ == '__main__':
    print "starting..."
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="the path of the output of jdepend")
    args = parser.parse_args()
    f = FileCorrection()
    f.correctFiles(args.path)
    print "finished"

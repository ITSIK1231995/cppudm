import os

def cleanUpErrinjModeConfFile(line):
    return line.rstrip("\n").replace(";", "").replace('"', "").strip().split("=")

def convertToString(line):
    return str(line)

def getFilePath(legacyModeConfigFilesDirectory, filename):
    return os.path.join(legacyModeConfigFilesDirectory, filename)

def getRootDirectory(relativePath):
    return r'..\\' + relativePath

def findFile(fileNameFromUser ="../"):
    path = "../" + fileNameFromUser
    return path if os.path.isfile(path) else ''

def findDir(dirNameFromUser):
    path = "../" + dirNameFromUser
    return path if os.path.isdir(path) else ''
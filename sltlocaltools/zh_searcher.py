#!/usr/bin/python
# -*- coding:UTF-8 -*-

# extract Chinese from folder

import os
import re
import codecs
from optparse import OptionParser
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class DataModel:
    def __init__(self):
        self.fileName = ''
        self.res = []

    def __init__(self,fileName,res=[]):
        self.fileName = fileName
        self.res = res

    def isEqual(self,other):
        if self.fileName != other.fileName:
            return 0
        if self.res.sort() != other.res.sort():
            return 0
        return 1

    def __str__(self):
        content = '/*\n'+self.fileName + '\n*/\n'
        for item in self.res:
            content = content + '"'+item + '"="' + item + '";\n'
        return content

class Searcher:
    def __init__(self):
        self.filePath = ''
        self.outPath = ''
        self.content = ''

    def execute(self):
        res = []
        content = ''
        if os.path.isfile(self.filePath):
            tmpArr = self.searchContent(self.filePath)
            fileName = os.path.split(self.filePath)[1]
            dataModel = DataModel(fileName,tmpArr)
            if len(tmpArr) > 0:
                res.append(dataModel)
            return res
        if os.path.isdir(self.filePath):
            files = self.searchFiles()
            for item in files:
                tmpArr = self.searchContent(item)
                if len(tmpArr) == 0:
                    continue
                fileName = os.path.split(item)[1]
                dataModel = DataModel(fileName, tmpArr)
                res.append(dataModel)
                content += str(dataModel)
        self.content = content
        return res;

    def searchFiles(self):
        res = []
        for root, dirs, files in os.walk(self.filePath):
            for fileObj in files:
                filePath = os.path.join(root, fileObj)
                filePath = os.path.realpath(filePath)
                ext = os.path.splitext(filePath)[1]
                if ext in ['.h','.m','.mm'] and os.path.isfile(filePath):
                    res.append(filePath)
        return res

    def searchContent(self,filePath=''):
        res = []
        with open(filePath) as file:
            for line in file.readlines():
                line = line.decode("utf-8")
                regrex = ur'@"[^"]*[\u4E00-\u9FA5]+[^"\n]*?\"'
                result = re.findall(regrex, line, re.I | re.M | re.S)
                for item in result:
                    tmpStr = item.encode('utf-8')
                    tmpStr = tmpStr[2:-1]
                    res.append(tmpStr)
        tmpSet = set(res)
        res = list(tmpSet)
        return res

    def saveToFile(self):
        f = codecs.open(self.outPath, 'w', 'utf-8')
        print self.content
        f.write(self.content)
        f.close()

if __name__ == '__main__':
    parser =  OptionParser(usage="%prog [-f]", version="%prog 1.0")
    parser.add_option("-f", "--file",action="store", dest="filePath",
                      help="search Chinese in this file or folder")

    parser.add_option("-o", "--out",action="store", dest="outPath",
                      help="save result to outPath")
    (options, args) = parser.parse_args()
    # get file path
    filePath = options.filePath
    outPath = options.outPath
    if filePath == None or outPath == None:
        parser.print_help()
        exit()

    searcher = Searcher()
    searcher.filePath = os.path.realpath(filePath)
    searcher.outPath = os.path.realpath(outPath)
    searcher.execute()
    searcher.saveToFile()
    print 'Done!'
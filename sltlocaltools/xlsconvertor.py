#!/usr/bin/python
# -*- coding:UTF-8 -*-

# convert strings to xls or convert xls to strings

import codecs
import re
import os
import sys
import xlwt
import xlrd
from optparse import OptionParser


reload(sys)
sys.setdefaultencoding('utf-8')

class DataModel:
    def __init__(self):
        self.entries = {} # {'en':'hello','zh-Hans':'你好'}
        self.langKey = '' # hello

    def addEntry(self,code,value):
        self.entries[code] = value

    def value(self,code):
        return self.entries.get(code)

    def isEqual(self,other):
        if other.langKey != self.langKey:
            print 'o:' + str(other)
            print 'my:' + str(self)
            print 'key not equal'
            return 0
        if len(self.entries) != len(other.entries):
            print 'count not equal'
            return 0
        for key in self.entries.keys():
            value = self.entries.get(key)
            valueOther = other.entries.get(key)
            if value != valueOther:
                print 'value not equal'
                return 0
        return 1

    def __str__(self):
        content = 'key:' + self.langKey + ' '
        for key in self.entries.keys():
            value = self.entries.get(key)
            content += key + ':' + value + '\n'
        return content

class StringsParser:
    def __init__(self):
        self.itemsDict = {}  # {key:dataModel}
        self.languageCodes = [] # 语言key zh-Hans,en等
        self.stringspaths = []
        self.dirPath = ''
        self.execelPath = ''
        self.name = ''
        self.stringsName = 'Localizable.strings'
    def parser(self):
        # 遍历lproj结尾的文件夹
        # 生成keys
        # 生成stringsmdodel
        if(os.path.exists(self.dirPath) == 0):
            return  None
        # 获取该目录下的所有文件或文件夹目录
        filePaths = self.findAllStrings()
        for itemFilePath in filePaths:
            code = os.path.basename(os.path.dirname(itemFilePath))
            code = code[:-6]
            self.languageCodes.append(code)
            pattern = re.compile(ur'".*"=".*";')
            for line in codecs.open(itemFilePath):
                if line.startswith('"') == 0:
                    continue
                arr = line.split('=')
                key = arr[0].strip()
                key = re.split(ur'"', key)[1]
                value = arr[1].strip()
                value = re.split(ur'"|;', value)[1]
                tmpDataModel = self.itemsDict.get(key)
                if tmpDataModel == None:
                    tmpDataModel = DataModel()
                    self.itemsDict[key] = tmpDataModel
                dataModel = tmpDataModel
                dataModel.langKey = key
                dataModel.addEntry(code,value)

    def findAllStrings(self):
        # 遍历lproj结尾的文件夹
        # 生成keys
        # 生成stringsmdodel
        if (os.path.exists(self.dirPath) == 0):
            return None
        # 获取该目录下的所有文件或文件夹目录
        files = os.listdir(self.dirPath)
        res = []
        for index, file in enumerate(files):
            # 得到该文件下所有目录的路径
            m = os.path.join(self.dirPath, file)
            if m.endswith('.lproj') == 0:
                continue
            if file.startswith('Base'):
                continue
            # 判断该路径下是否是文件夹
            if (os.path.isdir(m) == 0):
                continue;
            h = os.path.split(m)[1]
            key = str(h).split('.')[0]
            self.languageCodes.append(str(h).split('.')[0])
            stringsPath = os.path.join(m, self.stringsName)
            res.append(stringsPath)
        return res

    def writeToExecel(self):
        # 获取book,获取表 第一行表头,第二行
        wb = xlwt.Workbook(encoding='utf-8');
        ws = wb.add_sheet(self.name);
        # 第一行
        colNames = ['keyName']
        tmp = list(set(self.languageCodes))
        colNames.extend(tmp)
        for index,item in enumerate(colNames):
            ws.write(0, index, item)
            row = 1
            col = index
            for subIndex,languageKey in enumerate(self.itemsDict.keys()):
                if col == 0:
                    ws.write(row,col,languageKey)
                else:
                    dataModel = self.itemsDict[languageKey]
                    value = dataModel.value(item)
                    ws.write(row, col, value)
                row += 1;

        wb.save(self.execelPath);

class XlsParser:
    def __init__(self):
        self.xlsPath = ''
        self.stringsDir = ''
        self.itemsDict = {} # {key:DataModel}
        self.languageCodes = []
    def parserXls(self):
        if os.path.exists(self.xlsPath) == 0:
            print self.xlsPath + ' not exist!'
            return
        # first line
        data = xlrd.open_workbook(self.xlsPath)
        table = data.sheet_by_index(0)
        if table == None:
            print 'Sheet1 not exist!'
            return

        nrows = table.nrows
        ncols = table.ncols
        for i in range(nrows):
            if i == 0:
                self.languageCodes = table.row_values(0)
            else:
                rowVals = table.row_values(i)
                langKey = ''
                for j in range(ncols):
                    if j == 0:
                        langKey = table.cell(i,0).value
                    else:
                        code = self.languageCodes[j]
                        text = table.cell(i,j).value
                        tmpDataModel = self.itemsDict.get(langKey)
                        if tmpDataModel == None:
                            tmpDataModel = DataModel()
                            tmpDataModel.langKey = langKey
                            self.itemsDict[langKey] = tmpDataModel
                        tmpDataModel.addEntry(code,text)
        del self.languageCodes[0]

    def writeToStringsFile(self):
        allCodes = self.languageCodes
        for code in allCodes:
            # filePath
            dirPath = os.path.join(self.stringsDir,code + '.lproj')
            if os.path.exists(dirPath) == 0:
                os.mkdir(dirPath)
            stringPath = os.path.join(dirPath,'Localizable.strings')
            content = ''
            for langKey in self.itemsDict.keys():
                dataModel = self.itemsDict[langKey]
                line = '"' + langKey + '"="' +  dataModel.value(code) + '";\n'
                content += line
            # save
            f = codecs.open(stringPath, 'w', 'utf-8')
            f.write(content)
            f.close()



class Convertor:
    def __init__(self):
        self.xlsPath = ''
        self.stringsDir = ''

    def convertStringsToXls(self):
        stringsParser = StringsParser()
        stringsParser.dirPath = self.stringsDir
        stringsParser.name = 'Sheet1'
        stringsParser.execelPath = self.xlsPath
        stringsParser.parser()
        stringsParser.writeToExecel()

    def convertXlsTostrings(self):
        parser = XlsParser()
        parser.stringsDir = self.stringsDir
        parser.xlsPath = self.xlsPath
        parser.parserXls()
        parser.writeToStringsFile()

if __name__ == '__main__':
    parser = OptionParser(usage="%prog [-f]", version="%prog 1.0")
    parser.add_option("-t", "--type", action="store", dest="type",
                      help="1 means convert to xls,2 means convert to strings")
    parser.add_option("-s", "--strdir", action="store", dest="strPath",
                      help="strings'dir path")
    parser.add_option("-x", "--xlspath", action="store", dest="xlspath",
                      help="xls file path")
    (options, args) = parser.parse_args()

    type = options.type
    strPath = os.path.realpath(options.strPath)
    xlsPath = os.path.realpath(options.xlspath)
    convertor = Convertor()
    convertor.stringsDir = strPath
    convertor.xlsPath = xlsPath
    if type == '1': # convert to xls
        convertor.convertStringsToXls()
    elif type == '2':
        convertor.convertXlsTostrings()
    print 'Done!'


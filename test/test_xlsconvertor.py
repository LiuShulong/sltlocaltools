#!/usr/bin/python
# -*- coding:UTF-8 -*-

import sys
import os
import unittest
import xlrd
import shutil
import codecs

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)

from sltlocaltools import xlsconvertor

xlsPath = os.path.join(parent_path, 'test/fixtures/demo/res.xls')

class XlsConvertorTestCase(unittest.TestCase):

    def setUp(self):
        if os.path.exists(xlsPath):
            os.remove(xlsPath)

    def test_dataModel(self):
        dataModel = xlsconvertor.DataModel()
        languagekey = 'hello'
        dataModel.langKey = languagekey
        dataModel.addEntry('en','hello')
        dataModel.addEntry('zh-Hans','你好')
        self.assertEqual(dataModel.value('en'),'hello')
        self.assertEqual(dataModel.value('zh-Hans'),'你好')

    def test_findAllStrings(self):
        dirPath = os.path.join(parent_path,'test/fixtures/strings')
        stringParser = xlsconvertor.StringsParser()
        stringParser.dirPath = dirPath
        arr = stringParser.findAllStrings()
        arr.sort()
        expect = [os.path.join(dirPath,'en.lproj/Localizable.strings'),os.path.join(dirPath,'zh-Hans.lproj/Localizable.strings')]
        expect.sort()
        self.assertIsNotNone(arr)
        self.assertEqual(expect,arr)

    def test_parser(self):
        stringsParser = xlsconvertor.StringsParser()
        stringsParser.dirPath = os.path.join(parent_path,'test/fixtures/strings')
        stringsParser.parser()

        dataModel = xlsconvertor.DataModel()
        key1 = 'MJRefreshHeaderIdleText'
        dataModel.langKey = key1
        dataModel.addEntry('zh-Hans','下拉可以刷新')
        dataModel.addEntry('en','Pull down to refresh')
        expectDict = {}
        expectDict[key1] = dataModel


        dataModel2 = xlsconvertor.DataModel()
        key2 = 'MJRefreshHeaderPullingText'
        dataModel2.langKey = key2
        dataModel2.addEntry('zh-Hans','松开立即刷新')
        dataModel2.addEntry('en','Release to refresh')
        expectDict[key2] = dataModel2

        self.assertEqual(len(stringsParser.itemsDict),2)
        resModel1 = stringsParser.itemsDict[key1]
        self.assertTrue(dataModel.isEqual(resModel1))
        resModel2 = stringsParser.itemsDict[key2]
        self.assertTrue(dataModel2.isEqual(resModel2))

    def test_writeToXls(self):
        stringsParser = xlsconvertor.StringsParser()
        stringsParser.dirPath =  os.path.join(parent_path,'test/fixtures/strings')
        stringsParser.name = 'test'
        stringsParser.execelPath = xlsPath
        stringsParser.parser()
        stringsParser.writeToExecel()

        data = xlrd.open_workbook(xlsPath)
        table = data.sheet_by_name('test')  # 通过名称获取
        self.assertIsNotNone(table)
        row0 = table.row_values(0)
        expectRow0 = [u'keyName', u'zh-Hans', u'en']
        self.assertEqual(row0,expectRow0)

        row1 = table.row_values(1)
        row1.sort()
        expectRow1 = [u'MJRefreshHeaderIdleText', u'下拉可以刷新', u'Pull down to refresh']
        expectRow1.sort()
        self.assertEqual(row1,expectRow1)

        row2 = table.row_values(2)
        row2.sort()
        expectRow2 = [u'MJRefreshHeaderPullingText', u'Release to refresh', u'松开立即刷新']
        expectRow2.sort()
        self.assertEqual(row2, expectRow2)

    def testParserXlsToStrs(self):
        parser = xlsconvertor.XlsParser()
        parser.xlsPath = os.path.join(parent_path,'test/fixtures/xls/res.xls')
        parser.parserXls()

        dataModel = xlsconvertor.DataModel()
        key1 = 'MJRefreshHeaderIdleText'
        dataModel.langKey = key1
        dataModel.addEntry('zh-Hans', '下拉可以刷新')
        dataModel.addEntry('en', 'Pull down to refresh')
        expectDict = {}
        expectDict[key1] = dataModel

        dataModel2 = xlsconvertor.DataModel()
        key2 = 'MJRefreshHeaderPullingText'
        dataModel2.langKey = key2
        dataModel2.addEntry('zh-Hans', '松开立即刷新')
        dataModel2.addEntry('en', 'Release to refresh')
        expectDict[key2] = dataModel2


        self.assertEqual(len(parser.itemsDict),2)
        resModel1 = parser.itemsDict[key1]
        self.assertTrue(dataModel.isEqual(resModel1))
        resModel2 = parser.itemsDict[key2]
        self.assertTrue(dataModel2.isEqual(resModel2))

    def testParserXlsToFile(self):
        testPath = os.path.join(parent_path, 'test/fixtures/test')
        if os.path.exists(testPath):
            shutil.rmtree(testPath)
        os.mkdir(testPath)

        converTor = xlsconvertor.Convertor()
        converTor.xlsPath = os.path.join(parent_path,'test/fixtures/xls/res.xls')
        converTor.stringsDir = testPath
        converTor.convertXlsTostrings()

        zhContent = '"MJRefreshHeaderIdleText"="下拉可以刷新";\n"MJRefreshHeaderPullingText"="松开立即刷新";\n'
        enContent = '"MJRefreshHeaderIdleText"="Pull down to refresh";\n"MJRefreshHeaderPullingText"="Release to refresh";\n'

        path1 = os.path.join(testPath,'en.lproj/Localizable.strings')
        path2 = os.path.join(testPath,'zh-Hans.lproj/Localizable.strings')

        content1 = ''
        file1 = codecs.open(path1, 'r', 'utf-8')
        content1 =  content1.join(file1.readlines())
        file1.close()
        self.assertEqual(enContent,content1)
        content2 = ''
        file2 = codecs.open(path2, 'r', 'utf-8')
        content2 =  content2.join(file2.readlines())
        file2.close()
        self.assertEqual(zhContent,content2)

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python
# -*- coding:UTF-8 -*-

import sys
import os
import unittest

parent_path = os.path.dirname(sys.path[0])
print "path:" + parent_path
if parent_path not in sys.path:
    sys.path.append(parent_path)

from sltlocaltools import zh_searcher

class SearcherTestCase(unittest.TestCase):
    def test_searchcontent(self):
        searcher = zh_searcher.Searcher()
        filePath = os.path.join(parent_path,'test/fixtures/find/ViewController.m')
        searcher.filePath = filePath
        res = searcher.searchContent(filePath)
        res.sort()
        self.assertIsNotNone(res)
        expect = ['龙defin','确定','字段1','ddd字段2dd']
        expect.sort()
        self.assertEqual(expect,res)

    def test_searchfiles(self):
        searcher = zh_searcher.Searcher()
        filePath = os.path.join(parent_path,'test')
        searcher.filePath = filePath
        res = searcher.searchFiles()
        res.sort()
        self.assertIsNotNone(res)
        tmpArr = ['fixtures/find/test.mm','fixtures/find/ViewController.m','fixtures/find/ViewController.h']
        expect = []
        for item in tmpArr:
            tmpPath = os.path.join(filePath,item)
            expect.append(tmpPath)
        expect.sort()
        self.assertEqual(expect,res)

    def test_exectute(self):
        searcher = zh_searcher.Searcher()
        filePath = os.path.join(parent_path, 'test/fixtures/find')
        searcher.filePath = filePath
        res = searcher.execute()
        model1 = zh_searcher.DataModel('ViewController.h',['我是接口d'])
        model2 = zh_searcher.DataModel('ViewController.m',['确定', '字段1', 'ddd字段2dd']);
        self.assertTrue(model1.isEqual(res[0]))
        self.assertTrue(model2.isEqual(res[1]))

if __name__ == '__main__':
    unittest.main()

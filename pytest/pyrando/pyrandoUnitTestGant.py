#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 3 sept. 2010

@author: mikfer

high level tests 
GANT 


'''
import unittest
import ConfigParser, os
from lib import gantlib 


class Test(unittest.TestCase):


    def setUp(self):
        project_name = 'pyrando'
        project_utdatadir = 'utdata'
        project_path = os.getcwd()[0:os.getcwd().find(project_name) + len(project_name)]
        self.__ut1c = ConfigParser.RawConfigParser()
        self.__ut1c.readfp(open(project_path + os.sep + project_utdatadir + os.sep + 'ut1.cfg'))
    
    def tearDown(self):
        pass


    def testGant(self):
        # Creer une instance d'Album  4
        gantlib.startGantMaster(self.__ut1c.get('gant', 'path'))
                   

        

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateRando']
    unittest.main()

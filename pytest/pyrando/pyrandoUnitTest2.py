#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 3 sept. 2010

@author: mikfer

high level tests 

'''
import unittest
from core.rando import Rando
import ConfigParser, os
from core.album import Album
import logging
import logging.config

logging.config.fileConfig(os.getcwd()[0:os.getcwd().find('pyrando') + len('pyrando')] 
                          + os.sep + 'src' + os.sep + 'logging.conf')
logger = logging.getLogger("test")

class Test(unittest.TestCase):


    def setUp(self):
        project_name = 'pyrando'
        project_utdatadir = 'utdata'
        project_path = os.getcwd()[0:os.getcwd().find(project_name) + len(project_name)]
        self.__ut1c = ConfigParser.RawConfigParser()
        self.__ut1c.readfp(open(project_path + os.sep + project_utdatadir + os.sep + 'ut1.cfg'))
    
    def tearDown(self):
        pass

 
    def xtestAlbumPicasaFriends(self):
        r = Rando(self.__ut1c.get('rando', 'shortname'))
        # Ajouter une instance de Gpx
        r.addGPX(self.__ut1c.get('gpx1', 'path'), \
                   self.__ut1c.get('gpx1', 'shortname'))
        # Creer une instance d'Album  sur un autre user picas web,
        # dans ce cas certaines infos ne sont pas accessibles...
        r.addAlbum(self.__ut1c.get('album1', 'path'), \
                   'pmihvr', \
                    '20100724 POinte du Midi (Aravis)', \
                   self.__ut1c.get('picasaweb', 'mailaddress'), \
                   self.__ut1c.get('picasaweb', 'password'), \
                   'hugues.villeger@free.fr')
        #
        r.geolocatePhotos('pmihvr')
        r.syncrhonizeAlbum('pmihvr')
        r.getInfoAlbum('pmihvr')
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateRando']
    unittest.main()

#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 3 sept. 2010

@author: mikfer

high level tests 
Album management
1 - test backup 
2 - test upload to picasa web


'''
import unittest
from core.rando import Rando
import ConfigParser, os, sys
import shelve
from core.kml import Kml
from core.album import Album
from core.kml import Kml
from core.gpx import Gpx
from core.hiker import Hiker
import logging
import logging.config

logging.config.fileConfig(os.getcwd()[0:os.getcwd().find('pyrando') + len('pyrando')] 
                          + os.sep + 'src' + os.sep + 'logging.conf')
logger = logging.getLogger("test")


class Test(unittest.TestCase):


    def setUp(self):
        logger.debug("setUp")   
        project_name = 'pyrando'
        project_utdatadir = 'utdata'
        project_path = os.getcwd()[0:os.getcwd().find(project_name) + len(project_name)]
        self.__ut1c = ConfigParser.RawConfigParser()
        self.__ut1c.readfp(open(project_path + os.sep + project_utdatadir + os.sep + 'ut1.cfg'))
        self.__dbpath = project_path + os.sep + project_utdatadir + os.sep + 'ut.dbm'
    
    def tearDown(self):
        pass


    def xtestAlbumCreation(self):
        # Creer une instance de hiker
        h = Hiker('hiker','hikerman',
                   self.__ut1c.get('picasaweb', 'mailaddress'),
                     self.__ut1c.get('picasaweb', 'user'),
                   self.__ut1c.get('picasaweb', 'password'))
        # Creer une instance d'Album  
        a = Album(self.__ut1c.get('album1', 'path'),
                   self.__ut1c.get('album1', 'shortname'),
                   self.__ut1c.get('album1', 'longname'),
                   h)
        a.listPhotos()
        plist = a.getPhotos()
        
    def xtestRandoCreation(self):
        # creer une instance de Rando r avec (nom rando)
        r = Rando(self.__ut1c.get('rando', 'shortname'))
        # Creer une instance de hiker
        h = Hiker('hiker','hikerman',
                   self.__ut1c.get('picasaweb', 'mailaddress'),
                     self.__ut1c.get('picasaweb', 'user'),
                   self.__ut1c.get('picasaweb', 'password'))
        # Creer une instance d'Album  
        r.addAlbum(self.__ut1c.get('album1', 'path'),
                   self.__ut1c.get('album1', 'shortname'),
                   self.__ut1c.get('album1', 'longname'),
                   h)

    def xtestShelveWriteDBM(self):
        # creer une instance de Rando r1 avec (nom rando)
        r1 = Rando(self.__ut1c.get('rando', 'shortname'))
        # Creer une instance de hiker
        h = Hiker('hiker','hikerman',
                   self.__ut1c.get('picasaweb', 'mailaddress'),
                     self.__ut1c.get('picasaweb', 'user'),
                   self.__ut1c.get('picasaweb', 'password'))
        # Creer une instance d'Album  
        r1.addAlbum(self.__ut1c.get('album1', 'path'),
                   self.__ut1c.get('album1', 'shortname'),
                   self.__ut1c.get('album1', 'longname'),
                   h)
        # Ajouter une instance de Gpx
        r1.addGPX(self.__ut1c.get('gpx1', 'path'), 
                   self.__ut1c.get('gpx1', 'shortname'))
        r1.getInfoAlbum()
        # geolocaliser les photos de l'album
        r1.geolocatePhotos() 
        r1.syncrhonizeAlbum()
        # creer une autre instance de Rando r2 avec (nom rando)
        r2 = Rando(self.__ut1c.get('rando2', 'shortname'))
        # Ajouter une instance d'Album  
        r2.addAlbum(self.__ut1c.get('album2', 'path'), 
                   self.__ut1c.get('album2', 'shortname'), 
                   self.__ut1c.get('album2', 'longname'), 
                   h)
        # Ajouter une instance de Gpx
        r2.addGPX(self.__ut1c.get('gpx2', 'path'), 
                   self.__ut1c.get('gpx2', 'shortname'))
        #
        #sys.setrecursionlimit(100000)
        logger.debug( str(r1.__dict__))
        logger.debug("rec limit=" +  str(sys.getrecursionlimit()))
        base = shelve.open(self.__dbpath)
        #base[r1.getName()] = {'info': [r1.getName(),r1.getName()],'rando': [r1]}
        #base[r2.getName()] = {'info': [r2.getName(),r2.getName()],'rando': [r2]}
        # constituer la clef rando
        rkey1 = r1.getFmtDate().split(' ')[0] + ';' + r1.getShortName() + ';' + r1.getLongName()
        base[rkey1] = r1
        rkey2 = r2.getFmtDate().split(' ')[0] + ';' + r2.getShortName() + ';' + r2.getLongName()
        base[rkey2] = r2
        for i in range(1, 10):
            rkeyi = r1.getFmtDate().split(' ')[0] + ';' + str(i) + ';' + r1.getShortName() + ';' + r1.getLongName()
            base[rkeyi] = r1
            
            
        
        base.close()
        
        
    def xtestShelveXReadDBM(self):
        base = shelve.open(self.__dbpath)
        list = base.keys()
        logger.debug( len(list))
        for k in list:
            logger.debug( "key=" + k)
            #r = base[k]['rando'][0]
            r = base[k]
            logger.debug(type(r))
            r.getShortName()
            r.getInfoAlbum()
        base.close()
        
    def xtestAlbumRestoreBackup(self):
        # Creer une instance de hiker
        h = Hiker('hiker','hikerman',
                   self.__ut1c.get('picasaweb', 'mailaddress'),
                     self.__ut1c.get('picasaweb', 'user'),
                   self.__ut1c.get('picasaweb', 'password'))
        # Creer une instance d'Album  
        a = Album(self.__ut1c.get('album1', 'path'),
                   self.__ut1c.get('album1', 'shortname'),
                   self.__ut1c.get('album1', 'longname'),
                   h)
        # backup de l'album dans sous rep .orig et renommage des photos
        a.backupAlbum()
        a.restoreAlbum()
        
    def xtestAlbumUpload(self):
        # Creer une instance de hiker
        h = Hiker('hiker','hikerman',
                   self.__ut1c.get('picasaweb', 'mailaddress'),
                     self.__ut1c.get('picasaweb', 'user'),
                   self.__ut1c.get('picasaweb', 'password'))
        # Creer une instance d'Album  
        a = Album(self.__ut1c.get('album1', 'path'),
                   self.__ut1c.get('album1', 'shortname'),
                   self.__ut1c.get('album1', 'longname'),
                   h)
        # backup de l'album dans sous rep .orig et renommage des photos
        a.uploadAlbumToPicasaWeb()
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateRando']
    unittest.main()

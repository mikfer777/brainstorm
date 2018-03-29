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
from core.gpx import Gpx
from core.hiker import Hiker
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

    def testGpxWaiPoints(self):
        # Creer  une instance de Gpx
        g = Gpx(self.__ut1c.get('gpx1', 'path'),
                   self.__ut1c.get('gpx1', 'shortname'))
        # get the waypoint list
        wptlist = g.getWayPoints()
        for w in wptlist:
            print w[0], w[1], w[2], w[3], w[4], w[5]
        
        
    def testPhotoGeolocation(self):
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
        # Ajouter une instance de Gpx
        r.addGPX(self.__ut1c.get('gpx1', 'path'),
                   self.__ut1c.get('gpx1', 'shortname'))
        # geolocaliser les photos de l'album
        r.geolocatePhotos() # ou r.geolocatePhotos('PMI','pmigpx') si n 


    def testKMLGeneration(self):
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
        # Ajouter une instance de Gpx
        r.addGPX(self.__ut1c.get('gpx1', 'path'),
                   self.__ut1c.get('gpx1', 'shortname'))
        # lire les infos du gpx
        r.getInfoGPX() # ou r.getInfoGPX('pmigpx') si n gpx
        # geolocaliser les photos de l'album
        r.geolocatePhotos() # ou r.geolocatePhotos('PMI','pmigpx') si n 
        #r.uploadAlbumToPicasaWeb()
        r.syncrhonizeAlbum()
        #creer le kml a partir du gpx
        r.createKML('pmikml')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateRando']
    unittest.main()

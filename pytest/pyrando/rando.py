#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os #@UnusedImport
import sys
from core.kml import Kml
from core.album import Album
from core.kml import Kml
from core.gpx import Gpx
from datetime import  timedelta, datetime
import time


try:
    from pytz import timezone
except ImportError:
    print u"""
    installer pytz pour utiliser ce programme
    A télecharger sur www.wxpython.org"""
    sys.exit(0)

import logging
logger = logging.getLogger("core.rando")
    
    
    
class Rando:
    """
    Classe Rando
    
    La classe rando est constituée de 1 a N Album, 1 a N Gpx, 1 a N Kml....
    """


    def __init__(self, shortname='myRando', longName='myLongRando', date=None, gauge=None):
        logger.debug("__init__")   
        self.__shortName = shortname
        self.__longName = longName
        self.__albums = []
        self.__gpxs = []
        self.__kmls = []
        if date == None:
            self.__date = datetime.now(timezone('Europe/Paris')) 
        else:
            self.__date = date
        self.__gauge = gauge

        
    def __getstate__(self):
        # http://www.dil.univ-mrs.fr/~garreta/PythonBBSG/docs/python-2.6.2-docs-html/library/pickle.html
        # remove the gauge from the object rando before serialization
        r = self.__dict__.copy() # copy the dict since we change it
        del r['_Rando__gauge']       # remove __doc entry
        return r
    
    def setGauge(self, gauge):
        self.__gauge = gauge
        for a in self.__albums: a.setGauge(self.__gauge)

    def getShortName(self):
        return self.__shortName

    def getLongName(self):
        return self.__longName

    def getFmtDate(self):
        fmt = "%Y-%m-%d %H:%M:%S %Z%z"
        return self.__date.strftime(fmt)
    
    def getDate(self):
        return self.__date

    
    def addAlbum(self, albumpath, albumname='myAlbum', Picasaname=None, hiker=None):
        self.__albums.append(Album(albumpath, albumname, Picasaname, hiker, self.__gauge))
        
    def __getAlbum(self, albumname=None):
        for a in self.__albums:
            if (a.getName() == albumname  or albumname == None): return a 
        return None
            
    def __getGpx(self, gpxname=None):
        for g in self.__gpxs:
            if (g.getName() == gpxname or gpxname == None): return g 
        return None
            
    def addGPX(self, gpxpath, gpxname):
        self.__gpxs.append(Gpx(gpxpath, gpxname))
        
    def getAlbum(self, albumname=None):
        return(self.__getAlbum(albumname))
        
    def getGpx(self, gpxname=None):
        return(self.__getGpx(gpxname))
        
    def getInfoAlbum(self, albumname=None):
        a = self.__getAlbum(albumname)
        plist = a.getSortedPhotosListByGeolocation()
        for p in plist:
            logger.debug(p[0] + " is " + p[1].getDatedName())
            if p[1].isPicasaDataSet():  logger.debug(p[1].getPicasaData()[0] + " - " + p[1].getPicasaData()[1] + " - " + p[1].getPicasaData()[2])
 
    def getStat(self, albumname=None):
        a = self.__getAlbum(albumname)
        plist = a.getPhotos()
        geo, sync = 0, 0
        for p in plist:
            if p.isPicasaDataSet(): sync += 1
            if p.isGeolocable(): geo += 1    
        return (len(plist), geo, sync)         
        
    def uploadAlbumToPicasaWeb(self, albumname=None):
        a = self.__getAlbum(albumname)
        if not a.isAlbumPicasaExist():
            a.uploadAlbumToPicasaWeb()
    
    def getinfoAlbumOnPicasaWeb(self, albumname=None):
        a = self.__getAlbum(albumname)
        if a.isAlbumPicasaExist():
            a.getinfoAlbumOnPicasaWeb()
            
    def uploadAlbum(self, albumname=None):
        if albumname: logger.debug('uploadAlbum, albumname=' + albumname)
        a = self.__getAlbum(albumname)
        if not a.isAlbumPicasaExist():
            logger.info('Album upload in progress...')
            a.uploadAlbumToPicasaWeb()
            logger.info('Album upload album done.')
        else:
            logger.warning('Picasa album not exist !!')        

    def syncrhonizeAlbum(self, albumname=None):
        if albumname: logger.debug('syncrhonizeAlbum, albumname=' + albumname)
        a = self.__getAlbum(albumname)
        if a.isAlbumPicasaExist():
            logger.info('Album Synchro in progress...')
            a.syncrhonizeWithAlbumOnPicasaWeb()
            logger.info('Album Synchro album done.')
        else:
            logger.warning('Picasa album not exist !!')
        
    def backupAlbum(self, albumname=None):
        a = self.__getAlbum(albumname)
        a.backupAlbum()
       
    def restoreAlbum(self, albumname=None):
        a = self.__getAlbum(albumname)
        a.restoreAlbum()

                
    def getInfoGPX(self, gpxname=None):
        g = self.__getGpx(gpxname)
        print g.getName()

        
    def createKML(self, kmlname, gpxname=None, albumname=None):
        g = self.__getGpx(gpxname)
        a = self.__getAlbum(albumname)
        k = Kml(kmlname)
        k.createKmlFromGpx(g, a)
        

    def geolocatePhotos(self, albumname=None, gpxname=None):
        a = self.__getAlbum(albumname)
        g = self.__getGpx(gpxname) 
        logger.info('Photo Geolocation in progress...')   
        plist = a.getPhotos()
        for p in plist:
            logger.debug(p.getDatedName() + " - " + p.getModel())
            #fix bug : ID: 3063438
            if p.isGeolocable():
                _coordinates = g.getCoordinatesForTime(p.getDateTimeOriginalLocal())
                p.setCoordinates(_coordinates)
                logger.debug('Photo Geolocation done.')    

if __name__ == "__main__":
    pass

#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from xml.dom import minidom
from lib import kmlextlib as kmlext





 

debug = 0  
    
    
    
class Kml:
    """
    Classe Kml
    
    desc
    """
    
    def __init__(self, initpath=os.curdir + os.sep + 'myKml', name='myKml'):
        self.__shortName = name
        self.__initPath = initpath
        self.__album = None
        self.__gpx = None
        
    def __writeKmlFile(self):  
        _kmlFile = open(self.__initPath, 'w')
        #_kmlFile.write(self.__kmlDoc.toprettyxml('  ', newl='\n', encoding='utf-8'))
        _kmlFile.write(self.__kmlDoc.toxml())
        self.__kmlDoc.unlink()  # ?????     

    def __dumpKmlFile(self):  
        _kmlDoc = minidom.parse(self.__initPath)
        print _kmlDoc.toxml()
        
    def __initKml(self):  
        """
        init kml doc
        """
        self.__kmlPath = self.__gpx.getInitPath()
        self.__initPath = os.path.split(self.__kmlPath)[0] + '/' + ((os.path.split(self.__kmlPath)[1]).split('.'))[0] + '.kml'
        print self.__initPath
        self.__kmlDoc = minidom.Document()
        #_
        _kmlElement = self.__kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
        _kmlElement.setAttribute('xmlns', 'http://earth.google.com/kml/2.2')
        _kmlElement = self.__kmlDoc.appendChild(_kmlElement)
        #
        self.__documentElement = self.__kmlDoc.createElement('Document')
        self.__documentElement = _kmlElement.appendChild(self.__documentElement)
        #
        _nameElement = self.__kmlDoc.createElement('Name')
        _nameElement.appendChild(self.__kmlDoc.createTextNode(self.__gpx.getName()))
        _nameElement = self.__documentElement.appendChild(_nameElement)      
    
    def __insertLookAtFragment(self):  
        """
        insert the LookAt xml fragment
        """
        kmlext.addLookAtFragment(self.__documentElement, self.__gpx)
        
    def __insertStyleFragment(self):  
        """
        insert the Style xml fragment
        """
        kmlext.addStyleFragment(self.__documentElement)
        
    def __insertTrackFolderFragment(self):  
        """
        insert the Track folder xml fragment
        """
        _st = self.__gpx.getStartEndTime()
        kmlext.addTrackFragment(self.__documentElement, self.__gpx)
        
    #Bug id ID: 3067062
    def __insertWaypointsPlacemarkFragment(self):  
        """
        insert the Waypoints  placemark  xml fragment
        """
                #search the Folder WayPoints  to insert placemark inside        
        _wptelem = None
        folderElemlist = self.__documentElement.getElementsByTagName('Folder')
        for folder in folderElemlist:
            nameElem = folder.getElementsByTagName('name')
            if nameElem.length != 0:
                if nameElem[0].childNodes[0].nodeValue == 'Waypoints':
                    _wptelem = folder
                    break       
        _wptlist = self.__gpx.getWayPoints()
        for _w in _wptlist:
            kmlext.addWaypointsPlacemarkFragment(_wptelem, _w)
        
    def __insertPhotoFolderFragment(self):  
        """
        insert the Photo folder xml fragment
        """
        kmlext.addPhotoFolderFragment(self.__documentElement)     
           
    def __insertWaypointsFolderFragment(self):  
        """
        insert the Photo folder xml fragment
        """
        kmlext.addWaypointsFolderFragment(self.__documentElement)       
        
        
        
    def __insertPhotosPlaceMarkFragment(self):
        """
        insert the PLacemark xml fragment
        """
        _photoList = self.__album .getSortedPhotosListByGeolocation()
        _ppreviouskey = None
        _pprevious = None
        _kmlFrag = ''
        # bug - fix - ID: 3067058
        #search the Folder Photo to insert placemark inside        
        _photoelem = None
        folderElemlist = self.__documentElement.getElementsByTagName('Folder')
        for folder in folderElemlist:
            nameElem = folder.getElementsByTagName('name')
            if nameElem.length != 0:
                if nameElem[0].childNodes[0].nodeValue == 'Photos':
                    _photoelem = folder
                    break            
        for _p in _photoList:
            # fix bug  ID: 3061920 add the if _p[1].isPicasaDataSet(): condition
            if _p[1].isPicasaDataSet():
                if _p[0] == _ppreviouskey:
                    _kmlFrag += kmlext.getPhotosPlacemarkFragmentBody(_p[1], self.__album)
                else:
                    if _ppreviouskey != None:
                        kmlext.addPhotosPlacemarkFragment(_photoelem, _pprevious, _kmlFrag)
                        _kmlFrag = ''
                    _kmlFrag += kmlext.getPhotosPlacemarkFragmentHead(_p[1])
                    _kmlFrag += kmlext.getPhotosPlacemarkFragmentBody(_p[1], self.__album)
                    _ppreviouskey = _p[0]
                    _pprevious = _p[1]
        if _ppreviouskey != None:
            kmlext.addPhotosPlacemarkFragment(_photoelem, _pprevious, _kmlFrag)
        
    def __buildKml(self):
        """
        build Kml file from Gpx and Album objects 
        """
        self.__initKml()
        self.__insertLookAtFragment()
        self.__insertStyleFragment()
        self.__insertTrackFolderFragment()
        self.__insertWaypointsFolderFragment()
        self.__insertWaypointsPlacemarkFragment()
        # bug - fix - ID: 3067058
        self.__insertPhotoFolderFragment()
        self.__insertPhotosPlaceMarkFragment()
        
        
                
    def getName(self):
        return self.__shortName

    def getInitPath(self):
        return self.__initPath        
        
    def createKmlFromGpx(self, gpx, album):
        self.__album = album
        self.__gpx = gpx
        self.__buildKml()
        self.__writeKmlFile()
        #self.__dumpKmlFile()



if __name__ == "__main__":
    pass

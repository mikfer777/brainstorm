#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from xml.dom import minidom
from datetime import datetime
from lib import decimaldegrees as dd
from lib import gislib as gis


try:
    from pytz import timezone
except ImportError:
    print u"""
    installer pytz pour utiliser ce programme
    A télecharger sur www.wxpython.org"""
    sys.exit(0)



    

debug = 0  
    
    
    
class Gpx:
    """
    Classe Gpx
    
    desc
    """
    

    
    def __init__(self, initpath=os.curdir + os.sep + 'myGpx', name='myGpx'):
        self.__shortName = name
        self.__initPath = initpath
        self.__doc = None
        
    def __setDocRoot(self):
        self.__doc = minidom.parse(self.__initPath)
        
    def __getDocRoot(self):
        if self.__doc == None:
            self.__setDocRoot()
        return  self.__doc
    
    def __getstate__(self):
        # http://www.dil.univ-mrs.fr/~garreta/PythonBBSG/docs/python-2.6.2-docs-html/library/pickle.html
        # remove the _Gpx__doc from the object dict before serialization
        gpx = self.__dict__.copy() # copy the dict since we change it
        del gpx['_Gpx__doc']       # remove __doc entry
        return gpx

    def __setstate__(self, gpx):
        self.__doc = minidom.parse(gpx['_Gpx__initPath']) # before deserialization, rebuild the doc root obect
        self.__dict__.update(gpx) # update the object dict for synchro


    def getName(self):
        return self.__shortName

    def getInitPath(self):
        return self.__initPath        

    def listTrkTime(self):
        ltime = []
        root = self.__getDocRoot()
        trkElemList = root.getElementsByTagName('trk')
        for trk in trkElemList:
            #print trk.nodeName, trk.nodeType, trk.nodeValue
            trkptElemList = trk.getElementsByTagName('trkpt')
            for trkpt in trkptElemList:
                #print trkpt.nodeName, trkpt.nodeType, trkpt.getAttribute('lat'),trkpt.getAttribute('lon')
                timeElemList = trkpt.getElementsByTagName('time')
                for time in timeElemList:
                    #your time is of type 1 (ELEMENT_NODE), normally you need to have TEXT_NODE to get a string. This will work: time.childNodes[0].nodeValue
                    #print time.nodeName, time.nodeType, time.childNodes[0].nodeValue
                    ltime.append(time.childNodes[0].nodeValue)
        return ltime[:]
    
    def getStartEndTime(self):
        root = self.__getDocRoot()
        trkElemList = root.getElementsByTagName('trk')
        trkptElemList = trkElemList[0].getElementsByTagName('trkpt')
        startTimeElemList = trkptElemList[0].getElementsByTagName('time')
        startTime = startTimeElemList[0].childNodes[0].nodeValue
        endTimeElemList = trkptElemList[len(trkptElemList) - 1].getElementsByTagName('time')
        endTime = endTimeElemList[0].childNodes[0].nodeValue
        return (startTime, endTime)
    
    def getStartCoordinates(self):
        _coordinates = ''
        root = self.__getDocRoot()
        trkElemList = root.getElementsByTagName('trk')
        trkptElemList = trkElemList[0].getElementsByTagName('trkpt')
        return(trkptElemList[0].getAttribute('lon') , trkptElemList[0].getAttribute('lat'), trkptElemList[0].getElementsByTagName('ele')[0].childNodes[0].nodeValue)
        
    def getCoordinates(self):
        _coordinates = ''
        root = self.__getDocRoot()
        trkElemList = root.getElementsByTagName('trk')
        trkptElemList = trkElemList[0].getElementsByTagName('trkpt')
        for trkpt in trkptElemList:
            _coordinates += ' ' + trkpt.getAttribute('lon') + ',' + trkpt.getAttribute('lat') + ',' + trkpt.getElementsByTagName('ele')[0].childNodes[0].nodeValue
        return _coordinates
    
    def getWayPoints(self):
        wptlist = []
        root = self.__getDocRoot()
        wptElemList = root.getElementsByTagName('wpt')
        for wpt in wptElemList:
            wptlist.append((wpt.getAttribute('lat'), wpt.getAttribute('lon'), wpt.getElementsByTagName('ele')[0].childNodes[0].nodeValue, \
                           wpt.getElementsByTagName('name')[0].childNodes[0].nodeValue, wpt.getElementsByTagName('cmt')[0].childNodes[0].nodeValue, \
                            wpt.getElementsByTagName('desc')[0].childNodes[0].nodeValue))
        return wptlist[:]
    
    def getCoordinatesForTime(self, timelocal):
        """ 
            
        """
        #convert local time in utc time
        _utc = timezone('UTC')
        timelocal_utc = timelocal.astimezone(_utc)
        _root = self.__getDocRoot()
        _trkElemList = _root.getElementsByTagName('trk')
        _timeElemList = _trkElemList[0].getElementsByTagName('time')
        min_time_utc = timelocal_utc
        max_time_utc = timelocal_utc
        minlat = minlon = maxlat = maxlon = elev = 0
        for _time in _timeElemList:
            # format time as date with UTC timezone 
            _time_utc = _utc.localize(datetime.strptime(_time.childNodes[0].nodeValue, "%Y-%m-%dT%H:%M:%SZ"))
            # <
            if timelocal_utc < _time_utc:
                max_time_utc = _time_utc
                trkpt = _time.parentNode
                maxlat = trkpt.getAttribute('lat')
                maxlon = trkpt.getAttribute('lon')
                elev = trkpt.getElementsByTagName('ele')[0].childNodes[0].nodeValue
                break
            # >
            if timelocal_utc > _time_utc:
                min_time_utc = _time_utc
                max_time_utc = timelocal_utc
                trkpt = _time.parentNode
                minlat = trkpt.getAttribute('lat')
                minlon = trkpt.getAttribute('lon')
                elev = trkpt.getElementsByTagName('ele')[0].childNodes[0].nodeValue
            # ==
            if timelocal_utc == _time_utc:
                min_time_utc = max_time_utc = _time_utc
                trkpt = _time.parentNode
                minlat = maxlat = trkpt.getAttribute('lat')
                minlon = maxlon = trkpt.getAttribute('lon')
                elev = trkpt.getElementsByTagName('ele')[0].childNodes[0].nodeValue
                break
            #
        if debug:    
            print "[%s] < [%s] > [%s] >sec=%s <sec=%s" % (min_time_utc, timelocal_utc , max_time_utc, \
            (timelocal_utc - min_time_utc).seconds, (max_time_utc - timelocal_utc).seconds)    
            print "Decimal: min lat=[%s] min lon=[%s] \t\t max lat=[%s] max lon=[%s]\t\t elev=[%s]" % (minlat, minlon, maxlat, maxlon, elev) 
            print  "DMS:\t\t", dd.dmsPrintformat(dd.decimal2dms(float(minlat))), "\t", dd.dmsPrintformat(dd.decimal2dms(float(minlon))), "\t\t\t\t", \
                dd.dmsPrintformat(dd.decimal2dms(float(maxlat))), "\t", dd.dmsPrintformat(dd.decimal2dms(float(maxlon))), \
                "Ecart: %i m" % (int(gis.getDistance((float(minlat), float(minlon)), (float(maxlat), float(maxlon))) * 1000)) , "\n"
                
        if (timelocal_utc - min_time_utc).seconds > (max_time_utc - timelocal_utc).seconds:
            return (float(maxlat), float(maxlon), float(elev))
        else:
            return (float(minlat), float(minlon), float(elev))

if __name__ == "__main__":
    pass

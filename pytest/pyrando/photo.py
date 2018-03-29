#! /usr/bin/env python
#-*- coding: iso-8859-15 -*-



import os
import sys
import time
import shutil
from datetime import  timedelta, datetime
import time


try:
    from pytz import timezone
except ImportError:
    print u"""
    installer pytz pour utiliser ce programme
    A télecharger sur www.wxpython.org"""
    sys.exit(0)

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
except ImportError:
    print u"""
    installer PIL Python pour utiliser ce programme
    A télecharger sur www.wxpython.org"""
    sys.exit(0)
    
import logging
logger = logging.getLogger("core.photo")
    
THUMBNAILDIR = '.thumbnail'    
    
    
    
    

class Photo:
    """
    Classe Photo
    
    l'Objet photo...
    
    """
    
    
    def __get_exif(self):
        ret = {}
        i = Image.open(self.__fullPhotoOriginalName)
        info = i._getexif()
        if info == None:return
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded in ('DateTimeOriginal', 'Model'):
                ret[decoded] = value
        return ret

    def __create_thumbnail(self):        
        size = 128, 128
        try:
            im = Image.open(self.__fullPhotoOriginalName)
            im.thumbnail(size)
            im.save(self.__fullPhotoThumbnailName, "JPEG")
        except IOError:
            logger.error("cannot create thumbnail for:" + self.__fullPhotoOriginalName, sys.exc_info()[0])
            raise

            
    def __init__(self, album_root_dir, album_name, photo_initpath, photo_name):
        
        self.__lattitude = self.__longitude = self.__elevation = 0
        self.__albumRootDir = album_root_dir
        self.__initPath = photo_initpath
        self.__albumName = album_name
        self.__photoOriginalName = photo_name
        self.__fullPhotoOriginalName = self.__initPath + os.sep + self.__photoOriginalName
        self.__fullPhotoThumbnailName = self.__initPath + os.sep + THUMBNAILDIR + os.sep + os.path.splitext(self.__photoOriginalName)[0] + "_thumbnail.jpg"
        self.__PicasaMediaUrl = ''
        self.__PicasaHTMLLink = ''
        self.__PicasaAlbumUrl = ''
        self.__PicasaSummary = ''
        exifInfo = self.__get_exif()
        #fix bug: ID: 3063438
        if exifInfo != None: 
            if exifInfo.has_key('Model'):self.__ModelName = exifInfo['Model']
            if exifInfo.has_key('DateTimeOriginal'):
                #format DateTimeOriginal as index
                #self.__DateTimeOriginalIndex=exifInfo['DateTimeOriginal'].split(' ')[0].replace(':','') + \
                #exifInfo['DateTimeOriginal'].split(' ')[1].replace(':','')
                # format DateTimeOriginal as date with local timezone
                local = timezone('Europe/Paris')
                self.__DateTimeOriginalLocal = local.localize(datetime.strptime(exifInfo['DateTimeOriginal'], "%Y:%m:%d %H:%M:%S"))
                # fix bug ID: 3065842
                #b = timedelta(hours=1)
                #self.__DateTimeOriginalLocal = self.__DateTimeOriginalLocal + b
                # format photo dated name            
                self.__PhotoDatedName = self.__albumName + "_" + exifInfo['DateTimeOriginal'].split(' ')[0].replace(':', '') + '_' + \
                exifInfo['DateTimeOriginal'].split(' ')[1].replace(':', '') + ".jpg"
            #format full path photo dated name   
            self.__fullPhotoDatedName = self.__albumRootDir + os.sep + self.__PhotoDatedName
        else:
            self.__PhotoDatedName = self.__photoOriginalName
            self.__DateTimeOriginalLocal = None
            self.__fullPhotoDatedName = self.__albumRootDir + os.sep + self.__PhotoDatedName 
            self.__ModelName = 'Not available'
            logger.warning("No exif Info !!! ==> " + self.__photoOriginalName) 
        #create thumbnail
        self.__create_thumbnail()
        
        
        
        
    def getInitPath(self):
        return self.__initPath
    
    def setCoordinates(self, coordinates):
        self.__lattitude = coordinates[0]
        self.__longitude = coordinates[1]
        self.__elevation = coordinates[2]
        
    def setPicasaData(self, medialUrl, htmlLink, albumurl, summary):
        _pos = str(medialUrl).rfind('/')
        self.__PicasaMediaUrl = str(medialUrl)[0:_pos] + '/s800' + str(medialUrl)[_pos:len(str(medialUrl))]
        _sstart = str(htmlLink).find('href=\"')
        _send = str(htmlLink).find('\"', _sstart + 6)
        self.__PicasaHTMLLink = str(htmlLink)[_sstart + 6:_send]
        _sstart = str(albumurl).find('href=\"')
        _send = str(albumurl).find('#', _sstart + 6)
        self.__PicasaAlbumUrl = str(albumurl)[_sstart + 6:_send]
        #fix bug ID: 3061834
        if summary != None: self.__PicasaSummary = summary

    def isGeolocable(self):
        if self.__DateTimeOriginalLocal != None:
            return True 
        else: 
            return False
        
    def isPicasaDataSet(self):
        # fix bug  ID: 3061920 != None replaced by != '' 
        if self.__PicasaMediaUrl != '':
            return True 
        else: 
            return False
 
    def getCoordinates(self):
        return (self.__lattitude , self.__longitude, self.__elevation)  
    
    def getLattitude(self):
        return self.__lattitude

    def getLongitude(self):
        return self.__longitude

    def getElevation(self):
        return self.__elevation

    
    def getPicasaData(self):
        return (self.__PicasaMediaUrl , self.__PicasaHTMLLink, self.__PicasaAlbumUrl)    
    
    def getPicasaMediaUrl(self):
        return  self.__PicasaMediaUrl
    
    def getPicasaHTMLLink(self):
        return  self.__PicasaHTMLLink
    
    def getPicasaSummary(self):
        return self.__PicasaSummary
    
    def getPicasaAlbumUrl(self):
        return  self.__PicasaAlbumUrl    

    def getOriginalName(self):
        return self.__photoOriginalName

    def getDateTimeOriginalLocal(self):
        return self.__DateTimeOriginalLocal      
 
    def getDatedName(self):
        return self.__PhotoDatedName
    
    def getFullPhotoDatedName(self):
        return self.__fullPhotoDatedName
    
    def getFullPhotoThumbnailName(self):
        return self.__fullPhotoThumbnailName
        
    def getModel(self):
        return self.__ModelName
        
    def pilSaveOriginal(self):
        logger.debug('copie de %s vers: %s\n' % (self.__fullPhotoOriginalName, self.__fullPhotoDatedName))
        original_size = os.path.getsize(self.__fullPhotoOriginalName)
        im = Image.open(self.__fullPhotoOriginalName)
        logger.debug(im.format, im.size, im.mode)
        im.save(self.__fullPhotoDatedName, "JPEG", quality=75)
        compress_size = os.path.getsize(self.__fullPhotoDatedName)
        logger.debug('original size= %s copy size = %s\n' % (str(original_size), str(compress_size)))
        
    def createDated(self):
        logger.debug('copie de %s vers: %s' % (self.__fullPhotoOriginalName, self.__fullPhotoDatedName))
        if os.path.isfile(self.__fullPhotoDatedName): 
            print "%s already created!, skip" % (self.__fullPhotoDatedName)
            return
        shutil.copy2(self.__fullPhotoOriginalName, self.__fullPhotoDatedName)

    def removeDated(self):        
        if os.path.isfile(self.__fullPhotoDatedName) and self.__DateTimeOriginalLocal != None:
            logger.debug('remove de %s ' % (self.__fullPhotoDatedName)) 
            os.remove(self.__fullPhotoDatedName)


    def backupOriginal(self, backupdir):
        logger.debug('backup de %s vers: %s' % (self.__fullPhotoOriginalName, backupdir + os.sep + self.__photoOriginalName))
        if os.path.isfile(backupdir + os.sep + self.__photoOriginalName):
            logger.warning("%s already backuped!, skip" % (self.__fullPhotoOriginalName))
            return
        shutil.copy2(self.__fullPhotoOriginalName, backupdir + os.sep + self.__photoOriginalName)
        os.remove(self.__fullPhotoOriginalName)
        logger.debug('backup %s removed!' % (self.__fullPhotoOriginalName))
        self.__fullPhotoOriginalName = backupdir + os.sep + self.__photoOriginalName
        logger.debug('backup __fullPhotoOriginalName = %s' % (self.__fullPhotoOriginalName))

    def restoreOriginal(self, backupdir):
        logger.debug('restore de %s vers: %s' % (self.__fullPhotoOriginalName, self.__initPath + os.sep + self.__photoOriginalName))
#        if os.path.isfile(self.__initPath + os.sep + self.__photoOriginalName):
#            logger.warning("%s already restored!, skip" % (self.__initPath + os.sep + self.__photoOriginalName))
#            return
        shutil.copy2(self.__fullPhotoOriginalName, self.__initPath + os.sep + self.__photoOriginalName)
        os.remove(self.__fullPhotoOriginalName)
        logger.debug('restore %s removed!' % (self.__fullPhotoOriginalName))
        self.__fullPhotoOriginalName = self.__initPath + os.sep + self.__photoOriginalName
        logger.debug('restore __fullPhotoOriginalName = %s' % (self.__fullPhotoOriginalName))
        
        
        
        
if __name__ == "__main__":
    p = Photo('myPhoto')

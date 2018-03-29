#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, time
import sys
import string
from core.photo import Photo
from core.hiker import Hiker
from lib import decimaldegrees as dd

try:
    import gdata.photos.service
    import gdata.media
    import gdata.geo
    from gdata.service import CaptchaRequired
except ImportError:
    print u"""
    installer gdata pour utiliser ce programme
    A télecharger sur www.wxpython.org"""
    sys.exit(0)
    
import logging
logger = logging.getLogger("core.album")



# bug fix ID 3066039
BACKUPDIR = '.original'
THUMBNAILDIR = '.thumbnail'
    
class Album:
    """
    Classe Album
    
    l'Objet album...
    """

    def __init__(self, root_dir=os.curdir + os.sep + 'myAlbum', shortname='myAlbum', Picasaname='Picasa name', hiker=None , gauge=None):
        
        
        logger.debug("__init__")   
        self.__lPhotos = []
        self.__gauge = gauge
        self.__root_dir = root_dir
        self.__shortName = shortname
        self.__PicasaName = Picasaname
        self.__PicasaGphotoId = 0
        self.__hiker = hiker
        self.__explore()
        self.__gd_client = None

        
    def __getstate__(self):
        # http://www.dil.univ-mrs.fr/~garreta/PythonBBSG/docs/python-2.6.2-docs-html/library/pickle.html
        # remove the gauge from the object Album before serialization
        a = self.__dict__.copy() # copy the dict since we change it
        del a['_Album__gauge']       # remove __doc entry
        return a
    
    def setGauge(self, gauge):
        self.__gauge = gauge
    
    def getName(self):
        return self.__shortName
    
    def getHiker(self):
        return self.__hiker
    
    def getPicasaName(self):
        return self.__PicasaName

    def getRootDir(self):
        return self.__root_dir
        
    def __get_jpegs(self, filenames):
        """
        liste comprehension pour filtrer les fichiers jpeg (.jpg, .jpeg, .JPEG, ..)
        """
        return [f for f in filenames if os.path.splitext(f)[-1].lower() in ['.jpg', '.jpeg']]
        
    def listPhotos(self):
        logger.debug("photo number= " + str(len(self.__lPhotos)))
        for p in self.__lPhotos: 
            logger.debug(p.getInitPath() + " - " + p.getDatedName() + " - " + p.getModel())
            logger.debug("Coordinates DMS:\t lat=" + dd.dmsPrintformat(dd.decimal2dms(p.getCoordinates()[0])) + "\t long=" + 
                          dd.dmsPrintformat(dd.decimal2dms(p.getCoordinates()[1])) + "\t elev=" + str(p.getCoordinates()[2]))


    def getPhotos(self):
        return self.__lPhotos[:]
    
      
    def getSortedPhotosListByGeolocation(self):
        _lSortedPhotos = []
        for p in self.__lPhotos:
            _key = str(p.getCoordinates()[0]) + str(p.getCoordinates()[1])
            _lSortedPhotos.append((_key, p))
        _lSortedPhotos.sort()
        return _lSortedPhotos[:]
            
    
    def stat(self):
        photos_count, dirs_count = 0, 0
        if os.path.isdir(self.__root_dir + os.sep + BACKUPDIR):
            rootdir = self.__root_dir + os.sep + BACKUPDIR
        else:
            rootdir = self.__root_dir
        for dirpath, dirnames, filenames in os.walk(rootdir):
            photosrep = self.__get_jpegs(filenames)
            if photosrep:
                photos_count += len(photosrep)
                dirs_count += 1
        logger.debug(photos_count, dirs_count)
        
    def __normalize(self, c, dirpath):
        o = c
        for i in range(0, len(string.whitespace)):
            if c.find(string.whitespace[i]) != -1: 
                logger.debug("trouvé:" + string.whitespace[i] + "a: " + str(c.find(string.whitespace[i])))
                c = string.replace(c, string.whitespace[i], '_')
        if o != c:
            os.rename(dirpath + os.sep + o, dirpath + os.sep + c)
        return c
        
    def __explore(self):        
        if not os.path.isdir(self.__root_dir + os.sep + THUMBNAILDIR):
            os.mkdir(self.__root_dir + os.sep + THUMBNAILDIR)
        if os.path.isdir(self.__root_dir + os.sep + BACKUPDIR):
            rootdir = self.__root_dir + os.sep + BACKUPDIR
        else:
            rootdir = self.__root_dir
        for dirpath, dirnames, filenames in os.walk(rootdir):
            logger.debug('dirnames: %s filenames: %s' % (dirnames, filenames))
            photosrep = self.__get_jpegs(filenames)
            if photosrep:
                gmax = len(photosrep)
                if self.__gauge : self.__gauge.Show(True)
                k = 0
                for p in photosrep:
                    logger.debug("p=" + p)
                    p = self.__normalize(p, dirpath.replace('\\', '/'))
                    self.__lPhotos.append(Photo(self.__root_dir, self.__shortName, dirpath.replace('\\', '/'), p))
                    k += 100 / gmax
                    if self.__gauge : self.__gauge.SetValue(k)
                if self.__gauge : self.__gauge.Show(False)
                break
        
    def backupAlbum(self):
        if not os.path.isdir(self.__root_dir + os.sep + BACKUPDIR):
            os.mkdir(self.__root_dir + os.sep + BACKUPDIR)
        gmax = len(self.__lPhotos)
        if self.__gauge : self.__gauge.Show(True)
        k = 0
        for p in self.__lPhotos: 
            p.backupOriginal(self.__root_dir + os.sep + BACKUPDIR)
            p.createDated()
            k += 100 / gmax
            if self.__gauge : self.__gauge.SetValue(k)
        if self.__gauge : self.__gauge.Show(False)
        
    def restoreAlbum(self):
        if not os.path.isdir(self.__root_dir + os.sep + BACKUPDIR):
            return
        gmax = len(self.__lPhotos)
        if self.__gauge : self.__gauge.Show(True)
        k = 0
        for p in self.__lPhotos: 
            p.restoreOriginal(self.__root_dir + os.sep + BACKUPDIR)
            p.removeDated()
            k += 100 / gmax
            if self.__gauge : self.__gauge.SetValue(k)
        os.rmdir(self.__root_dir + os.sep + BACKUPDIR)
        if self.__gauge : self.__gauge.Show(False)
        
    def __setGDCklient(self):
        try:
            logger.debug('picasa mail: ' + self.__hiker.getPicasaMail())
            logger.debug('picasa pass:' + self.__hiker.getPicasaPassword())
            self.__gd_client = gdata.photos.service.PhotosService()
            self.__gd_client.email = self.__hiker.getPicasaMail()
            self.__gd_client.password = self.__hiker.getPicasaPassword()
            #self.__gd_client.source = 'exampleCo-exampleApp-1'
            self.__gd_client.ProgrammaticLogin()
        except CaptchaRequired:
            logger.error("erreur de login picasa")
            raise
        except:
            logger.error("Unexpected error:", sys.exc_info()[0])
            raise

    def isAlbumPicasaExist(self):
        if self.__gd_client == None: self.__setGDCklient()
        picalbums = self.__gd_client.GetUserFeed(user=self.__hiker.getPicasaUser())   
        for picalbum in picalbums.entry:
            logger.debug('title: %s, number of photos: %s, id: %s' % (picalbum.title.text, picalbum.numphotos.text, picalbum.gphoto_id.text)) 
            if picalbum.title.text == self.__PicasaName:
                self.__PicasaGphotoId = picalbum.gphoto_id.text
                return True
        return False
    
    def uploadAlbumToPicasaWeb(self):
        if self.__gd_client == None: self.__setGDCklient()
        picalbum = self.__gd_client.InsertAlbum(title=self.__PicasaName, summary='pyrando uploaded album')
        # bug fix ID: 3062799 
        self.__PicasaGphotoId = picalbum.gphoto_id.text
        album_url = '/data/feed/api/user/%s/albumid/%s' % (self.__hiker.getPicasaUser(), self.__PicasaGphotoId)
        gmax = len(self.__lPhotos)
        if self.__gauge : self.__gauge.Show(True)
        k = 0
        for p in self.__lPhotos: 
            picphoto = self.__gd_client.InsertPhotoSimple(album_url, p.getDatedName(), 'Uploaded using the API', p.getFullPhotoDatedName(), content_type='image/jpeg')
            logger.debug(p.getFullPhotoDatedName() + " uploaded")
            k += 100 / gmax
            if self.__gauge : self.__gauge.SetValue(k) 
            time.sleep(0.015)
                
            
    def getinfoAlbumOnPicasaWeb(self):
        if self.__gd_client == None: self.__setGDCklient()
        if self.__PicasaGphotoId != 0:
            picphotos = self.__gd_client.GetFeed('/data/feed/api/user/%s/albumid/%s?kind=photo' % (self.__hiker.getPicasaUser(), self.__PicasaGphotoId))
            for picphoto in picphotos.entry:
                tags = self.__gd_client.GetFeed('/data/feed/api/user/%s?kind=tag' % self.__hiker.getPicasaUser())
                for tag in tags.entry:
                    logger.debug('Tag', tag.title.text)
                logger.debug('Photo title:' + " - " + picphoto.title.text)
                logger.debug('GetAclLink:%s\nGetAlbumUri:%s\nGetAlternateLink:%s\nGetCommentsUri:%s\nGetEditLink:%s\nGetEditMediaLink:%s\nGetFeedLink:%s\nGetHt \
                        mlLink:%s\nGetLicenseLink:%s\nGetMediaURL:%s\nGetNextLink:%s\nGetPostLink:%s\nGetPrevLink:%s\nGetSelfLink:%s\nGetTagsUri;%s\n'\
                        % (str(picphoto.GetAclLink()), str(picphoto.GetAlbumUri()), str(picphoto.GetAlternateLink()), \
                           str(picphoto.GetCommentsUri()), str(picphoto.GetEditLink()), str(picphoto.GetEditMediaLink()), str(picphoto.GetFeedLink()), \
                           str(picphoto.GetHtmlLink()), str(picphoto.GetLicenseLink()), str(picphoto.GetMediaURL()), str(picphoto.GetNextLink()), \
                           str(picphoto.GetPostLink()), str(picphoto.GetPrevLink()), str(picphoto.GetSelfLink()), str(picphoto.GetTagsUri())))
                
                
    def syncrhonizeWithAlbumOnPicasaWeb(self):
        if self.__gd_client == None: self.__setGDCklient()
        if self.__PicasaGphotoId != 0:
            picphotos = self.__gd_client.GetFeed('/data/feed/api/user/%s/albumid/%s?kind=photo' % (self.__hiker.getPicasaUser(), self.__PicasaGphotoId))
            gmax = len(picphotos.entry)
            if self.__gauge : self.__gauge.Show(True)
            k = 0
            for picphoto in picphotos.entry:
                for p in self.__lPhotos:
                    #bug fix ID: 3067902
                    if p.getDatedName() == picphoto.title.text or p.getOriginalName() == picphoto.title.text:
                        logger.debug('Photo title:' + picphoto.title.text)
                        p.setPicasaData(picphoto.GetMediaURL(), picphoto.GetHtmlLink(), picphoto.GetAlternateLink(), picphoto.summary.text)
                        k += 100 / gmax
                        if self.__gauge : self.__gauge.SetValue(k) 
                        time.sleep(0.015)
                        break
            if self.__gauge : self.__gauge.Show(False)


if __name__ == "__main__":
    a = Album()
    #print os.__doc__ , dir(os)

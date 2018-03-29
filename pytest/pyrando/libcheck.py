#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 3 sept. 2010

@author: mferreol
'''
import sys

try:
    from pytz import timezone
except ImportError:
    print u"""
    installer pytz-2010k pour utiliser ce programme
    A télecharger sur http://pypi.python.org/pypi/pytz"""
    sys.exit(0)

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
except ImportError:
    print u"""
    installer PIL pour utiliser ce programme
    A télecharger sur http://effbot.org/downloads/#pil"""
    sys.exit(0)
    
try:
    import gdata.photos.service
    import gdata.media
    import gdata.geo
except ImportError:
    print u"""
    installer gdata 2.0.11 pour utiliser ce programme
    A télecharger sur http://code.google.com/p/gdata-python-client/downloads/list"""
    sys.exit(0)        

if __name__ == '__main__':
    pass

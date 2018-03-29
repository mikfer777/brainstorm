#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 3 sept. 2010

@author: mikfer
Create the config files for unit testing

'''
import ConfigParser, os
import sys
from datetime import datetime

try:
    from pytz import timezone
except ImportError:
    print u"""
    installer pytz-2010k pour utiliser ce programme
    A télecharger sur http://pypi.python.org/pypi/pytz"""
    sys.exit(0)

                    
if __name__ == "__main__":
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    now_utc = datetime.now(timezone('Europe/Paris'))
    print now_utc.strftime(fmt)
    #print os.__doc__ , dir(os)
    print os.getcwd()
    project_name = 'pyrando'
    project_utdatadir = 'utdata'
    project_path = os.getcwd()[0:os.getcwd().find(project_name) + len(project_name)]
    config = ConfigParser.RawConfigParser()
    config_pathname = project_path + os.sep + project_utdatadir + os.sep + 'ut1.cfg'
    try:
        config.readfp(open(config_pathname))
        print config.get('rando', 'shortname')
        print config.get('rando', 'longname')
        print config.get('album1', 'shortname')
        print config.get('album1', 'longname')
        print config.get('album1', 'path')
    except IOError:
        # Writing our configuration file to 'example.cfg'
        config.add_section('picasaweb')
        config.set('picasaweb', 'mailaddress', 'michel.ferreol@free.fr')
        config.set('picasaweb', 'user', 'michel.ferreol@free.fr')
        config.set('picasaweb', 'password', 'gnome(398)')
        config.add_section('gant')
        config.set('gant', 'path', '/home/mik/product/antG405/gant-master')
        config.add_section('rando')
        config.set('rando', 'shortname', 'pmirando')
        config.set('rando', 'longname', u'bivouac Pointe du Midi \u20ac et Pic du Jalouvre')
        config.add_section('album1')
        config.set('album1', 'shortname', 'PMI')
        config.set('album1', 'longname', 'PMI20100724Pic_du_Jalouvre_pyrandotest')
        config.set('album1', 'path', project_path + os.sep + project_utdatadir + os.sep + 'ut1' + os.sep + '2010PMI')
        config.add_section('gpx1')
        config.set('gpx1', 'shortname', 'pmigpx')
        config.set('gpx1', 'longname', 'trace GPS PMI')
        config.set('gpx1', 'path', project_path + os.sep + project_utdatadir + os.sep + 'ut1' + os.sep + '20100724PointeduMidi.gpx')
        config.add_section('rando2')
        config.set('rando2', 'shortname', 'tgctrail')
        config.set('rando2', 'longname', 'TGC trail tour de la grande Casse')
        config.add_section('album2')
        config.set('album2', 'shortname', 'TGC')
        #encodage utf-8 d'une chaine de caractères € = code point \u20ac en encodage utf-8 
        #par defaut l'encodage de python est utf-8 sys.getdefaultencoding() , on peut donc ce passer de u''
        config.set('album2', 'longname', u'TGC20100828 Tour de la  \u20ac  Grande Casse€€ héhéhéê')
        config.set('album2', 'path', project_path + os.sep + project_utdatadir + os.sep + 'ut2' + os.sep + '2010TGC')
        config.add_section('gpx2')
        config.set('gpx2', 'shortname', 'tgcgpx')
        config.set('gpx2', 'longname', 'trace GPS TGC')
        config.set('gpx2', 'path', project_path + os.sep + project_utdatadir + os.sep + 'ut2' + os.sep + '2010TGC.gpx')
        with open(config_pathname, 'wb') as configfile:
            config.write(configfile)
            
    
    

    

    
    
    
    

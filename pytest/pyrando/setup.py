#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# source d'inspiration: http://wiki.wxpython.org/cx_freeze
 
import sys, os, glob
from cx_Freeze import setup, Executable
 
#############################################################################
# preparation des options 
path = sys.path.append(os.path.join("..", "lib"))
path = sys.path.append(os.path.join("..", "core"))
path = sys.path.append(os.path.join("..", "wxgui"))
includes = []
excludes = []
packages = []

#includefiles = glob.glob(r'D:\install\python27\lib\site-packages\pytz\zoneinfo\*')
includefiles = []
print includefiles
options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "include_files":includefiles
           }
 
#############################################################################
# preparation des cibles
base = None
print  sys.platform 
if sys.platform == "win32":
    base = "Win32GUI"
else:
    if sys.platform == "linux2":
        pass
 
cible_1 = Executable(
    script="../wxgui/wxApp1.py",
    base=base,
    compress=True,
    icon=None,
    )
 
cible_2 = Executable(
    script="libcheck.py",
    base=base,
    compress=True,
    icon=None,
    )
 

#############################################################################
# creation du setup


setup(
    name="test_cx_freeze",
    version="0.1",
    description="simple test de cx_freeze avec ..",
    author="mikfer",
    options={"build_exe": options},
    executables=[cible_1, cible_2]
    )

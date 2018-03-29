#! /usr/bin/env python
#-*- coding: iso-8859-15 -*-

import os
import sys
import time
import thread
import Image

try:
    import wx
except ImportError:
    print u"""
    installer wxPython pour utiliser ce programme
    A télecharger sur www.wxpython.org"""
    sys.exit(0)

import  wx.lib.newevent

# ---------------------------------------------
# labels utilisées sur le bouton 'btn_action'
# ---------------------------------------------
START_ACTION = u"Compresser"
STOP_ACTION = u"Arrêter"
# ---------------------------------------------

# ---------------------------------------------
#creation d'evenement personnalisées
# ---------------------------------------------
(UpdateCountEvent, EVT_UPDATE_COUNT) = wx.lib.newevent.NewEvent()
(UpdateCompressEvent, EVT_UPDATE_COMPRESS) = wx.lib.newevent.NewEvent()
(StopCountEvent, EVT_STOP_COUNT) = wx.lib.newevent.NewEvent()
(InterruptCountEvent, EVT_INTERRUPT_COUNT) = wx.lib.newevent.NewEvent()
(StopCompressEvent, EVT_STOP_COMPRESS) = wx.lib.newevent.NewEvent()
(InterruptCompressEvent, EVT_INTERRUPT_COMPRESS) = wx.lib.newevent.NewEvent()
(ErrorCompressEvent, EVT_ERROR_COMPRESS) = wx.lib.newevent.NewEvent()
# ---------------------------------------------

def pluralize(num):
    """
    fonction qui renvoie un 's' si le nombre passé en
    argument est superieur à 1
    """
    return num > 1 and "s" or ""

def normalize(size):
    """
    fonction qui prend en argument un nombre d'octets
    et renvoie la taille la plus adapté
    """
    seuil_Kio = 1024
    seuil_Mio = 1024 * 1024
    seuil_Gio = 1024 * 1024 * 1024

    if size > seuil_Gio:
        return "%.2fGio" % (size / float(seuil_Gio))
    elif size > seuil_Mio:
        return "%.2fMio" % (size / float(seuil_Mio))
    elif size > seuil_Kio:
        return "%.2fKio" % (size / float(seuil_Kio))
    else:
        return "%io" % size

def o_normalize(nb):
    """
    fonction qui permet de separer un nombre par tranche de trois:
    o_normalize(1234567890) => "1 234 567 890"
    """
    nb = str(nb)[::-1] # 12345 => "54321"
    l = []
    for i in range(0, len(nb), 3):
        l.append(nb[i:i + 3][::-1]) # ["345", "12"]
    return " ".join(l[::-1]) # "12 345"

def get_jpegs(filenames):
    # liste comprehension pour filtrer les fichiers jpeg (.jpg, .jpeg, .JPEG, ..)
    return [f for f in filenames if os.path.splitext(f)[-1].lower() in ['.jpg', '.jpeg']]

class CountThread(object):
    """
    Classe qui permet de compter le nombre de fichier jpeg 
    dans un ensemble de dossier.
    Prend en parametre le dossier racine de la recherche
    et la fenetre (wx) a laquelle renvoyer les evenements 
    """
    def __init__(self, win, root_dir):
        self.win = win 
        self.root_dir = root_dir

    def Start(self):
        self.keepGoing = self.running = True
        thread.start_new_thread(self.Run, ())

    def Stop(self):
        self.keepGoing = False

    def IsRunning(self):
        return self.running

    def Run(self):
        photos_count, dirs_count = 0, 0
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            photos = get_jpegs(filenames)
            if photos:
                photos_count += len(photos)
                dirs_count += 1
                evt = UpdateCountEvent(photos_count=photos_count,
                                                   dirs_count=dirs_count) 
                wx.PostEvent(self.win, evt) 

            if not self.keepGoing:
                # en cas d'interruption du thread
                evt = InterruptCountEvent()
                wx.PostEvent(self.win, evt)
                self.running = False
                return

        # le thread se termine normalement
        self.running = False
        evt = StopCountEvent(photos_count=photos_count, photo_dir=self.root_dir)
        wx.PostEvent(self.win, evt)

class CompressThread(object):
    """
    Classe qui permet de recompresser les fichiers jpeg
    dans un ensemble de dossier.
    Prend en parametre le dossier racine de la recherche
    et la fenetre (wx) a laquelle renvoyer les evenements
    """
    def __init__(self, win, root_dir):
        self.win = win
        self.root_dir = root_dir

    def Start(self):
        self.keepGoing = self.running = True
        thread.start_new_thread(self.Run, ())

    def Stop(self):
        self.keepGoing = False

    def IsRunning(self):
        return self.running

    def Run(self):
        photos_count, dirs_count = 0, 0
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            photos = get_jpegs(filenames)
            if photos:
                for f in photos:
                    if not self.keepGoing:
                        break
                    try:
                        name = os.path.join(dirpath, f)
                        original_size = os.path.getsize(name)
                        im = Image.open(name)
                        im.save(name)
                        compress_size = os.path.getsize(name)
                    except IOError:
                        evt = ErrorCompressEvent(
                    message=u"erreur lors du traitement du fichier '%s'" % name)
                        wx.PostEvent(self.win, evt)
                    else:
                        evt = UpdateCompressEvent(
                            original_size=original_size,
                            compress_size=compress_size)
                        wx.PostEvent(self.win, evt)

            if not self.keepGoing:
                # interruption du traitement
                evt = InterruptCompressEvent()
                wx.PostEvent(self.win, evt)
                self.running = False
                return

        self.running = False
        evt = StopCompressEvent()
        wx.PostEvent(self.win, evt)

class MainFrame(wx.Frame):

    def __init__(self, *args, **kwargs):

        wx.Frame.__init__(self, *args, **kwargs)

        self.CreateWidgets()
        self.DoLayout()
        self.DoBinding()
        self.SetInitialValues()

    def CreateWidgets(self):

        panel = self.panel = wx.Panel(self)

        self.staticText_dir = wx.StaticText(panel, -1,
                                            u"répertoire à recompresser:")
        self.textCtrl_dir = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
        self.btn_dir = wx.Button(panel, -1, "...", size=(30, -1))

        self.btn_action = wx.Button(panel, -1)
        font = wx.Font(family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_NORMAL,
                                      weight=wx.FONTWEIGHT_NORMAL, pointSize=18)
        self.btn_action.SetFont(font)
        self.btn_action.SetLabel(START_ACTION)


        self.statusBar = wx.StatusBar(self)
        self.statusBar.SetFieldsCount(4)
        self.statusBar.SetStatusWidths([-3, -2, -1, -1])
        self.SetStatusBar(self.statusBar)

    def DoLayout(self):

        szr = wx.GridBagSizer(5, 5)

        szr.Add(self.staticText_dir, (0, 0), flag=wx.ALIGN_CENTRE)
        szr.Add(self.textCtrl_dir, (0, 1),
                                   flag=wx.EXPAND | wx.ALIGN_CENTRE_HORIZONTAL)
        szr.Add(self.btn_dir, (0, 2), flag=wx.ALIGN_CENTRE_HORIZONTAL)
 
        szr.AddGrowableCol(1)

        main_szr = wx.GridBagSizer(5, 5)
        main_szr.Add((0, 0), (0, 0))
        main_szr.Add(szr, (1, 1), flag=wx.EXPAND)
        main_szr.Add(self.btn_action, (2, 1), flag=wx.EXPAND)
        main_szr.Add((0, 0), (3, 2))

        main_szr.AddGrowableCol(1)
        main_szr.AddGrowableRow(2)

        self.panel.SetSizerAndFit(main_szr)

        self.SetSize((500, 200))
        self.SetMinSize((500, 200))


    def DoBinding(self):

        self.Bind(wx.EVT_BUTTON, self.OnBtnDir, self.btn_dir)
        self.Bind(wx.EVT_BUTTON, self.OnBtnAction, self.btn_action)
        self.Bind(EVT_UPDATE_COUNT, self.OnUpdateCount)
        self.Bind(EVT_UPDATE_COMPRESS, self.OnUpdateCompress)
        self.Bind(EVT_STOP_COUNT, self.OnStopCount)
        self.Bind(EVT_STOP_COMPRESS, self.OnStopCompress)
        self.Bind(EVT_INTERRUPT_COUNT, self.OnInterrupt)
        self.Bind(EVT_INTERRUPT_COMPRESS, self.OnInterrupt)
        self.Bind(EVT_ERROR_COMPRESS, self.OnErrorCompress)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
 

    def SetInitialValues(self):

        self.count_thread = None
        self.compress_thread = None
 
        self.original_size = 0
        self.compress_size = 0
        self.compressed_photo = 0
        self.error = 0

        for i in range(self.StatusBar.GetFieldsCount()):
            self.StatusBar.SetStatusText('', i)

    def OnClose(self, evt):

        self.StopThreads()
        evt.Skip()

    def OnBtnDir(self, evt):

        photo_dir = self.textCtrl_dir.GetValue()
        if os.path.isdir(photo_dir):
            defaultPath = photo_dir
        else:
            defaultPath = ""
        dlg = wx.DirDialog(self, u"Choissisez le répertoire à recompresser",
                                                       defaultPath=defaultPath)

        if dlg.ShowModal() == wx.ID_OK:
            self.textCtrl_dir.SetValue(dlg.GetPath())

        dlg.Destroy()
        evt.Skip()

    def OnBtnAction(self, evt):

        action = self.btn_action.GetLabel()
        if action == START_ACTION:
 
            photo_dir = self.textCtrl_dir.GetValue()
            evt.Skip()

            if not os.path.isdir(photo_dir):
                dlg = wx.MessageDialog(self, u'Répertoire invalide',
                              'Erreur', wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
                return False

            self.StartAction(photo_dir)

        elif action == STOP_ACTION:

            self.StopThreads()


    def StopThreads(self):
            busy = wx.BusyInfo(u'Arrêt en cours ... veuillez patienter')
            wx.Yield()
            
            for thrd in self.count_thread, self.compress_thread:
                if thrd and thrd.IsRunning():
                    thrd.Stop()
                    while thrd.IsRunning():
                        time.sleep(0.1)

            self.SetInitialValues()
 
            self.btn_action.SetLabel(START_ACTION)


    def StartAction(self, photo_dir):

        self.SetInitialValues()
        self.statusBar.SetStatusText(u"Trouvé 0 photo dans 0 répertoire")
        self.btn_dir.Enable(False)
        self.count_thread = CountThread(self, photo_dir)
        self.count_thread.Start()
        self.btn_action.SetLabel(STOP_ACTION)

    def OnUpdateCount(self, evt):

        photos_count, dirs_count = evt.photos_count, evt.dirs_count
        self.statusBar.SetStatusText(u"Trouvé %i photo%s dans %i répertoire%s" % 
                (photos_count,
                pluralize(photos_count),
                 dirs_count,
                 pluralize(dirs_count)))
  

    def OnStopCount(self, evt):
        self.count_thread = None
        self.photos_count = evt.photos_count
        self.compress_thread = CompressThread(self, evt.photo_dir)
        self.compress_thread.Start()

    def OnInterrupt(self, evt):
        self.SetInitialValues()
        self.statusBar.SetStatusText('action interrompue!!')
        self.btn_action.SetLabel(START_ACTION)
        self.btn_dir.Enable(True)

    def OnStopCompress(self, evt):

        if self.photos_count:
            dlg = wx.MessageDialog(self,
u"""traitement terminée!
%i image%s compressée%s
%i erreur%s
taille originale: %s octets
taille finale: %s octets
gain: %s soit %i%%""" % (self.photos_count, pluralize(self.photos_count),
                       pluralize(self.photos_count),
               self.error, pluralize(self.error),
                       o_normalize(self.original_size),
                       o_normalize(self.compress_size),
                       normalize(self.original_size - self.compress_size),
                      ((self.original_size - self.compress_size) / 
                                             float(self.original_size) * 100)),
               'fin du traitement', wx.OK | wx.ICON_INFORMATION)
        else:
            dlg = wx.MessageDialog(self,
            u"Aucune photo à recompresser.",
               'fin du traitement',
           wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
       
        self.SetInitialValues()
        self.statusBar.SetStatusText(u'compression terminée')
        self.btn_action.SetLabel(START_ACTION)
        self.btn_dir.Enable(True)


    def OnUpdateCompress(self, evt):

        self.compressed_photo += 1
        self.original_size += evt.original_size
        self.compress_size += evt.compress_size

        self.statusBar.SetStatusText("%i/%i" % 
              (self.compressed_photo, self.photos_count), 2)
        self.statusBar.SetStatusText("%s => %s" % 
              (normalize(self.original_size), normalize(self.compress_size)), 1)
        self.statusBar.SetStatusText("%i%%" % 
              (int(round(100 * self.compressed_photo // self.photos_count))), 3)

    def OnErrorCompress(self, evt):
        print evt.message
        self.error += 1


if __name__ == "__main__":

    app = wx.PySimpleApp(redirect=False)
    fr = MainFrame(None, -1, "recompresseur de photos")
    fr.Show(True)
    app.MainLoop()
    

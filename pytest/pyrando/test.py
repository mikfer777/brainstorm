#Boa:Frame:Frame1

import wx

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1PANEL1, wxID_FRAME1PANEL2, wxID_FRAME1STATICBOX1, 
] = [wx.NewId() for _init_ctrls in range(4)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(615, 346), size=wx.Size(600, 477),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self.SetClientSize(wx.Size(600, 477))

        self.staticBox1 = wx.StaticBox(id=wxID_FRAME1STATICBOX1,
              label='staticBox1', name='staticBox1', parent=self,
              pos=wx.Point(360, 112), size=wx.Size(200, 312), style=0)
        self.staticBox1.SetToolTipString(u'staticBox1')

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(-80, -104), size=wx.Size(200, 100),
              style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_FRAME1PANEL2, name='panel2', parent=self,
              pos=wx.Point(56, 216), size=wx.Size(200, 100),
              style=wx.TAB_TRAVERSAL)
        self.panel2.SetWindowVariant(wx.WINDOW_VARIANT_SMALL)

    def __init__(self, parent):
        self._init_ctrls(parent)
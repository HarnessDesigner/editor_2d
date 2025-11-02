import wx

from collections import OrderedDict


class Artist:

    def __init__(self, editor, obj):
        self.editor = editor
        self.obj = obj

    def update(self, vert, bmp):
        self.editor.update_obj(self.obj, vert, bmp)


class Editor2D(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, style=wx.BORDER_NONE)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self._on_erase_background)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_MOTION, self._on_motion)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self._on_left_up)
        self.Bind(wx.EVT_LEFT_DCLICK, self._on_left_dclick)
        self.Bind(wx.EVT_RIGHT_DOWN, self._on_right_down)
        self.Bind(wx.EVT_RIGHT_UP, self._on_right_up)
        self.Bind(wx.EVT_RIGHT_DCLICK, self._on_right_dclick)
        self.Bind(wx.EVT_MOUSEWHEEL, self._on_mouse_wheel)

        self.__objects = OrderedDict()
        self.__bitmaps = []
        self._pending_update = False

    def _on_erase_background(self, _):
        pass

    def _on_paint(self, evt):
        dc = wx.BufferedPaintDC(self)
        gcdc = wx.GCDC(dc)

        gcdc.SetPen(wx.TRANSPARENT_PEN)
        gcdc.SetBrush(wx.TRANSPARENT_BRUSH)

        gcdc.Clear()

        self._pending_update = False
        for value in self.__objects.values():
            if value['bmp'].IsOk():
                gcdc.DrawBitmap(value['bmp'], *value['vert'])

        gcdc.Destroy()
        del gcdc

        evt.Skip()

    def _on_motion(self, evt):
        evt.Skip()

    def _on_left_down(self, evt):
        evt.Skip()

    def _on_left_up(self, evt):
        evt.Skip()

    def _on_left_dclick(self, evt):
        evt.Skip()

    def _on_right_down(self, evt):
        evt.Skip()

    def _on_right_up(self, evt):
        evt.Skip()

    def _on_right_dclick(self, evt):
        evt.Skip()

    def _on_mouse_wheel(self, evt):
        evt.Skip()

    def add_line(self, obj) -> Artist:
        self.__objects[obj] = dict(vert=(0, 0), bmp=wx.NullBitmap)
        return Artist(self, obj)

    def update_obj(self, obj, vert, bmp):
        self.__objects[obj] = dict(vert=vert, bmp=bmp)

        value = self.__objects[obj]

        if value['bmp'].IsOk():
            value['bmp'].Destroy()

        value['bmp'] = bmp
        value['vert'] = vert

    def draw_idle(self):
        def _do():
            self.Refresh()
            self.Update()

        if not self._pending_update:
            self._pending_update = True
            wx.CallAfter(_do)

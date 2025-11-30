import wx

class HSizer(wx.BoxSizer):

    def __init__(self, parent, text, ctrl, suffix=None, in_panel=False):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)

        if in_panel:
            panel = wx.Panel(parent, wx.ID_ANY, style=wx.BORDER_NONE)
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            if text is not None:
                st = wx.StaticText(panel, wx.ID_ANY, label=text)
                sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

            ctrl.Reparent(panel)
            sizer.Add(ctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

            if isinstance(suffix, str):
                suffix = wx.StaticText(panel, wx.ID_ANY, label=suffix)
                sizer.Add(suffix, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, 5)
            elif suffix is not None:
                suffix.Reparent(panel)
                sizer.Add(suffix, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, 5)

            panel.SetSizer(sizer)
            self.Add(panel, 0)

        else:
            if text is not None:
                st = wx.StaticText(parent, wx.ID_ANY, label=text)
                self.Add(st, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

            self.Add(ctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

            if isinstance(suffix, str):
                suffix = wx.StaticText(parent, wx.ID_ANY, label=suffix)

            if suffix is not None:
                self.Add(suffix, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, 5)


class WireInfoPanel(wx.Panel):

    def on_material(self, evt: wx.CommandEvent):
        value = evt.GetString()
        self.wire_info.material = value
        self.update_wire()
        evt.Skip()

    def on_shielded(self, evt: wx.CommandEvent):
        value = bool(evt.GetSelection())
        self.wire_info.is_shielded = value
        self.update_wire()
        evt.Skip()

    def on_volts(self, evt: wx.SpinDoubleEvent):
        value = evt.GetValue()
        self.wire_info.volts = value
        self.update_wire_length()
        evt.Skip()

    def on_volt_drop(self, evt: wx.SpinDoubleEvent):
        value = evt.GetValue()
        self.wire_info.allowed_voltage_drop = value
        self.update_wire_length()
        evt.Skip()

    def on_awg(self, evt: wx.SpinEvent):
        value = evt.GetInt()
        self.wire_info.awg = value
        self.update_wire()
        self.update_editor()
        evt.Skip()

    def on_load(self, evt: wx.SpinDoubleEvent):
        value = evt.GetValue()
        self.wire_info.load = value
        self.update_wire_length()
        evt.Skip()

    def on_conductor(self, evt: wx.SpinEvent):
        value = evt.GetInt()
        self.wire_info.num_conductors = value
        self.update_wire_length()
        evt.Skip()

    def on_mm2(self, evt: wx.SpinDoubleEvent):
        value = evt.GetValue()
        self.wire_info.mm2 = value
        self.update_wire()
        self.update_editor()
        evt.Skip()

    def on_color1(self, evt: wx.ColourPickerEvent):
        value = evt.GetColour()
        self.wire_info.color = value
        self.update_wire()
        self.update_editor()
        evt.Skip()

    def on_color2(self, evt: wx.ColourPickerEvent):
        value = evt.GetColour()
        self.wire_info.stripe_color = value
        self.update_wire()
        self.update_editor()
        evt.Skip()

    def update_editor(self):
        def _do():
            self.GetParent().update_bitmap()
            self.GetParent().Update()
            self.GetParent().Refresh()

        wx.CallAfter(_do)

    def update_wire_length(self):
        self.length_ft_ctrl.SetLabel(str(round(self.wire_info.length_ft, 4)))
        self.length_m_ctrl.SetLabel(str(round(self.wire_info.length_m, 4)))
        self.length_cm_ctrl.SetLabel(str(round(self.wire_info.length_m * 100.0, 4)))
        self.voltage_drop_ctrl.SetLabel(str(round(self.wire_info.voltage_drop, 2)))
        self.recommended_awg_ctrl.SetLabel(str(self.wire_info.recommended_awg))

        mm2 = self.wire_info.recommended_mm2
        if mm2 is None:
            self.recommended_mm2_ctrl.SetLabel(str(mm2))
        else:
            self.recommended_mm2_ctrl.SetLabel(str(round(mm2, 4)))

        self.weight_lb_ctrl.SetLabel(str(round(self.wire_info.weight_lb, 4)))
        self.weight_kg_ctrl.SetLabel(str(round(self.wire_info.weight_kg, 4)))
        self.resistance_ctrl.SetLabel(str(round(self.wire_info.resistance, 4)))

    def update_wire(self):
        if self.wire_info is None:
            return

        self.set_wire(self.wire_info)

    def set_wire(self, wi: WireInfo):
        self.material_ctrl.SetStringSelection(wi.material)
        self.shielded_ctrl.SetSelection(int(wi.is_shielded))
        self.volts_ctrl.SetValue(wi.volts)
        self.volt_drop_ctrl.SetValue(wi.allowed_voltage_drop)
        self.conductor_ctrl.SetValue(wi.num_conductors)
        self.awg_ctrl.SetValue(wi.awg)
        self.mm2_ctrl.SetValue(wi.mm2)
        self.od_mm_ctrl.SetLabel(str(round(wi.od_mm, 4)))
        self.voltage_drop_ctrl.SetLabel(str(round(wi.voltage_drop, 2)))
        self.recommended_awg_ctrl.SetLabel(str(wi.recommended_awg))

        mm2 = wi.recommended_mm2
        if mm2 is None:
            self.recommended_mm2_ctrl.SetLabel(str(mm2))
        else:
            self.recommended_mm2_ctrl.SetLabel(str(round(mm2, 4)))

        self.conductivity_ctrl.SetLabel(str(round(wi.conductivity, 4)))
        self.resistivity_ctrl.SetLabel(str(round(wi.resistivity, 4)))
        self.diameter_mm_ctrl.SetLabel(str(round(wi.diameter_mm, 4)))
        self.diameter_inch_ctrl.SetLabel(str(round(wi.diameter_inch, 4)))
        self.in2_ctrl.SetLabel(str(round(wi.in2, 4)))
        self.length_ft_ctrl.SetLabel(str(round(wi.length_ft, 4)))
        self.length_m_ctrl.SetLabel(str(round(wi.length_m, 4)))
        self.length_cm_ctrl.SetLabel(str(round(wi.length_m * 100.0, 4)))
        self.length_cm_ctrl.SetLabel(str(round(wi.length_m * 100.0, 4)))
        self.weight_lb_ctrl.SetLabel(str(round(wi.weight_lb, 4)))
        self.weight_kg_ctrl.SetLabel(str(round(wi.weight_kg, 4)))
        self.resistance_ctrl.SetLabel(str(round(wi.resistance, 4)))
        self.color1_ctrl.SetColour(wi.color)
        self.color2_ctrl.SetColour(wi.stripe_color)

        self.wire_info = wi

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.wire_info: WireInfo = None

        material_choices = [item[1] for item in WireInfo.material_choices]
        material_ctrl = self.material_ctrl = wx.Choice(self, wx.ID_ANY, choices=material_choices)
        material_suffix_ctrl = self.material_suffix_ctrl = wx.StaticText(self, wx.ID_ANY, label='Ag/Cu')
        material_ctrl.Bind(wx.EVT_CHOICE, self.on_material)

        shielded_ctrl = self.shielded_ctrl = wx.Choice(self, wx.ID_ANY, choices=['No', 'Yes'])
        shielded_ctrl.Bind(wx.EVT_CHOICE, self.on_shielded)

        volts_ctrl = self.volts_ctrl = wx.SpinCtrlDouble(self, wx.ID_ANY, value='12.0', min=3.3, max=240.0, initial=12.0, inc=0.1)
        volts_ctrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_volts)

        load_ctrl = self.load_ctrl = wx.SpinCtrlDouble(self, wx.ID_ANY, value='0.0', min=0.0, max=300.0, initial=0.0, inc=0.1)
        load_ctrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_load)

        volt_drop_ctrl = self.volt_drop_ctrl = wx.SpinCtrlDouble(self, wx.ID_ANY, value='0.0', min=0.0, max=3.0, initial=0.0, inc=0.1)
        volt_drop_ctrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_volt_drop)

        conductor_ctrl = self.conductor_ctrl = wx.SpinCtrl(self, wx.ID_ANY, value='1', min=1, max=7, initial=1)
        conductor_ctrl.Bind(wx.EVT_SPINCTRL, self.on_conductor)

        awg_ctrl = self.awg_ctrl = wx.SpinCtrl(self, wx.ID_ANY, value='22', min=0, max=30, initial=22)
        awg_ctrl.Bind(wx.EVT_SPINCTRL, self.on_awg)

        mm2_ctrl = self.mm2_ctrl = wx.SpinCtrlDouble(self, wx.ID_ANY, value='0.3255', min=0.0509, max=53.4751, initial=0.3255, inc=0.0001)
        mm2_ctrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_mm2)

        color1_ctrl = self.color1_ctrl = wx.ColourPickerCtrl(self, wx.ID_ANY, size=(75, -1))
        color1_ctrl.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_color1)

        color2_ctrl = self.color2_ctrl = wx.ColourPickerCtrl(self, wx.ID_ANY, size=(75, -1))
        color2_ctrl.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_color2)

        od_mm_ctrl = self.od_mm_ctrl = wx.StaticText(self, wx.ID_ANY, label='0.0000')
        voltage_drop_ctrl = self.voltage_drop_ctrl = wx.StaticText(self, wx.ID_ANY, label='0.0000')
        recommended_awg_ctrl = self.recommended_awg_ctrl = wx.StaticText(self, wx.ID_ANY, label='00')
        recommended_mm2_ctrl = self.recommended_mm2_ctrl = wx.StaticText(self, wx.ID_ANY, label='00.0000')
        conductivity_ctrl = self.conductivity_ctrl = wx.StaticText(self, wx.ID_ANY, label='0.0000')
        resistivity_ctrl = self.resistivity_ctrl = wx.StaticText(self, wx.ID_ANY, label='0.0000')
        diameter_mm_ctrl = self.diameter_mm_ctrl = wx.StaticText(self, wx.ID_ANY, label='00.0000')
        diameter_inch_ctrl = self.diameter_inch_ctrl = wx.StaticText(self, wx.ID_ANY, label='0.0000')
        in2_ctrl = self.in2_ctrl = wx.StaticText(self, wx.ID_ANY, label='0.0000')
        length_ft_ctrl = self.length_ft_ctrl = wx.StaticText(self, wx.ID_ANY, label='000.0000')
        length_m_ctrl = self.length_m_ctrl = wx.StaticText(self, wx.ID_ANY, label='000.0000')
        length_cm_ctrl = self.length_cm_ctrl = wx.StaticText(self, wx.ID_ANY, label='000.0000')
        weight_lb_ctrl = self.weight_lb_ctrl = wx.StaticText(self, wx.ID_ANY, label='000.0000')
        weight_kg_ctrl = self.weight_kg_ctrl = wx.StaticText(self, wx.ID_ANY, label='000.0000')
        resistance_ctrl = self.resistance_ctrl = wx.StaticText(self, wx.ID_ANY, label='000.0000')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany((
            (HSizer(self, 'Material:', material_ctrl, material_suffix_ctrl), 0),
            (HSizer(self, 'Shielded:', shielded_ctrl), 0),
            (HSizer(self, 'Conductor Count:', conductor_ctrl), 0),
            (HSizer(self, 'Load:', load_ctrl, 'A'), 0),
            (HSizer(self, 'Length:', length_ft_ctrl, 'ft', in_panel=True), 0),
            (HSizer(self, 'Length:', length_m_ctrl, 'm', in_panel=True), 0),
            (HSizer(self, 'Length:', length_cm_ctrl, 'cm', in_panel=True), 0),
            (HSizer(self, 'Volts:', volts_ctrl, 'V'), 0),
            (HSizer(self, 'Max Drop:', volt_drop_ctrl, 'V'), 0),
            (HSizer(self, 'Actual Drop:', voltage_drop_ctrl, 'V', in_panel=True), 0),
            (HSizer(self, 'Size:', awg_ctrl, 'AWG'), 0),
            (HSizer(self, 'Size:', mm2_ctrl, 'mm²'), 0),
            (HSizer(self, 'Size:', in2_ctrl, 'in²'), 0),
            (HSizer(self, 'Primary Color:', color1_ctrl), 0),
            (HSizer(self, 'Stripe Color:', color2_ctrl), 0),
            (HSizer(self, 'Diameter (total):', od_mm_ctrl, 'mm'), 0),
            (HSizer(self, 'Recommended Size:', recommended_awg_ctrl, 'AWG', in_panel=True), 0),
            (HSizer(self, 'Recommended Size:', recommended_mm2_ctrl, 'mm²', in_panel=True), 0),
            (HSizer(self, 'Conductivity:', conductivity_ctrl, 'S/m'), 0),
            (HSizer(self, 'Resistivity:', resistivity_ctrl, '(Ω x mm2)/m'), 0),
            (HSizer(self, 'Conductor Diameter:', diameter_mm_ctrl, 'mm'), 0),
            (HSizer(self, 'Conductor Diameter:', diameter_inch_ctrl, 'in'), 0),
            (HSizer(self, 'Weight:', weight_lb_ctrl, 'lb', in_panel=True), 0),
            (HSizer(self, 'Weight:', weight_kg_ctrl, 'kg', in_panel=True), 0),
            (HSizer(self, 'Resistance:', resistance_ctrl, 'Ω', in_panel=True), 0)
        ))

        self.SetSizer(sizer)

#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  gui.py
#
#  This file is part of PySetWacom
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  PySetWacom is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  PySetWacom is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
# generated by wxGlade 0.9.3 on Mon Jan 20 20:58:31 2020
#

# stdlib
import os
import signal
import webbrowser

# 3rd party
import wx
from pubsub import pub
from domdf_wxpython_tools.validators import ValidatorBase

# this package
from PySetWacom.profile import get_profiles_list, Profile, profiles_dir


# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class GUI(wx.Frame):
	def __init__(self, *args, **kwds):
		# begin wxGlade: GUI.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.SetSize((500, 400))
		
		# Menu Bar
		self.GUI_menubar = wx.MenuBar()
		wxglade_tmp_menu = wx.Menu()
		self.GUI_menubar.menu_new_profile = wxglade_tmp_menu.Append(wx.ID_ANY, "New Profile", "")
		self.Bind(wx.EVT_MENU, self.on_menu_new_profile, id=self.GUI_menubar.menu_new_profile.GetId())
		self.GUI_menubar.menu_open_directory = wxglade_tmp_menu.Append(wx.ID_ANY, "Open Profiles Directory", "")
		self.Bind(wx.EVT_MENU, self.on_menu_open_directory, id=self.GUI_menubar.menu_open_directory.GetId())
		self.GUI_menubar.menu_delete_profile = wxglade_tmp_menu.Append(wx.ID_ANY, "Delete Profile", "")
		self.Bind(wx.EVT_MENU, self.on_menu_delete_profile, id=self.GUI_menubar.menu_delete_profile.GetId())
		self.GUI_menubar.menu_quit = wxglade_tmp_menu.Append(wx.ID_ANY, "Quit", "")
		self.Bind(wx.EVT_MENU, self.on_quit, id=self.GUI_menubar.menu_quit.GetId())
		self.GUI_menubar.Append(wxglade_tmp_menu, "PySetWacom")
		self.SetMenuBar(self.GUI_menubar)
		# Menu Bar end
		self.profile_choice = wx.Choice(self, wx.ID_ANY, choices=["", "New Profile"])
		self.devices_list = wx.ListBox(self, wx.ID_ANY, choices=[])
		self.buttons_list = wx.ListBox(self, wx.ID_ANY, choices=[])

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_CHOICE, self.on_profile_changed, self.profile_choice)
		self.Bind(wx.EVT_LISTBOX, self.on_device_changed, self.devices_list)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_button_edit, self.buttons_list)
		# end wxGlade
		
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		
		self.refresh_profiles_list()
		
		self.selected_device = None
		self.selected_profile = None
		
		# Create pubsub receiver to listen for TrayIcon changing the Profile
		pub.subscribe(self.tray_changed_profile, "tray_changed_profile")
		
		# Setup timer for listening to signal events
		signal.signal(signal.SIGUSR1, self.receive_signal)
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, lambda *args: None, self.timer)
		self.timer.Start(1000)

	def __set_properties(self):
		# begin wxGlade: GUI.__set_properties
		self.SetTitle("PySetWacom")
		self.profile_choice.SetSelection(0)
		self.devices_list.SetMinSize((200, 400))
		self.buttons_list.SetMinSize((400, 400))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: GUI.__do_layout
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		grid_sizer_1 = wx.BoxSizer(wx.VERTICAL)
		grid_sizer_2 = wx.FlexGridSizer(2, 2, 2, 5)
		profile_label = wx.StaticText(self, wx.ID_ANY, "Profile")
		grid_sizer_1.Add(profile_label, 0, wx.EXPAND, 0)
		grid_sizer_1.Add(self.profile_choice, 0, wx.ALL | wx.EXPAND, 0)
		devices_label = wx.StaticText(self, wx.ID_ANY, "Devices")
		grid_sizer_2.Add(devices_label, 0, wx.EXPAND, 0)
		buttons_label = wx.StaticText(self, wx.ID_ANY, "Buttons")
		grid_sizer_2.Add(buttons_label, 0, wx.EXPAND, 0)
		grid_sizer_2.Add(self.devices_list, 1, wx.EXPAND, 0)
		grid_sizer_2.Add(self.buttons_list, 1, wx.EXPAND, 0)
		grid_sizer_1.Add(grid_sizer_2, 1, wx.EXPAND, 0)
		sizer_1.Add(grid_sizer_1, 1, wx.ALL | wx.EXPAND, 5)
		self.SetSizer(sizer_1)
		self.Layout()
		# end wxGlade
	
	def receive_signal(self, signum, stack):
		print('My PID is:', os.getpid())
		print('Received:', signum)
		if signum == 10:
			self.Show()
	
	def tray_changed_profile(self, selected_profile):
		print(f"Tray Changed Profile To {selected_profile}")
		self.profile_choice.SetStringSelection(selected_profile)
		self.on_profile_changed()
	
	def OnClose(self, event):
		if event.CanVeto():
			event.Veto()
		self.Hide()
	
	def on_profile_changed(self, event=None):  # wxGlade: GUI.<event_handler>
		print(495)
		
		index = self.profile_choice.GetSelection()
		
		profile_name = self.profile_choice.GetString(index)
		
		# if self.selected_profile and (profile_name == self.selected_profile.name):
		# 	print(self.selected_profile.name)
		# 	print(profile_name)
		# 	return
		
		# Clear Devices and Buttons
		self.buttons_list.Clear()
		self.devices_list.Clear()
		
		if index == 0:
			pass
		elif index == 1:
			self.create_new_profile()
		else:
			self.load_profile(profile_name)
			pub.sendMessage("gui_changed_profile", selected_profile=self.selected_profile.name)
	
	def load_profile(self, profile_name):
		self.selected_profile = Profile.load(profile_name)
		
		for index, device in enumerate(self.selected_profile.devices):
			print(device)
			self.devices_list.Append(device.name)
	
	def refresh_profiles_list(self):
		self.profile_choice.Clear()
		
		self.profiles = get_profiles_list()
		# print(self.profiles)
		
		for profile in self.profiles:
			self.profile_choice.Append(profile)
	
	def on_device_changed(self, event):  # wxGlade: GUI.<event_handler>
		devices_list = event.GetEventObject()
		self.selected_device = self.selected_profile.devices[devices_list.GetSelection()]
		self.update_mapping_list()
		
		event.Skip()
	
	def update_mapping_list(self):
		self.buttons_list.Clear()
		print([str(button) for button in self.selected_device.buttons])
		self.buttons_list.AppendItems([str(button) for button in self.selected_device.buttons])
		self.buttons_list.Refresh()
	
	def on_button_edit(self, event):  # wxGlade: GUI.<event_handler>
		
		selection_index = event.GetEventObject().GetSelection()
		selected_button = self.selected_device._buttons[selection_index]
		
		with EditMappingDialog(self, self.selected_device.buttons[selection_index]) as dlg:
			if dlg.ShowModal() == wx.ID_APPLY:
				selected_button.mapping = dlg.combo_value.GetValue()
				self.update_mapping_list()
				self.buttons_list.SetSelection(selection_index)
				
				self.selected_profile.save()
				self.selected_profile.apply()
		
		event.Skip()
	
	def create_new_profile(self):
		# New Profile
		with wx.TextEntryDialog(self, "Profile Name", caption="New Profile") as dlg:
			textctrl = dlg.FindWindowById(3000)
			
			textctrl.SetValidator(NewProfileValidator(self.profiles))
			
			if dlg.ShowModal() == wx.ID_OK:
				self.selected_profile = Profile.new(dlg.GetValue())
				self.selected_profile.save()
				self.refresh_profiles_list()
			
			if self.selected_profile is None:
				self.profile_choice.SetSelection(0)
			else:
				idx = self.profiles.index(self.selected_profile.name)
				self.profile_choice.SetSelection(idx)
				self.load_profile(self.selected_profile.name)
				pub.sendMessage("new_profile_created", selected_profile=self.selected_profile.name)
	
	def on_menu_new_profile(self, event):  # wxGlade: GUI.<event_handler>
		self.create_new_profile()
		event.Skip()
	
	def on_menu_open_directory(self, event):  # wxGlade: GUI.<event_handler>
		webbrowser.open(str(profiles_dir))
		event.Skip()
	
	def on_menu_delete_profile(self, event):  # wxGlade: GUI.<event_handler>
		print("Event handler 'on_menu_delete_profile' not implemented!")
		event.Skip()
	
	def on_quit(self, event):  # wxGlade: GUI.<event_handler>
		print("Event handler 'on_quit' not implemented!")
		event.Skip()

# end of class GUI


class CaptureKeystrokeDialog(wx.Dialog):
	def __init__(self, *args, **kwds):
		# begin wxGlade: CaptureKeystrokeDialog.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetSize((200, 200))
		self.panel_1 = wx.Panel(self, wx.ID_ANY, style=wx.WANTS_CHARS)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade
		
		self.panel_1.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		self.panel_1.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
		
		self.keystrokes = []
		
	def __set_properties(self):
		# begin wxGlade: CaptureKeystrokeDialog.__set_properties
		self.SetTitle("Capture Key Combo")
		self.SetSize((200, 200))
		self.panel_1.SetBackgroundColour(wx.Colour(107, 142, 35))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: CaptureKeystrokeDialog.__do_layout
		grid_sizer_5 = wx.GridSizer(1, 1, 0, 0)
		grid_sizer_5.Add(self.panel_1, 1, wx.EXPAND, 0)
		self.SetSizer(grid_sizer_5)
		self.Layout()
		# end wxGlade
	
	def GetKeyCombo(self):
		return self.keystrokes
	
	def OnKeyUp(self, event):
		self.append_keystroke("-", event.KeyCode)
		
	def OnKeyDown(self, event):
		self.append_keystroke("+", event.KeyCode)
	
	def append_keystroke(self, prefix, code):
		print(code)
		
		if code in self.broken_keys:
			return
		
		if code in self.special_keys:
			keystroke = prefix + self.special_keys[code]
		else:
			#if prefix == "+":
			keystroke = prefix + chr(code).lower()
			# else:
			# 	return
		
		self.keystrokes.append(keystroke)

	broken_keys = {
			wx.WXK_RETURN,
			wx.WXK_NUMPAD_ENTER,
			# Super reads as Alt?
			wx.WXK_SPACE,
			309, # Menu? Key. Reads as j
			wx.WXK_INSERT,
			wx.WXK_HOME,
			wx.WXK_DELETE,
			wx.WXK_END,
			# Haven't tested numpad as don't have one
			}
	
	special_keys = {
			wx.WXK_CONTROL: "ctrl",
			wx.WXK_ALT: "alt",
			wx.WXK_SHIFT: "shift",
			# TODO: meta
			wx.WXK_UP: "up",
			wx.WXK_NUMPAD_UP: "up",
			wx.WXK_DOWN: "down",
			wx.WXK_NUMPAD_DOWN: "down",
			wx.WXK_LEFT: "left",
			wx.WXK_NUMPAD_LEFT: "left",
			wx.WXK_RIGHT: "right",
			wx.WXK_NUMPAD_RIGHT: "right",
			wx.WXK_BACK: "backspace",
			wx.WXK_ESCAPE: "esc",
			wx.WXK_TAB: "tab",
			wx.WXK_NUMPAD_TAB: "tab",
			wx.WXK_PAGEDOWN: "PgDn",
			wx.WXK_PAGEUP: "PgUp",
			wx.WXK_F1: "f1",
			wx.WXK_F2: "f2",
			wx.WXK_F3: "f3",
			wx.WXK_F4: "f4",
			wx.WXK_F5: "f5",
			wx.WXK_F6: "f6",
			wx.WXK_F7: "f7",
			wx.WXK_F8: "f8",
			wx.WXK_F9: "f9",
			wx.WXK_F10: "f10",
			wx.WXK_F11: "f11",
			wx.WXK_F12: "f12",
			wx.WXK_F13: "f13",
			wx.WXK_F14: "f14",
			wx.WXK_F15: "f15",
			wx.WXK_F16: "f16",
			wx.WXK_F17: "f17",
			wx.WXK_F18: "f18",
			wx.WXK_F19: "f19",
			wx.WXK_F20: "f20",
			wx.WXK_F21: "f21",
			wx.WXK_F22: "f22",
			wx.WXK_F23: "f23",
			wx.WXK_F24: "f24",
			# TODO: f25 to f35
			wx.WXK_WINDOWS_LEFT: "super",
			}

# end of class CaptureKeystrokeDialog


class EditMappingDialog(wx.Dialog):
	def __init__(
			self, parent, button_object, id=wx.ID_ANY,
			pos=wx.DefaultPosition, size=wx.DefaultSize,
			style=wx.DEFAULT_DIALOG_STYLE, name=wx.DialogNameStr):
				
		args = (parent, id)
		kwds = dict(pos=pos, size=size, style=style, name=name)
		self.button = button_object
		
		# begin wxGlade: EditMappingDialog.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.button_name = wx.StaticText(self, wx.ID_ANY, "Button Name")
		self.combo_value = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE)
		self.button_notebook = wx.Notebook(self, wx.ID_ANY)
		self.keyboard_tab = wx.Panel(self.button_notebook, wx.ID_ANY)
		self.control_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Control")
		self.alt_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Alt")
		self.delete_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Delete")
		self.shift_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Shift")
		self.super_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Super")
		self.left_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Left")
		self.right_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Right")
		self.up_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Up")
		self.down_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Down")
		self.backspace_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Backspace")
		self.pgup_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Page Up")
		self.pgdown_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Page Down")
		self.home_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Home")
		self.end_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "End")
		self.esc_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Esc")
		self.hyper_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Hyper")
		self.meta_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Meta")
		self.tab_button = wx.Button(self.keyboard_tab, wx.ID_ANY, "Tab")
		self.mouse_tab = wx.Panel(self.button_notebook, wx.ID_ANY)
		self.lmb_button = wx.Button(self.mouse_tab, wx.ID_ANY, "Left Click")
		self.mmb_button = wx.Button(self.mouse_tab, wx.ID_ANY, "Middle Click")
		self.rmb_button = wx.Button(self.mouse_tab, wx.ID_ANY, "Right Click")
		self.scroll_up_button = wx.Button(self.mouse_tab, wx.ID_ANY, "Scroll Up")
		self.scroll_down_button = wx.Button(self.mouse_tab, wx.ID_ANY, "Scroll Down")
		self.scroll_right_button = wx.Button(self.mouse_tab, wx.ID_ANY, "Scroll Right")
		self.scroll_left_button = wx.Button(self.mouse_tab, wx.ID_ANY, "Scroll Left")
		self.mouse_back_button = wx.Button(self.mouse_tab, wx.ID_ANY, "Back")
		self.mouse_forward_button = wx.Button(self.mouse_tab, wx.ID_ANY, "Forward")
		self.capture_combo_button = wx.Button(self, wx.ID_ANY, "Capture Key Combo")
		self.clear_button = wx.Button(self, wx.ID_ANY, "Clear Combo")

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self.on_add_control, self.control_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_alt, self.alt_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_delete, self.delete_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_shift, self.shift_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_super, self.super_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_left, self.left_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_right, self.right_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_up, self.up_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_down, self.down_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_backspace, self.backspace_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_pgup, self.pgup_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_pgdown, self.pgdown_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_home, self.home_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_end, self.end_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_esc, self.esc_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_hyper, self.hyper_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_meta, self.meta_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_tab, self.tab_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_lmb, self.lmb_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_mmb, self.mmb_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_rmb, self.rmb_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_scroll_up, self.scroll_up_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_scroll_down, self.scroll_down_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_scroll_right, self.scroll_right_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_scroll_left, self.scroll_left_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_mouse_back, self.mouse_back_button)
		self.Bind(wx.EVT_BUTTON, self.on_add_mouse_forward, self.mouse_forward_button)
		self.Bind(wx.EVT_BUTTON, self.on_grab_combo, self.capture_combo_button)
		self.Bind(wx.EVT_BUTTON, self.on_clear_combo, self.clear_button)
		# end wxGlade
	
		self.combo_value.SetValue(self.button.mapping)
		self.combo_value.SetFocus()
		
	def __set_properties(self):
		# begin wxGlade: EditMappingDialog.__set_properties
		self.SetTitle("Edit Mapping")
		self.button_name.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Ubuntu"))
		self.control_button.SetMinSize((90, -1))
		self.alt_button.SetMinSize((90, -1))
		self.delete_button.SetMinSize((90, -1))
		self.shift_button.SetMinSize((90, -1))
		self.super_button.SetMinSize((90, -1))
		self.left_button.SetMinSize((90, -1))
		self.right_button.SetMinSize((90, -1))
		self.up_button.SetMinSize((90, -1))
		self.down_button.SetMinSize((90, -1))
		self.backspace_button.SetMinSize((90, -1))
		self.pgup_button.SetMinSize((90, -1))
		self.pgdown_button.SetMinSize((90, -1))
		self.home_button.SetMinSize((90, -1))
		self.end_button.SetMinSize((90, -1))
		self.esc_button.SetMinSize((90, -1))
		self.hyper_button.SetMinSize((90, -1))
		self.meta_button.SetMinSize((90, -1))
		self.tab_button.SetMinSize((90, -1))
		self.lmb_button.SetMinSize((90, -1))
		self.mmb_button.SetMinSize((90, -1))
		self.rmb_button.SetMinSize((90, -1))
		self.scroll_up_button.SetMinSize((90, -1))
		self.scroll_down_button.SetMinSize((90, -1))
		self.scroll_right_button.SetMinSize((90, -1))
		self.scroll_left_button.SetMinSize((90, -1))
		self.mouse_back_button.SetMinSize((90, -1))
		self.mouse_forward_button.SetMinSize((90, -1))
		# end wxGlade
		
		self.SetTitle(f'Edit Mapping for button "{self.button.id}"')
		self.Bind(wx.EVT_BUTTON, self.OnApply, id=wx.ID_APPLY)

	def __do_layout(self):
		# begin wxGlade: EditMappingDialog.__do_layout
		outer_sizer = wx.BoxSizer(wx.VERTICAL)
		main_sizer = wx.BoxSizer(wx.VERTICAL)
		btn_sizer = wx.GridSizer(1, 2, 0, 0)
		grid_sizer_4 = wx.GridBagSizer(2, 2)
		grid_sizer_3 = wx.GridBagSizer(2, 2)
		main_sizer.Add(self.button_name, 0, 0, 0)
		main_sizer.Add(self.combo_value, 2, wx.ALL | wx.EXPAND, 2)
		grid_sizer_3.Add(self.control_button, (0, 0), (1, 1), 0, 0)
		grid_sizer_3.Add(self.alt_button, (0, 1), (1, 1), 0, 0)
		grid_sizer_3.Add(self.delete_button, (0, 2), (1, 1), 0, 0)
		grid_sizer_3.Add(self.shift_button, (0, 3), (1, 1), 0, 0)
		grid_sizer_3.Add(self.super_button, (0, 4), (1, 1), 0, 0)
		grid_sizer_3.Add(self.left_button, (1, 0), (1, 1), 0, 0)
		grid_sizer_3.Add(self.right_button, (1, 1), (1, 1), 0, 0)
		grid_sizer_3.Add(self.up_button, (1, 2), (1, 1), 0, 0)
		grid_sizer_3.Add(self.down_button, (1, 3), (1, 1), 0, 0)
		grid_sizer_3.Add(self.backspace_button, (1, 4), (1, 1), 0, 0)
		grid_sizer_3.Add(self.pgup_button, (2, 0), (1, 1), 0, 0)
		grid_sizer_3.Add(self.pgdown_button, (2, 1), (1, 1), 0, 0)
		grid_sizer_3.Add(self.home_button, (2, 2), (1, 1), 0, 0)
		grid_sizer_3.Add(self.end_button, (2, 3), (1, 1), 0, 0)
		grid_sizer_3.Add(self.esc_button, (2, 4), (1, 1), 0, 0)
		grid_sizer_3.Add(self.hyper_button, (3, 0), (1, 1), 0, 0)
		grid_sizer_3.Add(self.meta_button, (3, 1), (1, 1), 0, 0)
		grid_sizer_3.Add(self.tab_button, (3, 2), (1, 1), 0, 0)
		self.keyboard_tab.SetSizer(grid_sizer_3)
		grid_sizer_4.Add(self.lmb_button, (0, 0), (1, 1), 0, 0)
		grid_sizer_4.Add(self.mmb_button, (0, 1), (1, 1), 0, 0)
		grid_sizer_4.Add(self.rmb_button, (0, 2), (1, 1), 0, 0)
		grid_sizer_4.Add(self.scroll_up_button, (0, 3), (1, 1), 0, 0)
		grid_sizer_4.Add(self.scroll_down_button, (0, 4), (1, 1), 0, 0)
		grid_sizer_4.Add(self.scroll_right_button, (1, 0), (1, 1), 0, 0)
		grid_sizer_4.Add(self.scroll_left_button, (1, 1), (1, 1), 0, 0)
		grid_sizer_4.Add(self.mouse_back_button, (1, 2), (1, 1), 0, 0)
		grid_sizer_4.Add(self.mouse_forward_button, (1, 3), (1, 1), 0, 0)
		self.mouse_tab.SetSizer(grid_sizer_4)
		self.button_notebook.AddPage(self.keyboard_tab, "Keyboard")
		self.button_notebook.AddPage(self.mouse_tab, "Mouse")
		main_sizer.Add(self.button_notebook, 3, wx.EXPAND, 0)
		btn_sizer.Add(self.capture_combo_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 5)
		btn_sizer.Add(self.clear_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 5)
		main_sizer.Add(btn_sizer, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
		outer_sizer.Add(main_sizer, 1, wx.ALL | wx.EXPAND, 5)
		self.SetSizer(outer_sizer)
		outer_sizer.Fit(self)
		self.Layout()
		# end wxGlade
		
		self.btns = self.CreateStdDialogButtonSizer(wx.APPLY | wx.CANCEL)
		outer_sizer.Add(self.btns, 0, wx.BOTTOM | wx.EXPAND, 5)
	
	def OnApply(self, event):
		self.EndModal(wx.ID_APPLY)
	
	def add_special_key(self, spl_key_str):
		# Possible values
		# KEY: MODIFIER, SPECIALKEY or ASCIIKEY
		# MODIFIER: (each can be prefix with an l or an r for the left / right modifier (no prefix = left)
		# ctrl = ctl = control, meta, alt, shift, super, hyper
		# SPECIALKEY: f1 - f35, esc = Esc, up, down, left, right, backspace = Backspace, tab, PgUp, PgDn
		# ASCIIKEY: (usual characters the key produces, e.g.a, b, c, 1, 2, 3 etc.)
		
		self.combo_value.WriteText(f"key +{spl_key_str}  key -{spl_key_str} ")
		self.combo_value.SetInsertionPoint(self.combo_value.GetInsertionPoint() - len(spl_key_str) - 3)
		self.combo_value.SetFocus()
	
	def add_button(self, button_id):
		self.combo_value.WriteText(f"button +{button_id} ")
		self.combo_value.SetFocus()
	
	def on_add_control(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("ctrl")
		event.Skip()

	def on_add_alt(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("alt")
		event.Skip()
	
	def on_add_delete(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("delete")
		event.Skip()

	def on_add_shift(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("shift")
		event.Skip()
		
	def on_add_left(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("left")
		event.Skip()
		
	def on_add_right(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("right")
		event.Skip()
		
	def on_add_pgup(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("PgUp")
		event.Skip()

	def on_add_up(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("up")
		event.Skip()

	def on_add_down(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("down")
		event.Skip()

	def on_add_pgdown(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("PgDn")
		event.Skip()

	def on_add_home(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		print("Event handler 'on_add_home' not implemented!")
		event.Skip()

	def on_add_end(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		print("Event handler 'on_add_end' not implemented!")
		event.Skip()

	def on_add_super(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		print("Event handler 'on_add_super' not implemented!")
		event.Skip()

	def on_grab_combo(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		with CaptureKeystrokeDialog(self) as dlg:
			if dlg.ShowModal():
				self.combo_value.WriteText(" ".join(dlg.GetKeyCombo()))
		
		self.combo_value.SetFocus()

	def on_add_backspace(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("backspace")
		event.Skip()
		
	def on_add_hyper(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("hyper")
		event.Skip()
		
	def on_add_meta(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("meta")
		event.Skip()
		
	def on_add_esc(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_special_key("esc")
		event.Skip()
		
	def on_add_lmb(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_button(1)
		event.Skip()
		
	def on_add_rmb(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_button(3)
		event.Skip()
		
	def on_add_mmb(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_button(2)
		event.Skip()
		
	def on_add_scroll_up(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_button(4)
		event.Skip()
		
	def on_add_scroll_down(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_button(5)
		event.Skip()
	
	def on_add_scroll_right(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_button(7)
		event.Skip()
		
	def on_add_scroll_left(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_button(6)
		event.Skip()
		
	def on_add_mouse_back(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_button(8)
		event.Skip()
		
	def on_add_mouse_forward(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.add_button(9)
		event.Skip()
		
	def on_add_tab(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		print("Event handler 'on_add_tab' not implemented!")
		event.Skip()
		
	def on_clear_combo(self, event):  # wxGlade: EditMappingDialog.<event_handler>
		self.combo_value.Clear()
		self.combo_value.SetFocus()
		event.Skip()
# end of class EditMappingDialog


class app(wx.App):
	def OnInit(self):
		self.GUI = GUI(None, wx.ID_ANY, "")
		self.SetTopWindow(self.GUI)
		# self.GUI.Show()
		return True
	
	def Show(self, show=True):
		self.GUI.Show(show)
	

# end of class app


class NewProfileValidator(ValidatorBase):
	""" This validator is used to ensure that the user has entered something
		into the text object editor dialog's text field.
	"""
	
	def __init__(self, existing_profiles):
		"""
		Standard constructor.
		"""
		
		ValidatorBase.__init__(self)
		self.existing_profiles = existing_profiles
	
	def Clone(self):
		"""
		Standard cloner.

		Note that every validator must implement the Clone() method.
		"""
		return self.__class__(self.existing_profiles)
	
	def Validate(self, win):
		"""
		Validate the contents of the given text control.
		"""
		
		text = self.GetWindow().GetValue()
		if len(text) == 0:
			wx.MessageBox("Please enter a name for the Profile!", "Error", style=wx.ICON_ERROR)
			return self.set_warning()
		elif text in self.existing_profiles:
			wx.MessageBox("A Profile with that name already exists!\nPlease choose a unique name.", "Error",
							   style=wx.ICON_ERROR)
			return self.set_warning()
		else:
			return self.reset_ctrl()

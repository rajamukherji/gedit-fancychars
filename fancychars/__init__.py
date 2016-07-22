import os
from gi.repository import GObject, Gedit, Gdk, Gtk, Gio

cycles = {}
combos = {}
max_combo = 0

class FancyCharsPluginApp(GObject.GObject, Gedit.AppActivatable):
	__gtype_name__ = "FancyCharsPluginApp"
	
	app = GObject.property(type = Gedit.App)

	def __init__(self):
		GObject.Object.__init__(self)
		self.cycles_path = os.path.join(os.path.dirname(__file__), 'cycles.txt')
		self.combos_path = os.path.join(os.path.dirname(__file__), 'combos.txt')
		self.cycles_file = Gio.File.new_for_path(self.cycles_path)
		self.combos_file = Gio.File.new_for_path(self.combos_path)

	def do_activate(self):
		print("Plugin created for", self.app)
		self.reload()
		self.monitor = Gio.File.new_for_path(os.path.dirname(__file__)).monitor(0, None)
		self.monitor.connect("changed", self.reload)
		action = Gio.SimpleAction(name = "fancychars")
		action.connect('activate', self.edit)
		self.app.add_action(action)
		self.menu_ext = self.extend_menu("preferences-section")
		item = Gio.MenuItem.new(_("Fancy Chars Editor"), "app.fancychars")
		self.menu_ext.append_menu_item(item)

	def do_deactivate(self):
		print("Plugin stopped for", self.app)
		pass

	def do_update_state(self):
		pass
	
	def reload(self, *args):
		global cycles, combos, max_combo
		cycles = {}
		combos = {}
		max_combo = 0
		for line in open(self.combos_path, "r"):
			line = line.strip().split(" ")
			combos[line[0]] = line[1]
			max_combo = max(max_combo, len(line[0]))
			cycles[line[1]] = line[0]
		for line in open(self.cycles_path, "r"):
			line = line.strip().split(" ")
			for i in range(len(line) - 1):
				cycles[line[i]] = line[i + 1]
			cycles[line[-1]] = line[0]
		print(cycles)
		print(combos)
	
	def edit(self, *args):
		window = self.app.get_active_window()
		window.create_tab_from_location(self.combos_file, None, 1, 1, False, True)
		window.create_tab_from_location(self.cycles_file, None, 1, 1, False, True)

class FancyCharsPluginView(GObject.GObject, Gedit.ViewActivatable):
	__gtype_name__ = "FancyCharsPluginView"
	
	view = GObject.property(type = Gedit.View)
	
	def __init__(self):
		GObject.Object.__init__(self)
		self.chars = ""
	
	def do_activate(self):
		self.view.connect("key-press-event", self.on_key_press)
		self.buffer = self.view.get_buffer()
		self.cursor = self.buffer.get_insert()
	
	def do_deactivate(self):
		pass
	
	def do_update_state(self):
		pass
	
	def on_key_press(self, view, event):
		if event.is_modifier: return False
		keyval = event.keyval
		unicode = Gdk.keyval_to_unicode(keyval)
		buffer = self.buffer
		cursor = self.cursor
		if keyval in (Gdk.KEY_Up, Gdk.KEY_Down, Gdk.KEY_Left, Gdk.KEY_Right):
			self.chars = ""
		elif keyval == Gdk.KEY_Tab:
			for i in range(0, len(self.chars)):
				cycle = cycles.get(self.chars[i :])
				if cycle is not None:
					start = buffer.get_iter_at_mark(cursor)
					end = start.copy()
					start.backward_chars(len(self.chars) - i)
					self.chars = cycle
					buffer.delete(start, end)
					chars = self.chars.encode()
					buffer.insert(start, self.chars, len(chars))
					return True
		elif event.state & Gdk.ModifierType.CONTROL_MASK:
			self.chars = ""
		elif unicode == 0:
			return False
		elif 0 < unicode <= 32:
			self.chars = ""
		else:
			self.chars += chr(unicode)
			if len(self.chars) > max_combo:
				self.chars = self.chars[-max_combo :]
			for i in range(0, len(self.chars)):
				combo = combos.get(self.chars[i :])
				if combo is not None:
					start = buffer.get_iter_at_mark(cursor)
					end = start.copy()
					start.backward_chars(len(self.chars) - i - 1)
					self.chars = combo
					buffer.delete(start, end)
					chars = self.chars.encode()
					buffer.insert(start, self.chars, len(chars))
					return True
		return False

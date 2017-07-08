'''
textbox.py
'''

import libtcodpy as libtcod

'''
====================
Textbox
====================

A textbox that:
	<> can be opened from another program,
	<> allows the user to type text, which is persistant between update calls,
	<> has a separation between the interface and the backend,
	<> self.update() returns None every cycle, until the Enter key is pressed,
	   upon which it returns the string value of the text.
	<> uses the libtcodpy API, but could be easily modified to use another API
'''

class Textbox:
	def __init__(self,width,height):
		self.width = width
		self.height = height

		self._isActive = True
		self.text = ''

		self.window = libtcod.console_new(self.width,self.height)

	def update(self,console,x,y,color):
		if self._isActive == True:
			
			# get input
			key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)

			if key.vk != libtcod.KEY_NONE or key.c != libtcod.KEY_NONE:
				if key.vk == libtcod.KEY_ENTER:
				
					return self.enter()

				elif key.vk == libtcod.KEY_BACKSPACE:
					self.backspace()

				elif key.c:
					if len(self.text) < self.width:
						self.text += (str(chr(key.c)))

		self.render(console,x,y,color)

		return None


	def render(self,console,x,y,color):
		libtcod.console_set_default_foreground(self.window, color)

		libtcod.console_print_ex(self.window, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, self.text)

		libtcod.console_blit(self.window, 0, 0, self.width, self.height, 0, x, y, 1.0, 1.0)

		libtcod.console_flush()
		libtcod.console_clear(self.window)

	def clear(self):
		# clears the textbox, in case you need the textbox to clear if you click outside the box etc.
		self.text = ''

	def enter(self):
		# deletes the console, then returns the text
		libtcod.console_delete(self.window)

		return self.text

	def backspace(self):
		# delete the last character of the string
		if len(self.text) > 0:
			self.text = self.text[:-1]

	def activate(self):
		self._isActive = True
	def deactivate(self):
		self._isActive = False
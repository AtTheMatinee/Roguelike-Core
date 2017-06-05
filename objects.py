'''
objects.py
'''

'''
====================
Objects
====================
'''
import libtcodpy as libtcod
import math

class Object(object):
	def __init__(self, game, x, y, char, name, color, blocks=False):
		self.game = game
		self.x = x
		self.y = y
		self.char = char
		self.name = name
		self.color = color
		self.blocks = blocks

		self.game.addObject(self)
		self.game._currentLevel.addObject(self)
		self.renderFirst()
		if self.blocks == True:
			self.game._currentLevel.setHasObjectTrue(x,y)

	def draw(self):
		if libtcod.map_is_in_fov(self.game.map.fov_map, self.x, self.y):

			libtcod.console_set_default_foreground(self.game.ui.con, self.color)
			libtcod.console_put_char(self.game.ui.con, self.x, self.y, self.char, libtcod.BKGND_NONE)


	def clear(self):
		if libtcod.map_is_in_fov(self.game.map.fov_map, self.x, self.y):
			libtcod.console_put_char_ex(self.game.ui.con, self.x, self.y, '.', self.game.ui.color_light_ground_fore, self.game.ui.color_light_ground_back)

	def distanceTo(self,object):
		dx = object.x-self.x
		dy = object.y-self.y
		return math.sqrt(dx**2 + dy**2)

	def getNearbyActors(self):
		nearbyActors = []
		for actor in self.game._currentLevel._actors:
			if distanceTo(actor) <= 10:
				nearbyActors.append(actor)
		return nearbyActors

	def getNearbyObjects(self):
		nearbyObjects = []
		for obj in self.game._currentLevel._objects:
			if distanceTo(obj) <= 10:
				nearbyObjects.append(obj)
		return nearbyObjects

	def renderFirst(self):
		# Useful for making sure that actors render on top of objects
		self.game._currentLevel._objects.remove(self)
		self.game._currentLevel._objects.insert(0,self)

class Container(Object):
	def __init__(self, game, x, y, char, name, color, cache = [], blocks=False):
		self.game = game
		self.x = x
		self.y = y
		self.char = char
		self.name = name
		self.color = color
		self.cache = cache
		self.blocks = blocks

		self.game.addObject(self)
		self.game._currentLevel.addObject(self)
		self.renderFirst()
		if self.blocks == True:
			self.game._currentLevel.setHasObjectTrue(x,y)

class Corpse(Container):
	pass
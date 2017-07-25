'''
objectClass.py
'''
import libtcodpy as libtcod
import math
'''
====================
Object
====================
'''

class Object(object):
	identified = True
	def __init__(self, game, x, y, char, name, color, blocks=False, properNoun = False, alwaysVisible = False):
		self.game = game
		self.x = x
		self.y = y
		self.char = char
		self.name = name
		self.color = color
		self.blocks = blocks
		self.properNoun = properNoun
		self.alwaysVisible = alwaysVisible

		self.game.addObject(self)
		self.game._currentLevel.addObject(self)

		if self.blocks == True:
			self.game._currentLevel.setHasObjectTrue(x,y)

	def tick(self):
		pass

	def draw(self):
		if (libtcod.map_is_in_fov(self.game.map.fov_map, self.x, self.y) or
			(self.alwaysVisible == True) and self.game._currentLevel.getHasBeenExplored(self.x,self.y)):

			libtcod.console_set_default_foreground(self.game.ui.con, self.color)
			libtcod.console_put_char(self.game.ui.con, self.x, self.y, self.char, libtcod.BKGND_NONE)

	def clear(self):
		if libtcod.map_is_in_fov(self.game.map.fov_map, self.x, self.y):
			libtcod.console_put_char_ex(self.game.ui.con, self.x, self.y, '.', self.game.ui.color_light_ground_fore, self.game.ui.color_light_ground_back)

	def getName(self,useDefiniteArticle,showLevel = False):
		name = self.name
		if useDefiniteArticle == True and self.properNoun == False:
			name = "the "+name
		return name

	def distanceTo(self,object):
		dx = object.x-self.x
		dy = object.y-self.y
		return math.sqrt(dx**2 + dy**2)

	def distance(self,x,y):
		dx = x-self.x
		dy = y-self.y
		return math.sqrt(dx**2 + dy**2)

	def chessboardDistance(self,x,y):
		return max(abs(self.x-x), abs(self.y-y))

	def getNearbyActors(self):
		nearbyActors = []
		for actor in self.game._currentLevel._actors:
			if (actor != self) and (self.distanceTo(actor) <= 10):
				nearbyActors.append(actor)
		return nearbyActors

	def getNearbyObjects(self):
		nearbyObjects = []
		for obj in self.game._currentLevel._objects:
			if (obj != self) and (self.distanceTo(obj) <= 10):
				nearbyObjects.append(obj)
		return nearbyObjects

	def renderFirst(self):
		# Useful for making sure that actors render on top of objects
		self.game._currentLevel._objects.remove(self)
		self.game._currentLevel._objects.insert(0,self)

	def takeDamage(self, damage):
		# damage = [physical, armorPenetration, fire, frost, poison, bleed, holy, unholy, unblockable]
		pass

	def saveData(self):
		data = {
		'dataType':'Object',
		'class':self.__class__,
		'x':self.x,
		'y':self.y,
		'char':self.char,
		'name':self.name,
		'color':self.color,
		'blocks':self.blocks,
		'properNoun':self.properNoun,
		'alwaysVisible':self.alwaysVisible,
		}

		return data

	def loadData(self,data):
		self.game._currentLevel.setHasObjectFalse(self.x, self.y)
		self.x = data['x']
		self.y = data['y']
		self.char = data['char']
		self.name = data['name']
		self.color = data['color']
		self.blocks = data['blocks']
		self.properNoun = data['properNoun']
		self.alwaysVisible = data['alwaysVisible']
		return True

'''
objects.py
'''

'''
====================
Objects
====================
'''
import libtcodpy as libtcod
import random
import statusEffects
from objectClass import Object
import actors 


class Stairs(Object):
	def __init__(self, game, x, y, char, name, color, destination, blocks=False, properNoun = False, alwaysVisible = False):
		Object.__init__(self, game, x, y, char, name, color, alwaysVisible = True)
		self.destination = destination
		self.renderFirst()

	def saveData(self):
		data = Object.saveData(self)
		data['destination'] = self.destination

		return data

	def loadData(self,data):
		Object.loadData(self,data)
		self.destination = data['destination']
		return True


class Door(Object):
	def __init__(self, game, x, y, char, name, color, blocks=False, properNoun = False, alwaysVisible = False):
		Object.__init__(self, game, x, y, char, name, color, blocks)
		self.renderFirst()
	pass


class Container(Object):
	def __init__(self, game, x, y, char, name, color, cache = [], blocks=False, properNoun = False, alwaysVisible = False):
		Object.__init__(self, game, x, y, char, name, color, blocks=False)
		self.cache = cache
		self.renderFirst()


class Corpse(Container):
	def __init__(self, game, x, y, char, name, color, blocks=False, properNoun = False, alwaysVisible = False):
		Object.__init__(self, game, x, y, char, name, color, blocks=False)
		self.renderFirst()
	pass


class Pool(Object):
	def __init__(self, game, x, y, name, color, blocks=False, properNoun = False, alwaysVisible = False):
		char = '~'
		Object.__init__(self, game, x, y, char, name, color, blocks)
		self.renderFirst()

	def tick(self):
		if self.game._currentLevel.getHasObject(self.x, self.y) == True:
			for actor in self.game._currentLevel._actors:
				if actor.x == self.x and actor.y == self.y:
					# apply wet status effect to actor
					actor.addStatusEffect(statusEffects.Wet,15,False)

class Fire(Object):
	def __init__(self,game,x,y,name,color):
		self.baseColor = color
		self.charList = ['&','&','&','&','&','&','&','&',';',"'","`",' ']
		self.charIndex = 0
		self.animationFrameCounter = random.randint(0, 60)

		Object.__init__(self, game, x, y, self.charList[0], name, color)
		self.renderFirst()

	def tick(self):
		# effect objects within the explosion		
		for obj in self.game._currentLevel._objects:
			if obj != self and (obj.x == self.x) and (obj.y == self.y):
				obj.takeDamage([0,0,4,0,0,0,0,0,0])
				if isinstance(obj, Pool):
					self.game.removeObject(self)
					self.game._currentLevel.removeObject(self)

	def draw(self):
		if (libtcod.map_is_in_fov(self.game.map.fov_map, self.x, self.y) or
			(self.alwaysVisible == True) and self.game._currentLevel.getHasBeenExplored(self.x,self.y)):

			self.animationFrameCounter = (self.animationFrameCounter+1) % 90
			if self.animationFrameCounter == 0:
				# Advance the animation indices
				self.charIndex = (self.charIndex+1) % len(self.charList)

				# Advance the animation frames
				self.char = self.charList[self.charIndex]
				self.color = self.baseColor * (0.75 + (random.random()/2))

			libtcod.console_set_default_foreground(self.game.ui.con, self.color)
			libtcod.console_put_char(self.game.ui.con, self.x, self.y, self.char, libtcod.BKGND_NONE)

		elif self.charIndex != 0: 
			self.charIndex = 0

	def takeDamage(self,damage):
		phyDam = damage[0]
		fireDam = damage[2]
		frostDam = damage[3]
		if phyDam > fireDam or frostDam > fireDam:
			self.game.removeObject(self)
			self.game._currentLevel.removeObject(self)

class Explosion(Object):
	def __init__(self, game, x, y, color, damage, volume):
		name = 'explosion'
		char = ' '
		Object.__init__(self, game, x, y, char, name, color, blocks = False)
		self.damage = damage
		self.volume = volume

		self.explode()

	def explode(self):
		self.game._currentLevel.removeObject(self)

		cells = self.expand(self.x, self.y)

		# render the explosion (this will change drasticly after particle effects are implemented)
		for cell in cells:
			x,y = cell

			if libtcod.map_is_in_fov(self.game.map.fov_map,x,y):
				libtcod.console_set_char_background(self.game.ui.con, x, y, self.color, flag=libtcod.BKGND_SET)

		# Damage objects within the explosion		
		for obj in self.game._currentLevel._objects:
			if (obj.x,obj.y) in cells:
				obj.takeDamage(self.damage)

	def expand(self,x,y):
		# Expand the explosion out from the origin
		origin = (x,y)
		cells = set([origin])

		for i in xrange(20): # this could be 'while True:' but I wanted a definite exit point if the explosion is too large
			toBeExpanded = set()
			toBeExpanded.update(cells)
			while toBeExpanded:
				cell = toBeExpanded.pop()
				x,y = cell
				openCells = self.getNeighboringCells(x,y)
				for temp in openCells:
					if len(cells) < self.volume:
						cells.add(temp)
					else:
						return cells

	def getNeighboringCells(self,x,y):
		openCells = set()
		# check to see if the cells in the 8 directions around (x,y) are open
		for dx in xrange(-1,2):
			for dy in xrange(-1,2):
				tempX = x+dx
				tempY = y+dy

				if self.game._currentLevel.getBlocksMovement(tempX,tempY) == False:
					openCells.add((tempX,tempY))

		return openCells


class Cloud(Object):
	def __init__(self, game, x, y, name, color, volume, blocks=False, properNoun = False, alwaysVisible = False):
		char = ' '
		Object.__init__(self, game, x, y, char, name, color, blocks)
		self.volume = volume
		self.renderFirst()
		self.canExplode = False

		self.diffusionRate = .1 # percent of the gass volume that is dissapated each tick
		self.minThreshold = 0.3 # minimum value before a cell is removed from the list
		self.cells = {(self.x,self.y): self.volume}

		self.blocksSight = False


	def tick(self):
		# remove the cloud object it it has completely dissapated
		if len(self.cells) < 1:
			self.game._currentLevel.removeObject(self)
			return

		toBeDiffused = {}
		toBeDiffused.update(self.cells)
		while toBeDiffused:
			cell = toBeDiffused.popitem()
			x,y = cell[0]
			# get adjacent cells
			openCells = self.getNeighboringCells(x,y)
			for tempCell in openCells:
				if tempCell in self.cells:
					# move volume from high volume to low volume
					if cell[1] > self.cells[tempCell]:
						self.cells[tempCell] += (self.diffusionRate*cell[1])

				else:
					self.cells[tempCell] = (self.diffusionRate*cell[1])

				self.cells[cell[0]] -= (self.diffusionRate*cell[1]/1.5)

		# remove the cells that are below the threshold
		tempCells = {}
		tempCells.update(self.cells)
		for cell in tempCells:
			if self.cells[cell] <= self.minThreshold:
				x,y = cell
				if self.blocksSight == True:
					self.game._currentLevel.setBlocksSightFalse(x,y)
				# remove the cell
				self.cells.pop(cell)

		# effect objects within the cloud		
		for obj in self.game._currentLevel._objects:
			if obj != self and (obj.x,obj.y) in self.cells:
				self.hitEffect(obj)

		if self.blocksSight == True:
			self.game.map.initializeFOV(self.game._currentLevel)

	def getNeighboringCells(self,x,y):
		openCells = set()
		# check to see if the cells in the 8 directions around (x,y) are open
		for dx in xrange(-1,2):
			for dy in xrange(-1,2):
				tempX = x+dx
				tempY = y+dy

				if self.game._currentLevel.getBlocksMovement(tempX,tempY) == False:
					openCells.add((tempX,tempY))

		return openCells

	def draw(self):
		for cell in self.cells:
			x,y = cell
			if self.blocksSight == True:
				self.game._currentLevel.setBlocksSightTrue(x,y)

			color = self.color*self.cells[cell]
			if libtcod.map_is_in_fov(self.game.map.fov_map,x,y):
				libtcod.console_set_char_background(self.game.ui.con, x, y, color, flag=libtcod.BKGND_SET)

	def hitEffect(self,actor):
		pass

	def takeDamage(self,damage):
		# Explodes if it takes fire damage
		if self.canExplode == True and damage[2] >= 1: # if the cloud takes fire damage
			self.canExplode = False
			for cell in self.cells:
				x,y = cell
				Explosion(self.game,x,y,libtcod.flame,[5,0,2,0,0,0,0,0,0],5)
				self.cells[cell] = 0


class WaterCloud(Cloud):
	def hitEffect(self,actor):
		actor.addStatusEffect(statusEffects.Wet,3,False)


class GlassCloud(Cloud):
	def hitEffect(self,actor):
		actor.takeDamage([2, 1, 0,0,0, 0.1, 0,0,0])

class PoisonCloud(Cloud):
	def __init__(self, game, x, y, name, color, volume, blocks=False):
		Cloud.__init__(self, game, x, y, name, color, volume, blocks)
		self.canExplode = True

	def hitEffect(self,actor):
		actor.takeDamage([0,0,0,0, 2, 0,0,0,0])


class DamageCloud(Cloud):
	def __init__(self, game, x, y, name, color, volume, damage, blocks=False, properNoun = False, alwaysVisible = False):
		Cloud.__init__(self, game, x, y, name, color, volume, blocks)
		self.damage = damage

	def hitEffect(self,actor):
		actor.takeDamage(self.damage)

class SmokeCloud(Cloud):
	def __init__(self, game, x, y, name, color, volume, blocks=False):
		Cloud.__init__(self, game, x, y, name, color, volume, blocks)
		self.blocksSight = True
		# blocks sight within the cloud
	'''
	def hitEffect(self,obj):
		if isinstance(obj,actors.Actor):
			obj.addStatusEffect(statusEffects.Invisible, 1, True)
	'''


class Trace(Object):
	# visual indicator of the last known position of an actor's target
	def __init__(self, game, x, y, char, name, color, tracer, blocks=False, properNoun = False, alwaysVisible = False):
		Object.__init__(self, game, x, y, char, name, color, alwaysVisible = True)
		self.tracer = tracer
		self.renderFirst()
		self.timer = 10

	def tick(self):
		self.timer -= 1
		#print
		if (self.tracer != None and
			self.tracer.state != None and
			self.tracer.state.lastKnownPosition != None):

			x,y = self.tracer.state.lastKnownPosition

			if x == self.x and y == self.y:
				#print "Flag"
				if self.tracer.state.trace == self and self.timer > 0:
					return

		self.game._currentLevel.removeObject(self)

	def draw(self):
		if self.game.ui.visibleTrace == True:
			Object.draw(self)

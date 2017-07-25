'''
map.py
'''
import libtcodpy as libtcod

import random

#import actors

#import actorStats

import objects

import actorSpawner

import dungeonGeneration

import randomChoice

#import states

FOV_ALGORITHM = 0
FOV_LIGHT_WALLS = True
FOV_RADIUS = 10

EMPTY_ROOM_CHANCE = 0.2 # Probability of a room containing 0 monsters

'''
====================
Map Classes
====================
'''

class Map:
	def __init__(self, game, mapWidth, mapHeight):
		self.game = game
		self.mapWidth = mapWidth
		self.mapHeight = mapHeight

		self.levelSeeds = game.getSeeds()

		self._levels = [] #stores lookup to every level object

		# Initialize the Field of View map object
		self.fov_map = libtcod.map_new(mapWidth,mapHeight)

	def createNewLevel(self):
		map = self
		# Generate the layout of newLevel
		depth = len(self._levels)
		seed = self.levelSeeds[depth]
		mapType = dungeonGeneration.RoomAddition()

		# Initialize mapType
		newLevel = Level(map, self.mapWidth, self.mapHeight, seed, mapType, depth)
		self._levels.append(newLevel)

		#self.loadLevel(depth)
		return newLevel

	def loadLevel(self,index):
		level = self._levels[index]

		self.game._currentLevel = level
		level.generateLevel()
		self.initializeFOV(level)
		return level

	def initializeFOV(self,level):
		for y in xrange(self.mapHeight):
			for x in xrange(self.mapWidth):
				blocksSight = level.getBlocksSight(x,y)
				blocksMovement = level.getBlocksMovement(x,y)
				libtcod.map_set_properties(self.fov_map,x,y,not blocksSight,not blocksMovement)

	def fovRecompute(self,x,y,reinitializeFOV = False):
		libtcod.map_compute_fov(self.fov_map, x, y, FOV_RADIUS, FOV_LIGHT_WALLS, FOV_ALGORITHM)

class Level:
	'''
	TODO: Have the level divide the terrain into different environments.
	then have each level generate a color map, reflecting different types 
	of environments. replace the tile color in the GameUI object with the 
	GameUI's noisemap multiplied by the coresponding cell in the level's
	color map.
	'''
	def __init__(self, map, mapWidth, mapHeight, seed, mapType, levelDepth):
		self.map = map # points to the map object that stores every level
		self.game = self.map.game
		self.mapWidth = mapWidth
		self.mapHeight = mapHeight
		self.seed = seed 
		self.mapType = mapType

		self.terrain = []
		self.rooms = []
		self._objects = []
		self._items = []
		self._actors = []

		self.levelDepth = levelDepth

		self.StairsUp = None
		self.StairsDown = None
		self.clearStairs = True

		Level._blocksMovement = 1 # bitwise map flag
		Level._blocksSight = 2 # bitwise map flag
		Level._hasObject = 4 # bitwise map flag
		Level._hasBeenExplored = 8 # bitwise map flag
 
	def generateLevel(self):
		# Creates an empty 2D array
		if len(self.terrain) == 0:	
			self.terrain = [[0
				for y in range(self.mapHeight)]
					for x in range(self.mapWidth)]

			self.mapType.generateLevel(self, self.mapWidth, self.mapHeight,self.seed)

		self.pathMap = libtcod.path_new_using_map(self.map.fov_map,1)

	def populateRoom(self,roomX, roomY, roomWidth, roomHeight, room):
		maxRoomDifficulty = 3

		if random.random() >= EMPTY_ROOM_CHANCE:
			# populate monsters
			difficulty = random.randint(0,maxRoomDifficulty)
			for i in xrange(difficulty):
				x = 0
				y = 0
				while x == 0 and y == 0:
					tempX = random.randint(0,roomWidth-1)
					tempY = random.randint(0,roomHeight-1)

					# the first condition is necessary, because the edges of some rooms go out of bounds
					if ((room[tempX][tempY] == 0) and 
						(self.getBlocksMovement(roomX + tempX,roomY + tempY) == False) and
						(self.getHasObject(roomX + tempX,roomY + tempY) == False)):
						x = roomX + tempX
						y = roomY + tempY

				# placeholder Monster Spawn
				monsterTable = [
				{'Mirehound':5,'Plague Rat':2,'Snakeman':1,'Snakeman Champion':1},
				{'Mirehound':4,'Plague Rat':3,'Snakeman':2,'Snakeman Archer':1},
				{'Mirehound':4,'Plague Rat':2,'Snakeman':2,'Snakeman Archer':2},
				{'Mirehound':2,'Plague Rat':2,'Snakeman':2,'Snakeman Archer':2},
				{'Mirehound':2,'Plague Rat':2,'Snakeman':2,'Snakeman Archer':2,'Ghost':1},
				{'Mirehound':2,'Plague Rat':2,'Snakeman':3,'Snakeman Archer':3,'Ghost':1,'Snakeman Champion':1},
				{'Mirehound':2,'Plague Rat':2,'Snakeman':2,'Snakeman Archer':3,'Ghost':2,'Snakeman Champion':2}

				]
				depth = min(self.levelDepth, len(monsterTable)-1)
				self.game.actorSpawner.spawn(x,y,randomChoice.choose(monsterTable[depth]))

	def placeStairs(self,downStairsX,downStairsY,upStairsX,upStairsY):
		# place stairs down
		destination = self.levelDepth + 1
		self.stairsDown = objects.Stairs(self.game, downStairsX, downStairsY, '>', 'Stairs', libtcod.white, destination)

		# place stairs up
		destination = self.levelDepth - 1
		self.stairsUp = objects.Stairs(self.game, upStairsX, upStairsY, '<', 'Stairs', libtcod.white, destination)

		if self.clearStairs == True:
			for actor in self.stairsUp.getNearbyActors():
				# move actors away from the stairs
				x = None
				while x == None:
					tempX = random.randint(1,self.mapWidth-1)
					tempY = random.randint(1,self.mapHeight-1)
					if self.getBlocksMovement(tempX,tempY) == False:
						x = tempX
						y = tempY
				self.setHasObjectFalse(actor.x, actor.y)
				actor.x = x
				actor.y = y
				self.setHasObjectTrue(actor.x, actor.y)

	'''
	==== Tile Bitwise Operators ====
	'''

	def setBlocksMovementTrue(self,x,y):
		'''
		Sets the bitmask value _blocksMovement to True for
		the tile at self.terrain[x][y]
		'''
		self.terrain[x][y] = (self.terrain[x][y] | Level._blocksMovement)

	def setBlocksMovementFalse(self,x,y):
		'''
		Sets the bitmask value _blocksMovement to False for
		the tile at self.terrain[x][y]
		'''
		self.terrain[x][y] = (self.terrain[x][y] & ~ Level._blocksMovement)

	def getBlocksMovement(self,x,y):
		'''
		Unpacks the bitmask value for _blocksMovement and returns
		True if the bit is 1 or False if the bit is 0
		'''
		val = bool((self.terrain[x][y] & Level._blocksMovement) != 0)
		return val

	def setBlocksSightTrue(self,x,y):
		'''
		Sets the bitmask value _blocksSight to True for
		the tile at self.terrain[x][y]
		'''
		self.terrain[x][y] = (self.terrain[x][y] | Level._blocksSight)

	def setBlocksSightFalse(self,x,y):
		'''
		Sets the bitmask value _blocksSight to False for
		the tile at self.terrain[x][y]
		'''
		self.terrain[x][y] = (self.terrain[x][y] & ~ Level._blocksSight)
		
	def getBlocksSight(self,x,y):
		'''
		Unpacks the bitmask value for _blocksSight and returns
		True if the bit is 1 or False if the bit is 0
		'''
		val = bool((self.terrain[x][y] & Level._blocksSight) != 0)
		return val

	def setHasObjectTrue(self,x,y):
		'''
		Sets the bitmask value _isVisible to True for
		the tile at self.terrain[x][y]
		'''
		self.terrain[x][y] = (self.terrain[x][y] | Level._hasObject)

	def setHasObjectFalse(self,x,y):
		'''
		Sets the bitmask value _isVisible to False for
		the tile at self.terrain[x][y]
		'''
		self.terrain[x][y] = (self.terrain[x][y] & ~ Level._hasObject)

	def getHasObject(self,x,y):
		'''
		Unpacks the bitmask value for _isVisible and returns
		True if the bit is 1 or False if the bit is 0
		'''
		val = bool((self.terrain[x][y] & Level._hasObject) != 0)
		return val

	def setHasBeenExploredTrue(self,x,y):
		'''
		Sets the bitmask value _hasBeenExplored to True for
		the tile at self.terrain[x][y]
		'''
		self.terrain[x][y] = (self.terrain[x][y] | Level._hasBeenExplored)

	def setHasBeenExploredFalse(self,x,y):
		'''
		Sets the bitmask value _hasBeenExplored to False for
		the tile at self.terrain[x][y]
		'''
		self.terrain[x][y] = (self.terrain[x][y] & ~ Level._hasBeenExplored)
		
	def getHasBeenExplored(self,x,y):
		'''
		Unpacks the bitmask value for _hasBeenExplored and returns
		True if the bit is 1 or False if the bit is 0
		'''
		val = bool((self.terrain[x][y] & Level._hasBeenExplored) != 0)
		return val

	'''
	==== Level Lists Management ====
	'''

	def addObject(self, object):
		self._objects.append(object)

	def removeObject(self, object):
		self._objects.remove(object)

	def addItem(self,item):
		self._items.append(item)

	def removeItem(self,item):
		self._items.remove(item)

	def addActor(self, actor):
		self._actors.append(actor)

		# give experience for reaching this floor
		actor.gainXPExplore(self)


	def removeActor(self, actor):
		self._actors.remove(actor)

	def saveData(self):
		data = {
		'terrain': self.terrain,
		'levelDepth':self.levelDepth
		}

		data['_objects'] = []
		for obj in self._objects:
			# store index reference in game._objects
			index = self.game._objects.index(obj)
			data['_objects'].append(index)


		data['_items'] = []
		for item in self._items:
			# store index reference in game._objects
			index = self.game._objects.index(item)
			data['_items'].append(index)

		data['_actors'] = []
		for actor in self._actors:
			# store index reference in game._objects
			index = self.game._objects.index(actor)
			data['_actors'].append(index)

		if self.StairsUp != None:
			data['StairsUp'] = self.game._objects.index(self.StairsUp)
		else:
			data['StairsUp'] = None

		if self.StairsDown != None:
			data['StairsDown'] = self.game._objects.index(self.StairsDown)
		else:
			data['StairsDown'] = None

		return data

	def loadData(self,data):
		if self.levelDepth != data['levelDepth']:
			print "Error: level ",self.levelDepth," was loaded at depth ",data['levelDepth']

		self.terrain = data['terrain']

		# Objects are handled elsewhere, as the levels must be loaded before objects can be created

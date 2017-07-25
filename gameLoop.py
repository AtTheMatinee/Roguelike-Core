'''
game.py
'''

import libtcodpy as libtcod

import worldMap

from config import *

import objects

import objectClass

from actors import Actor

#import actorStats

import textwrap

import factions

import actorSpawner

import itemSpawner

import spellSpawner

import commands

import statusEffects

import shelve

import random

'''
====================
Game Engine
====================
'''

class GameLoop:
	def __init__(self,ui,mapWidth,mapHeight,seed):
		# ====================
		# Initialization
		# ====================
		self.ui = ui
		self.mapWidth = mapWidth
		self.mapHeight = mapHeight

		self.globalSeed = seed

		self.experiencePerLevel = 0

		self._currentActor = 0
		self._currentLevel = None
		self._objects = []

		self._messages = []

		self.turnCost = 12
		self.spendEnergyOnFailure = False
		self.stopAfterEveryProcess = False

		self.actorSpawner = actorSpawner.ActorSpawner(self)
		self.itemSpawner = itemSpawner.ItemSpawner(self)
		self.spellSpawner = spellSpawner.SpellSpawner(self)
		self.factions = factions.FactionTracker()
		# !!! When I continue an old game, load saved game.factions._factions

	def process(self):
		'''
		The process() method asks the current actor for a command
		object, then allows that command object to execute itself.
		If the command fails to execute, the old command may provide
		a new command to try instead. If there is no alternative,
		the method gives up and tries again on the next frame.
		'''
		#import pdb; pdb.set_trace()
		
		actor = self._currentLevel._actors[self._currentActor % len(self._currentLevel._actors)]

		# Prevent the loop from skipping an actor if they havn't taken their turn E.G. the player
		if (actor.energy >= self.turnCost) and (actor.needsInput()): return

		command = None
		while (command == None): # cycle through alternatives until one resolves
			actor = self._currentLevel._actors[self._currentActor % len(self._currentLevel._actors)]

			if (actor.energy >= self.turnCost) or (actor.gainEnergy()):	

				if actor.needsInput(): return

				command = actor.getCommand()

			else:
				self._currentActor = (self._currentActor + 1) % len(self._currentLevel._actors)
				if self.stopAfterEveryProcess == True: return

		success,alternative = command.perform()
		while alternative != None:
			command = alternative
			success,alternative = command.perform()

		if (self.spendEnergyOnFailure == True) or (success == True):
			if actor == self.hero:
				# after the hero has successfully taken a turn,
				# update the tick method on every object in the level
				for obj in self._currentLevel._objects:
					obj.tick()

			self._currentActor = (self._currentActor + 1) % len(self._currentLevel._actors)

	def message(self,newMsg,color = UI_PRIMARY_COLOR):
		# split the message if the line is too long
		newMsgLines = textwrap.wrap(newMsg,MSG_WIDTH)

		for line in newMsgLines:
			# if the buffer is full, remove the first line to make room for the new one
			if len(self._messages) == MSG_HEIGHT:
				del self._messages[0]

			# add the new line as a tuple with the text and the color
			self._messages.append((line,color))

	def newGame(self,heroClass,heroName):
		self.map = worldMap.Map(self, self.mapWidth, self.mapHeight)

		for i in xrange(20):
			self.map.createNewLevel() #the location of this will probably change
		self.map.loadLevel(0)

		heroX = self._currentLevel.stairsUp.x
		heroY = self._currentLevel.stairsUp.y
		self.hero = self.actorSpawner.spawn(heroX,heroY,heroClass)
		if heroName == None:
			heroName = "Hero"
		else:
			self.hero.properNoun = True
		self.hero.name = heroName

	def saveGame(self):
		#print self._objects
		file = shelve.open('savegame','n')

		# ==== Game Engine Data ====
		file['mapWidth'] = self.mapWidth
		file['mapHeight'] = self.mapHeight
		file['globalSeed'] = self.globalSeed
		file['currentLevelIndex'] = self._currentLevel.levelDepth
		file['currentActor'] = self._currentActor

		if self.hero in self._objects:
			file['heroIndex'] = self._objects.index(self.hero)
		else:
			file['heroIndex'] = 0

		# ==== Game Objects Data ====
		savedObjects = []
		for obj in self._objects:
			data = obj.saveData()
			savedObjects.append(data)

		file['_objects'] = savedObjects

		# ==== Game Level Data ====
		savedLevels = []
		for level in self.map._levels:
			data = level.saveData()
			savedLevels.append(data)

		file['mapLevels'] = savedLevels

		file.close()

	def loadGame(self):
		file = shelve.open('savegame','r')

		# ==== Engine Data ====
		self.mapWidth = file['mapWidth']
		self.mapHeight = file['mapHeight']
		self.seed = file['globalSeed']

		# ==== Initialize levels ====
		self.map = worldMap.Map(self, self.mapWidth, self.mapHeight)

		savedLevels = file['mapLevels']
		for levelData in savedLevels:
			level = self.map.createNewLevel()
			level.loadData(levelData)
		
		# set curent level
		currentLevelIndex = file['currentLevelIndex']
		self.map.loadLevel(currentLevelIndex)


		# ==== Objects ====
		savedObjects = file['_objects']
		for objectData in savedObjects:

			try:
				# create an object of the same type
				if objectData['dataType'] == 'Object':
					x = objectData['x']
					y = objectData['y']
					char = objectData['char']
					name = objectData['name']
					color = objectData['color']
					blocks = objectData['blocks']
					properNoun = objectData['properNoun']
					alwaysVisible = objectData['alwaysVisible']

					if objectData['class'] == objects.Stairs:
						destination = objectData['destination']
						obj = objects.Stairs(self,x,y,char,name,color,destination,blocks,properNoun,alwaysVisible)

					elif objectData['class'] == objects.Trace:
						obj = objects.Trace(self,x,y,char,name,color,None,blocks,properNoun,alwaysVisible)
				
					else:
						try:
							obj = objectClass.Object(self,x,y,char,name,color,blocks,properNoun,alwaysVisible)
						except:
							self._objects.append(None)
							continue

				elif objectData['dataType'] == 'Actor':
					x = objectData['x']
					y = objectData['y']
					key = objectData['_spawnKey']
					obj = self.actorSpawner.spawn(x,y,key,new = False)

				elif objectData['dataType'] == 'Item':
					x = objectData['x']
					y = objectData['y']
					key = objectData['_spawnKey']
					level = objectData['level']
					obj = self.itemSpawner.spawn(x,y,key,level,False)

				else:
					print 'Cannot load ',objectData['class']
					self._objects.append(None)
					continue

				obj.loadData(objectData)

			except:
				print "Error loading ",objectData['class']
				continue

		# ==== Equip Actors ====
		for i in xrange(len(self._objects)):
			if isinstance(self._objects[i], Actor):
				actor = self._objects[i]
				actorData = savedObjects[i]
				# Inventory
				for itemIndex in actorData['inventory']:
					item = self._objects[itemIndex]
					item.moveToInventory(actor)

				# Equipment
				for itemIndex in actorData['equipment']:
					if itemIndex != None:
						item = self._objects[itemIndex]
						actor.equipItem(item)


			else:
				continue

		# ==== Fill Levels ====
		for i in xrange(len(self.map._levels)):
			level = self.map._levels[i]
			levelData = savedLevels[i]
			level._objects = []
			for index in xrange(len(levelData['_objects'])):
				level._objects.append(self._objects[ levelData['_objects'][index] ])

			level._items = []
			for index in xrange(len(levelData['_items'])):
				level._items.append(self._objects[ levelData['_items'][index] ])

			level._actors = []
			for index in xrange(len(levelData['_actors'])):
				level._actors.append(self._objects[ levelData['_actors'][index] ])

			stairsUpIndex = levelData['StairsUp']
			if stairsUpIndex != None:
				level.StairsUp = self._objects[stairsUpIndex]

			stairsDownIndex = levelData['StairsDown']
			if stairsDownIndex != None:
				level.StairsDown = self._objects[stairsDownIndex]


		# hero
		heroIndex = file['heroIndex']
		self.hero = self._objects[heroIndex]

		# current actor
		self._currentActor = file['currentActor']




		file.close()

	def getSeeds(self):
		random.seed(self.globalSeed)
		seeds = []
		for i in xrange(21):
			seeds.append(random.random())
		return seeds

	def addObject(self, object):
		self._objects.append(object)

	def removeObject(self, object):
		self._objects.remove(object)
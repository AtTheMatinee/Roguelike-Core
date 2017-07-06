'''
game.py
'''

import libtcodpy as libtcod

import worldMap

from config import *

#import objects

#import actors

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

		self.map = worldMap.Map(self, self.mapWidth, self.mapHeight)
		# !!! When I continue an old game, load saved game.map._levels and overwright new map._levels

	def process(self):
		'''
		The process method asks the current actor for a command
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
		for i in xrange(20):
			self.map.createNewLevel() #the location of this will probably change
		self.map.loadLevel(0)

		if heroName == None:
			heroName = "Hero"
		heroX = self._currentLevel.stairsUp.x
		heroY = self._currentLevel.stairsUp.y
		self.hero = self.actorSpawner.spawn(heroX,heroY,heroClass)
		self.hero.name = heroName
		#self.hero.addStatusEffect(statusEffects.Flaming,10,False)
		#self.hero.addStatusEffect(statusEffects.Wet,10,False)
		#self.hero.addStatusEffect(statusEffects.Frozen,10,False)
		#self.hero.addStatusEffect(statusEffects.Poisoned,4,False)
		#self.hero.addStatusEffect(statusEffects.Bleeding,2,False)
		#self.hero.addStatusEffect(statusEffects.Flamable,10,False)
		#self.hero.addStatusEffect(statusEffects.MortallyWounded,20,False)

	def saveGame(self):
		#print self._objects
		'''
		save seed, _currentLevel, _currentActor

		for each object in game._objects, save any relevent variables
		needed to create an exact copy of the object.

		for each level, save seed, and the index in game_objects
		to each object in level._objects, level._items, level._actors
		'''
		pass

	def loadGame(self,saveFile):
		pass
		'''
		for each object in the saved game._objects, create an instance 
		of the same object, overwrighting the new objects relevent 
		stats from the saved object

		reconstruct the level lists from the saved level variables
		'''

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
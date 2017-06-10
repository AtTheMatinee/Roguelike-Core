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

import dungeonGeneration

import commands

import statusEffects

'''
====================
Game Engine
====================
'''

class GameLoop:
	def __init__(self,ui,mapWidth,mapHeight):
		# ====================
		# Initialization
		# ====================
		self.ui = ui
		self.mapWidth = mapWidth
		self.mapHeight = mapHeight

		self._actors = []
		self._currentActor = 0
		self._objects = []
		self._currentLevel = None
		self._items = []

		self._messages = []

		self.turnCost = 12
		self.spendEnergyOnFailure = False
		self.stopAfterEveryProcess = False

		self.actorSpawner = actorSpawner.ActorSpawner(self)
		self.itemSpawner = itemSpawner.ItemSpawner(self)
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
		actor = self._actors[self._currentActor]

		# Prevent the loop from skipping an actor if they havn't taken their turn E.G. the player
		if (actor.energy >= self.turnCost) and (actor.needsInput()): return

		command = None
		while (command == None): # cycle through alternatives until one resolves
			actor = self._actors[self._currentActor]

			if (actor.energy >= self.turnCost) or (actor.gainEnergy()):	

				if actor.needsInput(): return
				command = actor.getCommand()

			else:
				self._currentActor = (self._currentActor + 1) % len(self._actors)
				if self.stopAfterEveryProcess == True: return

		success,alternative = command.perform()
		while alternative != None:
			command = alternative
			success,alternative = command.perform()

		if (self.spendEnergyOnFailure == True) or (success == True):
			self._currentActor = (self._currentActor + 1) % len(self._actors)

	def message(self,newMsg,color = UI_PRIMARY_COLOR):
		# split the message if the line is too long
		newMsgLines = textwrap.wrap(newMsg,MSG_WIDTH)

		for line in newMsgLines:
			# if the buffer is full, remove the first line to make room for the new one
			if len(self._messages) == MSG_HEIGHT:
				del self._messages[0]

			# add the new line as a tuple with the text and the color
			self._messages.append((line,color))

	def newGame(self):
		# TODO: Pregenerate all levels at the beginning
		mapType = dungeonGeneration.RoomAddition()
		self.map.createNewLevel(mapType) #the location of this will probably change

		heroName = "Hero"
		heroX = self.mapWidth/2#self._currentLevel.tempX
		heroY = self.mapHeight/2#self._currentLevel.tempY
		self.hero = self.actorSpawner.spawn(heroX,heroY,"Hero")
		self.hero.name = heroName
		self.hero.addStatusEffect(statusEffects.StatusEffect,10)

	def loadGame(self,saveFile):
		pass
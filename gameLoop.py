'''
game.py
'''

import libtcodpy as libtcod

import worldMap

#import objects

#import actors

#import actorStats

import factions

import actorSpawner

import dungeonGeneration

import commands

'''
====================
Game Engine
====================
'''

class GameLoop:
	def __init__(self,ui,mapWidth,mapHeight):
		self.ui = ui

		self._actors = []
		self._currentActor = 0
		self._objects = []
		self._currentLevel = None

		self.turnCost = 12
		self.spendEnergyOnFailure = False
		self.stopAfterEveryProcess = False

		game = self

		self.actorSpawner = actorSpawner.ActorSpawner(self)
		self.factions = factions.FactionTracker()

		self.map = worldMap.Map(game, mapWidth, mapHeight)
		mapType = dungeonGeneration.RoomAddition()
		self.map.createNewLevel(mapType) #the location of this will probably change

		heroName = "Hero"
		heroX = mapWidth/2#self._currentLevel.tempX
		heroY = mapHeight/2#self._currentLevel.tempY
		#self.hero = actors.Hero(game,heroX,heroY,'@',heroName,color = libtcod.white,stats = actorStats.Stats("Hero"),playerControlled = True)
		self.hero = self.actorSpawner.spawn(heroX,heroY,"Hero")
		self.hero.name = heroName


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

	def addActor(self,actor):
		self._actors.append(actor)

	def removeActor(self,actor):
		pass

	def addObject(self,actor):
		self._objects.append(actor)

	def removeObject(self,actor):
		pass

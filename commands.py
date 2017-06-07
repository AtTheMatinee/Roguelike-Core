'''
commands.py
'''
import random

import actors
'''
====================
Commands
====================
'''

class Command:
	def __init__(self, actor):
		self.actor = actor
		self.game = actor.game

		self.energyCost = 0

	def perform(self):
		self.actor.energy -= self.energyCost
		success = False
		alternative = None
		return success, alternative

class WalkCommand(Command):
	def __init__(self, actor, dx, dy):
		self.actor = actor
		self.game = actor.game
		self.dx = dx
		self.dy = dy

		self.energyCost = 12

	def perform(self):
		x = self.actor.x + self.dx
		y = self.actor.y + self.dy

		# see if tile blocks movement
		if (self.game._currentLevel.getBlocksMovement(x,y)):
			success = False
			alternative = None
			return success, alternative

		# See if there is another actor at the location
		if (self.game._currentLevel.getHasObject(x,y)):
			for o in self.game._currentLevel._objects:
				if (o.blocks == True and 
					(o.x == x) and
					(o.y == y)):
					# TODO: alternatives for combat and noncombat
					success = False

					# Return an AttackCommand alternative
					if (isinstance(o, actors.Actor) and
						self.game.factions.getRelationship(self.actor.faction, o.faction) == self.game.factions._hostile):
						alternative = AttackCommand(self.actor,o)

					else: alternative = WaitCommand(self.actor)

					return success, alternative

		# See if the location is a door
		
		# Move actor
		self.game._currentLevel.setHasObjectFalse(self.actor.x, self.actor.y)
		self.actor.x = x
		self.actor.y = y
		self.game._currentLevel.setHasObjectTrue(x,y)

		# consume energy
		self.actor.energy -= self.energyCost
		# set flags that change when a turn is taken
		self.actor.hasTakenTurn()

		success = True
		alternative = None
		return success, alternative

class WaitCommand(Command):
	def __init__(self, actor):
		self.actor = actor
		self.game = actor.game

		self.energyCost = 10

	def perform(self):
		self.actor.energy -= self.energyCost
		# set flags that change when a turn is taken
		self.actor.hasTakenTurn()
		
		success = True
		alternative = None
		return success, alternative

class OpenDoorCommand(Command):
	def __init__(self, door):
		pass

	def perform(self):
		pass

class CloseDoorCommand(Command):
	def __init__(self, door):
		pass

	def perform(self):
		pass

class AttackCommand(Command):
	def __init__(self,actor,target):
		self.actor = actor
		self.target = target
		'''
		[
		physical,
		fire,
		frost,
		poison,
		holy,
		unholy,
		unblockable
		]
		'''
		self.energyCost = 20 - actor.stats.get("attackSpeed")

	def perform(self):
		attack = self.actor.stats.get('attack')
		critChance = self.actor.stats.get('critChance')

		# calculate Critical Damage (for physical damage only)
		if ((random.random() <= critChance) and
			(attack[0] > 0)):
			attack[0] += random.randint(1,attack[0])

		if self.actor == self.actor.game.hero or self.target == self.actor.game.hero:
			self.actor.game.message("The " + self.actor.getName() + " attacks the " + self.target.getName())

		self.target.takeDamage(attack)
		self.target.mostRecentAttacker = self.actor

		self.actor.energy -= self.energyCost
		# set flags that change when a turn is taken
		self.actor.hasTakenTurn()

		success = True
		alternative = None
		return success, alternative
		


class CastSpellCommand(Command):
	pass

class FireRangedWeaponCommand(Command):
	pass

class UseCommand(Command):
	def __init__(self, actor, item):
		self.actor = actor
		self.game = actor.game
		self.item = item

		self.energyCost = 12

	def perform(self):
		if self.item.use(self.actor) == True:

			self.actor.energy -= self.energyCost
			# set flags that change when a turn is taken
			self.actor.hasTakenTurn()
			
			success = True
			alternative = None

		else:
			success = False
			alternative = None

		return success, alternative


class PickUpCommand(Command):
	def __init__(self, actor,x,y):
		self.actor = actor
		self.game = actor.game
		self.x = x
		self.y = y

		self.energyCost = 8

	def perform(self):
		success = False
		alternative = None
		# Check to see if there is an item at that location
		for item in self.game._currentLevel._items:
			if (item.x == self.x) and (item.y == self.y):

				# Check to see if the actors inventory has space
				if self.actor.inventorySize - len(self.actor.inventory) < 1:
					if self.actor == self.game.hero:
						self.game.message("You cannot carry the "+item.getName())
					success = False
					alternative = None
					return success, alternative

				# otherwise add the item to the actor's inventory
				# and remove it from the level
				else:
					item.moveToInventory(self.actor)

					self.actor.energy -= self.energyCost
					# set flags that change when a turn is taken
					self.actor.hasTakenTurn()
					

					success = True
					alternative = None

		return success, alternative

class DropCommand(Command):
	def __init__(self,actor,item):
		self.actor = actor
		self.item = item

		self.energyCost = 8

	def process(self):
		self.item.dropFromInventory(self.item,self.actor)

class ThrowCommand(Command):
	pass
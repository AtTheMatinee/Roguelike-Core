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
			for object in self.game._currentLevel._objects:
				if (object.blocks == True and 
					(object.x == x) and
					(object.y == y)):
					# TODO: alternatives for combat and noncombat
					success = False

					# Return an AttackCommand alternative
					if isinstance(object, actors.Monster):
						alternative = AttackCommand(self.actor,object)

					else: alternative = None

					return success, alternative

		# See if the location is a door
		
		# Move actor
		self.game._currentLevel.setHasObjectFalse(self.actor.x, self.actor.y)
		self.actor.x = x
		self.actor.y = y
		self.game._currentLevel.setHasObjectTrue(x,y)

		# consume energy
		self.actor.energy -= self.energyCost

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
		if random.random() <= critChance:
			attack[0] += random.randint(1,attack[0])

		self.target.takeDamage(attack)

		if self.actor == self.actor.game.hero or self.target == self.actor.game.hero:
			print ("The " + self.actor.name + " attacks the " + self.target.name)
		self.actor.energy -= self.energyCost
		success = True
		alternative = None
		return success, alternative
		#crit


class CastSpell(Command):
	pass
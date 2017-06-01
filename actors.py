'''
actors.py
'''
'''
====================
Actors
====================
'''
from objects import Object

import random

import actorStats

# TODO: impliment hostileTo = [] variable 

class Actor(Object):
	def __init__(self, game, x, y, char, name, color, blocks=True, stats = actorStats.Stats("None"), state = None, playerControlled = False):
		self.game = game
		self.x = x
		self.y = y
		self.char = char
		self.name = name
		self.color = color
		self.blocks = blocks

		self.game.addObject(self)
		self.game._currentLevel.addObject(self)
		self.game._currentLevel.setHasObjectTrue(x,y)

		self.energy = 0

		self.stats = stats

		self.playerControlled = playerControlled
		self.state = state
		self._defaultState = state
		self.statusEffects = []

		self.game.addActor(self)
		self.game._currentLevel.addActor(self)

		self._nextCommand = None

	def getCommand(self):
		if self.statusEffects:
			for statusEffect in self.statusEffects:
				statusEffect.effect()

		command = self._nextCommand

		if self.state:
			#AI states
			#knockback
			#confused
			#autowalk
			#asleep
			#autoexplore
			#afraid
			AICommand = self.state.getAICommand(self)
			if AICommand != None:
				command = AICommand

		self._nextCommand = None
		return command

	def setNextCommand(self,command):
		self._nextCommand = command

	def gainEnergy(self):
		self.energy += self.speed
		return (self.energy >= game.turnCost)

	def needsInput(self):
		if not self.playerControlled:
			return False
		else:
			return (self._nextCommand == None)

	def takeDamage(self, damage):
		'''
		damage = [physical, fire, frost, poison, holy, unholy, unblockable]
		defense = [n,%,%,%,%,%]
		TODO: instead of dying when your health reaches 0,
		health being at 0 puts the actor in a near death state,
		in which the next damage taken is fatal
		'''
		defense = self.stats.get("defense")

		physicalDam = max(0,(damage[0] - random.randint(0,defense[0])))

		# I have these seperated out so I can implement additional modifiers in the future
		fireDam = damage[1]*defense[1]
		frostDam = damage[2]*defense[2]
		poisonDam = damage[3]*defense[3]
		holyDam = damage[4]*defense[4]
		unholyDam = damage[5]*defense[5]

		totalDam = (physicalDam + fireDam + frostDam + poisonDam + holyDam + unholyDam + damage[6])

		health = self.stats.get("health")
		health -= totalDam
		self.stats.setBaseStat("health",health)
		self.checkDeath()


	def checkDeath(self):
		if (self.stats.get("health") <= 0):
			self.deathState()

	def deathState(self):
		print self.name + " dies"

class Hero(Actor):
	pass

class Monster(Actor):
	pass

class Elemental(Monster):
	pass
	# Takes damage every turn
	# heals 100% from their element
	# have a lot of elemental spells
	# have a spell that casts their elemental status effect on themself so they heal while it's in effect

if __name__ == "__main__":


	herostats = Stats(0)
	print herostats.get("health")

	class MagicRing:
		def __init__(self):
			self.id = 1
			self.modifier = {'add':{"health":5}}

	class MagicRobe:
		def __init__(self):
			self.id = 2
			self.modifier = {'mult':{'health':0.2}}

	class MagicHat:
		def __init__(self):
			self.id = 3
			self.modifier = {'add':{'health':5}}	

	ring = MagicRing()
	herostats.addModifier(ring.id,ring.modifier)
	print herostats.get("health")

	robe = MagicRobe()
	herostats.addModifier(robe.id,robe.modifier)
	print herostats.get("health")

	hat = MagicHat()
	herostats.addModifier(hat.id,hat.modifier)
	print herostats.get("health")
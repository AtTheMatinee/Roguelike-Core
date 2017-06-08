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

import libtcodpy as libtcod

class Actor(Object):
	def __init__(self, game, x, y, char, name, color, faction = None, blocks=True, stats = actorStats.Stats("None"), state = None,deathState = None, surviveMortalWound = False, inventorySize = 0, drops = {}, canEquipArmor = False, canEquipWeapons = False, playerControlled = False):
		self.game = game
		self.x = x
		self.y = y
		self.char = char
		self.name = name
		self.color = color
		self.faction = faction
		self.blocks = blocks

		self.nearbyActors = self.getNearbyActors()
		self.nearbyObjects = self.getNearbyObjects()
		
		self.surviveMortalWound = surviveMortalWound
		self.mortalWound = False
		self.hadLastChance = False
		self.canBePushed = True

		self.game.addObject(self)
		self.game._currentLevel.addObject(self)
		self.game._currentLevel.setHasObjectTrue(x,y)

		self.energy = 0

		self.stats = stats

		self.inventorySize = inventorySize
		self.inventory = []
		self.drops = drops

		self.equipSlots = [None]*6
		self.canEquipArmor = canEquipArmor
		self.canEquipWeapons = canEquipWeapons

		self.playerControlled = playerControlled
		self.state = state
		self._defaultState = state
		self.deathState = deathState
		self.statusEffects = []

		self.game.addActor(self)
		self.game._currentLevel.addActor(self)

		self._nextCommand = None

	def getCommand(self):
		# process status effects
		if self.statusEffects:
			for statusEffect in self.statusEffects:
				statusEffect.effect()

		command = self._nextCommand

		if self.state:
			#AI states
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
		self.energy += self.stats.get("speed")
		return (self.energy >= self.game.turnCost)

	def needsInput(self):
		if not self.playerControlled:
			return False
		else:
			return (self._nextCommand == None)

	def hasTakenTurn(self):
		# Reset Once per turn flags
		self.canBePushed = True

		if (self.mortalWound == True):
			self.hadLastChance = True

		self.nearbyActors = self.getNearbyActors()


	def takeDamage(self, damage):
		'''
		damage = [physical, armorPenetration, fire, frost, poison, bleed, holy, unholy, unblockable]
		defense = [physical, fire, frost, poison, bleed, holy, unholy]
		TODO: instead of dying when your health reaches 0,
		health being at 0 puts the actor in a near death state,
		in which the next damage taken is fatal
		'''
		defense = self.stats.get("defense")

		armor = max(0,(random.randint(0,defense[0]) - damage[1])) # physicalDefense - armorPenetration
		physicalDam = max(0,(damage[0] - armor))

		# I have these seperated out so I can implement additional modifiers in the future
		fireDam = damage[2] - damage[2]*defense[1] # inflicts inflamed
		frostDam = damage[3] - damage[3]*defense[2] # inflicts frozen
		poisonDam = damage[4] - damage[4]*defense[3] # inflicts poison
		bleedDam = damage[5] - damage[5]*defense[4] # does not do damage, only inflicts bleed status
		holyDam = damage[6] - damage[6]*defense[5]
		unholyDam = damage[7] - damage[7]*defense[6]

		totalDam = (physicalDam + fireDam + frostDam + poisonDam + holyDam + unholyDam + damage[6])

		health = self.stats.get("healthCurrent")
		health = min(health-totalDam,self.stats.get("healthMax"))
		self.stats.setBaseStat("healthCurrent",health)
		self.checkDeath()

	def heal(self,healValue):
		health =  min((self.stats.get("healthCurrent") + healValue), self.stats.get('healthMax'))
		self.stats.setBaseStat("healthCurrent",health)

	def checkDeath(self):
		if (self.stats.get("healthCurrent") <= 0):
			self.stats.setBaseStat("healthCurrent",0)
			if (self.surviveMortalWound == False) or ((self.mortalWound == True) and (self.hadLastChance)):
				self.death()
			else:
				self.mortalWound = True
				self.game.message(self.getName()+" is mortally wounded.",libtcod.red)

		elif (self.mortalWound == True) or (self.hadLastChance == True):
			self.mortalWound = False
			self.hadLastChance = False

	def death(self):
		if self.deathState != None:
			self.deathState.process()
		else:
			self.game.removeObject(self)
			self.game._currentLevel.removeObject(self)
			self.game._currentLevel.setHasObjectFalse(self.x,self.y)
			self.game.removeActor(self)
			self.game._currentLevel.removeActor(self)

			del self

	def dropLoot(self):
		# Drop Inventory and Equipment

		# Random Drop { itemKey : odds=1/n }
		level = 0
		if self.drops:
			for item,odds in self.drops.items():
				if random.random() <= 1.0/odds:
					self.game.itemSpawner.spawn(self.x,self.y,item,level)



	def addStatusEffect(self,statusEffect,timer):
		statusEffect = statusEffect(self,timer)
		self.statusEffects.append(statusEffect)

	def removeStatusEffect(self,statusEffect):
		self.statusEffects.remove(statusEffect)

class Hero(Actor):

	def getNearbyActors(self):
		nearbyActors = []
		for actor in self.game._currentLevel._actors:
			if (actor != self) and (libtcod.map_is_in_fov(self.game.map.fov_map, actor.x, actor.y)):
				nearbyActors.append(actor)
		return nearbyActors

	def getNearbyObjects(self):
		nearbyObjects = []
		for obj in self.game._currentLevel._objects:
			if (obj != self) and (libtcod.map_is_in_fov(self.game.map.fov_map, obj.x, obj.y)):
				nearbyObjects.append(obj)
		return nearbyObjects

		libtcod.map_is_in_fov(self.game.map.fov_map, x, y)

	def hasTakenTurn(self):
		# Reset Once per turn flags
		self.canBePushed = True

		if (self.mortalWound == True):
			self.hadLastChance = True

		self.nearbyActors = self.getNearbyActors()
		self.nearbyObjects = self.getNearbyObjects()

class Monster(Actor):
	pass

class Elemental(Monster):
	pass
	# Takes damage every turn
	# heals 100% from their element
	# have a lot of elemental spells
	# have a spell that casts their elemental status effect on themself so they heal while it's in effect


if __name__ == "__main__":


	herostats = actorStats.Stats(0)
	print herostats.get("healthMax")

	class MagicRing:
		def __init__(self):
			self.id = 1
			self.modifier = {'add':{"healthMax":5}}

	class MagicRobe:
		def __init__(self):
			self.id = 2
			self.modifier = {'mult':{'healthMax':0.2}}

	class MagicHat:
		def __init__(self):
			self.id = 3
			self.modifier = {'add':{'healthMax':5}}	

	class MagicStaff:
		def __init__(self):
			self.id = 4
			self.modifier = {'add':{'attack':[1,0,0,0,0,0,0,0,0]}}	

	ring = MagicRing()
	herostats.addModifier(ring.id,ring.modifier)
	print herostats.get("healthMax")

	robe = MagicRobe()
	herostats.addModifier(robe.id,robe.modifier)
	print herostats.get("healthMax")

	hat = MagicHat()
	herostats.addModifier(hat.id,hat.modifier)
	for i in xrange(10):
		print herostats.get("healthMax")

	staff = MagicStaff()
	herostats.addModifier(staff.id,staff.modifier)
	for i in xrange(10):
		print herostats.get("attack")
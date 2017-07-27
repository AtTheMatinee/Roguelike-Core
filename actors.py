'''
actors.py
'''
from objectClass import Object

import random

import actorStats

import statusEffects

import libtcodpy as libtcod

'''
====================
Actor Class
====================
'''

class Actor(Object):
	def __init__(self, game, x, y, char, name, color, level, faction = None, blocks=True, properNoun = False, alwaysVisible = False, stats = actorStats.Stats("None"), state = None,deathState = None, surviveMortalWound = False, inventorySize = 0, drops = {}, spells = [], canEquipArmor = False, canEquipWeapons = False, playerControlled = False):
		Object.__init__(self,game,x,y,char,name,color,blocks, properNoun, alwaysVisible)
		self.level = level
		self.faction = faction
		self.game._currentLevel.setHasObjectTrue(x,y)


		self.nearbyActors = []
		self.nearbyObjects = []
		self.recalculateNearbyObjects = True
		
		self.mostRecentAttacker = None
		self.experience = 0
		self.surviveMortalWound = surviveMortalWound
		self.mortalWound = False
		self.hadLastChance = False
		self.canBePushed = True

		self.dead = False
		self.invisible = False


		self.energy = 0

		self.stats = stats

		self.inventorySize = inventorySize
		self.inventory = []
		self.drops = drops
		self.spells = []

		self.equipSlots = [None]*6
		self.canEquipArmor = canEquipArmor
		self.canEquipWeapons = canEquipWeapons

		self.playerControlled = playerControlled
		self.state = state
		self._defaultState = state
		self.deathState = deathState
		self.statusEffects = []

		#self.game.addActor(self)
		self.game._currentLevel.addActor(self)

		self._nextCommand = None

	def getCommand(self):
		# recalculate the nearby actors if something has changed since the last recalculation
		self.recalculateObjects()

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

	def draw(self):
		if self.invisible == True:
			return

		Object.draw(self)

	def recalculateObjects(self):
		if self.recalculateNearbyObjects == True:
			self.nearbyActors = self.getNearbyActors()
			self.nearbyObjects = self.getNearbyObjects()
			self.recalculateNearbyObjects = False

	def needsInput(self):
		if not self.playerControlled:
			return False
		else:
			# This is the best place to call recalculateObjects that allows it to be called before the player has taken a turn
			self.recalculateObjects()
			return (self._nextCommand == None)

	def hasTakenTurn(self):
		# Magic Regen
		self.gainMagic(self.stats.get('magicRegen')*self.stats.get('magicMax'))

		# process status effects
		if self.statusEffects:
			for statusEffect in self.statusEffects:
				statusEffect.effect()

		# Reset Once per turn flags
		self.canBePushed = True

		if (self.mortalWound == True):
			self.hadLastChance = True

		self.recalculateNearbyObjects = True


	def takeDamage(self, damage):
		'''
		damage = [physical, armorPenetration, fire, frost, poison, bleed, holy, unholy, unblockable]
		defense = [physical, fire, frost, poison, bleed, holy, unholy]
		'''
		defense = self.stats.get("defense")

		armor = max(0,(random.randint(0,int(defense[0])) - int(damage[1]))) # physicalDefense - armorPenetration
		physicalDam = max(0,(damage[0] - armor))

		# ==== Fire ====
		fireDam = damage[2] - float(damage[2]*defense[1]) # inflicts inflamed
		if ((fireDam >= 1) and (random.random() <= 0.05) or 
			any(isinstance(se, statusEffects.Flamable) for se in self.statusEffects) ):
			for se in self.statusEffects:
				if (isinstance(se, statusEffects.Flamable)):
					se.remove()
			self.addStatusEffect(statusEffects.Flaming,10,False)

		# ==== Frost ====
		frostDam = damage[3] - float(damage[3]*defense[2]) # inflicts frozen
		if ((frostDam >= 1) and (random.random() <= 0.05) or 
			any(isinstance(se, statusEffects.Wet) for se in self.statusEffects) ):
			for se in self.statusEffects:
				if (isinstance(se, statusEffects.Wet)):
					se.remove()
			self.addStatusEffect(statusEffects.Frozen,10,False)

		# ==== Poison ====
		poisonDam = damage[4] - float(damage[4]*defense[3]) # inflicts poison
		if (poisonDam >= 1) and (random.random() <= 0.1):
			self.addStatusEffect(statusEffects.Poisoned,int(poisonDam)*2,False)

		# ==== Bleed ====
		bleedChance = damage[5] - float(damage[5]*defense[4]) # does not do damage, only inflicts bleed status
		if bleedChance > 0 and random.random() <= bleedChance:
			self.addStatusEffect(statusEffects.Bleeding,10,True)

		# ==== Holy ====
		holyDam = damage[6] - float(damage[6]*defense[5])
		
		# ==== Unholy ====
		unholyDam = damage[7] - float(damage[7]*defense[6])


		totalDam = (physicalDam + fireDam + frostDam + poisonDam + holyDam + unholyDam + damage[8])

		health = self.stats.get("healthCurrent")
		health = min(health-totalDam,self.stats.get("healthMax"))
		self.stats.setBaseStat("healthCurrent",health)
		self.checkDeath()

	def heal(self,healValue):
		health =  min((self.stats.get("healthCurrent") + healValue), self.stats.get('healthMax'))
		self.stats.setBaseStat("healthCurrent",health)

	def gainMagic(self,magicGain):
		magic =  min((self.stats.get("magicCurrent") + magicGain), self.stats.get('magicMax'))
		self.stats.setBaseStat("magicCurrent",magic)

	def checkDeath(self):
		if (self.stats.get("healthCurrent") <= 0):
			self.stats.setBaseStat("healthCurrent",0)
			if (self.surviveMortalWound == False) or ((self.mortalWound == True) and (self.hadLastChance)):
				self.death()
			elif self.mortalWound == False:
				self.mortalWound = True
				self.addStatusEffect(statusEffects.MortallyWounded,100,True)

		elif (self.mortalWound == True) or (self.hadLastChance == True):
			self.mortalWound = False
			self.hadLastChance = False

	def death(self):
		if self.dead == False:
			self.dead = True

			if self.deathState != None:
				self.deathState.process()
			else:
				self.game.removeObject(self)
				self.game._currentLevel.removeObject(self)
				self.game._currentLevel.setHasObjectFalse(self.x,self.y)
				self.game._currentLevel.removeActor(self)

	def dropLoot(self):
		# Drop Inventory and Equipment
		for i in xrange(len(self.equipSlots) -1):
			if self.equipSlots[i] != None:
				self.inventory.append(self.equipSlots[i])
				self.equipSlots[i] = None

		if len(self.inventory) > 0:
			for item in self.inventory:
				if random.random() <= 0.5:
					item.dropFromInventory(self)

		# Random Drop { itemKey : odds=1/n }
		level = self.level
		if self.drops:
			for item,odds in self.drops.items():
				if random.random() <= odds:
					self.game.itemSpawner.spawn(self.x,self.y,item,level,True)

	def addStatusEffect(self,statusEffect,timer,stacks):
		# see if an instance of that effect already exists, and that the effect cannot stack
		if (stacks == False):
			if any(isinstance(se, statusEffect) for se in self.statusEffects):
				return

		# else, add the effect
		statusEffect = statusEffect(self,timer)
		self.statusEffects.append(statusEffect)

	def removeStatusEffect(self,statusEffect):
		self.statusEffects.remove(statusEffect)

	def equipItem(self,item):
		if item in self.inventory:
			self.inventory.remove(item)
		if item in self.game._currentLevel._objects:
			self.game._currentLevel._objects.remove(item)
		if item in self.game._currentLevel._items:
			self.game._currentLevel._items.remove(item)

		#for slot in item.equipSlot:
			#self.equipSlots[slot] = item
		self.equipSlots[item.equipSlot] = item
		self.stats.addModifier(item,item.modifier)

	def gainXP(self):
		self.experience += 1

	def gainXPCombat(self,actor):
		pass

	def gainXPIdentify(self,item):
		pass

	def gainXPDiscovery(self,item):
		pass

	def gainXPExplore(self,floor):
		pass

	def findTarget(self,range = None):
		targetX = None
		targetY = None
		if self.playerControlled == True:
			targetX,targetY = self.game.ui.targetTile(range)

		else:
			fov = self.game.map.fov_map
			if libtcod.map_is_in_fov(fov,self.x,self.y) and self.state != None:
				if self.state.canTargetNemesis(self):
					target = self.mostRecentAttacker

				elif self.state.hostileToHero(self) and self.state.canTargetHero(self):
					target = self.game.hero

			if target != None:
				targetX = target.x
				targetY = target.y

		return targetX,targetY

	def saveData(self):
		data = Object.saveData(self)
		data['dataType'] = 'Actor'
		data['class'] = self.__class__
		data['_spawnKey'] = self._spawnKey
		data['level'] = self.level
		data['faction'] = self.faction
		
		data['experience'] = self.experience
		data['surviveMortalWound'] = self.surviveMortalWound

		data['energy'] = self.energy

		data['stats'] = self.stats.statBase

		data['inventorySize'] = self.inventorySize

		data['canEquipArmor'] = self.canEquipArmor
		data['canEquipWeapons'] = self.canEquipWeapons

		data['playerControlled'] = self.playerControlled

		# ==== Special Variables ====
		data['inventory'] = []
		for item in self.inventory:
			# store index reference in game._objects
			index = self.game._objects.index(item)
			data['inventory'].append(index)

		data['spells'] = []
		for spell in self.spells:
			spellData = spell.saveData()
			data['spells'].append(spellData)

		data['equipment'] = [None]*len(self.equipSlots)
		for i in xrange(len(self.equipSlots)):
			# store index reference in game._objects
			if self.equipSlots[i] != None:
				item = self.equipSlots[i]

				index = self.game._objects.index(item)

				data['equipment'][i] = index

		data['statusEffects'] = []
		for statusEffect in self.statusEffects:
			SEdata = statusEffect.saveData()
			data['statusEffects'].append(SEdata)

		return data

	def loadData(self,data):
		# After an instance of this object's class has been created, overwrite the base data with specific saved data
		Object.loadData(self,data)
		# loading Inventory and equipment are handled elsewhere, since they can only be managed after every game object has been recreated
		self.level = data['level']
		self.faction = data['faction']
		self.experience = data['experience']
		self.surviveMortalWound = data['surviveMortalWound']
		self.energy = data['energy']
		self.stats.statBase = data['stats']
		self.inventorySize = data['inventorySize']
		self.canEquipArmor = data['canEquipArmor']
		self.canEquipWeapons = data['canEquipWeapons']
		self.playerControlled = data['playerControlled']

		# Spells
		for spell in data['spells']:
			key = spell['_spawnKey']
			s = self.game.spellSpawner.spawn(self,key)
			self.spells.append(s)

		# Status Effects
		for SE in data['statusEffects']:
			SEClass = SE['class']
			timer = SE['timer']
			self.addStatusEffect(SEClass,timer,True)

		return True

'''
====================
Hero Class
====================
'''

class Hero(Actor):
	def __init__(self, game, x, y, char, name, color, level, faction = None, blocks=True, properNoun = False, alwaysVisible = False, stats = actorStats.Stats("None"), state = None,deathState = None, surviveMortalWound = False, inventorySize = 0, drops = {}, spells = [], canEquipArmor = False, canEquipWeapons = False, playerControlled = False):
		self.discoveredMonsters = set()
		self.killedMonsters = set()
		self.discoveredItems = set()
		self.floorsVisited = set()
		Actor.__init__(self, game, x, y, char, name, color, level, faction, blocks, properNoun, alwaysVisible, stats, state ,deathState , surviveMortalWound , inventorySize, drops, spells, canEquipArmor, canEquipWeapons, playerControlled)


	def getNearbyActors(self):
		nearbyActors = []
		for actor in self.game._currentLevel._actors:
			if (actor != self) and (libtcod.map_is_in_fov(self.game.map.fov_map, actor.x, actor.y)):
				nearbyActors.append(actor)
				self.gainXPDiscovery(actor)
		return nearbyActors

	def getNearbyObjects(self):
		nearbyObjects = []
		for obj in self.game._currentLevel._objects:
			if (obj != self) and (libtcod.map_is_in_fov(self.game.map.fov_map, obj.x, obj.y)):
				nearbyObjects.append(obj)
		return nearbyObjects

		libtcod.map_is_in_fov(self.game.map.fov_map, x, y)

	def draw(self):
		if (libtcod.map_is_in_fov(self.game.map.fov_map, self.x, self.y) or
			(self.alwaysVisible == True) and self.game._currentLevel.getHasBeenExplored(self.x,self.y)):
			color = self.color

			if self.invisible == True:
				color *= 0.5

			libtcod.console_set_default_foreground(self.game.ui.con, color)
			libtcod.console_put_char(self.game.ui.con, self.x, self.y, self.char, libtcod.BKGND_NONE)

	def hasTakenTurn(self):
		Actor.hasTakenTurn(self)

		self.nearbyObjects = self.getNearbyObjects()

	def addStatusEffect(self,statusEffect,timer,stacks):
		# see if an instance of that effect already exists, and that the effect cannot stack
		if (stacks == False):
			if any(isinstance(se, statusEffect) for se in self.statusEffects):
				return

		# else, add the effect
		statusEffect = statusEffect(self,timer)
		self.statusEffects.append(statusEffect)

		self.game.ui.reevaluateHeroStatusEffects = True

	def removeStatusEffect(self,statusEffect):
		self.statusEffects.remove(statusEffect)

		self.game.ui.reevaluateHeroStatusEffects = True

	def saveData(self):
		data = Actor.saveData(self)

		data['discoveredMonsters'] = self.discoveredMonsters
		data['killedMonsters'] = self.killedMonsters
		data['discoveredItems'] = self.discoveredItems
		data['floorsVisited'] = self.floorsVisited

		return data

	def loadData(self,data):
		# After an instance of this object's class has been created, overwrite the base data with specific saved data
		Actor.loadData(self,data)
		self.discoveredMonsters = data['discoveredMonsters']
		self.killedMonsters = data['killedMonsters']
		self.discoveredItems = data['discoveredItems']
		self.floorsVisited = data['floorsVisited']

	def gainXPCombat(self,actor):
		if actor._spawnKey in self.killedMonsters: return

		self.gainXP()
		self.killedMonsters.add(actor._spawnKey)

	def gainXPIdentify(self,item):
		if item._spawnKey in self.discoveredItems: return

		self.gainXP()
		self.discoveredItems.add(item._spawnKey)

	def gainXPDiscovery(self,actor):
		if actor._spawnKey in self.discoveredMonsters: return

		self.gainXP()
		self.discoveredMonsters.add(actor._spawnKey)

	def gainXPExplore(self,floor):
		if floor.levelDepth in self.floorsVisited: return

		self.gainXP()
		self.floorsVisited.add(floor.levelDepth)

'''
====================
Monster Class
====================
'''

class Monster(Actor):
	pass

'''
====================
====================
'''

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
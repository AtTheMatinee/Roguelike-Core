'''
commands.py
'''
import random

import actors

import libtcodpy as libtcod

from items import Equipment

import Items.rangedWeapons
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

					#elif canPush: Push
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
		armour penetration,
		fire,
		frost,
		poison,
		bleed,
		holy,
		unholy,
		unblockable
		]
		'''
		self.energyCost = 20 - int(actor.stats.get("attackSpeed"))

	def perform(self):
		attack = self.actor.stats.get('attack')
		critChance = self.actor.stats.get('critChance')

		# calculate Critical Damage (for physical damage only)
		if ((random.random() <= critChance) and
			(attack[0] > 0)):
			attack[0] += random.randint(1,int(attack[0]))

		if self.actor == self.actor.game.hero or self.target == self.actor.game.hero:
			self.actor.game.message(self.actor.getName(True).title() + " attacks " + self.target.getName(True))

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
	def __init__(self,actor,target):
		self.actor = actor
		self.target = target

		if ((self.actor.equipSlots[2] != None) and
			(isinstance(self.actor.equipSlots[2], rangedWeapons.RangedWeapon) == True) ):
			self.weapon = self.actor.equipSlots[2]
		else: self.weapon = False

class LoadRangedWeapon(Command):
	pass

class ThrowCommand(Command):
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
						self.game.message("You cannot carry "+item.getName(True))
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

	def perform(self):
		success = False
		alternative = None

		self.item.dropFromInventory(self.actor)

		self.actor.energy -= self.energyCost
		# set flags that change when a turn is taken
		self.actor.hasTakenTurn()

		success = True
		alternative = None

		return success, alternative


class EquipCommand(Command):
	# TODO: Implement multi-slot equipment
	
	def __init__(self,actor,item):
		self.actor = actor
		self.item = item

		self.energyCost = 12
	def perform(self):
		# Check to see if the actor is allowed to equip this
		if isinstance(self.item, Equipment):
			# Actor cannot equip equipment
			if ((self.item.equipSlot == 0) and (self.actor.canEquipArmor == False) or
				(self.item.equipSlot == 1) and (self.actor.canEquipWeapons == False)):
				self.actor.game.message(self.actor.getName(True)+" cannot equip "+self.item.getName(True))
				success = False
				alternative = None
				return success,alternative

			# Remove the item from the actor's inventory 
			#if self.item in self.actor.inventory:
				#self.actor.inventory.remove(self.item)

			if (self.actor.equipSlots[self.item.equipSlot] == None):

				# The slot is empty, equip the item in its slot
				#self.actor.equipSlots[self.item.equipSlot] = self.item
				#self.actor.stats.addModifier(self.item,self.item.modifier)
				self.actor.equipItem(self.item)

			else:
				# Unequip the item in the taken slot
				itemToUnequip = self.actor.equipSlots[self.item.equipSlot]
				unequip = UnequipCommand(self.actor, itemToUnequip)
				success, alternative = unequip.perform()

				if success == False:
					# If it fails, re-add the item to the player's inventory and return False
					#self.actor.inventory.append(self.item)
					return success, alternative
				
				# Equip the new item
				#self.actor.equipSlots[self.item.equipSlot] = self.item
				#self.actor.stats.addModifier(self.item,self.item.modifier)
				self.actor.equipItem(self.item)

			self.actor.game.message(self.actor.getName(True)+" has equipped a "+self.item.getName(False))
			self.actor.energy -= self.energyCost
			# set flags that change when a turn is taken
			self.actor.hasTakenTurn()
			
			success = True
			alternative = None

		else:
			success = False
			alternative = None

		return success, alternative


class UnequipCommand(Command):
	def __init__(self,actor,item):
		self.actor = actor
		self.item = item

		self.energyCost = 0

	def perform(self):
		# see if item can be unequipped
		if self.item.canBeUnequipped == True:
			# remove it from the appropriate equip slot
			self.actor.equipSlots[self.item.equipSlot] = None
			self.actor.stats.removeModifier(self.item)

			# See if the item will fit in the actor's inventory
			if (len(self.actor.inventory)+1 <= self.actor.inventorySize):
				self.actor.inventory.append(self.item)
			else:
				# If inventory is full, drop the item on the ground
				self.item.dropFromInventory(self.actor)

			success = True
			alternative = False

		else:
			self.actor.game.message(self.item.getName(True).title()+" cannot be unequipped.")
			success = False
			alternative = None

		return success,alternative


class GoUpStairsCommand(Command):
	def __init__(self,actor):
		self.actor = actor
		self.energyCost = 12

	def perform(self):
		game = self.actor.game
		currentLevel = game._currentLevel
		newLevelIndex = currentLevel.levelDepth-1 # levelDepth increases as you go down
		newLevel = game.map._levels[newLevelIndex] 

		# See if you are on an up staircase
		if ((self.actor.x == currentLevel.stairsUp.x) and 
			(self.actor.y == currentLevel.stairsUp.y) and
			(0 <= newLevelIndex < len(game.map._levels)) ):

			# Move the actor to the new level
			currentLevel.removeObject(self.actor)
			currentLevel.removeActor(self.actor)

			newLevel.addObject(self.actor)
			newLevel.addActor(self.actor)

			# if the actor is the player, load the new level
			if self.actor == game.hero:
				game.map.loadLevel(newLevelIndex)
				libtcod.console_clear(game.ui.con)

				# place actor on down stairs
				self.actor.x = newLevel.stairsDown.x
				self.actor.y = newLevel.stairsDown.y



			else:
				# if the level has been generated, place actor around down stairs
				if newLevel.stairsDown != None:
					self.actor.x = newLevel.stairsDown.x
					self.actor.y = newLevel.stairsDown.y

			self.actor.energy -= self.energyCost
			# set flags that change when a turn is taken
			self.actor.hasTakenTurn()
			success = True
			alternative = None

		else:
			success = False
			alternative = None

		return success, alternative


class GoDownStairsCommand(Command):
	def __init__(self,actor):
		self.actor = actor
		self.energyCost = 12

	def perform(self):
		game = self.actor.game
		currentLevel = game._currentLevel
		newLevelIndex = currentLevel.levelDepth+1 # levelDepth increases as you go down
		newLevel = game.map._levels[newLevelIndex] 

		# See if you are on a down staircase
		if ((self.actor.x == currentLevel.stairsDown.x) and 
			(self.actor.y == currentLevel.stairsDown.y) and
			(0 <= newLevelIndex < len(game.map._levels)) ):

			# Move the actor to the new level
			currentLevel.removeObject(self.actor)
			currentLevel.removeActor(self.actor)

			newLevel.addObject(self.actor)
			newLevel.addActor(self.actor)

			# if the actor is the player, load the new level
			if self.actor == game.hero:
				game.map.loadLevel(newLevelIndex)
				libtcod.console_clear(game.ui.con)

				# place actor on down stairs
				self.actor.x = newLevel.stairsUp.x
				self.actor.y = newLevel.stairsUp.y

			else:
				# if the level has been generated, place actor around down stairs
				if newLevel.stairsDown != None:
					self.actor.x = newLevel.stairsUp.x
					self.actor.y = newLevel.stairsUp.y

			self.actor.energy -= self.energyCost
			# set flags that change when a turn is taken
			self.actor.hasTakenTurn()
			success = True
			alternative = None

		else:
			success = False
			alternative = None

		return success, alternative

#class PushedCommand(Command):


#class PulledCommand(Command):

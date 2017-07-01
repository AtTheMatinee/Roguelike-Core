'''
rangedWeapons.py
'''
import actors
from items import Equipment,Item
import commands
'''
====================
Ranged Weapons
====================
'''
class Ammo(Item):
	identified = True
	def __init__(self, game, x, y, char, name, color, level, number, damage):
		Item.__init__(self, game, x, y, char, name, color, level, blocks=False, properNoun = False)
		self.number = int(number)
		self.damage = damage

	def hitEffect(self, obj):
		if isinstance(obj, actors.Actor):
			obj.takeDamage(self.damage)

	def use(self,actor):
		# create equip command
		loadAmmo = commands.LoadRangedWeaponCommand(actor,self)
		# set equip command's energyCost to 0, since you are already paying for UseCommand's cost
		loadAmmo.energyCost = 0
		# process equip command
		success,alternative = loadAmmo.perform()

		# if the item was equipped, return true, else return false
		return success

	def getName(self,useDefiniteArticle,showLevel = False):
		name = self.name
		if useDefiniteArticle == True and self.properNoun == False:
			if self.__class__.identified == True:
				name = "the "+self.name
			else:
				name = "the "+self.__class__.unidentifiedName

		#if useIndefiniteArticle:
		else:
			if self.__class__.identified == True:
				name = self.name
			else:
				name = self.__class__.unidentifiedName

		if (self.__class__.identified == True) and (showLevel == True):
			name = name+" ("+str(self.number)+")"
		
		return name


	def moveToInventory(self,actor):
		# Special move to inventory method for stacking items
		if self in self.game._currentLevel._objects:
			self.game._currentLevel.removeItem(self)
			self.game._currentLevel.removeObject(self)

		# See if there is any ammo of this type already in the inventory
		if any(isinstance(item, self.__class__) for item in actor.inventory):
			for item in actor.inventory:
				if item.name == self.name:
					# if there is, combine the stacks of ammo instead of adding a second stack
					item.number += self.number
					return

		actor.inventory.append(self)

class Bolts(Ammo):
	pass

class Arrows(Ammo):
	pass

class Darts(Ammo):
	pass


class RangedWeapon(Equipment):
	identified = True
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, maxRange, maxRounds, attackSpeed, ammoTypes = [], blocks=False):
		Equipment.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)
		self.equipSlot = 2

		self.maxRange = maxRange
		self.maxRounds = maxRounds
		self.attackSpeed = attackSpeed
		self.ammoTypes = ammoTypes

		self.loadedAmmoType = None
		self.loadedRounds = 0
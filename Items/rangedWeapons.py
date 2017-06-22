'''
rangedWeapons.py
'''
from items import Equipment,Item
'''
====================
Ranged Weapons
====================
'''
class Ammo(Item):
	def __init__(self, game, x, y, char, name, color, level, damage):
		Item.__init__(self, game, x, y, char, name, color, level, blocks=False, properNoun = False)
		self.damage = damage



class RangedWeapon(Equipment):
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, maxRange, attackSpeed, ammoTypes = [], blocks=False):
		Equipment.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)
		self.equipSlot = 2

		self.maxRange = maxRange
		self.attackSpeed = attackSpeed
		self.ammoTypes = ammoTypes
		self.loadedWith = []
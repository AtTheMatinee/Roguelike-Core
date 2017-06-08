'''
weapons.py
'''

from items import Equipment

'''
====================
Weapons
====================
'''

'''
class Equipment(Item):
	identified = True
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Item.__init__(self, game, x, y, char, name, color, level, blocks=False)
		self.equipSlot = equipSlot
		self.modifier = modifier

	def useItem(self,actor):
		self.equip(actor)

	def equip(self,actor):
		# TODO: move to commands
		actor.stats.addModifier(self,self.modifier)

	def unequip(self,actor):
		# TODO: move to commands
		actor.stats.removeModifier(self)

	def upgrade(self,level):
		pass

'''

class Weapon(Equipment):
	unidentifiedName = "Mysterious Potion"
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Equipment.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)
		self.equipSlot = 1
		'''
		Set default upgrade values for all stats for weapons, in case a weapon somehow gets a unusual modifier.
		'''


class Sword(Weapon):
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Weapon.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)

		'''
		attack[
		physical damage
		armor penetration
		fire damage
		frost damage
		poison damage
		bleed chance
		holy damage
		unholy damage
		unblockable damage
		]
		attackSpeed
		critChance
		''' 

class Mace(Weapon):
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Weapon.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)


class Spear(Weapon):
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Weapon.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)


class Dagger(Weapon):
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Weapon.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)





'''class MagicRing:
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

ring = MagicRing()
herostats.addModifier(ring.id,ring.modifier)
print herostats.get("healthMax")

robe = MagicRobe()
herostats.addModifier(robe.id,robe.modifier)
print herostats.get("healthMax")

hat = MagicHat()
herostats.addModifier(hat.id,hat.modifier)
print herostats.get("healthMax")'''
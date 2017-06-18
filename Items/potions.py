'''
potions.py
'''
from items import Item
import statusEffects
import libtcodpy as libtcod
'''
====================
Potions
====================
'''

class Potion(Item):
	identified = False
	unidentifiedName = "Mysterious Potion"
	def __init__(self, game, x, y, char, name, color, level, blocks=False):
		Item.__init__(self, game, x, y, char, name, color, level, blocks=False)


class HealthPotion(Potion):
	def __init__(self, game, x, y, char, name, color, level, blocks=False):
		Potion.__init__(self, game, x, y, char, name, color, level, blocks=False)
		
		self.healValue = 8 + 8*level

	def use(self,actor):
		#TODO: implement a fail state
		actor.heal(self.healValue)

		if self in actor.inventory:
			actor.inventory.remove(self)
			actor.game.message(actor.getName(True).title()+" drinks a "+self.getName(False))

		if self.__class__.identified == False:
			self.__class__.identified = True
			actor.game.message("You have identified "+self.getName(True),libtcod.cyan)

		return True


class Antidote(Potion):
	def __init__(self, game, x, y, char, name, color, level, blocks=False):
		Potion.__init__(self, game, x, y, char, name, color, level, blocks=False)

	def use(self,actor):
		# cure poison, if poisoned
		if any(isinstance(se, statusEffects.Poisoned) for se in actor.statusEffects):
			for se in actor.statusEffects:
				if (isinstance(se, statusEffects.Poisoned)):
					se.remove()

			# if it cures poison, identify it
			if self.__class__.identified == False:
				self.__class__.identified = True
				actor.game.message("You have identified "+self.getName(True),libtcod.cyan)

		if self in actor.inventory:
			actor.inventory.remove(self)
			actor.game.message(actor.getName(True).title()+" drinks a "+self.getName(False))

		return True


class Permafrost(Potion):
	def __init__(self, game, x, y, char, name, color, level, blocks=False):
		Potion.__init__(self, game, x, y, char, name, color, level, blocks=False)

	def use(self,actor):
		# cure poison, if poisoned
		if any(isinstance(se, statusEffects.Flaming) for se in actor.statusEffects):
			for se in actor.statusEffects:
				if (isinstance(se, statusEffects.Flaming)):
					se.remove()

		else:
			actor.takeDamage([0,0,0, 20, 0,0,0,0,0])

		if self in actor.inventory:
			actor.inventory.remove(self)
			actor.game.message(actor.getName(True).title()+" drinks a "+self.getName(False))

		# if potion is unidentified, identify it
		if self.__class__.identified == False:
			self.__class__.identified = True
			actor.game.message("You have identified "+self.getName(True),libtcod.cyan)

		return True


class Firebrew(Potion):
	def __init__(self, game, x, y, char, name, color, level, blocks=False):
		Potion.__init__(self, game, x, y, char, name, color, level, blocks=False)

	def use(self,actor):
		# cure poison, if poisoned
		if any(isinstance(se, statusEffects.Frozen) for se in actor.statusEffects):
			for se in actor.statusEffects:
				if (isinstance(se, statusEffects.Frozen)):
					se.remove()

		else:
			actor.takeDamage([0,0, 20, 0,0,0,0,0,0])

		if self in actor.inventory:
			actor.inventory.remove(self)
			actor.game.message(actor.getName(True).title()+" drinks a "+self.getName(False))

		# if potion is unidentified, identify it
		if self.__class__.identified == False:
			self.__class__.identified = True
			actor.game.message("You have identified "+self.getName(True),libtcod.cyan)

		return True
		

'''
potions.py
'''
from items import Item
import actors
import statusEffects
import libtcodpy as libtcod
'''
====================
Potions
====================

TODO:
	Holy Water
	Water
	Oil
	Ghost Essence
'''

class Potion(Item):
	identified = False
	unidentifiedName = "Mysterious Potion"
	def __init__(self, game, x, y, char, name, color, level, blocks=False):
		Item.__init__(self, game, x, y, char, name, color, level, blocks=False)

	def destroy(self,actor):
		if self in actor.inventory:
			actor.inventory.remove(self)
			actor.game.message(actor.getName(True).title()+" drinks a "+self.getName(False))

		# destroy if placed on map
		if self in self.game._currentLevel._objects:
			self.game._currentLevel._objects.remove(self)
		if self in self.game._currentLevel._items:
			self.game._currentLevel._items.remove(self)

	def thrownEffect(self,obj):	
		if isinstance(obj, actors.Actor):
			# defines what happens if the thrown object hits an actor
			self.game.message(obj.getName(True)+" was hit by a "+self.getName(False))
			self.use(obj)

class HealthPotion(Potion):
	def __init__(self, game, x, y, char, name, color, level, blocks=False):
		Potion.__init__(self, game, x, y, char, name, color, level, blocks=False)
		
		self.potency = 8 + 8*level

	def use(self,actor):
		actor.heal(self.potency)

		self.destroy(actor)

		if self.__class__.identified == False:
			self.__class__.identified = True
			actor.game.message("You have identified "+self.getName(True),libtcod.cyan)

		return True


class Poison(Potion):
	def __init__(self, game, x, y, char, name, color, level, blocks=False):
		Potion.__init__(self, game, x, y, char, name, color, level, blocks=False)

		self.potency = 3 + 2*level

	def use(self,actor):
		actor.addStatusEffect(statusEffects.Poisoned, self.potency, False)
		actor.takeDamage([0,0,0,0, self.potency, 0,0,0,0])

		self.destroy(actor)

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

		self.destroy(actor)

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

		self.destroy(actor)

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

		self.destroy(actor)

		# if potion is unidentified, identify it
		if self.__class__.identified == False:
			self.__class__.identified = True
			actor.game.message("You have identified "+self.getName(True),libtcod.cyan)

		return True
		
class GhostEssence(Potion):
	def __init__(self, game, x, y, char, name, color, level, blocks=False):
		Potion.__init__(self, game, x, y, char, name, color, level, blocks=False)

	def use(self,actor):
		actor.takeDamage([0,0,0,0,0,0,0,0,20])
		# Curse

		self.destroy(actor)

		# if potion is unidentified, identify it
		if self.__class__.identified == False:
			self.__class__.identified = True
			actor.game.message("You have identified "+self.getName(True),libtcod.cyan)

		return True
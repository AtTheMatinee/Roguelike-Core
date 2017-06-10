'''
potions.py
'''
from items import Item
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
		
		self.healValue = 8

	def use(self,actor):
		#TODO: implement a fail state
		actor.heal(self.healValue)

		if self in actor.inventory:
			actor.inventory.remove(self)
			actor.game.message(actor.name+" drinks a "+self.getName(False))

		if self.__class__.identified == False:
			self.__class__.identified = True
			actor.game.message("You have identified "+self.getName(True),libtcod.cyan)

		return True
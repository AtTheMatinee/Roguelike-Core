'''
potions.py
'''
from items import Item
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

	def getName(self):
		if self.__class__.identified == True:
			return self.name
		else: return self.__class__.unidentifiedName


class HealthPotion(Potion):
	def __init__(self, game, x, y, char, name, color, level, blocks=False):
		Potion.__init__(self, game, x, y, char, name, color, level, blocks=False)
		
		self.healValue = 8

	def use(self,actor):
		#TODO: implement a fail state
		actor.heal(self.healValue)

		if self in actor.inventory:
			actor.inventory.remove(self)
			actor.game.message(actor.name+" drinks a "+self.getName())

		if self.__class__.identified == False:
			self.__class__.identified = True
			actor.game.message("You have identified the "+self.getName())

		return True
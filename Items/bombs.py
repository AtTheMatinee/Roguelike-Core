'''
bombs.py
'''
from items import Item
'''
====================
Bombs
====================
'''

class Bomb(Item):
	identified = False
	def __init__(self, game, x, y, char, name, color, level, timer, blocks=False, properNoun = False):
		Item.__init__(self, game, x, y, char, name, color, level, blocks)

	def tick(self):
		if timer == 0:
			self.effect()
			return

		timer -= 1

	def effect(self):
		self.game._currentLevel.removeItem(self)
		self.game._currentLevel.removeObject(self)


class Grenade(Bomb):
	pass

class GasGrenade(Bomb):
	pass

class Spellbomb(Bomb):
	pass
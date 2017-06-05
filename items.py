'''
items.py
'''
from objects import Object
'''
====================
Items
====================
'''
class Item(Object):
	def useItem(self,actor):
		pass

class Equipment(Item):
	def useItem(self,actor):
		self.equip(actor)
	def equip(self,actor):
		pass
	def unequip (self,actor):
		pass

''' 
Gauntlet
Sword
Staff
Bow
Axe
Club
Dagger
'''
'''
itemSpawner.py
'''
import random
import Items
import libtcodpy as libtcod
'''
====================
Item Spawner
====================
'''

class ItemSpawner:
	def __init__(self,game):
		self.game = game
		self.itemType = None
		self.itemChangeChance = .2

		'''
		The loot heirarchy is a dictionary of lists of every item's parent and children classes.
		self._lootHeirarchy[item][parent][children]
		'_Special' branches are never deliberately spawned and can only happen by chance
		'''
		self._lootHeirarchy = {
		'Item':[None,['Potion','Equipment']], #'_Special'
		'Potion':['Item',['Medicine']], #'Poison','_Special'
		'Medicine':['Potion',['Health Potion']],
		'Health Potion':['Medicine',[]],
		'Equipment':['Item',['Weapon','Armor']], # Rings
		'Weapon':['Equipment',['Heavy Weapon','Light Weapon']], # Ranged Weapon
		'Heavy Weapon':['Weapon',['Mace']], # Axe, Club, Hammer, Maul, Halbard
		'Light Weapon':['Weapon',['Dagger','Sword','Spear']], # Machete, Staff, Claw, Hook
		'Dagger':['Light Weapon',[]],
		'Mace':['Heavy Weapon',[]],
		'Spear':['Light Weapon',[]],
		'Sword':['Light Weapon',[]],
		'Armor':['Equipment',['Hauberk']], # 'Heavy Armor','Light Armor'
		'Hauberk':['Armor',[]]
		}

		self.spawnMethods = {
		'Health Potion':self.spawnHealthPotion,
		'Dagger':self.spawnDagger,
		'Mace':self.spawnMace,
		'Spear':self.spawnSpear,
		'Sword':self.spawnSword,
		'Hauberk':self.spawnHealthPotion,
		}
	
	def getRandomLoot(self,item,canRandomize):
		# small chance to generate items of a different type
		self.itemType = item

		if canRandomize == True:
			# move up the hierarchy
			while self.itemType != 'Item':
				if (random.random() <= self.itemChangeChance):
					self.itemType = self.getParent(self.itemType)
				else: break

		# move down the hierarchy
		children = self.getChildren(self.itemType)
		while children:
			self.itemType = children[random.randint(0,len(children)-1) ]

			children = self.getChildren(self.itemType)

		return self.itemType

	def spawn(self,x,y,itemKey,level,randomize):
		itemKey = self.getRandomLoot(itemKey,randomize)
		
		if itemKey in self.spawnMethods:
			item = self.spawnMethods[itemKey](x,y,level)
			return item

	def getParent(self,item):
		if item in self._lootHeirarchy:
			return self._lootHeirarchy[item][0]
		else: print "PARENT ERROR"

	def getChildren(self,item):
		if item in self._lootHeirarchy:
			return self._lootHeirarchy[item][1]

		else: print "CHILD ERROR"

	def spawnDagger(self,x,y,level):
		modifier = {
		'add':{'attack':[2.0,0,0,0,0,0,0,0,0], 'attackSpeed':4},
		'mult':{'critChance':.5}
		}
		item = Items.weapons.Dagger(self.game, x, y, chr(24), "Dagger", libtcod.azure, level, 1, modifier)
		return item

	def spawnHealthPotion(self,x,y,level):
		item = Items.potions.HealthPotion(self.game, x, y, '!', "Health Potion", libtcod.azure, level, blocks=False)
		return item

	def spawnMace(self,x,y,level):
		modifier = {
		'add':{'attack':[3.0,2,0,0,0,0,0,0,0], 'attackSpeed':-2},
		}
		item = Items.weapons.Mace(self.game, x, y, chr(24), "Mace", libtcod.azure, level, 1, modifier)
		return item

	def spawnSpear(self,x,y,level):
		modifier = {'add':{'attack':[4.0,1,0,0,0,0,0,0,0]}}
		item = Items.weapons.Spear(self.game, x, y, chr(24), "Spear", libtcod.azure, level, 1, modifier)
		return item

	def spawnSword(self,x,y,level):
		modifier = {'add':{'attack':[3.0,0,0,0,0,0.1,0,0,0]}}
		item = Items.weapons.Sword(self.game, x, y, chr(24), "Sword", libtcod.azure, level, 1, modifier)
		return item

'''
for i in xrange(level):
	pick an item stat to level up at random
	each item will have it's own values that determine how much each stat is increased by

'''

if __name__ == '__main__':
	spawner = ItemSpawner(None)
	for i in xrange(10):
		print spawner.getRandomLoot('Dagger')
	print
	for i in xrange(10):
		print spawner.getRandomLoot('Potion')
	print
	for i in xrange(10):
		print spawner.getRandomLoot('Equipment')
	print
	for i in xrange(10):
		print spawner.getRandomLoot('Hauberk')
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
		'Item':[None,['Potion','Equipment']], #'_Special','Food'
		'Potion':['Item',['Medicine']], #'Poison','_Special'
		'Medicine':['Potion',['Health Potion','Firebrew Potion','Antidote','Permafrost Potion']],
		'Health Potion':['Medicine',[]],
		'Firebrew Potion':['Medicine',[]],
		'Permafrost Potion':['Medicine',[]],
		'Antidote':['Medicine',[]],
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
		'Antidote':self.spawnAntidote,
		'Firebrew Potion':self.spawnFirebrewPotion,
		'Permafrost Potion':self.spawnPermafrostPotion,
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
		
		# items have a slight chance of spawning at a higher or lower level
		if randomize == True:
			chance = random.random()
			if (chance <= 0.1) and (level > 0):
				level -= 1
			elif (chance >= 0.9):
				level += 1

		if itemKey in self.spawnMethods:
			item = self.spawnMethods[itemKey](x,y,level)
			item.upgrade(level)
			return item

	def getParent(self,item):
		if item in self._lootHeirarchy:
			return self._lootHeirarchy[item][0]
		else: print "PARENT ERROR"

	def getChildren(self,item):
		if item in self._lootHeirarchy:
			return self._lootHeirarchy[item][1]

		else: print "CHILD ERROR"

	# ==== Item Methods ====
	def spawnAntidote(self,x,y,level):
		item = Items.potions.Antidote(self.game, x, y, '!', "Antidote", libtcod.azure, level, blocks=False)
		return item

	def spawnDagger(self,x,y,level):
		modifier = {
		'add':{'attack':[2.0,0,0,0,0,0,0,0,0], 'attackSpeed':4},
		'mult':{'critChance':0.5}
		}
		item = Items.weapons.Dagger(self.game, x, y, chr(24), "Dagger", libtcod.azure, level, 1, modifier)
		return item

	def spawnFirebrewPotion(self,x,y,level):
		item = Items.potions.Firebrew(self.game, x, y, '!', "Firebrew Potion", libtcod.azure, level, blocks=False)
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

	def spawnPermafrostPotion(self,x,y,level):
		item = Items.potions.Permafrost(self.game, x, y, '!', "Permafrost Potion", libtcod.azure, level, blocks=False)
		return item

	def spawnSpear(self,x,y,level):
		modifier = {'add':{'attack':[5.0,0,0,0,0,0.1,0,0,0]}}
		item = Items.weapons.Spear(self.game, x, y, chr(24), "Spear", libtcod.azure, level, 1, modifier)
		return item

	def spawnSword(self,x,y,level):
		modifier = {'add':{'attack':[3.0,0,0,0,0,0.1,0,0,0]}}
		item = Items.weapons.Sword(self.game, x, y, chr(24), "Sword", libtcod.azure, level, 1, modifier)
		return item
		

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
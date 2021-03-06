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
		self._defaultIdentification = {}
		self.itemChangeChance = .2

		'''
		The loot heirarchy is a dictionary of lists of every item's parent and children classes.
		self._lootHeirarchy[item][parent][children]
		'_Special' branches are never deliberately spawned and can only happen by chance
		Some items have references to a parent, but the parent has no reference back to the item
			so that the item can mutate into similar items, but other items cannot mutate into it.
		'''
		self._lootHeirarchy = {
		'Item':[None,['Potion','Equipment','Ammo','Bomb']], #'_Special','Food','Magic Item'

		'Potion':['Item',['Medicine','Toxin']], #'_Special'
		'Medicine':['Potion',['Health Potion','Antidote','Invisibility Potion','Regeneration Potion']],
		'Toxin':['Potion',['Poison','Firebrew Potion','Permafrost Potion']],
		'Antidote':['Medicine',[]],
		'Health Potion':['Medicine',[]],
		'Invisibility Potion':['Medicine',[]],
		'Regeneration Potion':['Medicine',[]],
		'Poison':['Toxin',[]],
		'Firebrew Potion':['Toxin',[]],
		'Permafrost Potion':['Toxin',[]],

		'Equipment':['Item',['Weapon','Armor']], # Rings

		'Weapon':['Equipment',['Melee Weapon','Ranged Weapon']],
		'Melee Weapon':['Weapon',['Heavy Weapon','Light Weapon','Pole Arm']],
		'Heavy Weapon':['Weapon',['Mace']], # Axe, Club, Hammer, Maul, Morning Star,
		'Light Weapon':['Weapon',['Dagger','Sword']], # Machete, Staff, Claw, Hook, Curved Sword, Estoc,
		'Pole Arm':['Weapon',['Spear']], # Halbard, Scythe
		'Ranged Weapon':['Weapon',['Light Crossbow']],
		'Dagger':['Light Weapon',[]],
		'Mace':['Heavy Weapon',[]],
		'Spear':['Pole Arm',[]],
		'Sword':['Light Weapon',[]],
		'Serpent Sword':['Light Weapon',[]], # This was intentionally left out of 'Light Weapon' children
		'Light Crossbow':['Ranged Weapon',[]],


		'Armor':['Equipment',['Light Armor']], # 'Heavy Armor', 'Clothes'
		'Light Armor':['Armor',['Hauberk','Quilted Jacket']],
		'Hauberk':['Light Armor',[]],
		'Quilted Jacket':['Light Armor',[]],

		'Ammo':['Item',['Wooden Bolt','Steel Bolt']],
		'Wooden Bolt':['Ammo',[]],
		'Steel Bolt':['Ammo',[]],

		'Bomb':['Items',['Grenade','Smokebomb']],
		'Grenade':['Bomb',[]],
		'Smokebomb':['Bomb',[]]
		}
		'''
		Food
		Water
		Poisons
		Rings

		Bow (Secondary)
		Crossbow (Secondary)
		Shield (Secondary)
		Whip (Secondary)

		Wands (Primary Weapon that acts like multiple scrolls)
		Scrolls
		Books (Perminantly learn spells)

		Sword <Serpent Sword>
		Dagger
		Spear
		Mace
		Axe
		Club
		Hammer
		Maul
		Halbard *
		Scythe *
		Pitchfork *
		Lance *
		Morning Star
		Machete
		Staff
		Claw
		Hook
		Curved Sword
		Estoc (high armorPiercing damage)
		Javelin (terrible weapon except when thrown)

		ARMOR (affects defense, speed)
		Quilted Jacket [1.5,0.1,0.1,0,0,0,0]
		Leather Armor
		Hauberk [1.5,0,0,0,0.2,0,0]
		Brigandine
		Reinforced Chainmail
		Breastplate <Serpent Armour>
		Platemail Armor
		Fur Lined Armor
		Cloak
		Church Robes
		Occult Robes
		Leather Coat (Fire resistant)
		'''

		self.spawnMethods = {
		'Health Potion':self.spawnHealthPotion,
		'Poison':self.spawnPoison,
		'Antidote':self.spawnAntidote,
		'Firebrew Potion':self.spawnFirebrewPotion,
		'Permafrost Potion':self.spawnPermafrostPotion,
		'Invisibility Potion':self.spawnInvisibilityPotion,
		'Regeneration Potion':self.spawnRegenerationPotion,
		'Dagger':self.spawnDagger,
		'Mace':self.spawnMace,
		'Spear':self.spawnSpear,
		'Sword':self.spawnSword,
		'Light Crossbow':self.spawnLightCrossbow,
		'Serpent Sword':self.spawnSerpentSword,
		'Hauberk':self.spawnHauberk,
		'Quilted Jacket':self.spawnQuiltedJacket,
		'Serpent Armor':self.spawnHealthPotion,
		'Wooden Bolt':self.spawnWoodenBolt,
		'Steel Bolt':self.spawnSteelBolt,
		'Grenade':self.spawnGrenade,
		'Smokebomb':self.spawnSmokebomb
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
			index = random.randint(0,len(children)-1)
			self.itemType = children[index]

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

			# give the item a reference to it's own spawn key
			item._spawnKey = itemKey

			# store the default state of the item's class.identified variable, so it can be reset when you quit the game
			if item.__class__ not in self._defaultIdentification:
				identification = item.__class__.identified
				self._defaultIdentification[item.__class__] = identification

			return item

	def getParent(self,item):
		if item in self._lootHeirarchy:
			return self._lootHeirarchy[item][0]
		else: print "PARENT ERROR: "+str(item)

	def getChildren(self,item):
		if item in self._lootHeirarchy:
			return self._lootHeirarchy[item][1]

		else: print "CHILD ERROR: "+str(item)

	def resetIdentification(self):
		for class_, identification in self._defaultIdentification.items():
			class_.identified = identification

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

	def spawnGrenade(self,x,y,level):
		item = Items.bombs.Grenade(self.game, x, y, '*', 'Grenade', libtcod.azure, level, 3)
		return item

	def spawnHauberk(self,x,y,level):
		modifier = {
		'add':{'defense':[1.5,0,0,0,0.2,0,0]}
		}
		item = Items.armor.Hauberk(self.game, x, y, ']', "Hauberk", libtcod.azure, level, 0, modifier)
		return item

	def spawnHealthPotion(self,x,y,level):
		item = Items.potions.HealthPotion(self.game, x, y, '!', "Health Potion", libtcod.azure, level, blocks=False)
		return item

	def spawnInvisibilityPotion(self,x,y,level):
		item = Items.potions.InvisibilityPotion(self.game, x, y, '!', "Invisibility Potion", libtcod.azure, level, blocks=False)
		return item

	def spawnLightCrossbow(self,x,y,level):
		modifier = {}
		ammoTypes = [Items.rangedWeapons.Bolts]
		item = Items.rangedWeapons.RangedWeapon(self.game, x, y, chr(24), "Light Crossbow", libtcod.azure, level, 2, modifier, 8, 6, -4, ammoTypes, blocks=False)
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

	def spawnPoison(self,x,y,level):
		item = Items.potions.Poison(self.game, x, y, '!', "Poison", libtcod.azure, level, blocks = False)
		return item

	def spawnQuiltedJacket(self,x,y,level):
		modifier = {
		'add':{'defense':[1.5,0.1,0.1,0,0,0,0]}
		}
		item = Items.armor.Hauberk(self.game, x, y, ']', "Quilted Jacket", libtcod.azure, level,  0, modifier)
		return item

	def spawnRegenerationPotion(self,x,y,level):
		item = Items.potions.RegenerationPotion(self.game, x, y, '!', "Regeneration Potion", libtcod.azure, level, blocks=False)
		return item

	def spawnSerpentArmor(self,x,y,level):
		pass
		# Special varient of the chest plate armour

	def spawnSerpentSword(self,x,y,level):
		modifier = {'add':{'attack':[2.5,0,0,0,0.5,0.15,0,0,0]}}
		# TODO: possibly change this into a curved sword
		item = Items.weapons.Sword(self.game, x, y, chr(24), "Serpent Sword", libtcod.azure, level, 1, modifier)
		item.upgradePhysicalDamage = [1.0, 0,0,0,0,0,0,0,0]
		return item

	def spawnSmokebomb(self,x,y,level):
		item = Items.bombs.Smokebomb(self.game, x, y, '*', 'Smokebomb', libtcod.azure, level, 1)
		return item

	def spawnSpear(self,x,y,level):
		modifier = {'add':{'attack':[5.0,0,0,0,0,0.1,0,0,0]}}
		item = Items.weapons.Spear(self.game, x, y, chr(24), "Spear", libtcod.azure, level, 1, modifier)
		return item

	def spawnSteelBolt(self,x,y,level):
		number = random.randint(4,10)
		damage = [4,1,0,0,0,0,0,0,0]
		item = Items.rangedWeapons.Bolts(self.game, x, y, '/', "Steel Bolt", libtcod.azure, level, number, damage)
		return item

	def spawnSword(self,x,y,level):
		modifier = {'add':{'attack':[3.0,0,0,0,0,0.1,0,0,0]}}
		item = Items.weapons.Sword(self.game, x, y, chr(24), "Sword", libtcod.azure, level, 1, modifier)
		return item

	def spawnWoodenBolt(self,x,y,level):
		number = random.randint(4,14)
		damage = [3,0,0,0,0,0,0,0,0]
		item = Items.rangedWeapons.Bolts(self.game, x, y, '/', "Wooden Bolt", libtcod.azure, level, number, damage)
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
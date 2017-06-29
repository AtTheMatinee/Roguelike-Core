'''
actorSpawner.py
'''
import random
import actors
import actorStats
import states
import libtcodpy as libtcod
'''
====================
Actor Spawner
====================
'''

# TODO: Actors with inventorySize > 0 will sometimes spawn with items
# TODO: Revamp how monsters work
'''
	Monsters spawn at a certain level, which is consistant among monsters of that type
	Monsters upgrade the same way that items do
	Since monsters upgrade according to their level, monsters will vary more between 
	instances as the levels get higher
	Monsters that spawn in with gear will have gear appropriate to their levels
'''

class ActorSpawner:
	def __init__(self,game):
		self.game = game

		self.spawnMethods = {
			'Hero':self.spawnHero,
			'Gargoyle':self.spawnGargoyle,
			'Ghost':self.spawnGhost,
			'Golem':self.spawnGolem,
			'Angel':self.spawnAngel,
			'Demon':self.spawnDemon,
			'Cultist':self.spawnCultist,
			'Fire Elemental':self.spawnFireElemental,
			'Frost Elemental':self.spawnFrostElemental,
			'Swamp Hag':self.spawnSwampHag,
			'Mirehound':self.spawnMirehound,
			'Mimic':self.spawnChest,
			'Plague Rat':self.spawnPlagueRat,
			'Rougarou':self.spawnRougarou,
			'Snakeman':self.spawnSnakeman,
			'Snakeman Archer':self.spawnSnakemanArcher,
			'Wyrm':self.spawnWyrm,
			'Knight':self.spawnKnight
			}
		'''
			Hero
				Test
				Arbalest - Crossbow, Brigandine, ammo, health potion
				Assassin - Cloak and Dagger, various poisons (unidentified)
				Barbarian - Axe
				Cleric - Mace, Preist Robes, Heal Spell
				Knight - Plate Armor, Sword, and 
				Occultist - Dagger, debuff and offensive spells but low magic, so spells must be cast from HP
				Magician - weak spells, some magical items
				Mercenary - random, leveled up Armor and Weapon
				Alchemist - Begins with random potions identified
				Druid
			Lancer
			Brute
			Archer
			Rogue
		'''

	def spawn(self,x,y,key):
		level = 0
		if key in self.spawnMethods:
			actor = self.spawnMethods[key](x,y,level)

			# give the actor a reference to its own spawn key
			actor._spawnKey = key
			return actor

	def spawnAngel(self,x,y,level):
		pass

	def spawnAutomaton(self,x,y,level):
		pass

	def spawnCultist(self,x,y,level):
		pass

	def spawnDemon(self,x,y,level):
		pass

	def spawnHero(self,x,y,level):
		hero = actors.Hero(self.game,x,y,'@',"Hero",libtcod.white,level,faction = "Hero",stats = actorStats.Stats("Hero"),surviveMortalWound = True, inventorySize = 20, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		# add equipment
		weapon = self.game.itemSpawner.spawn(x,y,'Melee Weapon',8,False)
		hero.equipItem(weapon)

		armor = self.game.itemSpawner.spawn(x,y,'Armor', 1, False)
		hero.equipItem(armor)

		# add items to inventory
		for item in [("Health Potion",0),('Antidote',0),('Serpent Sword',1),('Light Crossbow',0),('Wooden Bolt',0),('Steel Bolt',0)]:
			gear,itemLevel = item
			g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
			g.moveToInventory(hero)
			g.__class__.identified = True

		return hero

	def spawnFireElemental(self,x,y,level):
		pass

	def spawnFrostElemental(self,x,y,level):
		pass

	def spawnGargoyle(self,x,y,level):
		pass

	def spawnGhost(self,x,y,level):
		pass

	def spawnGolem(self,x,y,level):
		pass

	def spawnKnight(self,x,y,level):
		pass

	def spawnChest(self,x,y,level):
		pass

	def spawnMirehound(self,x,y,level):
		lootDrops = {'Health Potion':2}
		mirehound = actors.Monster(self.game,x,y,'h',"Mirehound",libtcod.light_amber,level,faction = "Mirehounds",stats = actorStats.Stats("Mirehound"),state = states.AI(0.7,0.5,0.5,1,0,0),drops = lootDrops)
		mirehound.deathState = states.DeathState(mirehound)
		return mirehound

	def spawnPlagueRat(self,x,y,level):
		lootDrops = {'Health Potion':4} # antidote
		plagueRat = actors.Monster(self.game,x,y,'r',"Plague Rat",libtcod.light_amber,level,faction = "Plague Rats",stats = actorStats.Stats("Plague Rat"),state = states.AI(0.7,0.5,0.5,1,0,0))
		plagueRat.deathState = states.DeathState(plagueRat)
		return plagueRat

	def spawnRougarou(self,x,y,level):
		rougarou = actors.Monster(self.game,x,y,'R',"Rougarou",libtcod.grey,level,stats = actorStats.Stats("Rougarou"),state = states.AI(1,0.5,0.5,1,0,0))
		return rougarou

	def spawnSnakeman(self,x,y,level):
		level = 1

		lootDrops = {'Sword':5,'Health Potion':2}
		snakeman = actors.Monster(self.game,x,y,'S',"Snakeman",libtcod.desaturated_sea,level,faction = "Snakemen",stats = actorStats.Stats("Snakeman"),state = states.AI(0.9,0.5,0.5,1,0,0),drops = lootDrops, inventorySize = 4, canEquipArmor = True, canEquipWeapons = True)
		snakeman.deathState = states.DeathState(snakeman)

		# add equipment
		if random.random() <= .2:
			weapon = self.game.itemSpawner.spawn(x,y,'Serpent Sword',level,False)
			weapon.moveToInventory(snakeman)

		return snakeman

	def spawnSnakemanArcher(self,x,y,level):
		level = 1

		lootDrops = {'Wooden Bolts':5,'Health Potion':2}
		snakeman = actors.Monster(self.game,x,y,'S',"Snakeman Archer",libtcod.red,level,faction = "Snakemen",stats = actorStats.Stats("Snakeman"),state = states.AI(0.9,0.8,0.8,1,7,2),drops = lootDrops, inventorySize = 4, canEquipArmor = True, canEquipWeapons = True)
		snakeman.deathState = states.DeathState(snakeman)

		for name, level in [('Light Crossbow',0),('Steel Bolt',0),('Wooden Bolt',0)]:
			item = self.game.itemSpawner.spawn(x,y,name,level,False)
			item.moveToInventory(snakeman)

		# add equipment
		if random.random() <= .2:
			weapon = self.game.itemSpawner.spawn(x,y,'Serpent Sword',level,False)
			weapon.moveToInventory(snakeman)

		return snakeman

	def spawnSnakemanChampion(self,x,y,level):
		level = 1

		lootDrops = {'Sword':5,'Health Potion':2}
		snakeman = actors.Monster(self.game,x,y,'S',"Snakeman Champion",libtcod.desaturated_sea,level,faction = "Snakemen",stats = actorStats.Stats("Snakeman"),state = states.AI(0.9,0.5,0.5,1,0,0),drops = lootDrops, inventorySize = 4, canEquipArmor = True, canEquipWeapons = True)
		snakeman.deathState = states.DeathState(snakeman)

		# add equipment
		weapon = self.game.itemSpawner.spawn(x,y,'Serpent Sword',level,False)
		snakeman.equipItem(weapon)

		# Shield
		# Armor

		return snakeman

	def spawnSwampHag(self,x,y,level):
		pass

	def spawnWitch(self,x,y,level):
		pass

	def spawnWyrm(self,x,y,level):
		pass
		# Wyrms can be fire or frost elementals


class MobSpawner:
	def __init__(self,game):
		self.game = game
		self.actorSpawner = ActorSpawner(game)
'''
actorSpawner.py
'''
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

class ActorSpawner:
	def __init__(self,game):
		self.game = game

		self.spawnMethods = {
			'Hero':self.spawnHero,
			'Gargoyle':self.spawnGargoyle,
			'Golem':self.spawnGolem,
			'Angel':self.spawnAngel,
			'Demon':self.spawnDemon,
			'Fire Elemental':self.spawnFireElemental,
			'Frost Elemental':self.spawnFrostElemental,
			'Swamp Hag':self.spawnSwampHag,
			'Mirehound':self.spawnMirehound,
			'Mimic':self.spawnChest,
			'Plague Rat':self.spawnPlagueRat,
			'Rougarou':self.spawnRougarou,
			'Snakeman':self.spawnSnakeman,
			'Wyrm':self.spawnWyrm,
			'Knight':self.spawnKnight
			}

	def spawn(self,x,y,key):
		if key in self.spawnMethods:
			actor = self.spawnMethods[key](x,y)
			return actor

	def spawnAngel(self,x,y):
		pass

	def spawnDemon(self,x,y):
		pass

	def spawnHero(self,x,y):
		hero = actors.Hero(self.game,x,y,'@',"Hero",color = libtcod.white,faction = "Hero",stats = actorStats.Stats("Hero"),surviveMortalWound = True, inventorySize = 12, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		# Spawn gearcanEquipArmor = True, canEquipWeapons = True,
		for gear,level in {"Health Potion":0,"Sword":0,"Mace":0}.items():
			g = self.game.itemSpawner.spawn(x,y,gear,level)
			g.moveToInventory(hero)

		return hero

	def spawnFireElemental(self,x,y):
		pass

	def spawnFrostElemental(self,x,y):
		pass

	def spawnGargoyle(self,x,y):
		pass

	def spawnGolem(self,x,y):
		pass

	def spawnKnight(self,x,y):
		pass

	def spawnChest(self,x,y):
		pass

	def spawnMirehound(self,x,y):
		lootDrops = {'Health Potion':2}
		mirehound = actors.Monster(self.game,x,y,'h',"Mirehound",libtcod.light_amber,faction = "Mirehounds",stats = actorStats.Stats("Mirehound"),state = states.AI(),drops = lootDrops)
		mirehound.deathState = states.DeathState(mirehound)
		return mirehound

	def spawnPlagueRat(self,x,y):
		lootDrops = {'Health Potion':4} # antidote
		plagueRat = actors.Monster(self.game,x,y,'r',"Plague Rat",libtcod.light_amber,faction = "Plague Rats",stats = actorStats.Stats("Plague Rat"),state = states.AI())
		plagueRat.deathState = states.DeathState(plagueRat)
		return plagueRat

	def spawnRougarou(self,x,y):
		rougarou = actors.Monster(self.game,x,y,'R',"Rougarou",libtcod.grey,stats = actorStats.Stats("Rougarou"),state = states.AI())
		return rougarou

	def spawnSnakeman(self,x,y):
		lootDrops = {'Sword':5,'Health Potion':2}
		snakeman = actors.Monster(self.game,x,y,'S',"Snakeman",libtcod.desaturated_sea,faction = "Snakemen",stats = actorStats.Stats("Snakeman"),state = states.AI(),drops = lootDrops, canEquipArmor = True, canEquipWeapons = True)
		snakeman.deathState = states.DeathState(snakeman)
		return snakeman

	def spawnSwampHag(self,x,y):
		pass

	def spawnWyrm(self,x,y):
		pass
		# Wyrms can be fire, frost, or plague elementals

class MobSpawner:
	def __init__(self,game):
		self.game = game
		self.actorSpawner = ActorSpawner(game)
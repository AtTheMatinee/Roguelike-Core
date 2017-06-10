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
			'Ghost':self.spawnGhost,
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
		level = 0
		if key in self.spawnMethods:
			actor = self.spawnMethods[key](x,y,level)
			return actor

	def spawnAngel(self,x,y,level):
		pass

	def spawnDemon(self,x,y,level):
		pass

	def spawnHero(self,x,y,level):
		hero = actors.Hero(self.game,x,y,'@',"Hero",color = libtcod.white,faction = "Hero",stats = actorStats.Stats("Hero"),surviveMortalWound = True, inventorySize = 12, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		# add equipment
		weapon = self.game.itemSpawner.spawn(x,y,'Mace',0,False)
		hero.equipItem(weapon)
		print "hero.equipItem"

		# add items to inventory
		for gear,itemLevel in {"Potion":0}.items():
			g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
			g.moveToInventory(hero)
		print "hero item.moveToInventory(hero)"

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
		mirehound = actors.Monster(self.game,x,y,'h',"Mirehound",libtcod.light_amber,level,faction = "Mirehounds",stats = actorStats.Stats("Mirehound"),state = states.AI(),drops = lootDrops)
		mirehound.deathState = states.DeathState(mirehound)
		return mirehound

	def spawnPlagueRat(self,x,y,level):
		lootDrops = {'Health Potion':4} # antidote
		plagueRat = actors.Monster(self.game,x,y,'r',"Plague Rat",libtcod.light_amber,level,faction = "Plague Rats",stats = actorStats.Stats("Plague Rat"),state = states.AI())
		plagueRat.deathState = states.DeathState(plagueRat)
		return plagueRat

	def spawnRougarou(self,x,y,level):
		rougarou = actors.Monster(self.game,x,y,'R',"Rougarou",libtcod.grey,level,stats = actorStats.Stats("Rougarou"),state = states.AI())
		return rougarou

	def spawnSnakeman(self,x,y,level):
		lootDrops = {'Sword':5,'Health Potion':2}
		snakeman = actors.Monster(self.game,x,y,'S',"Snakeman",libtcod.desaturated_sea,level,faction = "Snakemen",stats = actorStats.Stats("Snakeman"),state = states.AI(),drops = lootDrops, canEquipArmor = True, canEquipWeapons = True)
		snakeman.deathState = states.DeathState(snakeman)
		return snakeman

	def spawnSwampHag(self,x,y,level):
		pass

	def spawnWyrm(self,x,y,level):
		pass
		# Wyrms can be fire, frost, or plague elementals

class MobSpawner:
	def __init__(self,game):
		self.game = game
		self.actorSpawner = ActorSpawner(game)
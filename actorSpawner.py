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
class ActorSpawner:
	def __init__(self,game):
		self.game = game

		self.spawnMethods = {
			'Hero':self.spawnHero,
			'Gargoyle':self.spawnGargoyle,
			'Golem':self.spawnGolem,
			'Angel':self.spawnAngel,
			'Demon':self.spawnDemon,
			'FireElemental':self.spawnFireElemental,
			'FrostElemental':self.spawnFrostElemental,
			'SwampHag':self.spawnSwampHag,
			'Mirehound':self.spawnMirehound,
			'Mimic':self.spawnChest,
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
		hero = actors.Hero(self.game,x,y,'@',"Hero",color = libtcod.white,faction = "Hero",stats = actorStats.Stats("Hero"),playerControlled = True)
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
		mirehound = actors.Monster(self.game,x,y,'h',"Mirehound",libtcod.light_amber,faction = "Mirehounds",stats = actorStats.Stats("Mirehound"),state = states.AI())
		return mirehound

	def spawnRougarou(self,x,y):
		rougarou = actors.Monster(self.game,x,y,'R',"Rougarou",libtcod.grey,stats = actorStats.Stats("Rougarou"),state = states.AI())
		return rougarou

	def spawnSnakeman(self,x,y):
		snakeman = actors.Monster(self.game,x,y,'S',"Snakeman",libtcod.desaturated_sea,faction = "Snakemen",stats = actorStats.Stats("Snakeman"),state = states.AI())
		return snakeman

	def spawnSwampHag(self,x,y):
		pass

	def spawnWyrm(self,x,y):
		pass
		# Wyrms can be fire, frost, or plague elementals

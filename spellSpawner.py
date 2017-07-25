'''
spellSpawner.py
'''
import Items
import libtcodpy as libtcod
'''
====================
Spell Spawner
====================
'''
class SpellSpawner:
	def __init__(self,game):
		self.game = game

		self.spawnMethods = {
			'Confusion':self.spawnConfusion,
			'Explode':self.spawnExplode,
			'Fear':self.spawnFear,
			'Fireball':self.spawnFireball,
			'Firebolt':self.spawnFirebolt,
			'Locate Player':self.spawnLocatePlayer,
			'Self Heal':self.spawnSelfHeal,
			'Invisibility':self.spawnInvisibility
		}

	def spawn(self,caster,key):
		if key in self.spawnMethods:
			spell = self.spawnMethods[key](caster)
			spell._spawnKey = key

			return spell

		else:
			print "Error: Cannot locate spell type '"+str(key)+"'"

	# ==== Spawn Methods ====

	def spawnConfusion(self,caster):
		spell = Items.spells.Confusion(self.game,"Confusion",caster)
		return spell

	def spawnExplode(self,caster):
		spell = Items.spells.Explode(self.game,"Explode",caster)
		return spell

	def spawnFear(self,caster):
		spell = Items.spells.Fear(self.game,"Fear",caster)
		return spell

	def spawnFireball(self,caster):
		spell = Items.spells.Fireball(self.game,"Fireball",caster)
		return spell

	def spawnFirebolt(self,caster):
		spell = Items.spells.Firebolt(self.game,"Firebolt",caster)
		return spell

	def spawnLocatePlayer(self,caster):
		spell = Items.spells.LocatePlayer(self.game,"Locate Player",caster)
		return spell

	def spawnSelfHeal(self,caster):
		spell = Items.spells.SelfHeal(self.game,"Heal",caster)
		return spell

	def spawnInvisibility(self,caster):
		spell = Items.spells.TurnInvisible(self.game,"Invisibility",caster)
		return spell

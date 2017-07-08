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
			'Explode':self.spawnExplode,
			'Fireball':self.spawnFireball,
			'Firebolt':self.spawnFirebolt,
			'Self Heal':self.spawnSelfHeal,
			'Invisibility':self.spawnInvisibility
		}

	def spawn(self,caster,key):
		if key in self.spawnMethods:
			spell = self.spawnMethods[key](caster)

			return spell

		else:
			print "Error: Cannot locate spell type '"+str(key)+"'"

	# ==== Spawn Methods ====

	def spawnExplode(self,caster):
		spell = Items.spells.Explode(self.game,"Explode",caster)
		return spell

	def spawnFireball(self,caster):
		spell = Items.spells.Fireball(self.game,"Fireball",caster)
		return spell

	def spawnFirebolt(self,caster):
		spell = Items.spells.Firebolt(self.game,"Firebolt",caster)
		return spell

	def spawnSelfHeal(self,caster):
		spell = Items.spells.SelfHeal(self.game,"Heal",caster)
		return spell

	def spawnInvisibility(self,caster):
		spell = Items.spells.TurnInvisible(self.game,"Invisibility",caster)
		return spell

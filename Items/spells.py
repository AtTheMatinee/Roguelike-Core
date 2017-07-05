'''
spells.py

TODO:
Each spell needs a 'should i do this' method for the AI that tells whether
the AI should use that particular spell at that moment. It should check for
available magic and (usually) whether the target is in range of the spell.
Spells that only effect the caster do not need for the target to be in range.

Damage is tied to caster level (and maybe caster damage stat)
'''

class Spell:
	def __init__(self, caster, x, y, level):
		self.caster = caster
		self.x = x
		self.y = y
		self.level = level

		self.magicCost = 1

	def effect(self):
		return True

	def shouldAIUseThis(self,caster,target):
		return False


class ProjectileSpell(Spell):
	pass

class ExplodingProjectileSpell(Spell):
	pass

class CloudSpell(Spell):
	# Duration of cloud is tied to actor level
	pass

class TrapSpell(Spell):
	pass

class ConeSpell(Spell):
	# Uses raycasting to apply an effect in a cone in a chosen direction
	pass

'''
====================
Spells
====================
'''

class UpgradeItem(Spell):
	# upgrades a random stat on an item
	pass

# ==== Fire ====
class Firebolt(ProjectileSpell):
	# Fire damage projectile
	pass

class FireStorm(Spell):
	pass

class FireCloud(CloudSpell):
	# creates a lingering multi-tile cloud that does slight fire damage to anything within it
	pass

class FireTrap(TrapSpell):
	# Creates a fire damage floor trap
	pass

# ==== Frost ====
class FrostBolt(ProjectileSpell):
	# Frost damage projectile
	pass

class FrostStorm(Spell):
	pass

class FrostCloud(CloudSpell):
	pass

class FrostTrap(TrapSpell):
	pass

# ==== Healing ====
class SelfHeal(Spell):
	pass
	# Caster and Target are the same actor

# ==== Holy ====
class Lightning(Spell):
	# do major holy damage to a random enemy
	pass

class LightningStorm(Spell):
	# do major holy damage to multiple random enemies
	pass
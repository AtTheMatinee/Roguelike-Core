'''
spells.py

TODO:
Each spell needs a 'should i do this' method for the AI that tells whether
the AI should use that particular spell at that moment. It should check for
available magic and (usually) whether the target is in range of the spell.
Spells that only effect the caster do not need for the target to be in range.

Damage is tied to caster level (and maybe caster damage stat)
'''
import libtcodpy as libtcod
import objects
'''
====================
Spells
====================
'''

class Spell:
	def __init__(self, game, name, caster):
		self.game = game
		self.name = name
		self.caster = caster

		self.requiresTarget = True
		self.range = 1
		self.magicCost = 1

	def cast(self,x=None,y=None,level=0):
		# if spell is cast without a target, this method will provide one
		# If the spell requires a target, the actor will be prompted to choose one
		# Otherwise the target defaults to the caster
		if x == None or y == None:
			if self.requiresTarget == True:
				x,y = self.caster.findTarget()
			else:
				x = self.caster.x
				y = self.caster.y

		if level == None:
			level = self.caster.level

		return self.effect(x,y,level)

	def effect(self,x,y,level):
		self.subtractMagicCost()
		return True

	def subtractMagicCost(self):
		# if an actor casts a spell that requires more magic than they have, 
		# the actor takes damage equal to the magic they lack
		magic = (self.caster.stats.get("magicCurrent") - self.magicCost)

		if magic < 0:
			healthDrain = abs(magic)
			self.caster.takeDamage([0,0,0,0,0,0,0,0,healthDrain])
			magic = 0

		self.caster.stats.setBaseStat("magicCurrent",magic)

	def shouldAIUseThis(self,caster,target):
		return False


class ProjectileSpell(Spell):
	def __init__(self, game, name, caster):
		Spell.__init__(self, game, name, caster)

		self.magicCost = 12
		self.requiresTarget = True

		self.damage = [5,0,0,0,0,0,0,0,0]
	
	def effect(self,x,y,level):
		success = False

		# Check for los to tile
		libtcod.line_init(self.caster.x, self.caster.y, x, y)
		x = self.caster.x
		y = self.caster.y
		tempX,tempY = libtcod.line_step()
		while (not tempX is None) and not (self.game._currentLevel.getBlocksMovement(x,y)):
			x = tempX
			y = tempY
			if (self.game._currentLevel.getHasObject(tempX,tempY)):
				break
			tempX,tempY = libtcod.line_step()

		# See if there is an object at those coordinates
		target = None
		for obj in self.game._currentLevel._objects:
			if obj.x == x and obj.y == y:
				target = obj

		if target != None:
			target.takeDamage(self.damage)
			success = True

		if success == True:
			self.game.message(self.caster.getName(True).title()+" casts "+self.name+".",libtcod.purple)
			self.subtractMagicCost()

		return success


class ExplodingProjectileSpell(Spell):
	def __init__(self, game, name, caster):
		Spell.__init__(self, game, name, caster)

		self.magicCost = 24
		self.requiresTarget = True

		self.damage = [20,10,0,0,0,0,0,0,0]
		self.color = libtcod.yellow
		self.volume = 20
	
	def effect(self,x,y,level):
		success = False

		# Check for los to tile
		libtcod.line_init(self.caster.x, self.caster.y, x, y)
		x = self.caster.x
		y = self.caster.y
		tempX,tempY = libtcod.line_step()
		while (not tempX is None) and not (self.game._currentLevel.getBlocksMovement(x,y)):
			x = tempX
			y = tempY
			if (self.game._currentLevel.getHasObject(tempX,tempY)):
				break
			tempX,tempY = libtcod.line_step()


		objects.Explosion(self.game,x,y,self.color,self.damage,self.volume)
		success = True

		if success == True:
			self.game.message(self.caster.getName(True).title()+" casts "+self.name+".",libtcod.purple)
			self.subtractMagicCost()

		return success
	pass

class CloudSpell(Spell):
	# Duration of cloud is tied to actor level
	pass

class ProjectileCloudSpell(Spell):
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
	def effect(self,x,y,level):
		# overwright the damage value
		fireDamage = 6 + (3*level) + self.caster.stats.get('attack')[3] # adjusted for level and caster fire damage
		self.damage = [0,0, fireDamage, 0,0,0,0,0,0]

		ProjectileSpell.effect(self,x,y,level)

class Fireball(ExplodingProjectileSpell):
	def effect(self,x,y,level):
		fireDamage = 6 + (3*level) + self.caster.stats.get('attack')[3] # adjusted for level and caster fire damage
		self.damage = [8,0,fireDamage,0,0,0,0,0,0]
		self.color = libtcod.red
		self.volume = 10 + 3*level

		ExplodingProjectileSpell.effect(self,x,y,level)


class FireStorm(Spell):
	pass

class FireCloud(CloudSpell):
	# creates a lingering multi-tile cloud that does slight fire damage to anything within it
	pass

class FireTrap(TrapSpell):
	# Creates a fire damage floor trap
	pass

class SelfImmolate(Spell):
	pass

# ==== Frost ====

class FrostBolt(ProjectileSpell):
	# Frost damage projectile
	def effect(self,x,y,level):
		# overwright the damage value
		frostDamage = 6 + (3*level) + self.caster.stats.get('attack')[4] # adjusted for level and caster frost damage
		self.damage = [0,0,0, frostDamage, 0,0,0,0,0]

		ProjectileSpell.effect(self,x,y,level)


class FrostStorm(Spell):
	pass

class FrostCloud(CloudSpell):
	pass

class FrostTrap(TrapSpell):
	pass

# ==== Healing ====
class Heal(Spell):
	def __init__(self, game, name, caster):
		Spell.__init__(self, game, name, caster)

		self.magicCost = 10
		self.requiresTarget = True

	def effect(self,x,y,level):
		success = False
		healValue = 4 + (2*level) + self.caster.stats.get('attack')[6] - self.caster.stats.get('attack')[7] # adjusted for level, holy damage, and unholy damage

		if  (self.caster.stats.get("magicCurrent") >= self.magicCost): # healing spells cannot be cast from HP
			targets = []
			for actor in self.game._currentLevel._actors:
				if actor.x == x and actor.y == y:
					targets.append(actor)

			for target in targets:
				if (target.stats.get('healthCurrent') < target.stats.get('healthMax')):
					target.heal(healValue)

					success = True

		if success == True:
			self.game.message(self.caster.getName(True).title()+" casts "+self.name+".",libtcod.purple)
			self.subtractMagicCost()

		return success

class SelfHeal(Heal):
	def __init__(self,game,name,caster):
		Heal.__init__(self,game,name,caster)
		self.requiresTarget = False

# ==== Holy ====
	# Inflict holy damage and Stun
class Lightning(Spell):
	# do major holy damage to a random enemy
	pass

class LightningStorm(Spell):
	# do major holy damage to multiple random enemies
	pass

# ==== Unholy ====
	# Inflict unholy damage and Bleed
# ==== Status ====
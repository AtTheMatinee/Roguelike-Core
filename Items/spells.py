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
import statusEffects
'''
====================
Spells
====================
'''

# ==== Spell Templates ====

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
				x,y = self.caster.findTarget(self.range)
				if x == None: return False # target tile was aborted
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
		if self.magicCost == 0: return
		
		magic = (self.caster.stats.get("magicCurrent") - self.magicCost)

		if magic < 0:
			healthDrain = abs(magic)
			self.caster.takeDamage([0,0,0,0,0,0,0,0,healthDrain])
			magic = 0

		self.caster.stats.setBaseStat("magicCurrent",magic)

	def shouldAIUseThis(self,caster,target = None):
		return False

	def successProbabilityByLevel(self,caster,target):
		# compare the level of the two actors and use that to calculate
		# the probability that a behavior spell will succeed. This returns
		# a number between 0.0 and 1.0.
		if caster == None or target == None:
			return 0.0

		n = (caster.level - target.level)/caster.level
		prob = 0.5 + (0.5*m)

		return prob

	def saveData(self):
		data = {
		'dataType':'Spell',
		'_spawnKey':self._spawnKey
		}

		return data

	def loadData(self,data):
		return False


class ProjectileSpell(Spell):
	def __init__(self, game, name, caster):
		Spell.__init__(self, game, name, caster)

		self.magicCost = 12
		self.requiresTarget = True
		self.range = 10

		self.damage = [5,0,0,0,0,0,0,0,0]
	
	def effect(self,x,y,level):
		success = False

		if self.caster.chessboardDistance(x,y) > self.range:
			self.game.message("Target is too far away.")
			return False

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

class ExplosionSpell(Spell):
	def __init__(self, game, name, caster):
		Spell.__init__(self, game, name, caster)

		self.magicCost = 12
		self.requiresTarget = False

		self.damage = [20,10,2,0,0,0,0,0,0]
		self.color = libtcod.yellow
		self.volume = 20

	def effect(self,x,y,level):
		objects.Explosion(self.game,x,y,self.color,self.damage,self.volume)
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
		self.range = 6

		self.damage = [20,10,0,0,0,0,0,0,0]
		self.color = libtcod.yellow
		self.volume = 20
	
	def effect(self,x,y,level):
		success = False

		if self.caster.chessboardDistance(x,y) > self.range:
			self.game.message("Target is too far away.")
			return False

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
	def __init__(self, game, name, caster):
		Spell.__init__(self, game, name, caster)

		self.magicCost = 12
		self.requiresTarget = False

		self.color = libtcod.gray
		self.volume = 20

	def effect(self,x,y,level):
		objects.Cloud(self.game, x, y, 'cloud', self.color, self.volume)
		success = True

		if success == True:
			self.game.message(self.caster.getName(True).title()+" casts "+self.name+".",libtcod.purple)
			self.subtractMagicCost()

		return success


class PoolSpell(Spell):
	pass

class ProjectileCloudSpell(Spell):
	pass

class TrapSpell(Spell):
	pass

class ConeSpell(Spell):
	# Uses raycasting to apply a damage effect in a cone in a chosen direction
	pass

'''
====================
Spells
====================
'''

class UpgradeItem(Spell):
	# upgrades a random stat on an item
	pass

class LocatePlayer(Spell):
	def __init__(self, game, name, caster):
		Spell.__init__(self, game, name, caster)

		self.magicCost = 8
		self.requiresTarget = False

	def effect(self,x,y,level):
		success = False
		if self.caster.state == None: # actor has no AI
			return success

		hero = self.caster.game.hero
		self.caster.state.lastKnownPosition = (hero.x,hero.y)
		success = True

		if success == True:
			self.subtractMagicCost()

	def shouldAIUseThis(self,caster,target = None):
		'''
		The AI shoul only use this spell if they have enough magic,
		they do not know where to look for the player,
		and they are not currently engaged in combat.
		'''
		if ( (caster.stats.get('magicCurrent') >= self.magicCost) and
			(caster.state.lastKnownPosition == None) and 
			(target == None) ):
			return True

		return False


class Explode(ExplosionSpell):
	def effect(self,x,y,level):
		physicalDam = 6 + (3*level)
		armorPenetration = level
		fireDam = level
		self.damage = [physicalDam,armorPenetration,fireDam,0,0,0,0,0,0]
		self.volume = self.volume = 10 + 3*level

		ExplosionSpell.effect(self,x,y,level)

	def shouldAIUseThis(self,caster,target = None):
		'''
		The AI shoul use this spell if they have less than
		one third of their health left and their target is
		within range.
		'''
		print "IMPLEMENT EXPLODE SPELL"

class TurnInvisible(Spell):
	def __init__(self, game, name, caster):
		Spell.__init__(self, game, name, caster)

		self.requiresTarget = False
		self.range = 1
		self.magicCost = 20

	def effect(self,x,y,level):
		timer = 7 + (3*level)
		self.caster.addStatusEffect(statusEffects.Invisible,timer,True)
		success = True

		if success == True:
			self.game.message(self.caster.getName(True).title()+" casts "+self.name+".",libtcod.purple)
			self.subtractMagicCost()

		return success

class Mimic(Spell):
	def __init__(self, game, name, caster):
		Spell.__init__(self, game, name, caster)

		self.requiresTarget = False
		self.range = 1
		self.magicCost = 8
		# Disguise yourself as an item, chest, alter, or some other object 

class Illusion(Spell):
	def __init__(self, game, name, caster):
		Spell.__init__(self, game, name, caster)

		self.requiresTarget = True
		self.range = 10
		self.magicCost = 8

		# create an object that looks like another object, but that doesn't do anything except take damage

class Fear(Spell):
	def __init__(self, game, name, caster):
		Spell.__init__(self, game, name, caster)

		self.requiresTarget = True
		self.range = 6
		self.magicCost = 12

	def effect(self,x,y,level):
		success = False

		if self.caster.chessboardDistance(x,y) > self.range:
			self.game.message("Target is too far away.")
			return False

		# See if there is an object at those coordinates
		target = None
		for obj in self.game._currentLevel._objects:
			if obj.x == x and obj.y == y:
				target = obj

		if target != None:
			success = True
			self.game.message(self.caster.getName(True).title()+" casts "+self.name+".",libtcod.purple)
			self.subtractMagicCost()

			if random.random() <= successProbabilityByLevel(self.caster,target):
				target.addStatusEffect(statusEffects.Afraid)

		return success

class Confusion(Spell):
	def __init__(self, game, name, caster):
		Spell.__init__(self, game, name, caster)

		self.requiresTarget = True
		self.range = 6
		self.magicCost = 10

	def effect(self,x,y,level):
		success = False

		if self.caster.chessboardDistance(x,y) > self.range:
			self.game.message("Target is too far away.")
			return False

		# See if there is an object at those coordinates
		target = None
		for obj in self.game._currentLevel._objects:
			if obj.x == x and obj.y == y:
				target = obj

		if target != None:
			success = True
			self.game.message(self.caster.getName(True).title()+" casts "+self.name+".",libtcod.purple)
			self.subtractMagicCost()

			if random.random() <= successProbabilityByLevel(self.caster,target):
				target.addStatusEffect(statusEffects.Confused)

		return success


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

class SelfImmolation(Spell):
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

class SelfIgnition(Spell):
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

# ==== Poison ====
# Create line of poisoned mire
# Create lake of poisoned mire

# ==== Holy ====
	# Inflict holy damage and Stun
class Lightning(Spell):
	# do major holy damage to a random enemy
	pass

class LightningStorm(Spell):
	# do major holy damage to multiple random enemies
	pass

# ==== Unholy ====
class Bloodlet(Spell):
	# inflicts damage and 1.0 bleed damage
	pass

class Decemation(Spell):
	# sets both the caster and target's hp to the lower of the two's previous hp
	pass

# ==== Status ====

# ==== Misc ====

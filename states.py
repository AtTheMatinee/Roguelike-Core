'''
states.py
'''
import commands
import libtcodpy as libtcod
import random
import objects
import math
import items
import Items
'''
====================
States
====================
'''

class State:

	def getAICommand(self,actor):
		if actor._nextCommand != None:
			return None
		else:
			command = commands.WaitCommand(actor)
			return command

	def saveData(self):
		data = {}

		return data

	def loadData(self,data):
		return False

class AI(State):
	def __init__(self, morale, retreatProbability, chargeProbability, meleeProbability, spellProbability, maxDistanceFromTarget, minDistanceFromTarget):
		self.morale = morale # percentage of health that actor can lose before it flees
		self.retreatProbability = retreatProbability # probability that actor will retreat instead of attack
		self.chargeProbability = chargeProbability # probability that actor will charge instead of attack
		self.meleeProbability = meleeProbability # the probability that the actor will choose melee if they can attack with both melee and ranged
		self.spellProbability = spellProbability # the probability that the actor will cast a spell if they could also attack
		self.maxDistanceFromTarget = maxDistanceFromTarget # when exceeded, actor will try to get closer
		self.minDistanceFromTarget = minDistanceFromTarget # when exceeded, actor will try to get farther away

		self.trace = None
		self.lastKnownPosition = None

		# wonder perameters
		self.changeDirectionChance = 0.2
		self.waitChance = 0.3
		self.dx = 0
		self.dy = 0

	def getAICommand(self,actor):
		if actor._nextCommand != None:
			return actor._nextCommand

		target = None
		fov = actor.game.map.fov_map
		if libtcod.map_is_in_fov(fov,actor.x,actor.y):
			if self.canTargetNemesis(actor):
				target = actor.mostRecentAttacker

			elif (self.hostileToHero(actor) and
				(self.canTargetHero(actor)) ):
				target = actor.game.hero

			#elif friendInRange and canTargetNemesis(friend) (attack the friend's nemesis)

		if (target == None):
			if self.canLookForTarget(actor) == True:
				command = self.lookForTarget(actor)

			elif self.shouldCastSpell(actor,None):
				command = self.castSpell(actor,None)

			elif self.shouldManageEquipment(actor):
				command = self.manageEquipment(actor)

			else:
				command = self.wander(actor)

		if (target != None):
			self.lastKnownPosition = (target.x, target.y)
			self.trace = None
			ableToAttack = self.canAttackTarget(actor, target)

			if self.damagePercent(actor) > self.morale:
				if self.canRunAwayFromTarget(actor, target):
					command = self.runAwayFromTarget(actor, target)
				elif self.canAttackTarget(actor, target):
					command = self.attackTarget(actor, target)
				else:
					command = self.wander(actor)

			elif ( (self.tooFarFromTarget(actor, target)) and
				(ableToAttack) and
				(self.canMoveTowardTarget(actor, target)) ):

				if random.random() < self.chargeProbability:
					command = self.moveTowardTarget(actor, target)
				else:
					command = self.attackTarget(actor, target)

			elif ( (self.tooCloseToTarget(actor, target)) and
				(ableToAttack) and
				(self.canMoveAwayFromTarget(actor, target)) ):

				if random.random() < self.retreatProbability:
					command = self.moveAwayFromTarget(actor, target)
				else:
					command = self.attackTarget(actor, target)

			elif ableToAttack:
				command = self.attackTarget(actor, target)

			elif ( (self.tooFarFromTarget(actor, target)) and
				(self.canMoveTowardTarget(actor, target)) ):
				command = self.moveTowardTarget(actor, target)

			elif ( (self.tooCloseToTarget(actor, target)) and
				(self.canMoveAwayFromTarget(actor, target)) ):
				command = self.moveAwayFromTarget(actor, target)

			elif self.shouldCastSpell(actor, target):
				command = self.castSpell(actor, target)

			elif self.shouldManageEquipment(actor):
				command = self.manageEquipment(actor)

			else:
				command = self.wait(actor)

		return command


		'''
		TODO: Consider Possible Future Behaviors
			too far from group center
			can move toward group center
			move toward group center
			too close to group center
			can move away from group center
			move away from group center
			enough friendlies in group
			item on the ground here
			item on the ground nearby
			pick up item

		'''

	def canTargetNemesis(self,actor):
		# returns True if the last thing to attack the actor is still alive
		if ( (actor.mostRecentAttacker != None) and
			(actor.mostRecentAttacker in actor.game._currentLevel._objects) and
			(actor.mostRecentAttacker.invisible == False) ):
			return True
		else:
			return False

	def canTargetHero(self,actor):
		# returns True if the hero is still alive and not invisible
		if ((actor.game.hero in actor.game._currentLevel._objects) and
			(actor.game.hero.invisible == False) ):
			return True
		else:
			return False

	def hostileToHero(self,actor):
		if (actor.game.factions.getRelationship(actor.faction, actor.game.hero.faction) == actor.game.factions._hostile):
			return True
		else:
			return False

	def canLookForTarget(self,actor):
		if (self.lastKnownPosition != None) and (self.damagePercent(actor) < self.morale):
			x,y = self.lastKnownPosition
			if x != actor.x or y != actor.y:
				if self.trace == None:
					self.trace = objects.Trace(actor.game, x, y, '@','', libtcod.red, actor)
				return True
			else:
				self.lastKnownPosition = None
				self.trace = None

		return False

	def lookForTarget(self,actor):
		traceX,traceY = self.lastKnownPosition
		bestDX = 0
		bestDY = 0
		leastDistance = actor.distance(traceX,traceY)
		for dx in xrange(-1,2): # -1, 0, 1
			for dy in xrange(-1,2): # -1, 0, 1
				x = actor.x + dx
				y = actor.y + dy
				if ((actor.game._currentLevel.getBlocksMovement(x,y) == False) and 
					(actor.game._currentLevel.getHasObject(x,y)) == False):

					distance = math.sqrt( (traceX-x)**2 + (traceY-y)**2 )

					if distance < leastDistance:
						bestDX = dx
						bestDY = dy
						leastDistance = distance
						
		command = commands.WalkCommand(actor,bestDX,bestDY)
		return command

	def damagePercent(self,actor):
		health = actor.stats.get('healthCurrent')
		maxHealth = actor.stats.get('healthMax')

		return (maxHealth-health)/maxHealth

	def wander(self,actor):
		if actor._nextCommand != None:
			return None
		else:
			if random.random() <= self.waitChance:
				command = commands.WaitCommand(actor)
			else:
				if ((self.dx == 0 and self.dy == 0) or
					(random.random() <= self.changeDirectionChance)):
					self.dx = random.randint(-1,1)
					self.dy = random.randint(-1,1)
				command = commands.WalkCommand(actor,self.dx,self.dy)
			return command

	def canAttackTarget(self,actor,target):
		# Check to see if the target is in melee range of the actor
		for dx in xrange(-1,2):
			for dy in xrange(-1,2):
				if (actor.x + dx == target.x) and (actor.y + dy == target.y):
					return True

		# Check to see if the actor can ranged attack the target
		if ((actor.equipSlots[2] != None) and
			(isinstance(actor.equipSlots[2], Items.rangedWeapons.RangedWeapon) == True) and
			(actor.equipSlots[2].loadedRounds > 0) and
			self.LOSToTarget(actor,target) ):
			return True

		# Check to see if the actor should cast a spell at the target
		if self.shouldCastSpell(actor,target):
			return True

		return False

	def attackTarget(self,actor,target):
		canMelee = False
		canRange = False
		# Check to see if the target is in melee range of the actor
		for dx in xrange(-1,2):
			for dy in xrange(-1,2):
				if (actor.x + dx == target.x) and (actor.y + dy == target.y):
					canMelee = True

		# Check to see if the actor can ranged attack the target
		if ((actor.equipSlots[2] != None) and
			(isinstance(actor.equipSlots[2], Items.rangedWeapons.RangedWeapon) == True) and
			(actor.equipSlots[2].loadedRounds > 0) and
			self.LOSToTarget(actor,target) ):
			canRange = True

		if ((canMelee == True) and 
			((canRange == False) or (random.random() < self.meleeProbability))):
			command = commands.AttackCommand(actor,target)

		else:
			command = commands.FireRangedWeaponCommand(actor,target)

		return command

	def LOSToTarget(self,actor,target):
		libtcod.line_init(actor.x, actor.y, target.x, target.y)
		x = actor.x
		y = actor.y
		lineX,lineY = libtcod.line_step()
		while (not lineX is None) and not (actor.game._currentLevel.getBlocksMovement(lineX,lineY)):
			x = lineX
			y = lineY
			if ((actor.game._currentLevel.getHasObject(x,y)) or
				(actor.game._currentLevel.getBlocksSight(x,y))):
				break
			lineX,lineY = libtcod.line_step()

		if x == target.x and y == target.y:
			return True
		else:
			return False

	def tooCloseToTarget(self,actor,target):
		if actor.distance(target.x,target.y) < self.minDistanceFromTarget:
			return True
		else:
			return False

	def canMoveAwayFromTarget(self,actor,target):
		# check the 8 tiles surrounding the actor and 
		# return True if the actor can move to one to  
		# increase their distance from the target
		greatestDistance = target.distance(actor.x, actor.y)
		for dx in xrange(-1,2): # -1, 0, 1
			for dy in xrange(-1,2): # -1, 0, 1
				x = actor.x + dx
				y = actor.y + dy
				if ((actor.game._currentLevel.getBlocksMovement(x,y) == False) and 
					(actor.game._currentLevel.getHasObject(x,y)) ==False):
					distance = target.distance(x,y)
					if distance > greatestDistance:
						return True

		return False

	def moveAwayFromTarget(self,actor,target):
		# check the 8 tiles surrounding the actor and
		# move to the one that maximizes the distance 
		# between it and the target
		bestDX = 0
		bestDY = 0
		greatestDistance = target.distance(actor.x, actor.y)
		for dx in xrange(-1,2): # -1, 0, 1
			for dy in xrange(-1,2): # -1, 0, 1
				x = actor.x + dx
				y = actor.y + dy
				if ((actor.game._currentLevel.getBlocksMovement(x,y) == False) and 
					(actor.game._currentLevel.getHasObject(x,y)) ==False):
					distance = target.distance(x,y)
					if distance > greatestDistance:
						bestDX = dx
						bestDY = dy
						greatestDistance = distance
						
		command = commands.WalkCommand(actor,bestDX,bestDY)
		return command

	def tooFarFromTarget(self,actor,target):
		if actor.distance(target.x,target.y) > self.maxDistanceFromTarget:
			return True
		else:
			return False

	def canMoveTowardTarget(self,actor,target):
		# check the 8 tiles surrounding the actor and 
		# return True if the actor can move to one to  
		# increase their distance from the target
		leastDistance = target.distance(actor.x, actor.y)
		for dx in xrange(-1,2): # -1, 0, 1
			for dy in xrange(-1,2): # -1, 0, 1
				x = actor.x + dx
				y = actor.y + dy
				if ((actor.game._currentLevel.getBlocksMovement(x,y) == False) and 
					(actor.game._currentLevel.getHasObject(x,y)) ==False):
					distance = target.distance(x,y)
					if distance < leastDistance:
						return True

		return False

	def moveTowardTarget(self,actor,target):
		# check the 8 tiles surrounding the actor and
		# move to the one that minimizes the distance 
		# between it and the target
		xList = [-1,0,1]
		random.shuffle(xList)
		yList = [-1,0,1]
		random.shuffle(yList)

		bestDX = 0
		bestDY = 0
		leastDistance = target.distance(actor.x, actor.y)
		for dx in xList:
		#for dx in xrange(-1,2): # -1, 0, 1
			for dy in yList:
			#for dy in xrange(-1,2): # -1, 0, 1
				x = actor.x + dx
				y = actor.y + dy
				if ((actor.game._currentLevel.getBlocksMovement(x,y) == False) and 
					(actor.game._currentLevel.getHasObject(x,y)) ==False):
					distance = target.distance(x,y)
					if distance < leastDistance:
						bestDX = dx
						bestDY = dy
						leastDistance = distance
						
		command = commands.WalkCommand(actor,bestDX,bestDY)
		return command

	def canRunAwayFromTarget(self,actor,target):
		# check the 8 tiles surrounding the actor and 
		# return True if the actor can move to one to  
		# decrease their distance from the target
		greatestDistance = target.distance(actor.x, actor.y)
		for dx in xrange(-1,2): # -1, 0, 1
			for dy in xrange(-1,2): # -1, 0, 1
				x = actor.x + dx
				y = actor.y + dy
				if ((actor.game._currentLevel.getBlocksMovement(x,y) == False) and 
					(actor.game._currentLevel.getHasObject(x,y)) ==False):
					distance = target.distance(x,y)
					if distance > greatestDistance:
						return True

		return False

	def runAwayFromTarget(self,actor,target):
		# check the 8 tiles surrounding the actor and
		# move to the one that maximizes the distance 
		# between it and the target
		xList = [-1,0,1]
		random.shuffle(xList)
		yList = [-1,0,1]
		random.shuffle(yList)

		bestDX = 0
		bestDY = 0
		greatestDistance = target.distance(actor.x, actor.y)
		for dx in xList: #xrange(-1,2): # -1, 0, 1
			for dy in yList: #xrange(-1,2): # -1, 0, 1
				x = actor.x + dx
				y = actor.y + dy
				if ((actor.game._currentLevel.getBlocksMovement(x,y) == False) and 
					(actor.game._currentLevel.getHasObject(x,y)) ==False):
					distance = target.distance(x,y)
					if distance > greatestDistance:
						bestDX = dx
						bestDY = dy
						greatestDistance = distance
						
		command = commands.WalkCommand(actor,bestDX,bestDY)
		return command

	def shouldManageEquipment(self,actor):
		if len(actor.inventory) < 1:
			return False

		for item in actor.inventory:
			if isinstance(item, items.Equipment):
				i = item.equipSlot
				if ((actor.equipSlots[i] == None) or 
					(item.level > actor.equipSlots[i].level)):
					return True

			elif (isinstance(item, Items.rangedWeapons.Ammo) and
				(isinstance(actor.equipSlots[2], Items.rangedWeapons.RangedWeapon)) and
				(actor.equipSlots[2].loadedRounds < 1) ):
				return True

		return False

	def manageEquipment(self,actor):
		for item in actor.inventory:
			if isinstance(item, items.Equipment):
				i = item.equipSlot
				if ((actor.equipSlots[i] == None) or 
					(item.level > actor.equipSlots[i].level)):

					return commands.UseCommand(actor,item)

			elif (isinstance(item, Items.rangedWeapons.Ammo) and
				(isinstance(actor.equipSlots[2], Items.rangedWeapons.RangedWeapon)) and
				(actor.equipSlots[2].loadedRounds < 1) ):

				return commands.UseCommand(actor,item)


		return commands.WaitCommand(actor)

	def shouldCastSpell(self,actor,target):
		if len(actor.spells) > 0:
			for spell in actor.spells:
				if spell.shouldAIUseThis(actor,target) == True:
					return True
		return False

	def castSpell(self,actor,target):
		command = commands.WaitCommand(actor)

		for spell in actor.spells:
			if spell.shouldAIUseThis(actor,target) == True:
				command = commands.CastSpellCommand(actor,spell)

		return command

	def wait(self,actor):
		command = commands.WaitCommand(actor)
		return command


class AIConfused(AI):
	def __init__(self):
		self.confusionChance = 0.8
		self.waitChance = 1.0/8

	def getAICommand(self,actor):
		if (random.random() <= self.confusionChance):
			if random.random() <= self.waitChance:
				actor._nextCommand = commands.WaitCommand(actor)
			else:
				dx = random.randint(-1,1)
				dy = random.randint(-1,1)
				actor._nextCommand = commands.WalkCommand(actor,dx,dy)


		if actor._nextCommand != None:
			return actor._nextCommand

		elif actor._defaultState != None:
			command = actor._defaultState.getAICommand(actor)
			return command

		else: return None


class AIAfraid(AI):
	def __init__(self):
		pass

	def getAICommand(self,actor):

		target = None
		fov = actor.game.map.fov_map
		if libtcod.map_is_in_fov(fov,actor.x,actor.y):
			if self.canTargetNemesis(actor):
				target = actor.mostRecentAttacker

			elif (self.hostileToHero(actor) and
				(self.canTargetHero(actor)) ):
				target = actor.game.hero

			else:
				nearbyActors = actor.getNearbyActors()
				if len(nearbyActors) > 0:
					target = nearbyActors[0]

		if (target == None):
			if actor._nextCommand != None:
				command = actor._nextCommand
			else:
				command = self.wait(actor)

		if (target != None):
			self.lastKnownPosition = (target.x, target.y)
			self.trace = None
			ableToAttack = self.canAttackTarget(actor, target)

			if self.canRunAwayFromTarget(actor, target):
				command = self.runAwayFromTarget(actor, target)
			
			elif self.canAttackTarget(actor, target):
				command = self.attackTarget(actor, target)
			
			elif actor._nextCommand != None:
				command = actor._nextCommand
			
			else:
				command = self.wait(actor)

		return command


class Autowalk(AI):
	pass


class AutoExplore(AI):
	pass

'''
====================
Death States
====================
'''

class DeathState:
	def __init__(self,owner):
		self.owner = owner
	
	def process(self):
		self.giveExperience(self.owner)
		self.effect()

		o = self.owner
		del self.owner

		o.game.removeObject(o)
		o.game._currentLevel.removeObject(o)
		o.game._currentLevel.setHasObjectFalse(o.x, o.y)
		o.game._currentLevel.removeActor(o)

		o._nextCommand = None

		o.game.message(o.getName(True).title()+" is dead.",libtcod.crimson)

		o.dropLoot()

		name = "Corpse of "+o.getName(True)
		objects.Corpse(o.game, o.x, o.y, "%",name, libtcod.crimson)

		o.deathState = None
		del o.statusEffects[:]
		del o

	def giveExperience(self,owner):
		#import pdb; pdb.set_trace()
		if (owner.mostRecentAttacker != None):
			owner.mostRecentAttacker.gainXPCombat(owner)

	def effect(self):
		pass

class ExplodeOnDeathState(DeathState):
	pass

class DropBombsOnDeath(DeathState):
	pass

class SpawnMobOnDeath(DeathState):
	pass
'''
states.py
'''
import commands
import libtcodpy as libtcod
import random
import objects
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

class AI(State):
	def __init__(self, morale, retreatProbability, chargeProbability, meleeProbability, maxDistanceFromTarget, minDistanceFromTarget):
		self.morale = morale # percentage of health that actor can lose before it flees
		self.retreatProbability = retreatProbability # probability that actor will retreat instead of attack
		self.chargeProbability = chargeProbability # probability that actor will charge instead of attack
		self.meleeProbability = meleeProbability # the probability that the actor will choose melee of they can attack with both melee and ranged
		self.maxDistanceFromTarget = maxDistanceFromTarget # when exceeded, actor will try to get closer
		self.minDistanceFromTarget = minDistanceFromTarget # when exceeded, actor will try to get farther away

		# wonder perameters
		self.changeDirectionChance = 0.2
		self.waitChance = 0.3
		self.dx = 0
		self.dy = 0

	def getAICommand(self,actor):
		target = None
		fov = actor.game.map.fov_map
		if libtcod.map_is_in_fov(fov,actor.x,actor.y):
			if self.canTargetNemesis(actor):
				target = actor.mostRecentAttacker

			elif self.hostileToHero(actor):
				target = actor.game.hero

		if (target == None):
			if self.shouldManageEquipment(actor):
				command = self.manageEquipment(actor)
			else:
				command = self.wander(actor)
			# or inventory management

		if (target != None):
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
		'''
	def canTargetNemesis(self,actor):
		# returns True if the last thing to attack the actor is still alive
		if ( (actor.mostRecentAttacker != None) and
			(actor.mostRecentAttacker in actor.game._currentLevel._objects) ):
			return True
		else:
			return False

	def hostileToHero(self,actor):
		if (actor.game.factions.getRelationship(actor.faction, actor.game.hero.faction) == actor.game.factions._hostile):
			return True
		else:
			return False

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

	def chaseTarget(self,actor,target):
		# pathfind to the player's location
		path = actor.game._currentLevel.pathMap
		libtcod.path_compute(path,actor.x,actor.y,target.x,target.y)

		if libtcod.path_size(path) < 1:
			command = self.wander(actor)
			return command
		else:
			x,y = libtcod.path_get(path,False)

		command = self.moveTowardLocation(actor,x,y)

		return command

	def moveTowardLocation(self,actor,x,y):
		dx = 0
		dy = 0

		# move to the point
		if actor.x < x: 
			dx = 1
		elif actor.x > x:
			dx = -1
		if actor.y < y:
			dy = 1
		elif actor.y > y:
			dy = -1
			
		if dx == 0 and dy == 0:
			pass

		# adjust for blocked movement

		command = commands.WalkCommand(actor,dx,dy)
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
		# TODO: LOS to target
		libtcod.line_init(actor.x, actor.y, target.x, target.y)
		x = actor.x
		y = actor.y
		lineX,lineY = libtcod.line_step()
		while (not lineX is None) and not (actor.game._currentLevel.getBlocksMovement(lineX,lineY)):
			x = lineX
			y = lineY
			if (actor.game._currentLevel.getHasObject(x,y)):
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
		# move to the one that maximizes the distance 
		# between it and the target
		bestDX = 0
		bestDY = 0
		leastDistance = target.distance(actor.x, actor.y)
		for dx in xrange(-1,2): # -1, 0, 1
			for dy in xrange(-1,2): # -1, 0, 1
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

	def runAwayFromTarget(self,actor,target):
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

	def wait(self,actor):
		command = commands.WaitCommand(actor)
		return command


class AIConfused(AI):
	def __init__(self):
		self.confusionChance = 0.5
		self.waitChance = 1.0/3
		self.timer = random.randint(3,5)

	def getAICommand(self,actor):
		if actor._nextCommand == None or (random.ramdom() <= self.confusionChance):
			if random.random() <= self.waitChance:
				command = commands.WaitCommand(actor)
			else:
				dx = random.randint(-1,1)
				dy = random.randint(-1,1)
				command = commands.WalkCommand(actor,dx,dy)
			return command

		# decrement timer (unless self.timer < 0, then it lasts forever)
		if self.timer == 0:
			actor.state = actor._defaultState
		elif self.timer > 0:
			self.timer -= 1

		else: return None


class DeathState:
	def __init__(self,owner):
		self.owner = owner
	
	def process(self):
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
'''
states.py
'''
import commands
import libtcodpy as libtcod
import random
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
	def __init__(self):

		# wonder
		self.changeDirectionChance = 0.2
		self.waitChance = 0.3
		self.dx = 0
		self.dy = 0
	
	def getAICommand(self,actor):
		fov = actor.game.map.fov_map
		if libtcod.map_is_in_fov(fov,actor.x,actor.y):
			return self.chasePlayer(actor)
		else:
			return self.wonder(actor)

	def wonder(self,actor):
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

	def chasePlayer(self,actor):
		player = actor.game.hero

		# use line of seight to chase player

		# pathfind to the player's location
		path = actor.game._currentLevel.pathMap
		libtcod.path_compute(path,actor.x,actor.y,player.x,player.y)

		if libtcod.path_size(path) <= 1:
			command = self.wonder(actor)
			return command
		else:
			x,y = libtcod.path_get(path,False)

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
			print "Flag"
		command = commands.WalkCommand(actor,dx,dy)
		return command


	def hunt(self,actor,target):
		# search for the player in the player's
		# last known location.
		pass

	def chase(self,target):
		pass

	def moveTowardLocation(self,actor,x,y):
		pass

	def moveAndShoot(self,actor,target):
		pass

	def turret(self,actor,target):
		pass

	def inflictMostDamage(self,target):
		pass

	def attackClosestEnemy(self,target):
		pass



class AIConfused:
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
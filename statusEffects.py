'''
statusEffects.py
'''
import libtcodpy as libtcod
import commands
import states
'''
====================
Status Effects
====================
'''

'''
Status Effect Tags
	Flamable
		become flaming if dealt fire damage
	Wet
		become frozen if dealt frost damage
		adds fire defense mult buff
	Frozen
		does frost damage up front
		adds speed mult debuff and physical defense add buff
	Flaming
		does fire damage per turn
		adds fire damage mult buff and fire resistance mult debuff modifiers
	Poisoned
		does 2 damage per turn for n turns, where n is the poison damage dealt
	Bleeding
		does 1/10 of actor's health in unblockable damage 
		per turn for up to 5 turns, stacks
	Invisible
		become flaming when dealt holy damage
	Cursed
	Blessed
'''

class StatusEffect(object):
	def __init__(self,actor,timer = 0):
		self.actor = actor
		self.game = actor.game
		self.timer = int(timer)

	def effect(self):
		if self.timer == 0:
			self.remove()
			return
			
		if self.timer > 0: self.timer -= 1

	def remove(self):
		self.actor.removeStatusEffect(self)
		self.game.message("The status effect has worn off.")

	def saveData(self):
		data = {
		'dataType':'StatusEffect',
		'class':self.__class__,
		'timer':self.timer
		}

		return data

	def loadData(self,data):
		return True



# ==== Status Effects ====
class Poisoned(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)

		# message
		self.game.message(self.actor.getName(True).title()+" is poisoned.",libtcod.violet)

	def effect(self):
		if self.timer == 0:
			self.remove()
			return

		# take poison damage
		self.actor.takeDamage([0,0,0,0, 2, 0,0,0,0])

		if self.timer > 0: self.timer -= 1

	def remove(self):
		self.actor.removeStatusEffect(self)
		self.game.message(self.actor.getName(True).title()+" is no longer poisoned.",libtcod.light_violet)


class Bleeding(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)
		self.timer = 10

		# does half of your current health over ten turns
		self.damage = max(0.5,self.actor.stats.get("healthCurrent")/20)
		
		# message
		self.game.message(self.actor.getName(True).title()+" is bleeding.",libtcod.violet)

	def effect(self):
		if self.timer == 0:
			self.remove()
			return

		# take bleed damage
		self.actor.takeDamage([0,0,0,0,0,0,0,0,self.damage])
		
		if self.timer > 0: self.timer -= 1

	def remove(self):
		self.actor.removeStatusEffect(self)
		self.game.message(self.actor.getName(True).title()+" is no longer bleeding.",libtcod.light_violet)


class Frozen(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)

		# message
		self.game.message(self.actor.getName(True).title()+" is frozen.",libtcod.violet)

		# Take Frost Damage (20 damage up front)
		self.actor.takeDamage([0,0,0, 20, 0,0,0,0,0])

		modifier = {'add':{'defense':[4,0,0,0,0,0,0]},'mult':{'speed':-0.33}}
		self.actor.stats.addModifier(self, modifier)

	def effect(self):
		if self.timer == 0:
			self.remove()
			return
			
		if self.timer > 0: self.timer -= 1

	def remove(self):
		self.actor.stats.removeModifier(self)
		self.actor.removeStatusEffect(self)
		self.game.message(self.actor.getName(True).title()+" is no longer frozen.",libtcod.light_violet)


class Flaming(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)

		self.damage = 2 # take 2 damage per turn for 10 turns

		# message
		self.game.message(self.actor.getName(True).title()+" is on fire.",libtcod.violet)

		modifier = {'add':{'attack': [0,0, 2, 0,0,0,0,0,0]} ,'mult':{'defense':[-0.5,0,-0.5,-0.5,-0.5,-0.5,-0.5]}}
		self.actor.stats.addModifier(self, modifier)

	def effect(self):
		if self.timer == 0:
			self.remove()
			return

		# Take Fire Damage
		self.actor.takeDamage([0,0, self.damage, 0,0,0,0,0,0])

		if self.timer > 0: self.timer -= 1

	def remove(self):
		self.actor.stats.removeModifier(self)
		self.actor.removeStatusEffect(self)
		self.game.message(self.actor.getName(True).title()+" is no longer on fire.",libtcod.light_violet)


class Flamable(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)

		# message
		self.game.message(self.actor.getName(True).title()+" is covered in flamable liquid.",libtcod.violet)

	def effect(self):
		if self.timer == 0:
			self.remove()
			return
			
		if self.timer > 0: self.timer -= 1

	def remove(self):
		self.actor.removeStatusEffect(self)
		self.game.message(self.actor.getName(True).title()+" is no longer flamable.",libtcod.light_violet)


class Wet(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)

		# message
		self.game.message(self.actor.getName(True).title()+" is soaked.",libtcod.violet)

	def effect(self):
		if self.timer == 0:
			self.remove
			return
			
		for se in self.actor.statusEffects:
			if (isinstance(se, Flaming)):
				se.remove()
				self.remove()

		if self.timer > 0: self.timer -= 1

	def remove(self):
		self.actor.removeStatusEffect(self)
		self.game.message(self.actor.getName(True).title()+" is no longer soaked.",libtcod.light_violet)

class Invisible(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)

		# message
		if self.actor.invisible == False:
			self.actor.invisible = True

			self.game.message(self.actor.getName(True).title()+" is invisible.",libtcod.violet)

	def effect(self):
		if self.timer == 0:
			self.remove()
			if not any(isinstance(se,Invisible) for se in self.actor.statusEffects):
				self.actor.invisible = False
			return

		if self.actor.invisible == False:
			self.actor.invisible = True

		if self.timer > 0: self.timer -= 1

	def remove(self):
		self.actor.removeStatusEffect(self)
		self.game.message(self.actor.getName(True).title()+" is no longer invisible.",libtcod.light_violet)

class Regenerating(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)

		self.healValue = self.actor.stats.get('healthMax')/20.0
		self.game.message(self.actor.getName(True).title()+" is regenerating health.",libtcod.violet)

	def effect(self):
		if self.timer == 0:
			self.remove()
			return

		# heal
		self.actor.heal(self.healValue)

		if self.timer > 0: self.timer -= 1

	def remove(self):
		self.actor.removeStatusEffect(self)
		self.game.message(self.actor.getName(True).title()+" is no longer regenerating health.",libtcod.light_violet)


class Confused(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)
		self.actor.state = states.AIConfused()

	def effect(self):
		if self.timer == 0:
			self.remove()
			self.actor.state = self.actor._defaultState
			return

		if self.timer > 0: self.timer -= 1

class Afraid(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)
		self.actor.state = states.AIAfraid()

	def effect(self):
		if self.timer == 0:
			self.remove()
			self.actor.state = self.actor._defaultState
			return

		if self.timer > 0: self.timer -= 1

# ==== Buffs ====

# ==== Debuffs ====

class MortallyWounded(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)

		# message
		self.game.message(self.actor.getName(True).title()+" is mortally wounded.",libtcod.red)

		# Add Modifier
		n = self.actor.stats.get('healthMax')/2
		modifier = {'add':{'healthMax':-n}}
		self.actor.stats.addModifier(self, modifier)

	def effect(self):
		if self.timer == 0:
			self.remove()
			return

		if self.timer > 0: self.timer -= 1

	def remove(self):
		self.actor.stats.removeModifier(self)
		self.actor.removeStatusEffect(self)
		self.game.message(self.actor.getName(True).title()+" has recovered from their wounds.")
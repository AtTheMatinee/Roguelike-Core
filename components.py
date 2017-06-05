'''
componentSystems.py
'''
'''
====================
Components
====================
'''
'''
Component Tags
	Flamable
	Wet
	Frozen
	Flaming
	Poisoned
	Explosive
	Invisible
	Undead
	Radiant
	Cursed
	Blessed
'''

class Component:
	def __init__(self,actor,timer):
		self.actor = actor
		self.game = actor.game
		self.timer = timer

	def effect(self):
		if self.timer == 0:
			self.actor.removeComponent(self)
			self.game.message("The status effect has worn off.")

		self.timer -= 1

# Status Effects

# Buffs

# Debuffs
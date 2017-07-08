'''
items.py
'''
from objects import Object
import actors
import commands
'''
====================
Items
====================
'''
class Item(Object):
	identified = False
	unidentifiedName = "Mysterious Item"
	def __init__(self, game, x, y, char, name, color, level, blocks=False, properNoun = False):
		Object.__init__(self, game, x, y, char, name, color, blocks=False, properNoun = False)	

		self.level = level

		self.game.addObject(self)
		self.game._currentLevel.addItem(self)

		self.renderFirst()
		if self.blocks == True:
			self.game._currentLevel.setHasObjectTrue(x,y)

	def getName(self,useDefiniteArticle,showLevel = False):
		name = self.name
		if useDefiniteArticle == True and self.properNoun == False:
			if self.__class__.identified == True:
				name = "the "+self.name
			else:
				name = "the "+self.__class__.unidentifiedName

		#if useIndefiniteArticle:
		else:
			if self.__class__.identified == True:
				name = self.name
			else:
				name = self.__class__.unidentifiedName

		if (self.__class__.identified == True) and (showLevel == True) and (self.level != 0):
			name = name+" ["+str(self.level)+"]"
		
		return name

	def moveToInventory(self,actor):
		self.game._currentLevel.removeItem(self)
		self.game._currentLevel.removeObject(self)
		actor.inventory.append(self)

	def dropFromInventory(self,actor):
		if self in actor.inventory:
			actor.inventory.remove(self)
			# Drop the item on the ground
			self.game._currentLevel.addItem(self)
			self.game._currentLevel.addObject(self)
			self.x = actor.x
			self.y = actor.y
			self.renderFirst()

	def use(self,actor):
		if self in actor.inventory:
			actor.inventory.remove(self)
			actor.game.message(actor.name +" uses "+self.getName(True))
		return True

	def thrownEffect(self,obj):
		if isinstance(obj, actors.Actor):
			# defines what happens if the thrown object hits an actor
			self.game.message(obj.getName(True)+" was hit by a "+self.getName(False))
			obj.takeDamage([2,0,0,0,0,0,0,0,0])

	def upgrade(self,level):
		pass


class Equipment(Item):
	identified = True
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False, canBeUnequipped = True):
		self.equipSlot = equipSlot
		self.modifier = modifier
		self.canBeUnequipped = canBeUnequipped
		Item.__init__(self, game, x, y, char, name, color, level, blocks=False)

	def use(self,actor):
		# create equip command
		equip = commands.EquipCommand(actor,self)
		# set equip command's energyCost to 0, since you are already paying for UseCommand's cost
		equip.energyCost = 0
		# process equip command
		success,alternative = equip.perform()

		# if the item was equipped, return true, else return false
		return success

	def addUpgrades(self,mod):
		# add the passed modifier to the item's existing modifiers
		for modType in mod.keys():
			# check to see if there are any mods of that type
			if modType in self.modifier:

				for statType in mod[modType].keys():
					# check to see if there are any mods for that type
					if statType in self.modifier[modType]:
						# if stat is attack or defense
						if statType == 'attack' or statType == 'defense':
							if len(mod[modType][statType]) != len(self.modifier[modType][statType]):
								break
							# add the list, one element at a time
							length = len(mod[modType][statType])
							for i in xrange(length):
								self.modifier[modType][statType][i] += mod[modType][statType][i]

						else:
							# stat is a normal stat, not a list
							# add the old modifier value to the new modifier value
							self.modifier[modType][statType] += mod[modType][statType]

					else:
						# self.modifier does not contain a modifier for that stat
						self.modifier[modType].update(mod[modType])
			
			else:
				# add the new modType
				self.modifier.update(mod)


class DogWhistle(Item):
	# Starting item for the Houndmaster; charms dogs
	pass
'''
items.py
'''
from objects import Object
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
		#self.game = game
		#self.x = x
		#self.y = y
		#self.char = char
		#self.name = name
		#self.color = color
		self.level = level
		#self.blocks = blocks
		#self.properNoun = properNoun

		#self.game.addObject(self)
		#self.game._currentLevel.addObject(self)
		#self.game.addItem(self)
		self.game._currentLevel.addItem(self)

		self.renderFirst()
		if self.blocks == True:
			self.game._currentLevel.setHasObjectTrue(x,y)

	def getName(self,useDefiniteArticle):
		if useDefiniteArticle == True and self.properNoun == False:
			if self.__class__.identified == True:
				return "the "+self.name
			else: return "the "+self.__class__.unidentifiedName
		else:
			if self.__class__.identified == True:
				return self.name
			else: return self.__class__.unidentifiedName

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


	def use(self,actor):
		if self in actor.inventory:
			actor.inventory.remove(self)
			actor.game.message(actor.name +" uses "+self.getName(True))
		return True

	def upgrade(self,level):
		pass

class Equipment(Item):
	identified = True
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False, canBeUnequipped = True):
		Item.__init__(self, game, x, y, char, name, color, level, blocks=False)
		self.equipSlot = equipSlot
		self.modifier = modifier
		self.canBeUnequipped = canBeUnequipped

	def use(self,actor):
		# create equip command
		equip = commands.EquipCommand(actor,self)
		# set equip command's energyCost to 0, since you are already paying for UseCommand's cost
		equip.energyCost = 0
		# process equip command
		success,alternative = equip.perform()

		# if the item was equipped, return true, else return false
		return success

	def upgrade(self,level):
		pass

class Armor(Equipment):
	unidentifiedName = "Mysterious Armor"

''' 
Gauntlet
Sword
Staff
Bow
Axe
Club
Dagger
'''
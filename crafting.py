'''
=================
 Crafting System
=================
'''

'''
==== Potions ====
'''
class Inventory:
	pass
# class to track item information

# use sets 
class Potion: # subclass of Item
	Potion._recipe = [] # randomly assign, use set
	Potion._name = None 
	Potion._discription = None # randomly assign

	def get_recipe(self,potionRecipes):
		pass

class HealthPotion(Potion):
	HealthPotion._recipe = []
	HealthPotion._name = "Health Potion"
	HealthPotion._discription = None

class Antidote(Potion):
	pass


class PotionRecipe: # subclass of Item
	self.recipe = []
	# subclasses get the recipe for their respective potions.

	def getRecipe(self):
		pass
'''
Health Potion
Oil
Confusion Poison
Bottled Cold
Bottled Fire
Paralysis
'''
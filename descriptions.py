'''
descriptions.py
'''
'''
====================
Descriptions
====================

Class Name

Health:  10
Magic:   10
Attack:  2
Defense: 2
Speed:   6

Description...

'''

descriptions = {
	'000':'''...''',
	
	'001':
'''Alchemist

Health:  15
Magic:   10
Attack:  2
Defense: 2
Speed:   6
''',
	
	'002':
'''Arbalest

Health:  20
Magic:   5
Attack:  2
Defense: 2
Speed:   6
''',
	
	'003':
'''Assassin

Health:  12
Magic:   5
Attack:  2
Defense: 2
Speed:   7
''',
	
	'004':
'''Barbarian

Health:  20
Magic:   10
Attack:  3
Defense: 2
Speed:   6
''',
	
	'005':
'''Cleric

Health:  20
Magic:   10
Attack:  3
Defense: 2
Speed:   6
''',
	
	'006':
'''Houndmaster

Health:  15
Magic:   8
Attack:  2
Defense: 3
Speed:   7
''',
	
	'007':
'''Knight

Health:  20
Magic:   10
Attack:  2
Defense: 2
Speed:   6
''',
	
	'008':
'''Occultist

Health:  15
Magic:   8
Attack:  2
Defense: 2
Speed:   6
''',
	
	'009':
'''Magician

Health:  12
Magic:   15
Attack:  2
Defense: 2
Speed:   6
''',
	
	'010':
'''Mercenary

Health:  20
Magic:   8
Attack:  2
Defense: 2
Speed:   6
''',
	
	'011':
'''Specialist

Health:  15
Magic:   8
Attack:  2
Defense: 2
Speed:   6
'''
}

def get(key):
	if key in descriptions:
		return descriptions[key]
	else: return descriptions['001']



if __name__ == '__main__':
	import random

	k = random.choice(descriptions.keys())
	print get(k)
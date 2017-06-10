'''
factions.py
'''
'''
====================
Factions
====================
'''
class FactionTracker:
	def __init__(self):
		self._hostile = 1
		self._neutral = 2
		self._friendly = 3

		self._factions = {
			"Hero":
				{
				"Hero": self._friendly,
				"Snakemen": self._hostile,
				"Plague Rats": self._hostile,
				"Mirehounds":self._hostile
				},
			"Plague Rats":
				{
				"Hero": self._hostile,
				"Snakemen": self._hostile,
				"Mirehounds":self._hostile,
				"Plague Rats": self._friendly
				},
			"Snakemen":
				{
				"Hero": self._hostile,
				"Snakemen": self._friendly,
				"Plague Rats": self._hostile,
				"Mirehounds": self._friendly
				},
			"Mirehounds":
				{
				"Hero": self._hostile,
				"Snakemen": self._friendly,
				"Plague Rats": self._hostile,
				"Mirehounds": self._friendly
				}
			}

	def getRelationship(self,faction,other):
		if faction in self._factions:
			if other not in self._factions[faction]:
				# other faction does not exist, create it
				self._factions[faction][other] = self._neutral

		else:
			#faction does not exist, create it
			self._factions[faction] = {}
			self._factions[faction][other] = self._neutral

		return self._factions[faction][other]

	def setRelationship(self,faction,other,value):
		if value not in [
			self._hostile,
			self._neutral,
			self._friendly
			]:
			print str(value) +" is not a valid relationship value"
			return

		if self.getRelationship(faction,other) != value:
			self._factions[faction][other] = value


if __name__ == "__main__":
	tracker = FactionTracker()
	print tracker.factions
	print tracker.factions["Hero"]
	print
	print tracker.factions["Snakemen"]["Hero"]
	print
	print tracker.getRelationship("Snakemen","Hero")
	print tracker.getRelationship("Mirehounds","Dancers")
	print tracker.getRelationship("Cobras","Snakemen")
	print
	tracker.setRelationship("Snakemen","Hero",tracker._friendly)
	print tracker.getRelationship("Snakemen","Hero")
	tracker.setRelationship("Snakemen","Unicorns",tracker._hostile)
	print tracker.getRelationship("Snakemen","Unicorns")
	tracker.setRelationship("Hero","Mirehounds",False)
	print tracker.getRelationship("Hero","Mirehounds")
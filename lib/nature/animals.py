"""Animals."""

from ppdRPG import _Object
from ppdRPG import configs
from ppdRPG.lib.basic import Npc, Player

class Human(_Object, Npc, Player):
	"""Human, can be either an Npc or a Player.
	
	baseType_ is a class, not a string.
	baseTypeArgs can be either a dictionary or a list or arguments.
	"""
	
	
	def __init__(self, gender, baseType, baseTypeArgs):
		
		if not baseType in [Npc, Player]:
			raise Exception('Invalid type.')
		else:
			self.baseType = baseType
			self.baseTypeArgs = baseTypeArgs
		
		if not gender in ['male','female']:
			raise Exception('Invalid gender.')
		else:
			self.gender = gender
		
		try:
			self.baseType.__init__(self, **baseTypeArgs)
		except AttributeError:
			self.baseType.__init__(self, *baseTypeArgs)

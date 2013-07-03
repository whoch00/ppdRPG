"""Animals."""

from ppdRPG import _Object
from ppdRPG import configs
from ppdRPG.lib.basic import Npc, Player

class Human(_Object, Npc, Player):
	"""Human, can be either an Npc or a Player."""
	# Re-write

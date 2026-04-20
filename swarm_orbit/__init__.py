"""swarm-orbit — Task orbit assignment for agent swarms.

Agents circle tasks like satellites orbit planets. Gravity wells attract
the right agent to the right task based on capability, load, and affinity.
"""
__version__ = "0.1.0"
from .orbit import TaskOrbit, Agent, GravityWell, OrbitalAssignment
__all__ = ["TaskOrbit", "Agent", "GravityWell", "OrbitalAssignment"]

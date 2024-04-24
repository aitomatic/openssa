"""Map-Reduce planning classes."""


from openssa.l2.planning.abstract.plan import AbstractPlan
from openssa.l2.planning.abstract.planner import AbstractPlanner


class MRTP(AbstractPlan):
    """Map-Reduce task plan (MRTP)."""


class AutoMRTPlanner(AbstractPlanner):
    """Automated (generative) Map-Reduce task planner."""

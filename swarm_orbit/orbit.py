"""Orbital mechanics for task assignment."""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class Agent:
    """An agent in the swarm."""
    id: str
    capabilities: List[str] = field(default_factory=list)
    load: float = 0.0  # 0.0 = idle, 1.0 = max capacity
    affinity: Dict[str, float] = field(default_factory=dict)  # task_type → affinity

    def available_capacity(self) -> float:
        return max(0.0, 1.0 - self.load)


@dataclass
class GravityWell:
    """A task that attracts agents based on capability match."""
    task_id: str
    task_type: str
    difficulty: float = 0.5  # 0.0 = trivial, 1.0 = extreme
    required_capabilities: List[str] = field(default_factory=list)
    priority: float = 0.5  # 0.0 = low, 1.0 = critical

    def gravitational_pull(self, agent: Agent) -> float:
        """Calculate attraction force between this well and an agent."""
        # Capability match (0-1)
        if not self.required_capabilities:
            cap_match = 0.5
        else:
            matches = sum(1 for c in self.required_capabilities if c in agent.capabilities)
            cap_match = matches / len(self.required_capabilities)
        
        # Affinity bonus (agent's learned preference for this task type)
        affinity = agent.affinity.get(self.task_type, 0.5)
        
        # Availability (busy agents have less pull)
        availability = agent.available_capacity()
        
        # Gravitational force = mass × matching × affinity × availability
        force = self.priority * cap_match * affinity * availability
        return force


@dataclass
class OrbitalAssignment:
    """Result of assigning an agent to orbit a task."""
    agent_id: str
    task_id: str
    pull: float
    rank: int  # 1 = strongest match


class TaskOrbit:
    """Manages orbital assignments for a swarm of agents around tasks.
    
    Usage:
        orbit = TaskOrbit()
        orbit.add_agent(Agent(id="scout-1", capabilities=["search", "nlp"]))
        orbit.add_well(GravityWell(task_id="t1", task_type="search", required_capabilities=["search"]))
        assignments = orbit.assign()
    """
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.wells: Dict[str, GravityWell] = {}

    def add_agent(self, agent: Agent) -> "TaskOrbit":
        self.agents[agent.id] = agent
        return self

    def add_well(self, well: GravityWell) -> "TaskOrbit":
        self.wells[well.task_id] = well
        return self

    def assign(self) -> List[OrbitalAssignment]:
        """Assign agents to tasks based on gravitational pull."""
        if not self.agents or not self.wells:
            return []
        
        # Calculate all pull forces
        pulls: List[Tuple[str, str, float]] = []
        for well in self.wells.values():
            for agent in self.agents.values():
                force = well.gravitational_pull(agent)
                pulls.append((agent.id, well.task_id, force))
        
        # Sort by pull (strongest first)
        pulls.sort(key=lambda x: x[2], reverse=True)
        
        # Greedy assignment (each agent gets one task, each task gets one agent)
        assigned_agents = set()
        assigned_tasks = set()
        assignments = []
        rank = 0
        
        for agent_id, task_id, pull in pulls:
            if agent_id in assigned_agents or task_id in assigned_tasks:
                continue
            rank += 1
            assignments.append(OrbitalAssignment(
                agent_id=agent_id, task_id=task_id, pull=round(pull, 4), rank=rank
            ))
            assigned_agents.add(agent_id)
            assigned_tasks.add(task_id)
        
        return assignments

    def unassigned_agents(self) -> List[str]:
        """Agents not currently pulled into any orbit."""
        assigned = {a.agent_id for a in self.assign()}
        return [a_id for a_id in self.agents if a_id not in assigned]

    def unassigned_tasks(self) -> List[str]:
        """Tasks with no agent in orbit."""
        assigned = {a.task_id for a in self.assign()}
        return [t_id for t_id in self.wells if t_id not in assigned]

"""Tests for swarm-orbit."""
import pytest
from swarm_orbit import TaskOrbit, Agent, GravityWell


def test_basic_assignment():
    orbit = TaskOrbit()
    orbit.add_agent(Agent(id="scout-1", capabilities=["search"]))
    orbit.add_well(GravityWell(task_id="t1", task_type="search", required_capabilities=["search"]))
    
    results = orbit.assign()
    assert len(results) == 1
    assert results[0].agent_id == "scout-1"
    assert results[0].task_id == "t1"
    assert results[0].pull > 0


def test_capability_matching():
    orbit = TaskOrbit()
    orbit.add_agent(Agent(id="a1", capabilities=["rust", "ml"]))
    orbit.add_agent(Agent(id="a2", capabilities=["python", "web"]))
    orbit.add_well(GravityWell(task_id="t1", task_type="train", required_capabilities=["ml"]))
    
    results = orbit.assign()
    assert results[0].agent_id == "a1"  # a1 has ml capability


def test_load_balancing():
    orbit = TaskOrbit()
    orbit.add_agent(Agent(id="busy", capabilities=["x"], load=0.95))
    orbit.add_agent(Agent(id="free", capabilities=["x"], load=0.1))
    orbit.add_well(GravityWell(task_id="t1", task_type="x", required_capabilities=["x"]))
    
    results = orbit.assign()
    assert results[0].agent_id == "free"  # less loaded agent wins


def test_empty_swarm():
    orbit = TaskOrbit()
    assert orbit.assign() == []


def test_unassigned():
    orbit = TaskOrbit()
    orbit.add_agent(Agent(id="a1"))
    orbit.add_agent(Agent(id="a2"))
    orbit.add_well(GravityWell(task_id="t1", task_type="x"))
    
    results = orbit.assign()
    assert len(orbit.unassigned_agents()) == 1  # one agent has no task
    assert len(orbit.unassigned_tasks()) == 0  # task is covered

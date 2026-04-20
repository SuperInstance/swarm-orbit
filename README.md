# swarm-orbit

Task orbit assignment for agent swarms. Agents circle tasks like satellites — gravity wells attract the right agent to the right task.

## How It Works

Each task is a **gravity well** with mass (priority) and required capabilities. Each agent has capabilities, current load, and learned affinities. Gravitational pull = priority × capability match × affinity × availability. Strongest pull wins.

## Usage

```python
from swarm_orbit import TaskOrbit, Agent, GravityWell

orbit = TaskOrbit()
orbit.add_agent(Agent(id="scout-1", capabilities=["search", "nlp"], load=0.2))
orbit.add_agent(Agent(id="builder-1", capabilities=["rust", "ml"], load=0.7))
orbit.add_well(GravityWell(task_id="t1", task_type="search", required_capabilities=["search"]))

assignments = orbit.assign()
# scout-1 orbits t1 (stronger pull — capability match + low load)
```

Zero deps. `pip install swarm-orbit`

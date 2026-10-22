import simpy

from dexter.simulation import SimManager, Grid


def test_grid(sample_grid):
    assert sample_grid[2, 2] == "A"
    assert sample_grid[1, 1] == "#"

    sample_grid.set_agent(0, 4)
    assert sample_grid[2, 2] == "·"
    assert sample_grid.agent_pos == (0, 4)


def test_grid_str():
    lines = str(Grid(2, 3)).splitlines()
    assert len(lines) == 4
    assert len({len(line) for line in lines}) == 1


def test_sim_manager_runs_processes():
    sim = SimManager()
    sim.add_resource("counter", simpy.Resource(sim.env, capacity=1))
    served = []

    def customer(env, name):
        with sim.get_resource("counter").request() as req:
            yield req
            yield env.timeout(2)
            served.append((name, env.now))

    sim.add_process("customer", customer)
    sim.activate_process("customer", "a")
    sim.run(until=10)

    assert served == [("a", 2)]

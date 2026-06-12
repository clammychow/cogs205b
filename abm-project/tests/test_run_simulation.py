import copy
import unittest

import numpy as np

from run_simulation import (
    Agent,
    ForagingABM,
    SimulationConfig,
    average_risky_pct_trajectory,
    init_agents,
    n_risky_from_start_pct,
    run_simulation,
    risky_pct,
    starting_risky_pct_sweep,
)


class TestRunSimulation(unittest.TestCase):
    def setUp(self):
        self.abm_mini = SimulationConfig(
            n_agents = 10, 
            n_timesteps = 10, 
            n_risky = 5
        )
        self.abm_risky_worse_EV = SimulationConfig(
            n_agents=10,
            n_timesteps=20,
            n_risky=5,
            payoffs={"risky": [(0.4, 4), (0.6, -4)], "safe": [(0.5, 4), (0.5, 0)]}
        )
        self.abm_risky_lower_variance = SimulationConfig(
            n_agents=10,
            n_timesteps=20,
            n_risky=5,
            payoffs={"risky": [(0.5, 3), (0.5, 1)], "safe": [(0.5, 4), (0.5, 0)]},
        )
        self.abm_negative_food_payoffs = SimulationConfig(
            n_agents=3,
            n_timesteps=10,
            n_risky=1,
            payoffs={"risky": [(1.0, -100)], "safe": [(1.0, -100)]},
            food_decay=0,
        )
        self.abm_4_food_payoffs = SimulationConfig(
            n_agents=4,
            n_timesteps=1,
            n_risky=2,
            payoffs={"risky": [(1.0, 4)], "safe": [(1.0, 4)]},
        )
    
    # Edge case / robustness verification
    def test_no_imitation(self):
        abm_no_imitation = copy.deepcopy(self.abm_mini)
        abm_no_imitation.copy_probability = 0
        run = run_simulation(abm_no_imitation)
        self.assertEqual(run.n_risky_final, 5)
        self.assertEqual(run.n_safe_final, 5)
        self.assertEqual(run.risky_pct_trajectory[0], run.risky_pct_trajectory[-1])
    
    def test_fixed_food(self):
        abm_fixed_food = copy.deepcopy(self.abm_mini)
        abm_fixed_food.fixed_food = 10
        run = run_simulation(abm_fixed_food)
        self.assertEqual(run.n_risky_final, 5)
        self.assertEqual(run.n_safe_final, 5)
        self.assertEqual(run.risky_pct_trajectory[0], run.risky_pct_trajectory[-1])

    def test_homogenous_safe_start(self):
        abm_no_risky = copy.deepcopy(self.abm_mini)
        abm_no_risky.n_risky = 0
        run = run_simulation(abm_no_risky)
        self.assertEqual(run.n_risky_final, 0)
        self.assertEqual(run.n_safe_final, 10)
        self.assertEqual(run.risky_pct_trajectory[0], run.risky_pct_trajectory[-1])

    def test_homogenous_risky_start(self):
        abm_all_risky = copy.deepcopy(self.abm_mini)
        abm_all_risky.n_risky = 10
        run = run_simulation(abm_all_risky)
        self.assertEqual(run.n_risky_final, 10)
        self.assertEqual(run.n_safe_final, 0)
        self.assertEqual(run.risky_pct_trajectory[0], run.risky_pct_trajectory[-1])

    def test_risky_worse_EV_loses(self):
        risky_finals = []
        for seed in range(10):
            config = copy.deepcopy(self.abm_risky_worse_EV)
            config.seed = seed
            run = run_simulation(config)
            risky_finals.append(run.n_risky_final)
        self.assertLess(np.mean(risky_finals), 5)

    def test_risky_lower_variance_loses(self):
        risky_finals = []
        for seed in range(10):
            config = copy.deepcopy(self.abm_risky_lower_variance)
            config.seed = seed
            run = run_simulation(config)
            risky_finals.append(run.n_risky_final)
        self.assertLess(np.mean(risky_finals), 5)

    # Additional implementation tests
    def test_config_validation(self):
        with self.assertRaises(ValueError):
            SimulationConfig(n_agents = 2)
        with self.assertRaises(ValueError):
            SimulationConfig(n_agents = 3, n_risky = 7)
        with self.assertRaises(ValueError):
            SimulationConfig(beta = -1)
        with self.assertRaises(ValueError):
            SimulationConfig(n_timesteps = -1)
        with self.assertRaises(ValueError):
            SimulationConfig(copy_probability = 2)
        with self.assertRaises(ValueError):
            SimulationConfig(n_risky = -1)
        with self.assertRaises(ValueError):
            SimulationConfig(payoffs = {"risky": [(1, 4), (0.5, 0)], "safe": [(1, 4)]})
        with self.assertRaises(ValueError):
            SimulationConfig(payoffs = {"risky": [(-1, 4), (1, 0)], "safe": [(1, 4)]})

    def test_food_floor(self):
        config = copy.deepcopy(self.abm_negative_food_payoffs)
        rng = np.random.default_rng(0)
        agents = init_agents(config, rng)
        abm = ForagingABM(agents, config)
        for _ in range(config.n_timesteps):
            abm.step(rng)
            for agent in abm.agents:
                self.assertGreaterEqual(agent.food, 0)

    def test_food_decay(self):
        config = copy.deepcopy(self.abm_4_food_payoffs)
        rng = np.random.default_rng(0)
        agents = init_agents(config, rng)
        abm = ForagingABM(agents, config)
        for _ in range(config.n_timesteps):
            abm.step(rng)
            for agent in abm.agents:
                self.assertEqual(agent.food, 2)

    def test_identical_payoffs(self):
        abm_id_payoffs = copy.deepcopy(self.abm_4_food_payoffs)
        abm_id_payoffs.n_timesteps = 10
        run = run_simulation(abm_id_payoffs)
        self.assertEqual(run.n_safe_final, run.n_risky_final)

    def test_risky_pct(self):
        agent_mix = [Agent("risky"), Agent("safe"), Agent("safe")]
        no_risky = [Agent("safe")]
        all_risky = [Agent("risky")]
        self.assertAlmostEqual(risky_pct(agent_mix), 100/3)
        self.assertEqual(risky_pct(no_risky), 0)
        self.assertEqual(risky_pct(all_risky), 100)

    def test_average_trajectory_shape(self):
        config = copy.deepcopy(self.abm_mini)
        batch = average_risky_pct_trajectory(config, n_runs=5)
        self.assertEqual(batch.mean_trajectory.shape, (config.n_timesteps + 1,))
        self.assertEqual(batch.std_trajectory.shape, (config.n_timesteps + 1,))

    def test_sweep_shape(self):
        start_pct = np.array([25.0, 50.0, 75.0])
        sweep = starting_risky_pct_sweep(self.abm_mini, start_pct, n_runs_per_starting_pct=3)
        self.assertEqual(len(sweep.start_risky_pct), 3)
        self.assertEqual(len(sweep.mean_final_risky_pct), 3)
        self.assertEqual(len(sweep.std_final_risky_pct), 3)

    def test_reproducibility(self):
        r1 = run_simulation(copy.deepcopy(self.abm_mini))
        r2 = run_simulation(copy.deepcopy(self.abm_mini))
        np.testing.assert_array_equal(r1.risky_pct_trajectory, r2.risky_pct_trajectory)


if __name__ == "__main__":
    unittest.main()
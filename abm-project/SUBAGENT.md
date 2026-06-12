# Verifying run_simulation.py
`run_simulation.py` contains an agent based model that examines the spread of a strategy based on an imitation rule. I want to verify that the code passes the following verification checks:
- Fixing copy probability to 0 results in no change in the percentage of the population that is risky.
- Fixing all agents' food amounts to a constant results in no change in the risky percentage.
- Allowing all agents to start with the same strategy results in no change in the risky percentage.
- Changing the expected value or variance of payoffs leads to expected changes in model outcomes.

## Your Task:
Run the unittest file at `tests/test_run_simulation.py`. If there are any failures, read `run_simulation.py` and propose possible fixes.

Then, review `run_simulation.py` for any major hidden edge-cases, logical inconsistencies, redundancies, or silent error handling that should be made explicit.

Common failure modes may include:
- unintended mutation of SimulationConfig objects
- unintended expected value differences between strategy payoffs
- inconsistent trajectory lengths
- invalid payoff probability distributions
- inaccurate food value or strategy updating
- plotting errors

Propose minimal fixes/refinements if needed.

### Constraints:
- do not write/edit any code yourself; only list suggestions
- make fixes simple
- do not change model logic
- do not change the test file
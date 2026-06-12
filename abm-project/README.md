# Foraging Strategy ABM
## Model Specification
The system features 100 agents in a ring system. Every timestep, agents gain or lose food depending on their current foraging strategy (risky or safe). Agents have a chance of copying a neighbor with an opposite strategy if the neighbor is more successul. This model runs and averages 30 simulations across 500 timesteps (~8 minutes to complete).

Main simulations use a 50/50 risky vs. safe agent starting composition. The model also conducts a sweep of different starting compositions.

### Agent Variables
Strategies:
- Risky: at each timestep, agent has a 40% chance of gaining 8 food or 60% chance of losing 2 food
- Safe: at each timestep, agent has a 50% chance of gaining 4 food or 50% chance of gaining 0 food

Accumulated Food:
- All agents experience a decay of 2 food at every timestep
- Food cannot go below 0
### Update Rules
Each timestep:
1. Agents forage and get payoffs added to food score
2. Agents experience food decay
3. Agents randomly observe one neighbor and decide whether to copy its strategy. Agents have a higher chance of copying when food difference is greater.

**Copy Probability:** If neighbor has more food AND a different strategy, $P(copy) = \frac{1}{1 + e^{-\beta \delta}}$, where $\delta$ is neighbor's food - agent's food and $\beta$ is a sensitivity parameter (default $\beta$ = 1.0 in all simulations).
### Metrics
- Mean percentage of risky agents over time, averaged across 30 runs (risky_prevalence_trajectory.png)
- Final mean risky percentage after 500 timesteps (final_average_composition.png)
- Final mean risky percentage after 500 timesteps with different starting risky proportions (starting_composition_sweep.png)

## Results
The risky strategy strongly dominates across all simulations, with a final mean proportion of risky agents at 95% over 30 runs. The averaged trajectory of risky prevalence shows a sharp increase in risky agents early on. This trajectory plateaus at around 100 timesteps and remains stable at around 95% risky for the remaining duration. Risky dominance is robust to initial starting conditions; a starting composition sweep reveals that risky dominance emerges even when as little as 20% of the population begins as risky, though final compositions are more variable with fewer initial risky agents.

Considering the expected values for both strategies are equal and risky dominance does not appear to be driven purely by starting composition, these results suggest that the observed risky dominance is driven by the interaction between the imitation rule and differences in stochastic payoff variances. Highly variable payoffs may produce short-term success spikes that allow risky agents to be disproportionately copied and amplified early on by an imitation rule sensitive to differences in current fitness. Thus, under the model assumptions, this imitation rule is sufficient to generate immediate and sustained dominance of a higher-variance strategy when strategies have equal expected values.
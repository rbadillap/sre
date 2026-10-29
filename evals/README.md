# Evals

Each eval checks that an agent with the skills loaded applies the method to a scenario. Every scenario comes from real use, or from a public postmortem linked as its source, written in general terms. The rules for writing one are in [docs/review/evals.md](../docs/review/evals.md).

One folder per orchestrator, one file per scenario. Each file has three parts:

- **Scenario**: every fact the agent needs, so the eval doesn't depend on live data.
- **Expected moves**: what the agent has to do and find, following the orchestrator's row in [docs/review/skills.md](../docs/review/skills.md).
- **Fails if**: specific behaviors that fail the eval.

To run one: load the package, give the agent the scenario as the situation in front of it, and compare its result with the expected moves and the failure conditions.

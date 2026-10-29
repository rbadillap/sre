# Reviewing an eval

An eval checks that an agent with the skills loaded applies the method to a scenario.

**1. It comes from real use.**
- Why: invented scenarios test what the author already expected. Real ones test what happened.
- Check: the eval says where the scenario came from, in general terms (a real incident, a release that went wrong). No names or private details. A public postmortem counts as real use: link it as the source, keep the scenario in general terms, and stop the facts at the moment the skill starts, so the published ending isn't given away.

**2. It has three parts: the scenario, the expected moves, and what fails it.**
- Why: "the answer looks good" isn't a test.
- Check: the expected moves follow the orchestrator's row in [skills.md](skills.md). The failure conditions are specific ("restarts pods before checking the database", "runs an apply that replaces the database").

**3. It checks the skipped parts.**
- Why: skipping a part of the question is the most common gap, and the easiest to miss in review.
- Check: if the scenario asks several things, each one has its own expected move.

**4. It runs the same way twice.**
- Why: an eval that passes by luck tells nothing.
- Check: the scenario includes every fact the agent needs. Nothing depends on live data.

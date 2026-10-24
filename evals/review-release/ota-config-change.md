# Reviewing a configuration change shipped over the air to a device fleet

Origin: a real review of a release flow in a prototype that ships Kubernetes workloads to edge devices over the air, with automatic rollback.

## Scenario

The release under review is version 2 of a demo application, with a new configuration value. It ships to a fleet of three edge devices: one canary and two in production. Each device runs its own lightweight Kubernetes, so no state is shared between devices.

- The application stores no data. Its configuration is a ConfigMap generated with a content hash in its name, so a Deployment rollback restores the previous configuration as well. Nothing enforces that every configuration value goes through that generator.
- On the device, the update step applies the manifests, waits for the rollout, checks a health endpoint, and watches 30 seconds for restarts. If a check fails, it rolls back and reports failure.
- The health endpoint returns "ok" regardless of the configuration value.
- A release script uploads the artifact, deploys it to the canary, and as soon as the canary finishes without failure, deploys to production. Nobody approves the step to production.
- The update server refuses a second artifact with the same name; the release script treats that refusal as "already uploaded" and continues.
- After a release is committed on a device, nothing watches it.

## Expected moves

1. Names what was reviewed: the release flow and a described change, without a diff.
2. Reframes from "will it install" to "will devices run the new value correctly".
3. Answers every state category, including the delivery system's own records, and marks device state as per instance.
4. Marks the configuration rollback-safe only on the condition that it goes through the hashed generator, and writes a way back after full release.
5. Finds that the gate between canary and production waits zero seconds after a 30-second soak, and that a script, not a person, moves to production.
6. Lists delayed effects and sets an observation time longer than them.
7. Uses absolute thresholds, since three devices have no traffic to compare.
8. Finds that nothing checks the new value: the health endpoint can't see it.
9. Notices that re-releasing a fix under the same name would deploy the old artifact, labeled as a hypothesis unless tested.
10. Gives a verdict of ready with conditions or not ready, with the conditions or options that would make it safe (at least: a wait and a second check before production, and a check of the new value), and names the decision owner.

## Fails if

- It treats the canary result as proof the release is safe.
- It assumes traffic or tenants exist.
- It approves without naming the gate between steps.
- It restates a discipline's text instead of applying it by name, or leaves claims unlabeled.

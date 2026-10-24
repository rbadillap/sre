# Blind spots in an over-the-air update flow for a device fleet

Origin: a real review of a prototype that ships Kubernetes workloads to edge devices over the air, with automatic rollback.

## Scenario

A small fleet of edge devices receives application updates from an over-the-air update server. Each device runs a lightweight Kubernetes and an update agent. A custom update step on the device:

- applies the new manifests;
- waits until the rollout of every Deployment completes;
- checks each Deployment's health endpoint, if the Deployment has a health annotation;
- watches for restarts during a 30-second soak;
- if any check fails, runs a rollback of the Deployments and reports the update as failed.

A release script sends each release to one canary device first. When the update server reports the canary deployment finished without failure, the script immediately sends the same release to the production group. Its final message is the same whether a failed canary was rolled back or left broken.

The device enrollment loop in the release script reads devices from a list in a shell pipeline. Devices whose name matches a pattern are accepted automatically.

The update server shows each device as installed or failed. Device inventory has no health attribute. Nothing pages or notifies anyone. A watchdog that would restart failing workloads after an update is planned but not built.

The repository includes test faults: a release that crashes N seconds after start, one that leaks memory and is killed after about a minute, one whose health endpoint starts failing after two minutes, and one with a bad configuration value.

## Expected moves

1. Reframes the question from "is there monitoring" to "would an operator know a release broke devices".
2. Counts operators as users, not only the people using the application.
3. Records that nothing pages anyone as the first gap.
4. Finds that a release failing after the 30-second soak passes the canary and reaches all production devices, with nothing watching afterwards. Uses the delayed test faults as evidence.
5. Finds that nothing leaves a device after a successful install: no health signal, no restart signal.
6. Finds that verification only covers Deployments, so changes to other resource kinds, or Deployments without the health annotation, pass unchecked.
7. Finds that a rollback reported as done is not health-checked, and that the release script's final message hides whether it worked.
8. Notices that a shell pipeline can hide a failed enrollment step, labeled as a hypothesis unless run.
9. Notices that devices which stop checking in are not watched, and that auto-accepted devices are an identity gap.
10. Ranks the gaps by reach and time unnoticed, and labels every claim verified, hypothesis or not verified.

## Fails if

- It reports that the system "has monitoring" because the update server shows installed and failed.
- It misses the gap between the 30-second soak and delayed failures.
- It proposes changes as done, or edits files outside `reliability/`.
- It writes gaps with no reach, no time unnoticed or no label.

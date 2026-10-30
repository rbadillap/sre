# Progressive delivery, by platform

Examples for step 7 of the skill.

## Kubernetes with Argo Rollouts

- A canary strategy with `setWeight` steps and `pause` durations sets the shares and observation times.
- An `AnalysisTemplate` runs queries during each step (for example, against Prometheus) comparing the canary with the stable version, and aborts the rollout when a query fails its condition.
- Abort moves traffic back to the stable version automatically. It doesn't revert data, so it only belongs to changes marked rollback-safe.

## Kubernetes without a rollout controller

- A Deployment's rolling update with `maxUnavailable: 0` and `maxSurge: 1` brings a new pod up before an old one goes away, but it has no analysis: it moves forward as long as pods are ready.
- `kubectl rollout status` confirms the rollout finished, not that requests succeed. Pair it with a soak period and a check of the business signal.
- PodDisruptionBudgets protect against voluntary evictions such as node drains. They don't control rolling updates.

## Feature flags

- A flag separates the deploy from the release: the code ships turned off, and turning it on is the release.
- Turning a flag off is usually faster than a rollback, and safer when the change touched state, as long as the old code path still reads what the new one wrote.

## Device fleets and over-the-air updates

- Groups of devices play the role of traffic shares: a canary group first, then the rest, with a gate between them.
- The observation time has to cover the device's own check cycle: an update that looks installed may fail after a restart or the next health check.
- An update that changes data on the device needs a manual rollback path, decided by a person.
- Recovery has to survive the failure it's meant to fix. If an update can stop the device from booting, or stop the update agent from connecting, the fix can't depend on that agent. The way back can be local recovery, a separate management channel, or planned physical intervention. Write down which one exists and how it was tested.
- One local recovery is A/B partitions, as [Mender](https://docs.mender.io/overview/customize-the-update-process) documents them. The update installs to the inactive partition, the device reboots into it, and the update is committed only after the health checks it needs pass. Booting alone doesn't prove the application works.
  - Rolling back without a commit depends on bootloader integration and a boot-attempt limit ([U-Boot integration](https://docs.mender.io/operating-system-updates-yocto-project/board-integration/bootloader-support/u-boot/manual-u-boot-integration)). Something also has to restart a device that hangs, so it gets back to the bootloader.
  - Going back to the other partition doesn't revert content stored elsewhere or shared data. Check what the recovery actually covers.
- Phases are batches. Mender's [phased rollouts](https://docs.mender.io/overview/deployment) set each phase as a share of the devices. The gate, the observation time and the criteria to go on still belong to the release plan. With a group whose members change, the real size of each phase can change too, so a percentage doesn't always cap how many devices get the update.

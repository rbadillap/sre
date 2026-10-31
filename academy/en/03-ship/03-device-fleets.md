---
title: "Device fleets"
stage: ship
order: 3
status: approved
teaches: "Plan an update for a fleet of devices so a way back still works when the update breaks the device: what can fail, which recovery survives each failure, and how you test it."
sources:
  - title: "Rivian, Part 573 Safety Recall Report 23V-783, filed with NHTSA"
    url: https://static.nhtsa.gov/odi/rcl/2023/RCLRPT-23V783-7227.PDF
  - title: "TechCrunch, A software update bricked Rivian infotainment systems"
    url: https://techcrunch.com/2023/11/14/a-software-update-bricked-rivian-infotainment-systems/
  - title: "The Register, Rivian bricks infotainment systems in 'fat finger' fiasco"
    url: https://www.theregister.com/2023/11/15/rivian_bricked_infotainment_systems/
  - title: "CrowdStrike, Preliminary Post Incident Review"
    url: https://www.crowdstrike.com/en-us/blog/falcon-content-update-preliminary-post-incident-report/
  - title: "Microsoft, KB5042421, CrowdStrike issue impacting Windows endpoints"
    url: https://support.microsoft.com/kb/5042421
  - title: "Microsoft, KB5042429, New recovery tool to help with CrowdStrike issue"
    url: https://support.microsoft.com/en-us/help/5042429
  - title: "Mender, Customize the update process"
    url: https://docs.mender.io/overview/customize-the-update-process
  - title: "Mender, State scripts"
    url: https://docs.mender.io/artifact-creation/state-scripts
  - title: "Mender, Deployment"
    url: https://docs.mender.io/overview/deployment
  - title: "Mender, Manual U-Boot integration"
    url: https://docs.mender.io/operating-system-updates-yocto-project/board-integration/bootloader-support/u-boot/manual-u-boot-integration
skills: [review-release]
version: "0.1.1"
---

# Device fleets

_Sources: [Rivian's recall report](https://static.nhtsa.gov/odi/rcl/2023/RCLRPT-23V783-7227.PDF), with [TechCrunch](https://techcrunch.com/2023/11/14/a-software-update-bricked-rivian-infotainment-systems/) and [The Register](https://www.theregister.com/2023/11/15/rivian_bricked_infotainment_systems/). [CrowdStrike's review](https://www.crowdstrike.com/en-us/blog/falcon-content-update-preliminary-post-incident-report/), with Microsoft's [KB5042421](https://support.microsoft.com/kb/5042421) and [KB5042429](https://support.microsoft.com/en-us/help/5042429). Mender's [update process](https://docs.mender.io/overview/customize-the-update-process), [state scripts](https://docs.mender.io/artifact-creation/state-scripts), [deployment](https://docs.mender.io/overview/deployment) and [U-Boot](https://docs.mender.io/operating-system-updates-yocto-project/board-integration/bootloader-support/u-boot/manual-u-boot-integration) pages._

## The question

On your own servers, you can usually reach a machine that a bad change broke. A device in someone's car or on someone's desk is different. If the update is what broke it, what still works to fix it?

## What happened at Rivian

Rivian sends its vehicles over-the-air (OTA) updates, software delivered over a network. Its report to NHTSA, the US road safety regulator, says:

- **November 13, 2023:** Rivian pushed update 2023.42, and some customers started installing it. "Within two hours of the OTA push", Rivian identified a problem with the infotainment system, the screen and controls in the cabin, and cancelled the update.
- **Who was affected:** the 1,463 vehicles that had installed it before the cancel. On them, windshield defroster controls and function "may have been unavailable". Rivian wasn't aware of any crashes or injuries.
- **November 15:** Rivian released 2023.42.02 to those vehicles.
- **By November 19:** all 1,463 had been fixed. The report says this was "through the new software update".

The press carries what Rivian said at the time:

- The cause: "a fat finger where the wrong build with the wrong security certificates was sent out".
- "A vehicle reset or sleep cycle will not solve the issue."
- The fix "may require physical repair in some cases".

The report's field for the cause says "NR", not reported, so the cause above comes only from Rivian's statements in the press. No source here says why the update channel still worked, or whether these vehicles have a second software copy to fall back on.

## What happened on Windows devices

[A deploy is not a release](01-a-deploy-is-not-a-release.md) covers how CrowdStrike's update of July 19, 2024 crashed Windows hosts. This part is about getting them back.

CrowdStrike's review says it released the update at 04:09 UTC and reverted it at 05:27, 78 minutes later. Hosts that came online after that, or didn't connect in that window, weren't affected. The review doesn't say how a host that had already crashed recovers.

Microsoft's articles do:

- **The symptom:** a blue screen and "a continual restarting state".
- **Restarting:** "We have received reports of successful recovery from some customers attempting multiple restart operations".
- **By hand:** at each device, start in safe mode, delete the file matching `C-00000291*.sys`, and restart. "You may be asked to enter your BitLocker recovery key", the key for the device's disk encryption.
- **With a tool:** a bootable USB drive that automates those steps. One option can need the BitLocker key. The other needs a local administrator account, and on some BitLocker setups a PIN or the key as well.
- **If those don't fit:** network boot for devices without USB. After the manual steps, "reimaging the device might be a solution", which means reinstalling it.
- **Before using any of them:** "first test it on multiple devices before you use it broadly".

## What Mender documents

Mender is an OTA update tool. These pages are documentation, not an incident.

- **Two partitions.** An update downloads to "the inactive rootfs partition", the copy of the system not in use. The device switches partitions and reboots.
- **Commit.** If the new image "passes all the integrity checks", the update is marked successful and stays. A script can "add custom integrity checks beyond what the Mender Client provides out of the box". The client "automatically rolls back an update if it can not reach the Mender Server".
- **Rollback.** If a check fails, the client reverts and reboots into the old partition. For rollback, U-Boot, a bootloader, needs a boot counter limit: "This is required for rollback support to work."
- **Data.** Scripts "can help revert migrations done as a part of the update". The partition swap isn't described as reverting them.
- **Phases.** A phased rollout sets each phase as a share of a group's devices. For a dynamic group, one whose members can change, the sizes are calculated when the deployment is created and aren't recalculated. If the group grows, the last phase expands. If it shrinks, the entire group "(potentially) gets updated before all the phases end".
- **Timing.** When a device gets an update is set by "the concrete moment the device contacts the server following its polling cycle".

## Reading the cases

The rest of this lesson is its own reading and method. This lesson's sources don't show two partitions saving a real fleet, because neither case says that mechanism was in use.

- **Cancelling protects devices that haven't updated.** Both companies stopped the update within two hours. Each stop helped the devices not yet reached, and each fleet still needed a fix for the rest.
- **Ask whether the way back survives.** Rivian's way back was another software update, and in the end it worked for every vehicle. Windows hosts in a restart loop could try restarting, which some customers reported worked. The other options added a key, an account, a USB drive or a network boot. This lesson's rule, not a source's: recovery has to survive the failure it's meant to fix.
- **Booting isn't working.** Mender's commit depends on checks. If they only prove the device booted, a broken application gets committed. This is this lesson's reading of "custom integrity checks", not Mender's claim.
- **A percentage isn't a cap.** With a dynamic group, the first phase can be everything that's left. Then the gate you planned never gets a chance.

## How to do it

1. List what the update could break, in order of depth: the application, the update agent's connection, booting, the device's stored data.
2. For each, name a way back that doesn't depend on the thing broken: a commit check, a bootloader fallback, a separate channel, or a visit in person.
3. Write what each way back needs: keys, accounts, tools, people, and how far away the devices are.
4. Test it on real devices, with the failure actually caused. A way back you've never run is a hypothesis.
5. Work out each phase as a number of devices, and compare it with the smallest the group could become. If phase 1 can cover what's left, the gate, as in [Rolling out in steps](02-rolling-out-in-steps.md), never runs.
6. Set observation time from the device's cycle: check-in time, plus install and reboot, plus when the first real use happens.

## Worked example

An example written for this lesson, using only the sources' facts.

- **Rivian, infotainment broken.** Reset or sleep cycle: Rivian said it wouldn't work. Another OTA update: worked for all 1,463. Physical repair: named as a possibility, and the report doesn't show it was needed.
- **Windows, restart loop.** Repeated restarts: worked for some, by reports Microsoft received. Safe mode by hand: may need a BitLocker key. USB tool: a USB drive and port, and depending on the option and on BitLocker, a key, an admin account, or both. Network boot: needs a network that can reach the device.
- **Tested in advance?** No source here says.

_If you use rbadillap/sre: `review-release` applies its rollout step to groups of devices. Its [platform notes](../../../skills/review-release/references/progressive-delivery.md) ask you to write which way back exists (local recovery, a separate management channel or planned physical intervention) and how it was tested. It writes a plan and doesn't update any device._

## In one sentence

"For each way an update can break a device, I name a way back that doesn't depend on the broken part, and I test it before I ship."

## Exercise

A hypothetical fleet: 1,000 parking payment terminals, in a dynamic group, with two partitions and a bootloader limit of 3 boot attempts. After 3 failed boots, the bootloader goes back to the old partition, and a watchdog restarts a terminal that hangs. There's no separate management channel. 40 terminals are a three-hour drive away. Each terminal checks for updates every 4 hours. Their update agent isn't Mender's client: it commits as soon as the device has booted. An update changes the system, and migrates a local file of transactions. Phases: 30%, then 70%.

1. For each failure, say which way back works as things stand, and what you'd change:
   - The new kernel doesn't boot.
   - The device boots, and the payment application crashes.
   - The device boots, and the update agent can't reach the server, because a certificate is wrong.
2. Does going back to the old partition undo the transactions file migration? What would you need to know or write?
3. How many terminals are in each phase when the deployment is created? Under the behavior in Mender's page, what could happen if 800 leave the group during the rollout?
4. A fault appears only during the nightly transaction upload, which runs once every 24 hours, at a different time on each terminal. An install and reboot take 1 hour at most. Ignoring how long the upload takes, how long must phase 1 stay open so that, in the worst case, every terminal in it has checked in, installed, and started one upload?
5. Pick a device you depend on: a phone, a router, a car. If its next update stopped it from starting, what way back exists, and what would it need from you? If you don't know, say so, and where you'd look.

---

_Written with an AI assistant from the sources above._

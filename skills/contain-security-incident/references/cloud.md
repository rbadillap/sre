# Containment, by cloud

Examples for steps 3 to 6 of the skill.

## AWS

- **Evidence:** CloudTrail for API calls (who, from which IP, with which tool, and when); AWS Config for the history of each resource; GuardDuty findings. Export what covers the period before changing anything.
- **Temporary credentials can't be revoked one by one.** "Revoke active sessions" on an IAM role adds a deny policy for every session issued before that moment (a condition on `aws:TokenIssueTime`). Current sessions stop working; workloads that assume the role again get new, valid credentials.
- **Disable, don't delete:** set the access key to inactive; attach a deny-all policy to an unknown user.
- **A disabled access key doesn't end the sessions created from it.** Temporary credentials obtained with the key (for example through `GetSessionToken`) keep working until they expire. For a known user, also attach a policy that denies everything for credentials issued before now, with a condition on `aws:TokenIssueTime`. Verify the exact policy against the current IAM documentation for revoking temporary credentials before using it.
- **Before removing a broad permission,** check what the workload actually uses with IAM Access Advisor, so the fix doesn't break it.
- **Persistence to look for:** new users, access keys and login profiles; roles whose trust policy changed, for example to trust an outside account; new Lambda functions or EC2 instances; changes to bucket policies or KMS key policies; security group rules.
- **Prevention:** permission boundaries so a role can't grant itself more; service control policies for the most dangerous actions; CI with short-lived credentials (OIDC) instead of human write access; a break-glass role that alerts when used.

## Kubernetes

- **Cut the service account's access first:** record its RoleBindings and ClusterRoleBindings, then remove them. That stops API calls made with any of its tokens at once, and the record lets you put them back.
- **Projected tokens are bound to their pod:** a token keeps working until it expires or its pod is deleted. Restarting the container doesn't invalidate it. So capture the evidence first (logs, `kubectl describe`, a copy of the filesystem if needed), then delete the pod to end its token, and let a fresh pod start under a trusted identity.
- **Long-lived token Secrets** (the older kind) work until the Secret is deleted. Record it, then delete it.
- **Isolate the workload's network** with a NetworkPolicy that denies its traffic while you capture evidence.
- Check RoleBindings and ClusterRoleBindings created during the period: they're a common way to keep access.

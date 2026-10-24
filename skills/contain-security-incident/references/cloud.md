# Containment, by cloud

Examples for steps 3 to 6 of the skill.

## AWS

- **Evidence:** CloudTrail for API calls (who, from which IP, with which tool, and when); AWS Config for the history of each resource; GuardDuty findings. Export what covers the period before changing anything.
- **Revoking a role's sessions:** "Revoke active sessions" on an IAM role adds a deny policy for every session issued before that moment (a condition on `aws:TokenIssueTime`). Current sessions stop working; workloads that assume the role again get new, valid credentials. To deny a single session instead, AWS documents conditions on `aws:userid` or `aws:SourceIdentity`.
- **Where revoking a role's sessions doesn't apply:** roles managed by IAM Identity Center, service-linked roles, and session tokens issued to the root user each need their own path. Check the current IAM documentation on revoking temporary credentials for these cases.
- **Disable, don't delete:** set the access key to inactive; attach a deny-all policy to an unknown user.
- **A disabled access key doesn't end the sessions created from it.** Temporary credentials obtained with the key (for example through `GetSessionToken`) keep working until they expire. For a known user, also attach a policy that denies everything for credentials issued before now, with a condition on `aws:TokenIssueTime`. Verify the exact policy against the current IAM documentation for revoking temporary credentials before using it.
- **Before removing a broad permission,** check what the workload actually uses with IAM Access Advisor, so the fix doesn't break it.
- **Persistence to look for:** new users, access keys and login profiles; roles whose trust policy changed, for example to trust an outside account; new Lambda functions or EC2 instances; changes to bucket policies or KMS key policies; security group rules.
- **Prevention:** permission boundaries so a role can't grant itself more; service control policies for the most dangerous actions; CI with short-lived credentials (OIDC) instead of human write access; a break-glass role that alerts when used.

## Kubernetes

- **Cut the service account's access first:** record the RoleBindings and ClusterRoleBindings that name it, then propose removing them. That removes what those bindings grant, and the record lets you put them back. It isn't the whole picture: bindings to groups it belongs to still apply, and cloud credentials it already exchanged through workload identity keep working until revoked at the cloud provider.
- **Projected tokens bound to a pod** keep working until they expire or the pod is deleted. Restarting the container doesn't invalidate them. Capture the evidence first (logs, `kubectl describe`, a copy of the filesystem if needed), then propose deleting the pod so a fresh one starts under a trusted identity. Tokens requested separately, not bound to the pod, last until they expire.
- **Long-lived token Secrets** (the older kind) work until the Secret is deleted. Record it, then propose deleting it.
- Every deletion here is a proposal for a person to run, after the evidence is captured.
- **Isolate the workload's network** with a NetworkPolicy that denies its traffic while you capture evidence.
- Check RoleBindings and ClusterRoleBindings created during the period: they're a common way to keep access.

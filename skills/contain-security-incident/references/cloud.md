# Containment, by cloud

Examples for steps 3 to 6 of the skill.

## AWS

- **Evidence:** CloudTrail for API calls (who, from which IP, with which tool, and when); AWS Config for the history of each resource; GuardDuty findings. Export what covers the period before changing anything.
- **Temporary credentials can't be revoked one by one.** "Revoke active sessions" on an IAM role adds a deny policy for every session issued before that moment (a condition on `aws:TokenIssueTime`). Current sessions stop working; workloads that assume the role again get new, valid credentials.
- **Disable, don't delete:** set the access key to inactive; attach a deny-all policy to an unknown user.
- **Before removing a broad permission,** check what the workload actually uses with IAM Access Advisor, so the fix doesn't break it.
- **Persistence to look for:** new users, access keys and login profiles; roles whose trust policy changed, for example to trust an outside account; new Lambda functions or EC2 instances; changes to bucket policies or KMS key policies; security group rules.
- **Prevention:** permission boundaries so a role can't grant itself more; service control policies for the most dangerous actions; CI with short-lived credentials (OIDC) instead of human write access; a break-glass role that alerts when used.

## Kubernetes

- Service account tokens: rotate by deleting the token secret or restarting with a new projected token; check RoleBindings and ClusterRoleBindings created in the period.
- Isolate a workload with a NetworkPolicy that denies its traffic, and keep the pod for analysis instead of deleting it.

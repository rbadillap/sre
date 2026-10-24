# Drift with Terraform

Examples for steps 2, 6 and 8 of the skill.

- **See drift without changing anything:** `terraform plan -refresh-only` shows how reality differs from the state, without proposing changes to match the code.
- **Never run `terraform apply` on a plan that also contains a destroy or a replace you didn't intend.** Fix the code first. Targeting single resources with `-target` is a last resort, not a way to work around a dangerous plan.
- **Why a replacement:** the plan marks the attribute with `# forces replacement`. For a database, typical causes are the identifier, the engine, encryption settings or the subnet group.
- **A resource that only moved in the code** is a change of address, not a replacement: a `moved` block lets the plan show a move instead.
- **Guardrails:**
  - `lifecycle { prevent_destroy = true }` on stateful resources;
  - the provider's own protection, such as deletion protection on a database;
  - a policy check on the plan's JSON in CI (for example with OPA or Conftest) that fails any plan destroying or replacing a stateful resource without an explicit approval;
  - a scheduled `plan -refresh-only` that alerts on drift.

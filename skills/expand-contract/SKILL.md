---
name: expand-contract
description: Discipline. Change a data structure, schema, format or interface in separate steps (add the new form next to the old one, move to it, then remove the old one) so every version that runs at the same time keeps working and a rollback stays safe. Applied by the orchestrators in this package when a change touches stored data, caches, messages or APIs.
license: MIT
metadata:
  sre-layer: discipline
---

# Expand and contract

**Change structures in separate steps, so there's never a moment when one running version can't read what another wrote.**

## When

Whenever a change alters something that more than one version reads or writes: database columns and indexes, cache formats, message schemas, file formats, API fields.

## When not

When only one version can ever run at a time and nothing outlives it. That's rare: rolling deploys, canaries and rollbacks all run two versions together.

## How

1. **Expand.** Add the new form next to the old one: a new column, a new index, a new field, a versioned key. The old version keeps working because nothing it uses is gone. The new version writes both forms.
2. **Migrate.** Copy existing data into the new form, as its own step, separate from any deploy. The copy never overwrites a newer write to the new form. Check that it matches.
3. **Switch.** Move reads to the new form only when nothing writes the old form alone: every running version writes both, or those writes are captured and copied. Before the switch, every captured change up to a cutoff point is applied, and the two forms stay in sync while reads move. One check that they match doesn't prove either. Wait until the new version has been stable for a while.
4. **Contract.** Remove the old form in a later release, only when going back past that point is no longer needed.

For a constraint such as a unique index: find and fix the data that breaks it first, and stop new violations at the source, then build the new constraint next to the old one. Never drop one and create the other as two steps with a gap between them.

## The mistake it prevents

A gap where the old structure is gone and the new one isn't ready: duplicates get in, a rollback reads a format it doesn't know, and the data stays wrong after the code is fixed.

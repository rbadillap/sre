SKILLS_REF_VERSION       ?= 0.1.1
CHECK_JSONSCHEMA_VERSION ?= 0.38.2
PLUGIN_SCHEMA            ?= https://agent-plugins.org/schemas/1.0.0/plugin.schema.json

SKILLS := $(sort $(dir $(wildcard skills/*/SKILL.md)))

agentskills = uvx --from skills-ref==$(SKILLS_REF_VERSION) agentskills $(1)

.DEFAULT_GOAL := help
.PHONY: help validate validate-skills validate-manifest

help: ## List targets
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

validate: validate-manifest validate-skills ## Check the manifest and every skill against their specs

validate-skills: ## Check every SKILL.md against the Agent Skills spec
	@for skill in $(SKILLS); do \
		$(call agentskills,validate $$skill) || exit 1; \
	done

validate-manifest: ## Check plugin.json against the Agent Plugins 1.0.0 schema
	uvx check-jsonschema==$(CHECK_JSONSCHEMA_VERSION) \
		--schemafile $(PLUGIN_SCHEMA) \
		plugin.json

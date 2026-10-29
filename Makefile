SKILLS_REF_VERSION       ?= 0.1.1
CHECK_JSONSCHEMA_VERSION ?= 0.38.2
PLUGIN_SCHEMA            ?= https://agent-plugins.org/schemas/1.0.0/plugin.schema.json

SKILLS := $(sort $(dir $(wildcard skills/*/SKILL.md)))

agentskills = uvx --from skills-ref==$(SKILLS_REF_VERSION) agentskills $(1)

.DEFAULT_GOAL := help
.PHONY: help validate validate-skills validate-metadata validate-manifest

help: ## List targets
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

validate: validate-manifest validate-skills validate-metadata ## Check the manifest, every skill against its spec, and the package's own metadata

validate-skills: ## Check every SKILL.md against the Agent Skills spec
	@for skill in $(SKILLS); do \
		$(call agentskills,validate $$skill) || exit 1; \
	done

validate-metadata: ## Check every skill's sre-* metadata, that each orchestrator has a template and a review row, and that orchestrators and the router carry the same disciplines paragraph
	@status=0; \
	guard=$$(grep '^\*\*Disciplines:\*\* ' skills/sre/SKILL.md); \
	[ -n "$$guard" ] || { echo "sre: missing the Disciplines paragraph"; status=1; }; \
	for skill in $(SKILLS); do \
		name=$$(basename $$skill); file=$$skill/SKILL.md; \
		layer=$$(sed -n 's/^  sre-layer: //p' $$file); \
		case "$$layer" in \
			orchestrator) \
				grep -q '^  sre-stage: ' $$file || { echo "$$name: missing sre-stage"; status=1; }; \
				grep -Eq '^  sre-safety: (reads-only|proposes|acts-with-approval)$$' $$file || { echo "$$name: missing or unknown sre-safety"; status=1; }; \
				ls $$skill/assets/*.md >/dev/null 2>&1 || { echo "$$name: no template in assets/"; status=1; }; \
				grep -q "^| \`$$name\` |" docs/review/skills.md || { echo "$$name: no row in docs/review/skills.md"; status=1; }; \
				grep -qxF "$$guard" $$file || { echo "$$name: Disciplines paragraph differs from the router's"; status=1; } ;; \
			router) \
				grep -Eq '^  sre-safety: reads-only$$' $$file || { echo "$$name: router needs sre-safety: reads-only"; status=1; } ;; \
			discipline) ;; \
			*) echo "$$name: missing or unknown sre-layer"; status=1 ;; \
		esac; \
	done; \
	[ $$status -eq 0 ] && echo "metadata ok"; exit $$status

validate-manifest: ## Check plugin.json against the Agent Plugins 1.0.0 schema
	uvx check-jsonschema==$(CHECK_JSONSCHEMA_VERSION) \
		--schemafile $(PLUGIN_SCHEMA) \
		plugin.json

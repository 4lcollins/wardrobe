-include .env

PROJECT_REF ?= $(SUPABASE_PROJECT_REF)

.PHONY: automation requirements app supabase-plan supabase-apply

requirements:
	uv lock --upgrade
	uv export --format requirements-txt --no-hashes --no-dev --no-emit-project --output-file requirements.txt

app:
	@echo "Starting Wardrobe Shiny App..."
	@if [ -d ".venv" ]; then \
		. .venv/bin/activate; \
		export PYTHONPATH=.; \
		shiny run app.py; \
	else \
		export PYTHONPATH=.; \
		shiny run app.py; \
	fi

automation:
	python -m src.automations.runner daily_outfit

supabase-plan:
	@if [ -z "$(PROJECT_REF)" ]; then \
		echo "Usage: make supabase-plan PROJECT_REF=<project-ref>"; \
		echo "Or set SUPABASE_PROJECT_REF in .env"; \
		exit 1; \
	fi
	supabase link --project-ref $(PROJECT_REF)
	supabase db push --dry-run

supabase-apply:
	@if [ -z "$(PROJECT_REF)" ]; then \
		echo "Usage: make supabase-apply PROJECT_REF=<project-ref> [SEED=1]"; \
		echo "Or set SUPABASE_PROJECT_REF in .env"; \
		exit 1; \
	fi
	supabase link --project-ref $(PROJECT_REF)
	@if [ "$(SEED)" = "1" ]; then \
		supabase db push --include-seed; \
	else \
		supabase db push; \
	fi

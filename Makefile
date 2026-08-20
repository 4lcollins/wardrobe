.PHONY: automation requirements run

requirements:
	uv lock --upgrade
	uv export --format requirements-txt --no-hashes --no-dev --no-emit-project --output-file requirements.txt

run:
	@echo "Starting Wardrobe Shiny App..."
	@if [ -d ".venv" ]; then \
		. .venv/bin/activate; \
		export PYTHONPATH=.; \
		shiny run shiny_app/app.py; \
	else \
		export PYTHONPATH=.; \
		shiny run shiny_app/app.py; \
	fi

automation:
	python -m src.automations.runner daily_brief

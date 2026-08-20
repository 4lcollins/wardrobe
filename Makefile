.PHONY: deploy requirements run

ICLOUD_PATH := $(HOME)/Library/Mobile Documents/com~apple~CloudDocs/Wardrobe

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

deploy:
	mkdir -p "$(ICLOUD_PATH)"
	rsync -av \
		--include='.env' \
		--exclude='.*' \
		--filter=':- .gitignore' \
		--delete \
		./ "$(ICLOUD_PATH)/"
	@echo "Deployed to $(ICLOUD_PATH)"

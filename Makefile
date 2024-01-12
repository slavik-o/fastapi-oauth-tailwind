.PHONY: run dev css fmt

run:
	@source .venv/bin/activate && python main.py

dev:
	@source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 4444

css:
	cd styles/ && pnpx tailwindcss -i app.css -o ../static/styles.css --watch

fmt:
	@source .venv/bin/activate && black .

.DEFAULT_GOAL := run

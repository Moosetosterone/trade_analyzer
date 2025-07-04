# Makefile for Trade Analyzer

PYTHON=venv/bin/python
PIP=venv/bin/pip

# Install all requirements
install:
	$(PIP) install -r requirements.txt

# Run the CLI
run:
	$(PYTHON) main.py

# Format code using black and isort
format:
	black .
	isort .

# Type check
typecheck:
	mypy .

# Run tests
test:
	pytest tests/ -v

# Clean Python cache
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -name "*.pyc" -delete

# Run all checks: format, type check, and test
check-all:
	make format
	make typecheck
	make test

# Run the Streamlit UI in development mode
dev:
	streamlit run ui/streamlit_app.py
# File: Makefile (Updated with the correct 'run' command)

.PHONY: setup fetch-model run test clean

# Installs dependencies into a virtual environment
setup:
	python3 -m venv venv
	@echo "Virtual environment created. Activate it using: source venv/bin/activate"
	@echo "Then run: pip install -r requirements.txt"

# Fetches the GGUF model
fetch-model:
	source venv/bin/activate && python scripts/download_model.py

# Runs the Streamlit web application using the module-safe method
run:
	source venv/bin/activate && python -m streamlit run app/streamlit_app.py

# Runs the command-line smoke test using the module-safe method
test:
	source venv/bin/activate && python -m scripts.test_analyst

# Cleans up Python cache files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
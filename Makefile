.PHONY: run-dev clean

# Create a virtual environment, update pip, install dependencies, and run the main script
run-dev: venv/bin/activate
	@echo "Running the development environment..."
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	. venv/bin/activate && python src/main.py TODO src/

# Create virtual environment
venv/bin/activate: requirements.txt
	@echo "Creating virtual environment..."
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	touch venv/bin/activate

# Clean up the virtual environment
clean:
	@echo "Cleaning up..."
	rm -rf venv

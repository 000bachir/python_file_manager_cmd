# Run the main Python script
start :
	python -B src/main.py


# Clean up cache files
clean:
	rm -rf __pycache__ .pytest_cache

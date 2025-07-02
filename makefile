
# pass a different input file to the run command (e.g. DSL=other.dsl)
DSL=examples/hello-world/hello.dsl


.PHONY: test run clean up down

test:
	@echo "Running tests..."
	PYTHONPATH=src pytest tests/

run:
	@echo "Starting application..."
	 PYTHONPATH=src python src/cli/main.py $(DSL)

clean:
	@echo "Cleaning up..."
	# Insert commands from clean.sh here
	rm -r out/

up:
	@echo "Starting services..."
	# Insert commands from up.sh here
	docker compose -f out/docker-compose.yml up db backend frontend

down:
	@echo "Stopping services and wiping data..."
	docker compose -f out/docker-compose.yml down --volumes


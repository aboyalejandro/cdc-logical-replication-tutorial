# Check if docker-compose is available, otherwise use docker compose
DOCKER_COMPOSE := $(shell command -v docker-compose 2> /dev/null || echo "docker compose")

# Build the Docker services
build:
	docker compose build

# Run the Docker services
run:
	docker compose up

# Stop the Docker services
stop:
	$(DOCKER_COMPOSE) down --volumes

# Clean Docker containers, images, and volumes
clean: stop
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans

# Insert data into the source database
insert-data:
	$(DOCKER_COMPOSE) run --rm cdc_scripts python /app/scripts/insert_data.py

# Update data in the source database
update-data:
	$(DOCKER_COMPOSE) run --rm cdc_scripts python /app/scripts/update_data.py

# Delete data from the source database
delete-data:
	$(DOCKER_COMPOSE) run --rm cdc_scripts python /app/scripts/delete_data.py

# Truncate a table from the source database
truncate:
	$(DOCKER_COMPOSE) run --rm cdc_scripts python /app/scripts/truncate_table.py

# Creates a table in the source database
create-table:
	$(DOCKER_COMPOSE) run --rm cdc_scripts python /app/scripts/create_table.py

# Drops a table from the source database
drop-table:
	$(DOCKER_COMPOSE) run --rm cdc_scripts python /app/scripts/drop_table.py
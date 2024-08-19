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

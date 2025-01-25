.DEFAULT_GOAL := help

.PHONY: help
help:  ## show this help.
	@grep -e '^\s+:.*?## .*$$' $(firstword $(makefile_list)) | \
		awk 'begin {fs = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: up
up: down
	docker compose up --build -d

.PHONY: down
down: ## Stop and remove all the Docker services, volumes and networks
	docker compose down -v --remove-orphans

.PHONY: logs
logs: ## show logs of a service, ex: make logs service=consumer
	docker compose logs $(service)

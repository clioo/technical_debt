.DEFAULT_GOAL := help

.PHONY: up
up: ## run the project
	@docker-compose up -d
	@docker attach technical_debt_app_1


.PHONY: down
down: ## stop and remove Docker containers
	@docker-compose down --remove-orphans


.PHONY: build
build: ## Build with cache capabilities
	@docker-compose build


.PHONY: rebuild
rebuild: ## Re-build images with no cache
	@docker-compose down --remove-orphans
	@docker-compose build --no-cache


.PHONY: test
test: ## Run flake8 and pytest tests
	@docker-compose run --rm app sh -c "pytest --flake8 -p no:warnings"

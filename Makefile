# === DJANGO MANAGEMENT COMMANDS ===
PIP=venv/bin/pip
MANAGE=python manage.py
DIR= warehouse_managment

# Load environment variables from warehouse_managment/.env
include warehouse_managment/.env

.PHONY: run setup migrate createsuperuser test shell

help:
	@echo "Usage: make <command>"
	@echo ""
	@echo "Project Commands:"
	@echo "  setup             - Install dependencies & migrate DB"
	@echo "  run               - Run Django dev server"
	@echo "  migrate           - Run makemigrations and migrate"
	@echo "  createsuperuser   - Create Django superuser"
	@echo "  test              - Run tests"
	@echo "  shell             - Django shell"
	@echo ""
	@echo "Database Commands (Docker in ./database/):"
	@echo "  db-up             - Start PostgreSQL service"
	@echo "  db-down           - Stop PostgreSQL service"
	@echo "  db-logs           - View PostgreSQL container logs"
	@echo "  db-ps             - List running containers"
	@echo "  db-psql           - Access PostgreSQL shell"
	@echo "  db-build          - Rebuild containers"
	@echo "  db-clean          - Remove all volumes & reset"
	@echo "  db-restart        - Restart containers"

# === PROJECT COMMANDS ===
setup:
	$(PIP) install -r requirements.txt
	cd $(DIR) && $(MANAGE) migrate

run:
	cd $(DIR) && $(MANAGE) runserver

migrate:
	cd $(DIR) && $(MANAGE) makemigrations
	cd $(DIR) && $(MANAGE) migrate

createsuperuser:
	cd $(DIR) && $(MANAGE) createsuperuser

test:
	cd $(DIR) && $(MANAGE) test

shell:
	cd $(DIR) && $(MANAGE) shell

seed:
	cd $(DIR) && $(MANAGE) seed_product
	cd $(DIR) && $(MANAGE) seed_warehouse



# === DOCKER DATABASE COMMANDS ===
db-up:
	cd database && docker-compose up -d

db-down:
	cd database && docker-compose down

db-logs:
	cd database && docker-compose logs -f

db-ps:
	cd database && docker-compose ps

db-build:
	cd database && docker-compose build

db-clean:
	cd database && docker-compose down -v --remove-orphans
	rm -rf database/db-data
	rm -rf database/pgadmin-data

db-restart:
	cd database && docker-compose restart

db-psql:
	cd database && docker-compose exec psql-client psql $(DATABASE_URL)


	

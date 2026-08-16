.PHONY: up down build logs migrate makemigrations shell dbshell superuser seed lint fmt test

up:
	docker compose up

build:
	docker compose build

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose run --rm web python manage.py migrate

makemigrations:
	docker compose run --rm web python manage.py makemigrations

shell:
	docker compose run --rm web python manage.py shell

dbshell:
	docker compose exec db psql -U $${POSTGRES_USER} -d $${POSTGRES_DB}

superuser:
	docker compose run --rm web python manage.py createsuperuser

seed:
	docker compose run --rm web python manage.py seed_demo

lint:
	docker compose run --rm web ruff check .
	docker compose run --rm web black --check .
	docker compose run --rm web djlint . --check

fmt:
	docker compose run --rm web ruff check --fix .
	docker compose run --rm web black .
	docker compose run --rm web djlint . --reformat

test:
	docker compose run --rm web pytest

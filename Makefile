manage_py := docker compose exec -it backend python ./app/manage.py

run:
	$(manage_py) runserver 0.0.0.0:8000

makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

createsuperuser:
	$(manage_py) createsuperuser

shell:
	$(manage_py) shell_plus --print-sql

sqlite:
	sqlite3 ./app/db.sqlite3

flake:
	docker compose exec -it backend flake8 app/

worker:
	cd app && celery -A settings worker -l info --autoscale 1,3
beat:
	cd app && celery -A settings beat -l info
pytest:
	docker compose exec -it backend pytest app/tests --cov=app --cov-report=html && coverage report --fail-under=78
gunicorn:
	cd app && gunicorn -w 4 settings.wsgi --timeout 3600 --max-requests 10000 --log-level DEBUG --bind 0.0.0.0:8000

collectstatic:
	$(manage_py) collectstatic --no-input && \
	docker cp backend:/tmp/static /tmp/static && \
	docker cp /tmp/static nginx:/etc/nginx/static

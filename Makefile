manage_py := python ./app/manage.py

run:
	$(manage_py) runserver 0.0.0.0:8000

makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

shell:
	$(manage_py) shell_plus --print-sql

sqlite:
	sqlite3 ./app/db.sqlite3

flake:
	flake8 app/

worker:
	cd app && celery -A settings worker -l info --autoscale 1,3
beat:
	cd app && celery -A settings beat -l info
pytest:
	pytest app/tests
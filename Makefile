manage_py := python ./app/manage.py

run:
	$(manage_py) runserver

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
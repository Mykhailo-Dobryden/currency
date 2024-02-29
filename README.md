# Currency

### Docker

#### Debug using breakpoint
Presets: gunicorn; 

Note, that on gunicorn-server, debbuging with breakpoint() don't work.

##### Curing of issue:

After running 'docker compose':
Run:

    'docker compose exec -it backend bash'

Inside container run:

    'python3 ./app/manage.py runserver 0.0.0.0:8001'

Note that 8000 port is for gunicorn server

#### Nginx

After launching Nginx container it's needed to run:

    'make collectstatic'

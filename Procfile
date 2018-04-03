web: gunicorn hc.wsgi --log-file - && worker: ./manage.py ensuretriggers && ./manage.py sendalerts
release: python manage.py makemigrations --merge && python manage.py migrate
worker: ./manage.py ensuretriggers && ./manage.py sendreports

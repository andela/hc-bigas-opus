web: gunicorn hc.wsgi --log-file - && worker: ./manage.py ensuretriggers && ./manage.py sendalerts && ./manage.py sendreports
release: python manage.py makemigrations --merge && python manage.py migrate

web: gunicorn hc.wsgi --log-file - && ./manage.py collectstatic && worker: ./manage.py ensuretriggers && ./manage.py sendalerts && worker: ./manage.py ensuretriggers && ./manage.py sendreports
release: python manage.py makemigrations --merge && python manage.py migrate

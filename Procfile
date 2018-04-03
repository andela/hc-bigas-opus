web: gunicorn hc.wsgi --log-file - && release: python manage.py makemigrations --merge && python manage.py migrate && worker: ./manage.py ensuretriggers && ./manage.py sendalerts
worker: ./manage.py ensuretriggers && ./manage.py sendreports

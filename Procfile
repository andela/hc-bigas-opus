web: gunicorn hc.wsgi --log-file -
release: python manage.py makemigrations --merge && python manage.py migrate

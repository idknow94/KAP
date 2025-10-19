release: python KAP/manage.py collectstatic --noinput
web: gunicorn KAP.wsgi:application --chdir KAP --bind 0.0.0.0:8000
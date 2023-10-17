run:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py migrate

superuser:
	poetry run python manage.py createsuperuser

shell:
	poetry run python manage.py shell_plus --ipython

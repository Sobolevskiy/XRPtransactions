start:
	chmod +x docker-entrypoint.sh
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs -f

user:
	docker exec xrptransactions_web_1 /bin/sh -c "export DJANGO_SUPERUSER_USERNAME=admin;export DJANGO_SUPERUSER_EMAIL=test@test.com;export DJANGO_SUPERUSER_PASSWORD=admin;python manage.py createsuperuser --no-input"

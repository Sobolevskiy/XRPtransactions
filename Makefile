start:
	chmod +x docker-entrypoint.sh
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs -f

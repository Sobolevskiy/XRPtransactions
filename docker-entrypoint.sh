#!/bin/bash
set -e

case "$1" in
    web)
        python manage.py migrate --noinput
        python manage.py actualize_transactions
        python manage.py runserver 0.0.0.0:8080
        ;;
    celery)
        celery -A XRPtransactions worker -l INFO
        ;;
    redis_consumer)
        python3 manage.py run_redis_consumer
        ;;
    receiver)
        python3 -m receiver
        ;;
    *)
        exec "$@"
esac

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
daphne -e ssl:5376:privateKey=privkey.pem:certKey=cert.pem config.asgi:application

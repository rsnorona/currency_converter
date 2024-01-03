pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py one_time_create_default_superuser
python3 manage.py one_time_create_currency_convertions
